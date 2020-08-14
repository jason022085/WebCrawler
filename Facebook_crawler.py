# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:22:55 2020

@author: Jason HF
"""
import sys
import pandas as pd
import re
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


def FindLinks(url, n):
    Links = []
    driver.get(url)
    for i in range(n):
        time.sleep(3)
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')

    soup = BeautifulSoup(driver.page_source)
    posts = soup.findAll('div', {'class': '_1dwg _1w_m _q7o'})
    for i in posts:
        Links.append('https://www.facebook.com' + i.find('a',
                                                         {'class': '_5pcq'}).attrs['href'].split('?', 2)[0])
    return Links


def expand(url):  # 尚未理解這段程式碼的細部功能，主要是負責展開留言。
    driver.get(url)
    try:
        driver.find_element_by_xpath('//a[@lang="en_US"]').click()
    except:
        print("Now is in EN_US")
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # 點擊「comments」，藉以展開留言
    try:
        driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[3]/div/div/div/div/div/div/div/div/div[2]/div[2]/form/div/div[2]/div[2]/div/span[2]').click()
        time.sleep(1)
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
    except:
        print('There is no comment!')
    k = 1
    while k < 20:
        try:
            driver.find_element_by_xpath(
                '//div/div[3]/ul/li['+str(k)+']/div[2]/div/a/div/span').click()
            print('Yes, I get one behind!')
        except:
            print('No other messages behind!')
        try:
            driver.find_element_by_xpath(
                '//div/div[3]/div['+str(k)+']/div/a/div/span').click()
            print('Yes, I get the next one!')
        except:
            print('No other messages below!')
        time.sleep(1)
        k += 1

# 文章內容與互動摘要


def PostContent(soup):
    # po文區塊
    userContent = soup.find('div', {'class': "_1dwg _1w_m _q7o"})
    # po文人資訊區塊
    PosterInfo = userContent.find('div', {'class': 'j_hw1cw3kzs'})
    # 互動摘要區(讚、留言與分享)
    feedback = soup.find('form', {'class': "commentable_item"})
    # 名稱
    Name = PosterInfo.find('a').attrs['title']
    # 網址
    Link = driver.current_url
    # 發文時間
    try:
        Time = PosterInfo.find('abbr').attrs['title']
    except:
        Time = PosterInfo.find('div', {'class': '_1atc fsm fwn fcg'}).text
    # 文章內容
    try:
        Content = userContent.find('div', {'data-testid': "post_message"}).text
    except:
        Content = ""
    # Like
    try:
        Like = feedback.find('span', {'class': '_81hb'}).text
    except:
        Like = '0'
    # 留言
    try:
        commentcount = feedback.find('a', {'class': '_3hg- _42ft'}).text
    except:
        commentcount = '0'
    # 觀看人數
    try:
        seecount = feedback.find(
            'a', {'data-testid': "UFI2SeenByCount/root"}).text
    except:
        seecount = '0'
    return pd.DataFrame(
        data=[{'Name': Name,
               'Link': Link,
               'Time': Time,
               'Content': Content,
               'Like': Like,
               'Seecount': seecount,
               'Commentcount': commentcount}],
        columns=['Name', 'Time', 'Content', 'Like', 'Commentcount', 'Seecount', 'Link'])

# 留言


def CrawlComment(soup):

    Comments = pd.DataFrame()
    # po文區塊
    userContent = soup.find('div', {'class': '_5pcr userContentWrapper'})

    # 回應貼文的留言
    for i in userContent.findAll('div', {'aria-label': "留言"}):
        try:
            CommentContent = i.find('span', {'dir': 'ltr'}).text
        except:
            CommentContent = 'Sticker'
        Comment = pd.DataFrame(data=[{'CommentID': i.find('a', {'class': "_6qw4"}).attrs['href'].split('comment_id=', 2)[1],
                                      'CommentName':i.find('a', {'class': "_6qw4"}).text,
                                      'CommentTime': i.find('abbr').attrs['data-tooltip-content'],
                                      'CommentContent':CommentContent,
                                      'Link':driver.current_url}],
                               columns=['CommentID', 'CommentName', 'CommentTime', 'CommentContent', 'Link'])
        Comments = pd.concat([Comments, Comment], ignore_index=True)

    # 用戶留言區
    userContent = soup.find('div', {'class': '_5pcr userContentWrapper'})

    # 回應留言的留言
    for i in userContent.findAll('div', {'aria-label': "留言回覆"}):
        try:
            CommentContent = i.find('span', {'dir': 'ltr'}).text
        except:
            CommentContent = 'Sticker'
        Comment = pd.DataFrame(data=[{'CommentID': i.find('a', {'class': "_6qw4"}).attrs['href'].split('comment_id=', 2)[1],
                                      'CommentName':i.find('a', {'class': "_6qw4"}).text,
                                      'CommentTime': i.find('abbr').attrs['data-tooltip-content'],
                                      'CommentContent':CommentContent,
                                      'Link':driver.current_url}],
                               columns=['CommentID', 'CommentName', 'CommentTime', 'CommentContent', 'Link'])
        Comments = pd.concat([Comments, Comment], ignore_index=True)
    return Comments

# 設定封鎖通知


def set_options():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    return options

# 登入


def login(driver):
    input_account = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/form/div[2]/div[1]/input')
    input_account.send_keys('jason022085@gmail.com')  # 輸入帳號
    time.sleep(0.1)
    input_password = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/input')
    input_password.send_keys('jason028520_jcdj4315')  # 輸入密碼
    time.sleep(0.1)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/form/div[2]/div[3]/button').click()
    return 0


driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=set_options())
Links = FindLinks(url='https://www.facebook.com/groups/246969398721876/', n=0)
login(driver)
# sys.exit()
# %%
# 抓下來所有留言
PostsInformation = pd.DataFrame()
PostsComments = pd.DataFrame()
Links = FindLinks(url='https://www.facebook.com/groups/246969398721876/', n=40)
for i in Links:
    print('Dealing with: ' + i)
    try:
        expand(i)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        PostsInformation = pd.concat(
            [PostsInformation, PostContent(soup)], ignore_index=True)
        PostsComments = pd.concat(
            [PostsComments, CrawlComment(soup)], ignore_index=True)
    except:
        print('Load Failed: ' + i)

# 刪除完全一樣的資料
PostsInformation.drop_duplicates(inplace=True)
PostsComments.drop_duplicates(inplace=True)
# 存檔
PostsInformation.to_excel('D:/PostsInformation.xlsx')
PostsComments.to_excel('D:/PostsComments.xlsx')
