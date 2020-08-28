# useful_scripts

useful scripts, will add any I come up with and write some usage-instructions here

FileOrganizer
---------
* cleans up its current working-directory by eighter moving or deleting files by their extensions or names
* actions for each extension and/or filename configurable within a .JSON-file (config file is automatically created with an example structure if not in directory)
* do not rename the 'delete' key!, that's a fixed key for files that'll be deleted.
* JSON-config-file contains a dictionary, keys are directory-names and values the extensions or filenames going into those directorys (directorys are created if not in working-directory)
* check the example organizer_config.JSON here for the correct format (note that you could omit the dot or put whole filenames there, the script checks if the values are at the end of the filenames so anything goes pretty much)
* note that the script (even if you choose to rename it) and the config-file (dont rename that tho) will never be moved or deleted by the script, so you can add .JSON and .py to your filters too.

WeatherGrabber
---------
Script that will use the OpenWeatherMaps-API to get weather info by city name (for now) and format it in a more useful+readable format (a table). The raw API-data is formated, only useful datapoints are kept and wind degrees is transformed into an easier to interpret direction.

The Data is a weather forecast for the next 5 days, listed in 3-hour periods, for an example see `berlin_weatherdata.csv`

Usage:
* run it directly and give the city name as a sys-argument, like so `weathergrabber.py berlin`
* integrate it in your own scripts and use the function `format_data(city_name, save: bool=False)` after creating an object of the `WeatherGrabber`-class. Arguments: city_name: string of the city youd like to get the data of, save: bool wether to save the data as a .csv-file in the same directory or not. Data will be returned as a pandas DataFrame if you choose to integrate the function in your own script

Disclaimer: As the API's response is transformed this might easily break if OWM chooses to change the structure of their API's responses in the future.