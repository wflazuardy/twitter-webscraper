'''
    Author  : Wildan Fajria Lazuardy
    Email   : wildanjawa@gmail.com
'''

# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Input variables
keyword = raw_input("Enter the keywords\t: ")
print "\nPlease enter the date with format (YYYY-MM-dd). \nExample\t: 2017-08-30"
print ""
date1 = raw_input("Take data from\t: ")
date2 = raw_input("Until\t\t\t: ")
print ""
pagedown = raw_input("Number of pagedown\t: ")

if date1 != "": date1 = "since:" + date1
if date2 != "": date2 = "until:" + date2

if pagedown == "":
    pagedown = 0
else:
    pagedown = int(pagedown)

# Combine the inputs to make a search query
query = "%s %s %s" %(keyword, date1, date2)

# Save file location
file = open('data/%s.csv'%keyword,'a')

if __name__ == "__main__":
    # Initiate browser
    browser = webdriver.Chrome('chromedriver.exe')

    browser.get("https://twitter.com/search-advanced")
    box_search = browser.find_element_by_class_name("search-input")
    box_search.send_keys(query, Keys.ENTER)

    time.sleep(2)

    elem = browser.find_element_by_tag_name("body")
    while pagedown:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        pagedown -= 1

    contents = browser.find_elements_by_class_name("tweet")
    for c in contents:
        username = c.find_element_by_class_name("username").text
        tweet = c.find_element_by_class_name("js-tweet-text-container").text.encode('utf-8')
        tweet = tweet.replace("\n", " ")

        # Making the soup, yummy!
        soup = BeautifulSoup(c.get_attribute('innerHTML'), 'html.parser')

        get_time = soup.find("a", {"class": "tweet-timestamp"})
        time = get_time['title']
        link = "https://twitter.com" + get_time['href']

        print "%s\t%s\t%s\t%s" %(username, time, tweet, link)

        file.write("%s;%s;%s;%s"%(username, time, tweet, link))
        file.write("\n")






