# useful_scripts

useful scripts, will add any I come up with and write some usage-instructions here

# FileOrganizer
- cleans up its current working-directory by eighter moving or deleting files by their extensions or names
- actions for each extension and/or filename configurable within a .JSON-file (config file is automatically created with an example structure if not in directory)
- do not rename the 'delete' key!, that's a fixed key for files that'll be deleted.
- JSON-config-file contains a dictionary, keys are directory-names and values the extensions or filenames going into those directorys (directorys are created if not in working-directory)
- check the example organizer_config.JSON here for the correct format (note that you could omit the dot or put whole filenames there, the script checks if the values are at the end of the filenames so anything goes pretty much)
- note that the script (even if you choose to rename it) and the config-file (dont rename that tho) will never be moved or deleted by the script, so you can add .JSON and .py to your filters too.
