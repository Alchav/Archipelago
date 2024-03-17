import os
import json

def write_file_list(directory_path, output_file_path):
    filenames = os.listdir(directory_path)
    filenames_without_extensions = [os.path.splitext(filename)[0] for filename in filenames]
    sorted_filenames = [filename for _, filename in sorted(zip([int(filename) for filename in filenames_without_extensions], filenames_without_extensions))]
    with open(output_file_path, 'w') as output_file:
        json.dump(sorted_filenames, output_file)

if __name__ == '__main__':
    # Set the directory path and output file path here
    directory_path_tame = '../MapRepositoryV94Tame'
    output_file_path_tame = 'worlds/sm_map_rando\data/mapRepositoryTame.json'
    directory_path_wild = '../MapRepositoryV94Wild'
    output_file_path_wild = 'worlds/sm_map_rando\data/mapRepositoryWild.json'

    # Call the write_file_list function with the specified directory and output file paths
    write_file_list(directory_path_tame, output_file_path_tame)
    write_file_list(directory_path_wild, output_file_path_wild)