#!/usr/bin/env python
# coding: utf-8

# # BEFORE USING PLEASE INSTALL THE FOLLOWING:
#pip install selenium
#pip install webdriver-manager
#pip install beautifulsoup4
#pip install requests

# # Import Libraries
from email import message
import json
from pickletools import read_int4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import re
import time
import pandas as pd
import csv
import requests
import os
from csv import writer

#Show That Libraries are imported without errors
print('Succesfully Imported Libraries')

# # Function to retrieve youtube channel subs
#obtaining youtube subs by channel link
def get_subs_by_channel_link(channellink):

    #set chrome options to incognito
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    #start chrome driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()

    #chromedriver get link
    driver.get(channellink)
    
    #wait for coockies button
    page_load = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button'))
    )
    
    #click cookies button
    button = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button')
    button.click()
    
    #wait for number of subs to be present
    page_load2 = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string'))
    )
    
    #set the subs_element (element in which subs are found)
    subs_element = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/yt-formatted-string').text
    
    #quit driver
    driver.quit()
    
    #if K in subs_element
    if 'K' in subs_element:

        #select first part of the subs_element, the actual value
        subs_split = subs_element.split(' ')
        subs = subs_split[0]

        #If there is a comma in the value for decimals, change it to a dot. Then replace K (*1000)
        if ',' in subs:
            subs_dot = subs.replace(',', '.')
            subs_float = float(subs_dot.replace('K', ''))
            subs_final = int(subs_float * 1000)

            #return subs
            return(subs_final)
        
        #If there is a no comma in the value for decimals. Then replace K (*1000)
        else:
            subs_float = float(subs.replace('K', ''))
            subs_final = int(subs_float * 1000)

            #return subs
            return(subs_final)

    #if mln in subs_element
    elif 'mln.' in subs_element:

        #Select first part of subs_element
        subs_split = subs_element.split(' ')
        subs = subs_split[0]
        
        #If there is a comma in subs for decimals, change it to a dot. Then replace M (*1000000)
        if ',' in subs:
            subs_dot = subs.replace(',', '.')
            subs_float = float(subs_dot)
            subs_final = int(subs_float * 1000000)

            #return subs
            return(subs_final)
        
        #If there is a no comma in subs for decimals. Then replace mln (*1000000)
        else:
            subs_float = float(subs)
            subs_final = int(subs_float * 1000000)

            #return subs
            return(subs_final)

    #if K and mln are not in subs_element, no decimal values avaible then.
    else:

        #select first part of the subs_element, the actual value
        subs_split = subs_element.split(' ')
        subs = subs_split[0]
        subs_final = subs

        #return subs
        return(subs_final)

# # Function to retrieve instagram data
#obtaining instagram subs by username
def get_instagram_data2(username):
        
    #set chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    #start chrome driver
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()

    #set URL
    URL = 'https://www.instagram.com/'+username+'/'

    #chromedriver get link
    driver.get(URL)
    
    #wait for cookies button
    page_load2 = WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]'))
    )
    
    #set button element and click coockies button
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')
    button.click()
    
    #Make sure amound of followers is present
    page_load2 = WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/button/div/span'))
    )

    #set insta_followers to the correct element
    insta_followers = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/button/div/span').get_attribute('title')
    
    #driver quit
    driver.quit()

    #return instagram followers
    return(insta_followers)

