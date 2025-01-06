import os

class FileSystem:
    def __init__(self, directry):
        self.directry = directry
        self.data = self._index_files(directry)

    def _clean_line(self, line):
        ''' Naive cleaner: lowercases everything, replaces all non-alphanumeric characters as whitespace, then split on whitespace. '''
        cleaned = ''
        for c in line:
            if c.isalnum():
                cleaned += c
            else:
                cleaned += ' '
        return cleaned.lower().split(' ')

    def _index_files(self, folder_path):
        ''' Goes throuh all the sub-folders and files recursively and creates indexes. '''
        data = {}
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                #base case for file
                with open(item_path, 'r') as file:
                    lines = file.readlines()
                    for i in range(len(lines)):
                        for token in self._clean_line(lines[i]):
                            this_index = {'dir': os.path.dirname(item_path), 'file': os.path.basename(item_path), 'line': i}
                            if token in data:
                                data[token].append(this_index)
                            else:
                                data[token] = [this_index]
            else:
                #recursive case for sub folder
                data = data | self._index_files(item_path)         
        return data

    def _tokenize_query(self, query):
        ''' Returns the list of tokens/clauses '''
        return query.strip('()').split(' ')

    def search(self, query):
        tokens = query.split(' ')

        results = []
        for token in tokens:
            if token in self.data:
                results.append(self.data[token])

        return results




class Clause:
    def __init__(self, body):
        self.tokens = self._tokenize(self)
        self.body = body

    def is_required(self):
        return self.body[0] == '+'

    def _tokenize(self):
        token_clause = self.body
        tokens = []

        #clean the current clause's + and ()
        if token_clause[0] == '+':
            token_clause = token_clause[1:]
        if token_clause[0] == '(':
            token_clause = token_clause[1:]
        if token_clause[-1] == ')':
            token_clause = token_clause[:-1]

        this_token = ''
        paren_count = 0
        for char in token_clause:
            if char == '(' and paren_count == 0:
                if this_token.strip() and this_token.strip() != '+':
                    tokens.append(this_token.strip())
                if this_token.strip() == '+':
                    this_token = '+'
                else:
                    this_token = char
                paren_count += 1
            elif char == '(':
                this_token += char
                paren_count += 1
            elif char == ')':
                this_token += char
                paren_count -= 1
                if paren_count == 0:
                    tokens.append(this_token.strip())
                    this_token = ''
            elif char == '+' and paren_count == 0:
                if this_token.strip():
                    tokens.append(this_token.strip())
                this_token = char
            else:
                this_token += char
        
        if this_token.strip():
            tokens.append(this_token.strip())

        return tokens




directry = '/workspaces/file-system-search-engine/files'
file_system = FileSystem(directry)

searching = 1
while searching == 1:
    print('\nMagic Search\n------------\n')
    print(f"Current directory is:\n{directry}\n")

    query = input("Let's start searching!\nExample: 'biz +foo +bar +(bat baz) bop' translates to 'foo' and 'bar' and (either 'bat' or 'baz') and optionally biz or bop.\n\nWhat do you want to search for? ")
    results = file_system.search(query)

    print('Results:\n---------\n')
    for item in file_system.search(query):
        print(item)


    searching = int(input('Search again? (Press 1 as Yes) '))