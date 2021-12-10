import requests
from flask import *
import json
from newsapi import NewsApiClient
import sched
import time
import threading
import logging

#define the log file and its paramiters 
logging.basicConfig(filename='C:\\Users\\louis\\OneDrive - University of Exeter\\ECM1400 Programming\\CourseWork//log.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)




#define the schedular 
s = sched.scheduler(time.time, time.sleep)
logging.info('#attempt to find config file ')
    #attempt to open the config file 
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    #config file is found 
    logging.debug('#config file found')
except:
    'config file not found - give an error'
    logging.critical('No config file found')
    
logging.info('#attempt to access API key and covid terms ')
    #attempt to get the news API key (add your own) and the serch fitler terms
try:
    covid_terms = config['covid_news_handling']['covid_terms']
    newsapi = NewsApiClient(api_key=config['covid_news_handling']['api_key'])
    #all has been dassigned correctly from the config 
    logging.debug('sucsess')
except:
    #soemthing went wrong - throw an error 
    logging.critical('missing config file or config file missing data')

#a function to get news articles via the newsapi module
def news_API_request(covid_terms: str ="Covid COVID-19 coronavirus" ) -> list:
    logging.info("covid_terms({0})".format(covid_terms))
    '''
    Returns an array of dictionarys of all the news articles given by the API request

            Parameters:
                    covid_terms (list): A list of covid terms to filter the news search

            Returns:
                    news_articles (list): List of dictionarys of all the news articles
    '''
    logging.debug('Getting news articles from news API')
    all_articles = newsapi.get_everything(q=covid_terms, language='en')
    logging.debug('sucess')
    #structures how the news will be placed in a dict
    news = {'title': [], 'content': [], 'url': []}
    news_articles = []
    title = []
    content = []
    URL = []
    x = -1
    #add the news to a list of dictionarys format 
    logging.debug('putting news into a list of dictionarys')
    #loop through all the articles
    for article in all_articles['articles']:
        x = x + 1
        title.append(article['title'])
        content.append(article['description'])
        URL.append(article['url'])
        #append each dictionary of article to the list news_articles
        news['title'].append(article['title'])
        news['content'].append(article['description'])
        news['url'].append(article['url'])
        news_articles.append({'title': news.get('title')[x],
                             'content': news.get('content')[x] + '\n'
                             + news.get('url')[x], 'status': 'open'})
    #return news articles list of dictionarys
    logging.debug('return list of dictioarys of news articles')
    return news_articles


updates = []

# a function to collect the scheduled updates from the api 
def get_scheduled_updates(update_title: str , time: str, utype: str) -> list:
    logging.info("get_sceduled_updates({0},{1}, {2})".format(update_title, time, utype))
    '''
    Uploads the toasts for the updates in the user interface 

            Parameters:
                    update_title (str): The header for the toast
                    time (str): the time the update is to be scheduled
                    utype (str): the type of update it is for

            Returns:
                    updates (list): List of dictionarys of all the toasts to be uploaded
    '''
    #append toast info to a list of dictioanrys 
    logging.debug('Attempting to append toast info to list (updates)')
    try:
        updates.append({'title': utype, 'content': str(update_title+' - (Update scheduled for: '+time+')'),
                        'type': utype})
        #return a list of dictionarys for each toast 
        logging.debug('Sucessfully appened toast info')
    except:
        logging.error('failed to append toast info')
    return updates

#a function that updates the news articles and threads them over to be scheduled for an update
def update_news(
    update_interval: int,
    update_name: str,
    newsToRemove: list,
    news_articles: list,
    do_update: str,
    ) -> list:
    
    logging.info("get_sceduled_updates({0}, {1}, {2}, {3}, {4})".format(update_interval, update_name, newsToRemove,news_articles, do_update ))
    
    '''
    Updates the news atricles and reuploads them to the api. Also makes sure not to
    re-upload previously deleted news articles

            Parameters:
                    update_interval (int): Delay for the schedule to do the update
                    update_name (str): The name for the shcedule
                    newsToRemove (list): List of the news articles that wont be reuploaded
                    news_articles (list): List of the current news articles 
                    do_update (str): yes or no for if an update is required
                    

            Returns:
                    news_articles (list): list of dictionarys of the new news articles
    '''
    #import shceduled covid updates now as it would have been defined by now 
    logging.debug('attempting to import schedule_coivd_updates from covid_data_handler.py ')
    try:
        from covid_data_handler import schedule_covid_updates
        logging.debug('import OK')
        #import is complete - you can now schedule updates
    except:
        #import failed - throw an error 
        logging.critical('failed to import')
        
    logging.debug('#check if update is needed')
    #check if an update is needed
    if do_update == 'yes':
        logging.debug('schedule an update for covid news')
        #if an update is needded then schedule it 
        threading.Thread(target=schedule_covid_updates,
                         name='news_update', args=(update_interval,
                         update_name, 'news')).start()
    else:
        #if an update isnt needed then filter it from previously deleted articles
        logging.debug('#no covid news update needed')
        if not newsToRemove:
            pass
            logging.debug('#No news to remove')
        else:
            #loop through all the articles of both lists
            for y in range(len(newsToRemove)):
                for x in range(len(news_articles)):
                    #compare each article from each list
                    if news_articles[x]['title'] == newsToRemove[y]:
                        #if any articles are on the newsToRemove list then delete them
                        del news_articles[x]
                        logging.debug('#retrun an updated list of news articles')
                        #return the clean list of news_articles
                        return news_articles
