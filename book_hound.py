"""
This script try to use the goodreads API to create a basic book recommendation engine

The idea is to input book 1, then see all users who liked/read this book
    --> then show book lists from what those users enjoyed
    --> as more books are selected by the user, the "web" of users who liked those same books grows smaller
        --> thus, recommendations get better

Michael Ershov
November 21, 2020
"""


#---------------------------------------------------------#
#             Goodreads API Access Attempt                #
#---------------------------------------------------------#




# from goodreads import client
import goodreads as vanilla_gr
import goodreads_api_client as gr
import time
import os

#grab the current execution file path name, return from code if not found
exec_path = os.path.realpath(__file__)
exec_path_bare = exec_path.split('/')[-1] #split up sptring on '/' char, output last bit (which is the file name)
print('Executing file name: ' + exec_path_bare)

try:
    import config
    API_KEY, API_SECRET = config.access_keys(exec_path_bare)
    print('Importing config file successful!')
    print('-----')
except ImportError as import_err:
    print('ERROR: ' + str(import_err))
    print('Add correct config.py file with API Keys then try again')
    quit() #stop running the code if no config.py file found



usrIn = input('Run the goodreads API or webscrape? [1 for API]: ')

if usrIn == str(1):
    client = gr.Client(developer_key=API_KEY)
    #Example: get 'The Last Wish' to see what parameters show up
    book = client.Book.show('1128434')
    print(book)

    print('sleeping zzz...')
    time.sleep(1) #stop for 1s (avoid API violation)

    #Show a ~random~ specific review info
    review = client.Review.show('3805')
    print(review)

    print('sleeping zzz...')
    time.sleep(1) #stop for 1s (avoid API violation)

    #Look at the book title?
    book_title = client.Book.title('The Last Wish')
    print(book_title)
    bt_work = book_title['work']
    print(bt_work)

    print('sleeping zzz...')
    time.sleep(1) #stop for 1s (avoid API violation)

    quit()



#---------------------------------------------------------#
#           Goodreads Web-Scraping Attempt                #
#---------------------------------------------------------#


##Code taken from stack overflow post on scraping goodreads with selenium
##Source: https://stackoverflow.com/questions/52794154/blocked-while-scraping-goodreads-com

import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import requests


use_driver = input('Use chrome driver? [1 for yes]: ')


def get_page(fnc_url_link):
    if not use_driver:
        # a = 1/0 #throws a floating-point error, goes to the except (uncomment if dont want to run try code)

        ####### REQUEST GET METHOD for URL
        t2 = time.time()
        r = requests.get(fnc_url_link)
        t3 = time.time()
        dT = t3-t2
        print('request time = {0}'.format(dT))

        ####### DATA FROM REQUESTS.GET
        t2 = time.time()
        data = r.text
        t3 = time.time()
        dT = t3-t2
        print('data time = {0}'.format(dT))

        t2 = time.time()
        soup_toreturn = BeautifulSoup(data, 'lxml')
        t3 = time.time()
        dT = t3-t2
        print('soup time = {0}'.format(dT))


        # # start session and get the search page
        # session = requests.Session()
        # response = session.get(fnc_url_link)
        #
        # # parse the search page using SoupStrainer and lxml
        # strainer = SoupStrainer('form', attrs={'id': 'form1'})
        # soup_toreturn = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

    elif use_driver:
        driver.get(fnc_url_link)
        soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')

    return soup_toreturn



##copy chromedriver into python folder, or just pass to it its path
##Currently, chromedriver binary lives in /usr/local/bin/

if use_driver:
    #Make the chrome driver headless for speed improvement
    chrome_options = webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)


url_location = 'https://www.goodreads.com/book/show/'






#See table below that explains website structure

#-----------------------------------------------------------------------------#
#                      Goodreads Javascript Structure                         #
#-----------------------------------------------------------------------------#
#  Content     |         CSS Class           |              ID                #
#-----------------------------------------------------------------------------#
#  Book title  |    '.gr-h1.gr-h1--serif'    |        '#bookTitle'            #
#    Author    |       '.authorName'         |     '#bookAuthors' (NA)        #
#  Book Meta   |     '.uitext.stacked'       |        '#bookMeta'             #
#   Details    |   '.uitext.darkGreyText'    |         '#details'             #
#  All Review  |    '.review' (in a list)    | '#bookReview' (all in string)  # <--- There are 30 reviews on the first page
#   Reviewers  |     '.user' (in a list)     | '#bookReview' (all in string)  # <--- 30 reviewers, link in the href here
# User's Stats | '.profilePageUserStatsInfo' |             -                  #
#-----------------------------------------------------------------------------#


