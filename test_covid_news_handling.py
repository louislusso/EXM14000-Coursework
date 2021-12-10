from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import covid_terms
from covid_html_handler import newsToRemove
from covid_news_handling import update_news
from covid_news_handling import get_scheduled_updates
import threading
# a test for the news_API_request function
def test_news_API_request() -> None:
    '''
    a test for the news_API_request function.

            Parameters:
                    None

            Returns:
                    None
    '''
    #check to see if theres a thing called covid_terms)
    assert news_API_request(covid_terms) 
    #check to see if the same news files are generated when using 
    # a string of covid terms rather than the variable attached to the string
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request(covid_terms)

#a test ofr the update_news fucntion
def test_update_news() -> None:
    '''
    a test ofr the update_news fucntion.

            Parameters:
                    None

            Returns:
                    None
    '''
    #find the current amount of threads 
    thread_count = threading.active_count()
    #call for a new update (should create a new thread)
    news_articles = news_API_request(covid_terms)
    news = update_news(10,'test_name',[],news_articles,'yes')
    #check to see if the tread count has increast 
    assert threading.active_count() > thread_count

# a test for the get_scheduled_updates function
def test_get_scheduled_updates() -> None:
    '''
    a test for the get_scheduled_updates function.

            Parameters:
                    None

            Returns:
                    None
    '''
    #input random arguments for the cheduled updates
    updates = get_scheduled_updates('update_title','11:11', 'data')
    #see if a list is returned
    assert isinstance(updates,list)