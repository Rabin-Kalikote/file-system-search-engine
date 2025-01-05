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
        return 'results'

file_system = FileSystem('/files')

print(file_system.search())