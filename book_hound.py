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
from selenium.webdriver.common.keys import Keys
import requests
import numpy as np
import pickle
import sys
import copy


use_driver = input('Use chrome driver? [1 for yes]: ')

try_threading_DOE = input('Try the threading DOE? [1 for yes]: ')

skip_scraping = input('Skip the scraping/starting with already-scraped data? [1 for yes]: ')


def get_page(fnc_url_link):
    if not use_driver:
        # a = 1/0 #throws a floating-point error, goes to the except (uncomment if dont want to run try code)
        # global globalDelay
        # globalDelay += .2
        time.sleep(1)
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


        ##Below is the old code that WORKED

        t2 = time.time()
        driver.get(fnc_url_link)
        t3 = time.time()
        dT = t3 - t2
        print('get time = {0}'.format(dT))

        t2 = time.time()
        soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')
        t3 = time.time()
        dT = t3 - t2
        print('soup time = {0}'.format(dT))


        # ##Below is the new code for infinite scrolling
        # ##Source: https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho
        #
        #
        # t2 = time.time()
        # driver.get(fnc_url_link)
        # t3 = time.time()
        # dT = t3 - t2
        # print('get time = {0}'.format(dT))
        #
        # t2 = time.time()
        # no_of_pagedowns = 20
        # elem = driver.find_element_by_tag_name("body")
        # while no_of_pagedowns:
        #     elem.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(0.2)
        #     no_of_pagedowns -= 1
        # soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')
        #
        # t3 = time.time()
        # dT = t3 - t2
        # print('soup + scroll time = {0}'.format(dT))

    return soup_toreturn



def get_page_inf_scroll(fnc_url_link, scroll_num = 20):
    ##Below is the new code for infinite scrolling

    continueFlag = True
    pageIter = 1
    ratingsListFnc = []
    ratingsList = None
    ratingsScore_AVG = None
    ratingsScore_OWN_temp = None

    page_limit = 15 ##Automatically stops if more than 5 pages
    star_limit = 3 ##Automatically stops once 3 or less stars encountered TODO: what if NONE is encountered?

    while continueFlag:
        append_string = '&page=' + str(pageIter)
        driver.get(fnc_url_link+append_string)

        temp_soup = BeautifulSoup(driver.page_source, 'lxml')

        small_ratingsList = temp_soup.select('.field.title')
        small_ratingsList.pop(0)
        small_ratingsScore_AVG = temp_soup.select('.field.avg_rating')  # This simply gets AVERAGE RATING OF THE BOOK
        small_ratingsScore_AVG.pop(0)
        small_ratingsScore_OWN = temp_soup.select('.staticStars.notranslate')
        # No need to pop from the notranslate selection

        ############################
        #####EXCTRACTION TIME#######
        ############################

        #Extract title string
        small_ratingsList = [ currRating.contents[1].contents[1].attrs for currRating in small_ratingsList ]

        #Extract the book's average rating from info string
        small_ratingsScore_AVG = [ float(currAVG.text.split('\n')[0].split(' ')[-1]) for currAVG in small_ratingsScore_AVG ]

        #Extract the actual score from the per-book rating
        tempRatingList_0 = [ currPers.attrs['title'] for currPers in small_ratingsScore_OWN ]
        tempRatingList_1 = [ star_assignment[tempRating] for tempRating in tempRatingList_0 ]
        small_ratingsScore_OWN = tempRatingList_1.copy()

        ############################
        ####END EXCTRACTION TIME####
        ############################





        if not ratingsList:
            ratingsList = small_ratingsList.copy()
            ratingsScore_AVG =  small_ratingsScore_AVG.copy()
            ratingsScore_OWN = small_ratingsScore_OWN.copy()
        else:
            ratingsList = ratingsList + small_ratingsList.copy()
            ratingsScore_AVG = ratingsScore_AVG + small_ratingsScore_AVG.copy()
            ratingsScore_OWN = ratingsScore_OWN + small_ratingsScore_OWN.copy()

        # ratingsList_to_add = temp_soup.select('.field.title')[1:]
        if not small_ratingsList:
            print('We have hit the final page! final page count: {}'.format(pageIter))
            continueFlag = False
            #Note, this count counts the base page as 1 page...so only 1 extra page --> 2 total pages

        elif pageIter >= page_limit:
            print('We have hit the set page limit! final page count: {}'.format(pageIter))
            continueFlag = False
            # Note, this count counts the base page as 1 page...so only 1 extra page --> 2 total pages

        elif any(temp_comp <= star_limit for temp_comp in small_ratingsScore_OWN):
            print('We have hit the "moderately bad" rated books! final page count: {}'.format(pageIter))
            #Remove any indices that are beyond the first 'setStar' rating
            first_index_beyond = ratingsScore_OWN.index(star_limit)

            ratingsList = ratingsList[0:first_index_beyond]
            ratingsScore_AVG = ratingsScore_AVG[0:first_index_beyond]
            ratingsScore_OWN = ratingsScore_OWN[0:first_index_beyond]

            continueFlag = False
            # Note, this count counts the base page as 1 page...so only 1 extra page --> 2 total pages


        else:
            print('currently at {}'.format(len(ratingsList)))
            pageIter += 1


    # soup_toreturn = BeautifulSoup(driver.page_source, 'lxml')

    print('soup + scroll time = {0}'.format(dT))

    return ratingsList, ratingsScore_AVG, ratingsScore_OWN






