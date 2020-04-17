#! python3

import os
import json
import sys
import shutil

# check for json file in working dir, create if not there and stop or continue program if there

DIR = os.getcwd()
CONFIG_NAME = 'organizer_config.JSON'
SCRIPT_NAME = os.path.basename(__file__)

print('looking for config-file...')
if not os.path.exists(os.path.join(DIR, CONFIG_NAME)):
    print('no config-file found, generating one...')
    config = {
        'sample_folder_name_1': ['.pdf', '.doc', '.txt'],
        'sample_folder_name_2': ['.mp4', '.mov'],
        'delete': []
    }
    with open(CONFIG_NAME, 'w') as outputfile:
        json.dump(config, outputfile, indent=2)
    print(f'config file generated as {CONFIG_NAME}. run this again after setting your preferences there.')
    input()
    sys.exit()
else:
    print('config-file found. reading config...')
    with open(CONFIG_NAME) as json_file:
        config = json.load(json_file)

# loop through all files of working dir, moving/ deleting them according to configs in JSON-file

    for directory, extension in config.items():
        if not os.path.exists(os.path.join(DIR, directory)) and directory != 'delete':
            print(f'couldn\'t find directory "{directory}", creating it...')
            os.mkdir(directory)

        if directory == 'delete':
            for item in extension:
                for filename in os.listdir(DIR):
                    if filename == CONFIG_NAME or filename == SCRIPT_NAME:
                        continue
                    elif filename.endswith(item):
                        os.remove(os.path.join(DIR, filename))
                        print(f'deleted "{filename}".')
        else:
            for item in extension:
                for filename in os.listdir(DIR):
                    if filename == CONFIG_NAME or filename == SCRIPT_NAME:
                        continue
                    elif filename.endswith(item):
                        try:
                            shutil.move(os.path.join(DIR, filename), os.path.join(DIR, directory))
                            print(f'moved "{filename}" into "{directory}".')
                        except:
                            print(f'"{filename}" already exists in "{directory}", skipping. (rename or replace it '
                                  f'manually.)')
                            continue

print('finished organizing, you can close this window now. (or press ENTER)')
input()
