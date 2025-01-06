import os

class Clause:
    def __init__(self, body):
        self.body = body
        self.tokens = self._tokenize()

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

        # break into sub-clauses and add as children of this clause (self)
        def add_token(token):
            if token[-1] == ')':
                tokens.append(Clause(token))
            else:
                tokens.append(token)
        current = ''
        paren_count = 0

        for i, char in enumerate(token_clause):
            if char == '(' and paren_count == 0:
                # start of a new parenthetical expression
                if current.strip():
                    # check if current is just a '+', if so, don't append yet
                    if current.strip() != '+':
                        add_token(current.strip())
                        current = char
                    else:
                        current += char
                else:
                    current = char
                paren_count += 1
            elif char == '(':
                # nested opening parenthesis
                current += char
                paren_count += 1
            elif char == ')':
                # closing parenthesis
                current += char
                paren_count -= 1
                if paren_count == 0:
                    add_token(current.strip())
                    current = ''
            else:
                current += char
        
        # add the last term if there is one
        if current.strip():
            add_token(current.strip())

        return tokens

print(Clause('(a (b +(c d) e +f) +(g h) i)').tokens)

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

    def search(self, query):
        search_clause = Clause(query)

        required = []
        optional = []

        #print(search_clause.tokens)

        for token in search_clause.tokens:
            if type(token) == str:
                if token[0] == '+':
                    required = set.intersection(*[set(list) for list in [required, self.data[token[1:]]]]) #keeps the common
                else:
                    for dir in self.data[token]:
                        found = False
                        for opt_dir in optional:
                            if opt_dir[0] == dir:
                                opt_dir[0] += 1
                                found = True
                        if not found:
                            optional.append((dir, 1))
            else:
                required += self.search(token.body)

        #print(f"Required {required}")
        #print(f"Optional {optional}")

        if not required:
            return [dir for dir, occurance in optional]
        
        return sorted(required, key=lambda x: max([occurance for dir, occurance in optional if dir == x] or [float('-inf')]), reverse=True) # returns sorted required based on the number of optional indexes


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
        with open(f'{item['dir']}/{item['file']}', 'r') as file:
            print(f"{item['dir']}/{item['file']} {item['line']}  {file.readlines()[item['line']]}")


    searching = int(input('Search again? (Press 1 as Yes) '))




# MORE WORK NEEDED. FINDS one word SUCCESSFULLY