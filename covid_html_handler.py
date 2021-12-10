from flask import *
import covid_data_handler
from time import sleep
from covid_data_handler import *
import sched
from time import time, sleep
from datetime import datetime
import threading
import json
import logging

try :
    log_file_location = config['misc']['log_file_location']
except:
    print('ERROR - cannot find filepath for log file')
logging.basicConfig(filename=log_file_location+'log.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.debug)


logging.info('#attempt to access config file for data')
try:
    location = config['covid_data_handler']['Toplocation']
    local_7day_infections = \
    process_covid_csv_data(parse_csv_data(str('Data_'
                           + covid_API_request(top_location,
                           top_location_type)[1]) + '.csv'))[2]
    nation_location = config['covid_data_handler']['Bottomlocation']
    national_7day_infections = \
    process_covid_csv_data(parse_csv_data(str('Data_'
                           + covid_API_request(bottom_location,
                           bottom_location_type)[1]) + '.csv'))[2]
    hospital_cases = process_covid_csv_data(parse_csv_data(str('Data_'
        + covid_API_request(bottom_location, bottom_location_type)[1])
        + '.csv'))[1]
    deaths_total = process_covid_csv_data(parse_csv_data(str('Data_'
        + covid_API_request(bottom_location, bottom_location_type)[1])
        + '.csv'))[0]
    logging.debug('#data sucessfully retreived from config')
except:
    logging.error('#some data or config file is missing')
headlines = news_API_request(covid_terms)

static_foler_name = config['covid_html_handler']['static_foler_name']

app = Flask(__name__,
            static_folder= static_foler_name
            )

newArticles = []
newsToRemove = []
news_articles = news_API_request(covid_terms)

# a function that loops indefinatley in the background that removes a toast when it 
#reaches its time of updating 
def toast_handler():
    """
This function takes in a csv file and parses it to return a list of strings,
each string comprises one line in the file.

:param csv_filename: The filepath to the csv file containing the data.

:return parsed_data: A list of strings containing values separated by commas

"""

    logging.debug('#toast_handler function called')
    
    '''
    Removes the toast from the user interface when the time is passed .

            Parameters:
                    None

            Returns:
                    render_template (list): re-renders the user interface without the 
                                            deleted update toast
    '''
    while True:
        #if there is an update toast on the screen
        if updates:
            for x in range(len(updates)):
                now = datetime.now()
                #collect the curent time on pc
                current_time = now.strftime('%H:%M:%S')
                pt = datetime.strptime(current_time, '%H:%M:%S')
                #find how many seconds have elapsed in the day so far
                current_seconds = pt.second + pt.minute * 60 + pt.hour \
                    * 3600
                #find how many seconds would have elapes till the time on toast
                pt = datetime.strptime((((updates[x]['content'])[-6:])[:5]), '%H:%M')
                final_seconds = pt.second + pt.minute * 60 + pt.hour \
                    * 3600
                #find the difference between the two 
                #if the current time is more than the time on the toast
                if final_seconds < current_seconds:
                    #delete that toast
                    del updates[x]
                    logging.debug('#return updated render_template')
                    #somehow reload the page here
                    print('about to redirect')
                    #redirect the user back to /index
                    return redirect('/index')
                
                


@app.route('/index')
def index() -> tuple:
    
    '''
    Main body for the user interface. All user interface operations happen in here.

            Parameters:
                    none

            Returns:
                    render_template (list): renders the whole user interface
    '''


    remove_update = request.args.get('update_item')
    if remove_update:
        for x in range(len(updates)):
            if updates[x]['title'] == remove_update:
                del updates[x]

                # need to actaully cancel the scheduled job
                # at the moment it only removes the toast

    newsTitleToRemove = request.args.get('notif')
    if str(newsTitleToRemove) == 'None':
        pass
    else:
        newsToRemove.append(newsTitleToRemove)
        finalArticles = update_news('x', 'x', newsToRemove,
                                    news_articles, 'no')

        return render_template(
            'index.html',
            title='Daily Update',
            image='logo.png',
            location=location,
            local_7day_infections=local_7day_infections,
            nation_location=nation_location,
            national_7day_infections=national_7day_infections,
            hospital_cases=str('Current hospital cases in '
                               + str(nation_location) + ': '
                               + str(hospital_cases)),
            deaths_total=str('Total deaths in ' + str(nation_location)
                             + ': ' + str(deaths_total)),
            news_articles=news_articles[:5],
            updates=updates,
            )

    update_title = request.args.get('two')
    update_covid = request.args.get('covid-data')
    the_time = request.args.get('update')
    update_news_articles = request.args.get('news')
    repeat_next_day = request.args.get('repeat')

    if update_title and the_time:

        threading.Thread(target=toast_handler, name='toast_handler',
                         args=()).start()

        # --------------get the time till it updates in seconds   ------------

        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        pt = datetime.strptime(current_time, '%H:%M:%S')
        current_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
        pt = datetime.strptime(the_time, '%H:%M')
        final_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
        if repeat_next_day:
            final_seconds = final_seconds +86400
        time_till_update = final_seconds - current_seconds

        if update_covid:
            update_covid = 'Update Covid Data'
            get_scheduled_updates(update_title, the_time, update_covid)


            # ----------------update the covid data------------

            threading.Thread(target=schedule_covid_updates,
                             name='data_update',
                             args=(time_till_update, update_title,
                             'data')).start()
            

        if update_news_articles:
            update_news_articles = 'Update News Articles'
            get_scheduled_updates(update_title, the_time,
                                 update_news_articles)

            # update the news articles

            update_news(time_till_update, update_title, newsToRemove,
                        news_articles, 'yes')
  
    
    return render_template(
        'index.html',
        title='Daily Update',
        image='logo.png',
        location=location,
        local_7day_infections=local_7day_infections,
        nation_location=nation_location,
        national_7day_infections=national_7day_infections,
        hospital_cases=str('Current hospital cases in '
                           + str(nation_location) + ': '
                           + str(hospital_cases)),
        deaths_total=str('Total deaths in ' + str(nation_location)
                         + ': ' + str(deaths_total)),
        news_articles=news_articles[:5],
        updates=updates,
        )

if __name__ == '__main__':
    app.run()
