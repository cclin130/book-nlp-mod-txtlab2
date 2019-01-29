import os
import sys

def replace(parent_path):
    for filepath in os.listdir(parent_path):
        new_path = os.path.join(parent_path, filepath.replace(' ', '_'))
        os.rename(os.path.join(parent_path, filepath), new_path)

        #if filepath is a folder
        if os.path.isdir(new_path):
            replace(new_path)


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        print('Filepath for parent directory required.')
    else:
        replace(sys.argv[1])
