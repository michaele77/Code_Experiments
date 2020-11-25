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



usrIn = input('Run the goodreads API or webscrape (1 for API)? ')

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
from selenium import webdriver
##copy chromedriver into python folder, or just pass to it its path
##Currently, chromedriver binary lives in /usr/local/bin/
driver = webdriver.Chrome()
#driver.set_window_position(-2000,0)#this function will minimize the window
# first_url = 1
# last_url = 10000     # Last book is 8,630,000

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

for book_reference_number in urlNum:
    driver.get(url_location+str(book_reference_number))
    soup = BeautifulSoup(driver.page_source, 'lxml')

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
        driver.get(goodreads_root + reviewer_info[i]['link'])
        user_soup = BeautifulSoup(driver.page_source, 'lxml')

        #fish out the ratings link on the top left hand corner of the user's page
        #add it to the dictionary once we have it
        reviewer_info[i]['ratings link'] = user_soup.select('.profilePageUserStatsInfo')[0].contents[1].attrs['href']


        #Step into the user's ratings page
        #NOTE: can change how the ratings are sorted by changing the "sort=ratings" bit
        driver.get(goodreads_root + reviewer_info[i]['ratings link'])
        ratings_soup = BeautifulSoup(driver.page_source, 'lxml')

        #iterate through all of the ratings, add it to the dictionary as a list of dictionaries (each one being the rating)
        #TODO: figure out how to make the javascript page scroll down to refesh to get all the ratings
        ratingsList = ratings_soup.select('.field.title')
        reviewer_info[i]['ratings'] = []
        for j,currRating in enumerate(ratingsList):
            if j == 0:
                #first listed element is some formatting thing
                continue
            reviewer_info[i]['ratings'].append(currRating.contents[1].contents[1].attrs) #append the rating's dictionary
            print(j)


    pass #breakpoint

# breakpoint hold
pass












