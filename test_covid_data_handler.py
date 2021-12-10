from covid_data_handler import parse_csv_data
from covid_data_handler import csv_filename
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
import threading
import sched
import time
s = sched.scheduler(time.time, time.sleep)

from covid_data_handler import process_covid_csv_data
print (csv_filename)
#a test for parse_csv_data that uses the default value (csv_filename)
def test_parse_csv_data(csv_filename: str = csv_filename)-> None:
    '''
    a test for parse_csv_data that uses the default value (csv_filename).

            Parameters:
                    csv_filename (str): Name of the file of which to parse

            Returns:
                    None
    '''
    #run the fucntion
    data = parse_csv_data(csv_filename)
    #check if the lines generated are 639 (same as file)
    assert len(data) == 639 
    
#a test for process_covid_csv_data function
def test_process_covid_csv_data()-> None:
    '''
    a test for process_covid_csv_data function.

            Parameters:
                    None

            Returns:
                    None
    '''
    #run the function and assign a variable to each return variable
    total_deaths, current_hospital_cases,last7days_cases  = process_covid_csv_data(parse_csv_data(csv_filename))
    #check if the numbers are what they should be for each varaible
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    assert total_deaths == 141_544

# a test ofr coivd_API_request function
def test_covid_API_request()-> None:
    '''
    a test ofr coivd_API_request function.

            Parameters:
                    None

            Returns:
                    None
    '''
    #create a request for englands covid stats
    data = covid_API_request('England','nation')[0]
    #check to see if a list is returned
    assert isinstance(data, list)
    
#a function for the checule_covid_updates function
def test_schedule_covid_updates() -> None:
    '''
    a function for the checule_covid_updates function.

            Parameters:
                    None

            Returns:
                    None
    '''
    #create a test update usning random data
    test_update = schedule_covid_updates(update_interval=5, update_name='update test', 
                                         update_type='data')
    #check the shceule list is empty after the update is complete 
    assert s.empty()