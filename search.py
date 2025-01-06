import os

class FileSystem:
    def __init__(self, directry):
        self.directry = directry

    def search_in_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
            return f"File: {filename}\nContent:\n{content}\n"

    def search_in_folder(self, folder_path):
        results = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                results.append(self.search_in_file(item_path)) #base case
            else:
                results += self.search_in_folder(item_path) #recursive case           
        return results

    
    def search(self):
        results = self.search_in_folder(self.directry)
        return results


file_system = FileSystem('/workspaces/file-system-search-engine/files')

for item in file_system.search():
    print(item)