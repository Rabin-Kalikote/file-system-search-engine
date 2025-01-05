import os

class FileSystem:
    def __init__(self, directry):
        self.directry = directry

    def search_in_file(filename):
        with open(file, 'r') as file:
            cleaned_lines = []
            for line in file.readlines():
                cleaned_lines.append(sum([c.lower() for c in line if (c.isalnum() or c == ' ')]).split(' '))
        print(cleaned_lines)
        return cleaned_lines
    
    def search(self):
        for filename in os.listdir(self.directry):
            file_path = os.path.join(self.directry, filename)

            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    print(f"File: {filename}\nContent:\n{content}\n")


file_system = FileSystem('/workspaces/file-system-search-engine/files')
print(file_system.search())