##copy chromedriver into python folder, or just pass to it its path
##Currently, chromedriver binary lives in /usr/local/bin/

if use_driver:
    #Make the chrome driver headless for speed improvement
    chrome_options = webdriver.chrome.options.Options()
    # chrome_options.add_argument("--headless")

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


#--------------------------------#
#  Goodreads Star Assignment     #
#--------------------------------#
#  Stars   |  field rating value #
#--------------------------------#
#   5      |  'it was amazing'   #
#   4      |  'really liked it'  #
#   3      |      'liked it'     #
#   2      |     'it was ok'     #
#   1      |  'did not like it'  #
#   N/A    |       No key        #
#--------------------------------#

star_assignment = {}

star_assignment['it was amazing']   = 5
star_assignment['really liked it']  = 4
star_assignment['liked it']         = 3
star_assignment['it was ok']        = 2
star_assignment['did not like it']  = 1


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



if try_threading_DOE:

    x = 136251
    urlNum = list(range(x,x+50))
    globalDelay = 0



    #Remove any problem books in the list
    print(urlNum)


    #Below for loop prototypes the multiprocessing attempt
    #First is the multiprocessing attempt

    import concurrent.futures
    MAX_THREADS = 30
    threads = min(MAX_THREADS, len(urlNum))
    comb_url_str = [url_location + str(i) for i in urlNum]


    print('Staring multiprocessing DOE...')
    tDOE_0 = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # time.sleep(1)  # to avoid the random-length HTML garbage anti-attack mechanism
        soup = executor.map(get_page, comb_url_str)

    dT_DOE_0 = time.time() - tDOE_0
    print('Multiprocessing time: {0}'.format(dT_DOE_0))
    print('~~~~~~~')

    for i in soup:
        try:
            print(i.select('#bookTitle')[0].text.strip())
        except:
            print('Blocked!~~~~~~~~~')

    time.sleep(5)

    #Second is the vanilla attempt
    print('Staring vanilla DOE...')
    tDOE_1 = time.time()
    for book_reference_number in urlNum:
        time.sleep(1)  # to avoid the random-length HTML garbage anti-attack mechanism

        soup = get_page(url_location + str(book_reference_number))


    dT_DOE_1 = time.time() - tDOE_1
    print('Vanilla Method time: {0}'.format(dT_DOE_1))
    print('~~~~~~~')

    time.sleep(5)

    pass #BREAKPOINT


urlNum = [1]        #some harry potter book
urlNum = [186074]   #The Name of the Wind
urlNum = [20518872] #The Three Body Problem

