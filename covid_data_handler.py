from uk_covid19 import Cov19API
import csv
import json
import sched
import time
from covid_news_handling import *
import logging

try :
    #attempt to read the log file location
    log_file_location = config['misc']['log_file_location']
except:
    #no log file can be found
    print('critical - cannot find filepath for log file')

#define the log file and its paramiters 
logging.basicConfig(filename=log_file_location +'log.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.debug)

#define the schedular
s = sched.scheduler(time.time, time.sleep)
logging.debug('Attempting to open config file')
try:
    #open the config file
    with open('config.json', 'r') as f:
        config = json.load(f)
        #confirm config file found and open
        logging.debug('Config file found')
except: 
    #config file has failed to open/be found
      logging.critical('Config file not found')
      
logging.debug('Attempting to read filename from config')      
try:
    #read the csv_filename from the config file      
    csv_filename = config['covid_data_handler']['csv_filename']
    logging.debug('file found sucessfully')
except:
    logging.error('No filename found')

#fucntion to update the data on the covid dashboard
def schedule_covid_updates(update_interval: int, update_name: str, update_type: str) -> None:
    logging.info("schedule_covid_updates({0}, {1}, {2})".format(update_interval,update_name,update_type))
    '''
    Schedules updates for covid data and covid news articles.

            Parameters:
                    update_interval (int): A integer for the delay
                    update_name (str): a string for the name

            Returns:
                     nothing: simply executes the command
    '''
    # check if the update if for the data 
    logging.debug('#is the update for data?')
    try:
        if update_type == 'data':
        #starting data update schedule 
            logging.debug('#scheduling update for covid data')
            s.enter(update_interval, update_name, covid_API_request,
                (top_location, top_location_type))

            s.enter(update_interval, update_name, covid_API_request,
                (bottom_location, bottom_location_type))

            s.enter(update_interval, update_name, process_covid_csv_data,
                (parse_csv_data(str('Data_'
                + covid_API_request(top_location,
                top_location_type)[1]) + '.csv'), ))

            s.enter(update_interval, update_name, process_covid_csv_data,
                (parse_csv_data(str('Data_'
                + covid_API_request(bottom_location,
                bottom_location_type)[1]) + '.csv'), ))

            s.run()
        #check if the update is for news
        elif update_type == 'news':
            logging.debug('#scheduling update for covid news articles')
            s.enter(update_interval, update_name, news_API_request,
                (covid_terms, ))
            s.run()
        
        else:
            pass
        #ignore update as update type is not specified
        logging.error('#no update type specified - will dismiss updates this time ')
    except:
        #missing attributes
        logging.critical('#function missing attributes')
    

#function that parses the csv data
def parse_csv_data(csv_filename: str) -> list:
    logging.info("parse_csv_data({0})".format(csv_filename))
    '''
    Returns an list of the covid data taken from the csv file.

            Parameters:
                    csv_filename (str): Name of the file to read

            Returns:
                    covid_csv_data (list): list of all values from the file
    '''
    logging.debug('opening file containing covid data')
    #create list to store the data
    covid_csv_data = []
    #open covid data file
    logging.info('#attempt to open file ({0})'.format(csv_filename))
    try:
        f = open(csv_filename, 'r')
        #file found and opened OK
        logging.debug('#sucessfully opened ({0})'.format(csv_filename))
    except:
        #file is not found
        logging.critical('#file not found--- ({0})'.format(csv_filename))
    #loop to go through all the lines in teh csv file
    for lines in csv.reader(f):
        #append each line to the list 
        covid_csv_data.append(lines)
    covid_csv_data = covid_csv_data
    #return the data as a list
    logging.debug('return list of data from file')
    return covid_csv_data

#function to process the data just parsed by the function above
def process_covid_csv_data(covid_csv_data: list) -> int: 
    logging.info("process_covid_csv_data")
    '''
    Returns a number for the total deaths, current hospital cases and cases in the last 7 days.

            Parameters:
                    covid_csv_data (list): list of all covid data

            Returns:
                    total_deaths (int): number of total deaths for the specified location
                    current_hospital_cases (int): current hospital cases for the specified location
                    last7days_cases (int): amount of new covid cases in the last 
                                           7 days for the specified location
    '''
    #deletes the first row of the csv (the titles of the collums)
    del covid_csv_data[0]
    last7days_cases = 0
    days = 0
    death_days = []
    
    #calculate the total deaths
    logging.debug('#calculate the total deaths')
    row_counter = 0
    logging.info('Attempting to calculate total deaths')
    try:
        #loop thoiugh every fow 
        for rows in covid_csv_data:
            row_counter = row_counter + 1
            if rows == 0:
                continue
            else:
                #checks to see if theres any data for deaths 
                if not rows[4]:
                    #if theres no death data for the last 50 dats it will set it to 0
                    if row_counter == 50:
                        logging.debug('No death data - setting to 0')
                        total_deaths = 0
                        break
                    continue
                else:
                    #if data for the deaths are found it will add it 
                    total_deaths = int(rows[4])
                    #once the top number for the collum if found then break the loop
                    break
            logging.debug('Total deaths sucsessfully calculated')
    except:
        #no rows or list with data is found so set it to 0
        logging.error('Total deaths not calculated - setting to 0')
        total_deaths = 0
        
    # calualte the hospital cases
    logging.info('# calualte the hospital cases')
    try:
        row_counter = 0
        #loop through the list of data
        for rows in covid_csv_data:
            row_counter = row_counter + 1
            if rows == 0:
                continue
            else:
                #checks to see if theres data in the row
                if not rows[5]:
                    #if theres not data in the first 50 rows then set the-
                    #current_hospital cases to 0 and break the loop
                    if row_counter == 50:
                        current_hospital_cases = 0
                        logging.debug('No hospital data - setting to 0')
                        break
                    continue
                else:
                    #a row of data is found and assigned to current_hospital_cases
                    current_hospital_cases = int(rows[5])
                    #break the loop
                    break
    except:
        #no list of data was found or list contained no rows so,
        #set current_hospital cases to 0
        logging.error('Hospital cases not calulated - setting to 0')

    # calculate the last 7days cases
    logging.info('# calculate the last 7days cases')
    try:
        iterations = 0
        days = 0
        #loop through all the rows in the list
        for rows in covid_csv_data:
            #once it loops 7 times break the loop
            if days == 7:
                break
            #last 7 day covid cases have been added
            logging.debug('#last 7 day covid cases have been added')
            if not rows[6]:
                #if theres no data in cell - move to next one down
                logging.debug('#no data in cell - moved down one')
                continue
            elif iterations == 0:
                iterations = iterations + 1
                continue
            else:
                #if data is found then add it to the last7days_cases variable 
                iterations = iterations + 1
                days = days + 1
                last7days_cases = last7days_cases + int(rows[6])
    except:
        logging.error('last 7 days cases not found - setting to 0')
    #return all three variables calculated 
    logging.debug('returning values({0},{1},{2})'.format(total_deaths,current_hospital_cases,last7days_cases))
    return (total_deaths, current_hospital_cases, last7days_cases)




#fucntion for requesting new data for a specific location via the covid_19 API
#default values are 'Exeter' and 'ltla'
def covid_API_request(location: str = 'Exeter', location_type: str = 'ltla') -> tuple :
    logging.info("covid_API_request({0}, {1})".format(location,location_type ))
    '''
   Gets covid data for a given location and writes it to a csv file.

            Parameters:
                    location (str): what location you want the data for 
                    location_type (str): the type of location it is 

            Returns:
                    covid_area_data (list): list of all the covid info retreived from the API
                    location (str): the same location used in the input, used for the filename
    '''
    # assign the filters
    areaType = 'areaType=' + location_type
    areaName = 'areaName=' + location
    all_nations = [areaType, areaName]
    
    #assign each collums title for the csv file and order it
    cases_and_deaths = {
        'areaCode': 'areaCode',
        'areaName': 'areaName',
        'areaType': 'areaType',
        'date': 'date',
        'cumDailyNsoDeathsByDeathDate': 'cumDailyNsoDeathsByDeathDate',
        'hospitalCases': 'hospitalCases',
        'newCasesBySpecimenDate': 'newCasesBySpecimenDate',
        }
    #write new covid data to file
    logging.debug('#write new covid data to file')
    api = Cov19API(filters=all_nations, structure=cases_and_deaths)
    logging.info('#attempt to access file location from config ')
    try:
        #attempt to access the file location for where to save the data from config 
        #appends the location name to the back of the file location to create a full filname
        filename = str(config['covid_data_handler']['csvFilenameFilepath']
                   + '_' + location + '.csv')
        logging.debug('#filename sucessfuly found -- ({0})'.format(filename))
        #the filename and filepath are sucessfully attached together
    except:
        #filepath is not found so a file cant be created 
        logging.critical('no filename found - cannot create file ')
    api.get_csv(save_as=filename)

    # read the file ive just made
    logging.debug('#reading new covid data file')
    covid_area_data = []
    logging.info('#attempt to open file ({0})'.format(filename))
    try:
        #open the file thats jsut been made
        f = open(filename, 'r')
        logging.debug('#sucessfully opened ({0})'.format(filename))
    except:
        #if no file is found then submit an error
        logging.critical('#file not found ({0})'.format(csv_filename))
    #skip the first row as its only titles for the collums
    next(csv.reader(f))
    #loop through each row in the new csv
    for lines in csv.reader(f):
        #append each row to a list 
        covid_area_data.append(lines)
    #returns the data
    logging.debug('return new data in a list and its location as a string')
    return (covid_area_data, location)  

logging.debug('Read location names from config file and asighn to variables')
try:
    #attempt to read the locations and location types for the top part and bottom
    #part for the user interface from the config file
    top_location = config['covid_data_handler']['Toplocation']
    top_location_type = config['covid_data_handler']['Toplocation_type']
    bottom_location = config['covid_data_handler']['Bottomlocation']
    bottom_location_type = config['covid_data_handler'
                              ]['Bottomlocation_type']
    logging.debug('Location names and types read susessfully')
except:
    #give an error if any of this config file reading goes wrong 
    logging.critical('Config file missing either location names or type or both')