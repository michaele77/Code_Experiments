"""
This file checks the snowbird reservation website for available dates.
If one of the dates that we want is available, sent a notification through email or text

Author: Michael Ershov
Date: 12/13/20
"""
#---------------------------------------------------------#
#                   IMPORT TIME                           #
#---------------------------------------------------------#
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
from urllib.request import urlopen
import base64
import io
from PIL import Image

import os
from twilio.rest import Client
from playsound import playsound
import vlc




#---------------------------------------------------------#
#                   USED FUNCTIONS                        #
#---------------------------------------------------------#

def setup_driver(op_headless = False):
    chrome_options = webdriver.chrome.options.Options()
    if op_headless:
        chrome_options.add_argument("--headless")

    fnc_driver = webdriver.Chrome(options=chrome_options)

    return fnc_driver


def get_soup(fnc_url_link, soupit = False):
    driver.get(fnc_url_link)
    if soupit:
        soup_to_return = BeautifulSoup(driver.page_source, 'lxml')
        return soup_to_return


def save_str_img(inputStr, file_loc):
    img = Image.open(io.BytesIO(inputStr))
    rgb_im = img.convert('RGB')
    rgb_im.save(file_loc + '.jpg')

def play_alarm(alarm_time=20):
    file = 'annoying_alarm.mp3'

    print('Playing alarm...')

    p = vlc.MediaPlayer(file)

    p.play()
    currTime = time.time()
    # Play for 20 seconds
    while time.time() < currTime + alarm_time:
        pass
    p.stop()



# def send_text_msg(message_text):
#     # Your Account Sid and Auth Token from twilio.com/console
#     # and set the environment variables. See http://twil.io/secure
#     account_sid = os.environ['AC7247fb44eb62d277a2d81dde0053b4c1']
#     auth_token = os.environ['642432a674cf8eb3de0366aa72f0a1c4']
#     client = Client(account_sid, auth_token)
#
#     message = client.messages \
#         .create(
#         body=message_text,
#         from_='+18583827358',
#         to='+18583827358'
#     )






#---------------------------------------------------------#
#                    MAIN FUNCTION                        #
#---------------------------------------------------------#
# Do not use main sentinal so that global variables can be used...
# We will not be using this file for imports anyway

snowbird_link = 'https://www.snowbird.com/parking/#parking_reservation'

# Setup the webdriver
driver = setup_driver(False)

# Get XML soup from the link
get_soup(snowbird_link)
time.sleep(0.5)
iframe_id = 'parking-widget'
driver.switch_to.frame(iframe_id)

# Grab all of the relevant dates
dec_18 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[3]/td[6]')
dec_19 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[3]/td[7]')
dec_20 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[1]')
dec_21 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[2]')
dec_22 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[3]')

prev_img_18 = dec_18.screenshot_as_base64
prev_img_19 = dec_19.screenshot_as_base64
prev_img_20 = dec_20.screenshot_as_base64
prev_img_21 = dec_21.screenshot_as_base64
prev_img_22 = dec_22.screenshot_as_base64

# # FOR DEBUGGING:
prev_img_20 = 'hello 1'


counter = 0

while(True):
    # Grab webpgage (refresh it)
    get_soup(snowbird_link)
    time.sleep(3)
    iframe_id = 'parking-widget'
    driver.switch_to.frame(iframe_id)

    # Get all of the specific days
    dec_18 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[3]/td[6]')
    dec_19 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[3]/td[7]')
    dec_20 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[1]')
    dec_21 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[2]')
    dec_22 = driver.find_element_by_xpath('/html/body/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[3]')

    # Get images of specific days
    curr_img_18 = dec_18.screenshot_as_base64
    curr_img_19 = dec_19.screenshot_as_base64
    curr_img_20 = dec_20.screenshot_as_base64
    curr_img_21 = dec_21.screenshot_as_base64
    curr_img_22 = dec_22.screenshot_as_base64


    # Now run comparisons
    if counter == 0:
        playTime = 10
    else:
        playTime = 100

    if curr_img_18 != prev_img_18:
        play_alarm(alarm_time = playTime)
        print('Day has changed! 18')
    if curr_img_19 != prev_img_19:
        play_alarm(alarm_time = playTime)
        print('Day has changed! 19')
    if curr_img_20 != prev_img_20:
        play_alarm(alarm_time = playTime)
        print('Day has changed! 20')
    if curr_img_21 != prev_img_21:
        play_alarm(alarm_time = playTime)
        print('Day has changed! 21')
    if curr_img_22 != prev_img_22:
        play_alarm(alarm_time = playTime)
        print('Day has changed! 22')


    # Set the previous days to be the current days for comparison
    prev_img_18 = curr_img_18
    prev_img_19 = curr_img_19
    prev_img_20 = curr_img_20
    prev_img_21 = curr_img_21
    prev_img_22 = curr_img_22


    print('Counter is at {0}'.format(counter))

    counter += 1





# a = soup.select('#parking_reservation')
# for i,elem in enumerate(a[0].children):
#     if i == 1:
#         nextElement = elem
#         break
#
# for i,elem in enumerate(nextElement.children):
#     print(elem)