if not skip_scraping:
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
            # ratings_soup = get_page(goodreads_root + reviewer_info[i]['ratings link'])
            # ratings_soup = get_page_inf_scroll(goodreads_root + reviewer_info[i]['ratings link'])
            ratingsList, ratingsScore_AVG, ratingsScore_OWN  = get_page_inf_scroll(goodreads_root + reviewer_info[i]['ratings link'])
            t1 = time.time()
            dT = t1 - t0
            print('ratings time = {0}'.format(dT))

            #iterate through all of the ratings, add it to the dictionary as a list of dictionaries (each one being the rating)
            #TODO: Figure out basic proxy gathering/proxy list for multithreading scraping
            #TODO: Once a basic 30x30 structure is saved, flesh out basics for net-creation algorithm
            #TODO: Get a prototype going
            #TODO: figure out how to make the javascript page scroll down to refesh to get all the ratings


            reviewer_info[i]['ratings'] = []
            for j in range(len(ratingsList)):
                reviewer_info[i]['ratings'].append(ratingsList[j])
                book_AVG_score = ratingsScore_AVG[j] #currently not used...include in the book node in the future
                reviewer_info[i]['ratings'][j]['score'] = ratingsScore_OWN[j]

        pass #breakpoint

    dTime = time.time() - currTime
    print('Time elapsed: {0} seconds'.format(dTime))
    print('That is {0} sec/user'.format(dTime / 30))

    ogRecLimit = sys.getrecursionlimit()
    sys.setrecursionlimit(100000)
    with open('book_hound_vars/extracted_html_data_ThreeBodyProblem_ratingPagelimit-15_userPages-1.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([book_info, reviewer_info], f)

    # Getting back the objects:
    with open('book_hound_vars/extracted_html_data_ThreeBodyProblem_ratingPagelimit-15_userPages-1.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        book_info_ld, reviewer_info_ld = pickle.load(f)

    sys.setrecursionlimit(ogRecLimit)

#At this point in the program, we have the following data structure:
#book_info     --> dict('title', 'author', 'meta', 'details', 'reviewers')
#                          |        |        |         |          |
#                          V        V        V         V          V
#                         str      str      str       str     list(30*str)

#reviewer_info --> list(30*dict) --> dict('name', 'link', 'ratings link', 'ratings')
#                                           |       |           |             |
#                                           V       V           V             V
#                                          str     str         str      list(30+x * dict) --> dict('title', 'href', 'score')
#                                                                                                     |        |       |
#                                                                                                     V        V       V
#                                                                                                    str      str    float

#At this point, we can search and display our measly 30 reviewers
#Let's search through each reviewer, and make
#   1) a 'Reviewer' node of each reviewer and
#   2) a 'Book' node for each of their rated books (after checking that it doesnt exist already

class BookNode:
    def __init__(self, input_book_info):
        self.title      = input_book_info['title']
        self.href       = input_book_info['href']
        self.raters     = [] #will track which users have rated this book (for traversal)

    def add_rater(self, input_rater, input_rater_score):
        inTuple = (input_rater, input_rater_score)
        self.raters.append(inTuple)


class UserNode:
    def __init__(self, input_reviewer_info):
        self.name           = input_reviewer_info['name']
        self.link           = input_reviewer_info['link']
        self.ratingsLink    = input_reviewer_info['ratings link']
        self.ratings        = input_reviewer_info['ratings'] #contains raw raters book list

        self.books          = [] #this variable will filter the self.ratings data, and will assign

    def add_book(self, input_book, input_score):
        inTuple = (input_book, input_score)
        self.books.append(inTuple)




pass #breakpoint



# Now let's save the raw data we extracted for net construction later
# Saving the objects:
ogRecLimit = sys.getrecursionlimit()
sys.setrecursionlimit(100000)

# Getting back the objects:
with open('book_hound_vars/extracted_html_data_ThreeBodyProblem_ratingPagelimit-15_userPages-1.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    book_info, reviewer_info = pickle.load(f)

sys.setrecursionlimit(ogRecLimit)


#Create the network with the correct class assignments
#For each book (in this case, 1) iterate through all of the users
#Create a user node for each user, and a book node for each of their corresponding rated books
#For each user's books, search that this book is not in the network before adding it

covered_books = [] #list to keep track of books that have been added to the net
covered_users = [] #list to keep track of users that have been added to the net
userNum = len(reviewer_info)

for idx_user in range(userNum):
    #Create the user node and add it to the tracker list
    currUser_dict = reviewer_info[idx_user]
    try:
        user_instance = UserNode(currUser_dict)
    except:
        print('DEAD USER~~~~')
        print('PASSING...')
        continue

    covered_users.append(user_instance)
    user_idx = covered_users.index(user_instance)

    #Now, iterate through the user's books
    bookNum = len(currUser_dict['ratings'])
    for idx_book in range(bookNum):
        currBook_dict = currUser_dict['ratings'][idx_book]

        #Check that the book is not in the net already
        #Track by full object pointer in the list
        book_instance = BookNode(currBook_dict)
        covered_book_hrefs = [i.href for i in covered_books]

        if book_instance.href not in covered_book_hrefs: #use hrefs for consistent string comprehension
            covered_books.append( book_instance )
            book_idx = len(covered_books) - 1
        else:
            #find the existing object in the list by searching through the hrefs
            book_idx = covered_book_hrefs.index(book_instance.href)

        #Now that we have the correct book object, let's add to both the book and user reference lists
        #first is book instance --> rater
        inRater = covered_users[user_idx]
        inScore = currBook_dict['score']
        covered_books[book_idx].add_rater(inRater, inScore)

        #second is user instance --> book
        inBook = covered_books[book_idx]
        inScore = currBook_dict['score']
        covered_users[user_idx].add_book(inBook, inScore)





pass #BREAKPOINT



#---------------------------------------------------------#
#                  Process the {Results}                  #
#---------------------------------------------------------#


##First, print the top 10 books, along with the number pointing to them
users_pointing_num = [len(i.raters) for i in covered_books]

#use numpy for index sorting
top_10_idx = np.argsort(users_pointing_num)[-100:]
print(top_10_idx)

print('Top 10 searched books')
print('[Title]: [Number of Users]')
for currI in reversed(top_10_idx):
    print('{0}: has {1} users digging it'.format( covered_books[currI].title, len(covered_books[currI].raters)))



pass #BREAKPOINT



#---------------------------------------------------------#
#          Initiating App Prototyping Sequence            #
#---------------------------------------------------------#





#---------------------------------------------------------#
#                  Summarized Learnings                   #
#---------------------------------------------------------#
#
#   1) Should either build up a SQL database through scraping beforehand for real time queries, or
#      scrape info in real-time as it is input (probably prefer the first one)
#
#   2) Use multi-threading for the scraping method
#       --> the method called when scraping should ideally be a class that assigns which
#           books/things to scrape automatically/from a queue
#       --> Use either N proxies (N being the number of threads active) or some VPN to avoid blocking
#       --> Blocking occurs when accesses happen > 1 requests/sec, remain blocked for a few hours
#       --> Implement logging so that we can scrape for some time then pause execution
#       --> Each individual IP assigned to a "crawler" that would operate at 1 request/sec throughput
#       --> Full throughput would simply be IP number * 1 [requests/sec]
#       FREE PROXY LIST: https://free-proxy-list.net/
#       PROXY IMPLEMENTATION TUTORIAL: https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
#
#   3) "Tinder-lke" front end
#       --> Swipe up for "you've read the book and liked it"         => network improves by matching common kindreds
#       --> Swipe down for "you've read the book and didn't like it" => network improves by cutting unalike kindred
#       --> Swipe right for "you haven't read this book, but interested" => add to will read books (no network change?)
#       --> Swipe left for "you haven't read this book, but not interested => banned from appearing (no network change?)
#---------------------------------------------------------#
#              Speed Demon: Tips + Tricks                 #
#---------------------------------------------------------#
# Assume that we will be scraping B books
#   Each book has N users
#       Each user has an average of P ratings pages

# Then, each user's links are:  T_user = P (1 to get to rating's page, then P-1 for subsequent page loads)
# Each book's links are:        T_books = N*T_users + overhead (overhead is # of user pages to click on, assume 2)
# Total links are:              T_total = B*T_books + overhead (overhead is # of book pages to click on, assume 1000)
#                                       = B*(N*P + 2) + 1000

# To convert to time, assume that we have 10 proxies, and each link takes ~1.5seconds
#                               T_time [hours] = 1.5*T_total/10/3600 = 0.15*T_total/3600

# If B == 50,000, N == 100, P == 2 --> Total links == 10,101,000 links == 420 hours
# If B == 20,000, N == 150, P == 1 --> Total links == 3,000,000 links == 125 hours