# # Start of the script to obtain Twitch Channel Data and Chats
#obtaining twitch data by twitchlink & amount of minutes to scrape
def get_data_twitch(twitchlink, minutes):
   
   #set chrome options
   chrome_options = webdriver.ChromeOptions()
   chrome_options.add_argument("--incognito")

   #start chrome driver
   driver = webdriver.Chrome(chrome_options=chrome_options)

   #channel to inspect
   driver.get(twitchlink)

   #maximize window
   driver.maximize_window()

   #Make sure chat is loaded in - wait for enough messages with time.sleep
   page_load = WebDriverWait(driver, 150).until(
   EC.presence_of_element_located((By.CLASS_NAME, 'chat-line__message'))
   )
   
   #Make sure that div with channel information is loaded in
   page_load2 = WebDriverWait(driver, 150).until(
   EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/main/div[1]/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div'))
   )

   #Variables for data
   chat_list = []
   messages = {}
   instagram_data = {}
   instagram_data_start = {}
   instagram_data_end = {}
   youtube_data = {}
   youtube_data_start = {}
   youtube_data_end = {}
   stream_dict = {}

   #Variables for descriptives (without dicts)
   emote_list_all = []
   chat_list_all = []
   badge_list_all = []
   users_all = []

   #additional social links
   youtube_link = []
   instagram_link = []
   twitter_link = []

   #count set to zero. Count is used to count the loop number
   count = 0

   # the value in rangeset decides how many minutes the loop will run (e.g. 2 minutes in this case)
   rangeset = minutes

   #start met loopen
   for i in range(rangeset):
       count = count + 1
       print("start collection")
       time.sleep(60)

       #Store page data
       stream_data = driver.page_source

       #Extract necessary divs
       soup = BeautifulSoup(stream_data, 'lxml')
       chats_selector = soup.find_all('div', class_='chat-line__message')
       channel_info = soup.find('div', class_='channel-info-content')
       twitch_additional_links = soup.find('div', class_='Layout-sc-nxg1ff-0 ckXJcK')

       #For the first loop (1), extract stream name, title, and all available and useful links
       if count == 1:
           
           #streamer name and title
           streamer = channel_info.find('h1').text
           messages['Streamer'] = streamer
           stream_title = channel_info.find('h2').text
           messages['stream title'] = stream_title

           #Social Links In Twitch Channel Description
           for link in twitch_additional_links.findAll('a'):

               #youtube link with channelname, if not in youtube_link list, then append to list
               if 'youtube.com/channel/' in link.get('href') and link.get('href') not in youtube_link:
                   txt = link.get('href')

                   #if there is a questionmark in in youtube link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt:
                       ylink = txt.split("?", 1)
                       youtlink = ylink[0]

                   #if no questionmark in youtube link
                   else:
                       youtlink = txt
                   
                   #append youtube link to youtube_link list and to youtube_data dictionairy
                   youtube_link.append(youtlink)
                   youtube_data['youtube_link'] = youtlink

               #youtube link without channelname, if not in youtube_link list, then append to list
               elif 'youtube.com/user/' in link.get('href') and link.get('href') not in youtube_link:
                   txt = link.get('href')
                   txt2 = txt.replace('user/','')
                   
                    #if there is a questionmark in in youtube link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt2:
                       ylink = txt2.split("?", 1)
                       youtlink = ylink[0]

                   #if no questionmark in youtube link
                   else:
                       youtlink = txt2
                   
                   #append youtube link to youtube_link list and to youtube_data dictionairy
                   youtube_link.append(youtlink)
                   youtube_data['youtube_link'] = youtlink

               #youtube link without channelname, if not in youtube_link list, then append to list
               elif 'youtube.com/' in link.get('href') and link.get('href') not in youtube_link:
                   txt = link.get('href')

                   #if there is a questionmark in in youtube link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt:
                       ylink = txt.split("?", 1)
                       youtlink = ylink[0]

                   #if no questionmark in youtube link
                   else:
                       youtlink = txt
                   
                   #append youtube link to youtube_link list and to youtube_data dictionairy
                   youtube_link.append(youtlink)
                   youtube_data['youtube_link'] = youtlink

               #find instagram link, if not in instagram_link list, then append to list
               elif 'instagram.com/' in link.get('href') and link.get('href') not in instagram_link:
                   txt = link.get('href')
                   instagram_link.append(txt)
                   instagram_data['instagram_link'] = txt

               #find twitter link, if not in twitter_link list, then append to list
               elif 'twitter.com/' in link.get('href') and link.get('href') not in twitter_link:
                   txt = link.get('href')
                   
                   #if there is a questionmark in in twitter link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt:
                       tlink = txt.split("?", 1)
                       twitlink = tlink[0]

                   #if no questionmark in twitter link
                   else:
                       twitlink = txt
                   
                   #append twitter link to twitter list and to messages dictionairy
                   twitter_link.append(twitlink)
                   messages['streamer_twitter'] = twitlink

               #pass all other links
               else:
                   pass

           #Social Links in Channel Info
           for link in channel_info.findAll('a'):
               
               #youtube link with channelname, if not in youtube_link list, then append to list
               if 'youtube.com/channel/' in link.get('href') and link.get('href') not in youtube_link:
                   txt = link.get('href')
                   
                   #if there is a questionmark in in youtube link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt:
                       ylink = txt.split("?", 1)
                       youtlink = ylink[0]

                   #if no questionmark in youtube link
                   else:
                       youtlink = txt
                   
                   #append youtube link to youtube_link list and to youtube_data dictionairy
                   youtube_link.append(youtlink)
                   youtube_data['youtube_link'] = youtlink
               
               #youtube link without channelname, if not in youtube_link list, then append to list
               elif 'youtube.com/user/' in link.get('href') and link.get('href') not in youtube_link:
                   txt = link.get('href')
                   txt2 = txt.replace('user/','')

                   #if there is a questionmark in in youtube link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt2:
                       ylink = txt2.split("?", 1)
                       youtlink = ylink[0]

                    #if no questionmark in youtube link   
                   else:
                       youtlink = txt2
                   
                   #append youtube link to youtube_link list and to youtube_data dictionairy
                   youtube_link.append(youtlink)
                   youtube_data['youtube_link'] = youtlink
                   
                #youtube link without channelname, if not in youtube_link list, then append to list
               elif 'youtube.com/' in link.get('href') and link.get('href') not in youtube_link:
                   txt = link.get('href')
                   
                   #if there is a questionmark in in youtube link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt:
                       ylink = txt.split("?", 1)
                       youtlink = ylink[0]

                    #if no questionmark in youtube link
                   else:
                       youtlink = txt
                   
                   #append youtube link to youtube_link list and to youtube_data dictionairy
                   youtube_link.append(youtlink)
                   youtube_data['youtube_link'] = youtlink
                   
               #find instagram link, if not in instagram_link list, then append to list
               elif 'instagram.com/' in link.get('href') and link.get('href') not in instagram_link:
                   txt = link.get('href')
                   instagram_link.append(txt)
                   instagram_data['instagram_link'] = txt
                   
               #find twitter link, if not in twitter_link list, then append to list
               elif 'twitter.com/' in link.get('href') and link.get('href') not in twitter_link:
                   txt = link.get('href')

                   #if there is a questionmark in in twitter link, used to add additional arguments, then remove the questionmark and everything behind it
                   if '?' in txt:
                       tlink = txt.split("?", 1)
                       twitlink = tlink[0]

                   #if no questionmark in twitter link
                   else:
                       twitlink = txt

                   #append twitter link to twitter list and to messages dictionairy    
                   twitter_link.append(twitlink)
                   messages['streamer_twitter'] = twitlink
               
               #pass all other links
               else:
                   pass
           
           #if link is filled in execute followers scrape function
           if len(instagram_link)>0:

               #get first link from list
               ilink = instagram_link[0]

               #set instagram_data dictionairy's key instagram_link with the correct link
               instagram_data['instagram_link'] = ilink

               #separate the username from rest of the link
               before, sep, after = ilink.partition('instagram.com/')
               strValue = after

               #remove additional '/'
               if '/' in strValue:
                   insta_acc = strValue.replace('/', '')
               
               #if no additional /
               else:
                   insta_acc = strValue

               #try execute instagram data function
               try:
                   insta_followers_2 = get_instagram_data2(insta_acc)
                   
               #SET NA if exception is given
               except:
                   insta_followers_2 = 'NA'

                #set start followers
               instagram_data_start['followers'] = insta_followers_2

           #if no instagram link in list, set followers to NA and set instagram_data['instagram_link'] to NA as well
           else:
               instagram_data_start['followers'] = 'NA'
               instagram_data['instagram_link'] = 'NA'

           #check if youtube is filled in and if so add amount of subs
           if len(youtube_link)>0:
               
               #set youtube_data['youtube_link'] with the correct youtube link
               youtube_data['youtube_link'] = youtube_link[0]

               #try youtube subs function and then set youtube_data_start['subs'] with the result of the function
               try:
                    youtube_subs = get_subs_by_channel_link(youtube_link[0])
                    youtube_data_start['subs'] =  youtube_subs
               
               #if exception is geven, set youtube_data_start['subs'] to NA
               except:
                    youtube_data_start['subs'] = 'NA'
                

           #if no youtube link in list, set start subs and youtube_data['youtube_link'] to NA 
           else: 
               youtube_data_start['subs'] = 'NA'
               youtube_data['youtube_link'] = 'NA'

           #append start data of youtube and instagram to youtube_data['start'] and instagram_data['start'] respectively      
           youtube_data['start'] = youtube_data_start
           instagram_data['start'] = instagram_data_start
           
       
       #end followers & youtube subs: if instagram is filled in and if count = rangeset - 1
       elif count == rangeset:
           
           #print that last loop of streamer has started
           print('Last loop of streamer started')
           
           #if link is filled in execute followers scrape function
           if len(instagram_link)>0:
               ilink = instagram_link[0]
               before, sep, after = ilink.partition('instagram.com/')
               strValue = after
               
               #remove additional '/'
               if '/' in strValue:
                   insta_acc = strValue.replace('/', '')
               
               #if no additional '/'
               else:
                   insta_acc = strValue
               
               #try to execute instagram data function
               try:
                   insta_followers_2 = get_instagram_data2(insta_acc)
               
               #SET NA if exception is given
               except:
                   insta_followers_2 = 'NA'

               #add insta_followers_2 to instagram_data_end dict
               instagram_data_end['followers'] = insta_followers_2
           
           #if no instagram link in list, set followers to NA  
           else:
               instagram_data_end['followers'] = 'NA'
           
           #check if youtube is filled in and if so add amount of subs
           if len(youtube_link)>0: 
               
               #try subs function and append result to youtube_data_end dict
               try:
                   youtube_subs = get_subs_by_channel_link(youtube_link[0])
                   youtube_data_end['subs'] = youtube_subs

               #if exception is give, add Subs = NA to youtube_data_end dict 
               except:
                   youtube_data_end['subs'] = 'NA'
               
           #if no youtube link in list, set subs to NA 
           else: 
               youtube_data_end['subs'] = 'NA'

           #append instagram and youtube end data to instagram data dict and youtube data dict respectively  
           instagram_data['end'] = instagram_data_end
           youtube_data['end'] = youtube_data_end

       #Extract strean time every loop
       stream_time = channel_info.find('span', class_=re.compile('live-time')).text
       stream_time_df = "Stream time: {}".format(stream_time)

       #append streamtime to chat_list list
       chat_list.append(stream_time_df)

       #Extract chat outputs to list
       for chat_selector in chats_selector:

           #create empty chats dict
           chats = {}

           #GET ID
           id_span = chat_selector.find('span', class_=re.compile('chat-author__display-name')).text

           #append hashed user id to chats dict
           chats['id'] = hash(id_span)

           #append hashes user id to all users
           users_all.append(hash(id_span))

           #Message
           chat_span = chat_selector.find('span', class_='text-fragment')

           #try to find message
           try:
               chat = chat_selector.find('span', class_=re.compile('text-fragment')).text 
               chat_list_all.append(chat)
               chats['message'] = chat_selector.find('span', class_=re.compile('text-fragment')).text      
           
           #if exception given, set to N/A
           except:
               chats['message'] = "N/A"     

           #Badge(s)
           badge_list = []

           #try to find badges
           try:
               badge_divs = chat_selector.find_all('img', class_='chat-badge')
               for badge_div in badge_divs:
                   badge = badge_div['alt']
                   badge_list.append(badge)
                   badge_list_all.append(badge)  
               chats['badge(s)'] = badge_list
           
           #if exception given, set to N/A
           except:
               chats['badge(s)'] = "N/A"

           #Emote(s)
           emote_list = []

           #try to find emotes
           try:
               emote_divs = chat_selector.find_all('img', class_='chat-image chat-line__message--emote')
               for emote_div in emote_divs:
                   emote = emote_div['alt']
                   emote_list.append(emote)
                   emote_list_all.append(emote)

           #if exception given, set to N/A
           except:
               emote_list.append("No emote")

           #add emote_list to chats dict
           chats['emote(s)'] = emote_list

           #Add lists to messages dict
           chat_list.append(chats)
           messages['messages'] = chat_list

       print("1 minute loop is done!")

    #check descriptives
   emote_count = len(pd.DataFrame(emote_list_all))
   badge_count = len(pd.DataFrame(badge_list_all))
   chat_count = len(pd.DataFrame(chat_list_all))
   users_count = len(pd.DataFrame(users_all))
   new_users_count = len(set(users_all))

   #Create descriptives list
   DescList = [twitchlink, emote_count, badge_count, chat_count, users_count, new_users_count]

   #add list as row to twitch data statistics
   with open('twitch_data_statistics.csv', 'a') as f_object:
 
    # Pass this file object to csv.writer()
    # and get a writer object
    writer_object = writer(f_object)
 
    # Pass the list as an argument into csv
    # the writerow(): create a new row with list 
    writer_object.writerow(DescList)
 
    # Close the file object
    f_object.close()
   
   #append instagram_data dict and youtube_data dict to messages dict, and append messages dict and twitchlink to stream_dict 
   messages['instagram'] = instagram_data
   messages['youtube'] = youtube_data
   stream_dict['link'] = twitchlink
   stream_dict['data'] = messages
   
   #return stream_dict
   return(stream_dict)