#Below we will parse through one book
#input is the book URL we will parse
#SOP is below:
#   -Go to input book site
#   -Get book statistics
#   -Iterate and create objects for the 30 reviewers on the first page
#   -Step into each reviewer's site using their href (using .user[i] text, search for href)
#       -Extract user's page statistics
#       -Step into the reviewer's rated books using their href (using .profilePageUserStatsInfo, search for hred)
#           -Get all of the user's rated books (using .bookalike.review[i] text)

urlNum = [1]

currTime = time.time()
for book_reference_number in urlNum:

    soup = get_page(url_location+str(book_reference_number))

    #Get general book info
    book_info = {}

    book_info['title'] = soup.select('#bookTitle')[0].text.strip()  #book title
    book_info['author'] = soup.select('.authorName')[0].text.strip() #author
    book_info['meta'] = soup.select('#bookMeta')[0].text.strip()   #book meta
    book_info['details'] = soup.select('#details')[0].text.strip()    #book details (stats)

    for i,v in enumerate(book_info):
        print('Book {0}: {1}'.format(i,v))

    #Now, step into the 30 reviewers on the first page
    book_info['reviewers'] = soup.select('.user') #Raw format (not text) of all reviewers

    reviewer_info = []
    for i, curr_user in enumerate(book_info['reviewers']):
        print('Reviewer {0} ~~~~~~~~~~~~~~~~~~'.format(i))
        reviewer_info.append({})
        reviewer_info[i]['name'] = curr_user.attrs['title']
        reviewer_info[i]['link'] = curr_user.attrs['href']

        #Step into the user's page
        goodreads_root = 'https://www.goodreads.com'
        t0 = time.time()
        user_soup = get_page(goodreads_root + reviewer_info[i]['link'])
        t1 = time.time()
        dT = t1 - t0
        print('user time = {0}'.format(dT))

        #fish out the ratings link on the top left hand corner of the user's page
        #add it to the dictionary once we have it
        try:
            reviewer_info[i]['ratings link'] = user_soup.select('.profilePageUserStatsInfo')[0].contents[1].attrs['href']
        except:
            try:
                #Author's page has a different layout type...
                reviewer_info[i]['ratings link'] = user_soup.select('.smallText')[0].contents[1].attrs['href']
                print('On an authors page!')
            except:
                #Some people make their profiles private...
                user_text = user_soup.select('#privateProfile')[0].text
                usertextList = []
                usertextList.append( user_text.split('This')[1][1:20] )
                usertextList.append( user_text.split('Sign in to ')[1].split('\n')[0] )

                print('On a private page, so no content available')
                print('From users page: {0}, {1}'.format(usertextList[0], usertextList[1]))
                print('skipping to next reviewer')
                continue


        #Step into the user's ratings page
        #NOTE: can change how the ratings are sorted by changing the "sort=ratings" bit
        t0 = time.time()
        ratings_soup = get_page(goodreads_root + reviewer_info[i]['ratings link'])
        t1 = time.time()
        dT = t1 - t0
        print('ratings time = {0}'.format(dT))

        #iterate through all of the ratings, add it to the dictionary as a list of dictionaries (each one being the rating)
        #TODO: figure out how to make the javascript page scroll down to refesh to get all the ratings
        #TODO: implement multi-core parallel processing: https://stackoverflow.com/questions/52748262/web-scraping-how-make-it-faster
        ratingsList = ratings_soup.select('.field.title')
        reviewer_info[i]['ratings'] = []
        for j,currRating in enumerate(ratingsList):
            if j == 0:
                #first listed element is some formatting thing
                continue
            reviewer_info[i]['ratings'].append(currRating.contents[1].contents[1].attrs) #append the rating's dictionary
            print(j)

    pass #breakpoint

dTime = time.time() - currTime
print('Time elapsed: {0} seconds'.format(dTime))
print('That is {0} sec/user'.format(dTime / 30))

#At this point in the program, we have the following data structure:
#book_info     --> dict('title', 'author', 'meta', 'details', 'reviewers'
#                          |        |        |         |          |
#                          V        V        V         V          V
#                         str      str      str       str     list(30*str)

#reviewer_info --> list(30*dict) --> dict('name', 'link', 'ratings link', 'ratings'
#                                           |       |           |             |
#                                           V       V           V             V
#                                          str     str         str      list(30+x * dict) --> dict('title', 'href')
#                                                                                                     |        |
#                                                                                                     V        V
#                                                                                                    str      str

#At this point, we can search and display


pass #breakpoint












