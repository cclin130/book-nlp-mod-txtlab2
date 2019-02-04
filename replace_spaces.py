import os
import sys

def replace_spaces(parent_path):
    for filepath in os.listdir(parent_path):
        new_path = os.path.join(parent_path, filepath.replace(' ', '_').replace('\'', ''))
        os.rename(os.path.join(parent_path, filepath), new_path)

        #if filepath is a folder
        if os.path.isdir(new_path):
            replace_spaces(new_path)


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print('Filepath for parent directory required.')
    else:
        replace_spaces(sys.argv[1])
