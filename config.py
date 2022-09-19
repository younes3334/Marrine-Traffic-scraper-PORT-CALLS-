# PARAMETERS FOR THE SCRIPT " port_marin_scraper_v2.py "

# Keyword to search for
# example of use : KEYWORD = "" if you want all the results, else KEYWORD = "MOROCCO" if you want only the results that contain the word "MOROCCO"
KEYWORD = ""


# Time to wait before the next process
# example of use : TIME_TO_WAIT = 180 if you want to wait 180 seconds before the next process
TIME_TO_WAIT = 180


# Data file name to save the data
# example of use : DATA_FILE_NAME = "_Marrinetraffic_data.csv" if you want to save the data in a file named "_Marrinetraffic_data.csv"
# the KEYWORD will be added to the file name if you have specified a KEYWORD to make the file name unique
DATA_FILE_NAME = KEYWORD + "_Marrinetraffic_data.csv"