# # Finding Data for List of Streamers
#x = start game int(0 < x < y)
#y = end game (x < int < 10)
#minutes = minutes scraped per channel
def twitch_datascraper(x,y,minutes):
    
    #import json again to prevent errors (known JSON bug)
    import json
    
    #games list
    games_list = []
    streamers_list = []
    streamer_list_final = []

    #chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()

    #get gaming directory
    driver.get('https://www.twitch.tv/directory/gaming')

    #Make sure element is loaded
    page_load = WebDriverWait(driver, 200).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div[1]/div[3]/div[2]'))
    )

    #Store page data
    games_data = driver.page_source

    #Extract div
    soup = BeautifulSoup(games_data, 'lxml')
    games_info = soup.find('div', class_='ScTower-sc-1dei8tr-0 fxnyeJ tw-tower')
    
    #find all links in games_info
    for link in games_info.findAll('a'):
        
        #if link in games_list then pass
        if link.get('href') in games_list:
            pass
        
        #if link not in games_list then if/else
        else:
            
            # if '/directory/game/' in link then append to games_list
            if '/directory/game/' in link.get('href'):
                games_list.append(link.get('href'))
            
            # if '/directory/game/' not in link then pass
            else:
                pass

    #for each game in gamelist (till 6th game)
    for item in games_list[x:y]:
        game_link = 'https://www.twitch.tv' + str(item)

        #get game link
        driver.get(game_link)

        #wait till channels are loaded
        page_load2 = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/section/div[4]/div/div[1]/div[1]/div[2]'))
        )

        #Store page data
        game_data = driver.page_source

        #Extract div
        soup2 = BeautifulSoup(game_data, 'lxml')
        game_info = soup2.findAll('div', class_='Layout-sc-nxg1ff-0 cUYIUW')

        #for each item in recommended game channels, dismiss the first 6 items and then take the next 6 items
        for item in game_info[6:12]:

            #for each link in item
            for link2 in item.findAll('a'):

                #if link in streamers list then pass
                if link2.get('href') in streamers_list:
                    pass

                #if link not in streamers list then pass
                else:

                    #if /videos in link then pass
                    if '/videos'in link2.get('href'):
                        pass
                    
                    #if /videos not in link then set streamer link
                    else:
                        streamerlink = 'https://www.twitch.tv' + link2.get('href')

                        #if adjusted link in streamers list then pass
                        if streamerlink in streamers_list:
                            pass

                        #if adjusted link not in streamers list then append
                        else:
                            streamers_list.append(streamerlink)
    
    #quit driver
    driver.quit()
    
    #print message
    print('Retrieving Streamers Done')

    #make csv ready for all descriptives
    with open("twitch_data_statistics.csv", "w", encoding = 'utf-8') as csv_file: 
        List = ['twitchlink', 'emote_count', 'badge_count', 'chat_count', 'users_count', 'new_users_count']
        writer = csv.writer(csv_file)
        writer.writerow(List) 
    
    #execute scrape script for each streamer
    for link in streamers_list:
        
        #try function to get twitch and other data
        try: 
            stream_dict_add = get_data_twitch(link, minutes)

        #if exception is given, set data of twitchlink to NA in stream_dict_add
        except:
            stream_dict_add = {"link":link, "data":"NA"}

        #add stream_dict_add to streamer_list_final and print 1 streamer done
        streamer_list_final.append(stream_dict_add)
        print('+1 streamer done')
    
    #create json dump
    json = json.dumps(streamer_list_final, indent=4)
    
    #export to json file
    with open("twitch_chat_json.json", "w") as outfile:
        outfile.write(json)

    #message that scraping is done    
    print('Scraping is done.')

#Show That Functions are imported without errors
print('Succesfully Imported functions')

#Ask For Input
start_scrape = int(input("Enter the starting game number (int between 0-6)"))
end_scrape = int(input("Enter the ending game number (int between 0-6)"))
minutes_to_scrape = int(input("Enter the number of minutes to scrape"))

#Execute Twitch Data Scraper
twitch_datascraper(start_scrape,end_scrape,minutes_to_scrape)

