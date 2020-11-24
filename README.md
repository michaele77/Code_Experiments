# Code Experiments 

This is a place where I experiment with different packages, new modules, or start the prototyping for new project ideas. Most of this repository is written in Python for speed of development, code readability, and the large availability of modules to simplify implementation.

# API Keys

The API Keys for the different APIs I use in the code experiments are stored in a config.py file that I import for any file that requires API keys. 
Config.py includes a function names "access_keys" that takes in the file name string, and returns the needed keys as strings. 
Config.py is not tracked by git for security.

# Files Included

## book_hound.py
An attempt to create a book recommendation engine using the goodreads API by creating a  book reviewer graph that would be traversed to find commonly agreed-upon books that are most pointed-to by the web.
Unfortunately, goodreads API only provides limited reviewer information and limited information about users; it also has a 1 result / second access limitation.

### To Dos
Use a web-scraper instead of the API to construct the reviewer graph. The information would be stored in a database that could be used for future queries. 

## craveit.py
Experimentation with a food-ranking app that searches nearby restaurants' menus for specific food items and displays them with actual images taken from review posts.
The yelp API not only provides limited endpoints to access images (only gives a maximum of 3 images), but it also provides zero menu information.

### To Dos 
Use a web-scraper to search for nearby restaurants based on location. A combination of the API (for getting restaurant names) and the web-scraper (for getting the menu/associated images) should be used.

## webscraper_PS5
An attempt to scrap commonly used websites for PS5 sales (Walmart, Best-buy, etc) and build a rough notifications program to text users once the PS5 is in stock.
Existing notification sites have a high latency (ie updating once a minute) which is often too slow for flash sales.

### To Dos 
None