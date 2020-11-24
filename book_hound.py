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






# breakpoint hold
pass












