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


    

    
    def search(self, query):
        results = self.search_in_folder(self.directry, query)
        return results


file_system = FileSystem('/workspaces/file-system-search-engine/files')

print(file_system.data)