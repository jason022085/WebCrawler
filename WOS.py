import pandas as pd
import time, re
import jieba
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
from Str_To_Cloud import English_Cloud
from Web import Web

class Paper:
    def __init__(self):
        self.Title = []
        self.ImpactFactor = []
        self.Abstract = []
        self.Keywords = []
        self.allInfo = []
        self.Web = Web()
        self.driver = self.Web.openWeb()

    def Search(self, url, keyword):
        self.driver.get(url)
        time.sleep(2)
        Keyword_box = self.driver.find_element_by_xpath("//input[@class='focusinput search-criteria-input']")
        self.Web.enter(Keyword_box, keyword)

        Setting_boxes = self.driver.find_element_by_xpath("//*[@id='WOS_GeneralSearch_input_form']/div[2]/div[2]/span")
        self.Web.click(Setting_boxes)

        ISTP_boxes = self.driver.find_element_by_id('editionitemISTP')
        self.Web.click(ISTP_boxes)

        ISSHP_boxes = self.driver.find_element_by_id('editionitemISSHP')
        self.Web.click(ISSHP_boxes)

        Time_select = Select(self.driver.find_element_by_xpath("//select[@aria-label='預先定義的時間範圍選項']"))
        Time_select.select_by_visible_text("最近 5 年")

        Search_button = self.driver.find_element_by_xpath('//*[@id="searchCell1"]/span[1]/button')
        self.Web.click(Search_button)
        time.sleep(2)

    
    def Page_Info(self):
        All_soup = self.Web.bs()
        Total_Count = int(All_soup.find(id="hitCount.top").get_text())
        # 搜尋結果數量
        print(Keyword, " 總共有", Total_Count, "個搜尋結果 (SSCI or SCI)")
        if (Review == 'y') or (Review == 'Y'):
            # 勾選Review
            Review_checkbox = self.driver.find_element_by_xpath('//*[@id="DocumentType_3"]')
            self.Web.click(Review_checkbox)
            # 限縮搜尋
            Review_checkbox = self.driver.find_element_by_xpath('//*[@id="DocumentType_tr"]/button[1]')
            self.Web.click(Review_checkbox)
            time.sleep(2)
            All_soup = self.Web.bs()
            # Review結果數量
            Total_Count = int(All_soup.find(id="hitCount.top").get_text())
            print(Keyword, " 總共有", Total_Count, "篇 Review papers (SSCI or SCI)")
        # 一頁 10 篇 paper
        all_Paper = All_soup.findAll('a', class_='smallV110 snowplow-full-record')
        
        # 點擊並爬取每一篇
        for Paper in all_Paper:
            Paper_url = 'http://apps.webofknowledge.com' + Paper.get('href')
            print(Paper_url)
            self.Paper_Info(Paper_url)

    def Paper_Info(self, Paper_url):
        self.driver.get(Paper_url)
        Paper_soup = self.Web.bs()
        
        # 期刊影響力
        ImpactFactor_button = self.driver.find_element_by_xpath('//a[@class="focusable-link snowplow-JCRoverlay"]')
        self.Web.click(ImpactFactor_button)
        ImpactFactor = self.driver.find_element_by_xpath('//table[@class="Impact_Factor_table"]/tbody/tr/td').text
        ImpactFactor = round(float(ImpactFactor), 1)
        self.ImpactFactor.append(ImpactFactor)
        print("期刊影響力: ", ImpactFactor)
        close_button = self.driver.find_element_by_xpath('//input[@alt="隱藏期刊資訊"]')
        self.Web.click(close_button)
        
        # 標題
        Title = Paper_soup.find('div', class_='title').value.get_text()
        print(Title)
        self.Title.append(Title)

        # 摘要
        all_Info = Paper_soup.findAll('div', class_='block-record-info')
        Abstract = all_Info[2].get_text()
        self.Abstract.append(Abstract)
        # print(Abstract)

        # 關鍵字
        Keywords = all_Info[3].get_text()
        self.Keywords.append(Keywords)
        # print(Keywords)

        self.Citation()

    def Citation(self):
        allCitation_button = self.driver.find_element_by_xpath('//a[@class="view-all-link snowplow-view-all-in-cited-references-page-top"]')
        self.Web.click(allCitation_button)
        Citation_Count =  self.driver.find_element_by_xpath('//p[@class="NEWpageTitle"]/span').text
        print("引用了", Citation_Count, "篇參考文獻")
        all_cite_soup = self.Web.bs()
        time.sleep(0.5)
        for count in range(30):
            try:
                cite = self.find_element_by_xpath(f'//*[@id="RECORD_{count}"]/div[3]').text
                print("抓到了!")#沒連結
            except:
                try:
                    cite = self.driver.find_element_by_xpath(f'//*[@id="RECORD_{count}"]/div[3]').text
                    print("抓到了!")#有連結
                except:
                    print("失敗了")
        print("引用文獻標題",cite.split('\n')[0])
        print("引用文獻作者",cite.split('\n')[1])
        print("引用文獻期刊",cite.split('\n')[2:])
        return 0

        # all_cite =  all_cite_soup.findAll('div', class_="search-results-item")
        # count=0
        # for cite in all_cite:
        #     count += 1
        #     try:
        #         cite_Title = cite.find('span', class_="reference-title").get_text()
        #         print("引用文獻標題: ", cite_Title)
        #     except:
        #         continue
        #     try:
        #         cite_Author = cite.find_element_by_xpath(f'//*[@id="FCR_NORMAL_DATA_{count}"]/div/div[1]').get_text()
        #         print("引用文獻作者: ", cite_Author)
        #     except:
        #         try:
        #             cite_Author = cite.find_element_by_xpath(f'//*[@id="RECORD_{count}"]/div[3]/div[1]').get_text()
        #             print("引用文獻作者: ", cite_Author)
        #         except:
        #             print("引用文獻作者錯誤")
        #     try:
        #         cite_CiteCount = cite.find('a', class_="snowplow-times-cited-link").get_text()
        #         print("引用文獻被引用次數: ", cite_CiteCount)
        #     except:
        #         print("被引用次數錯誤")


    def Parse(self, url, Keyword, Review):
        self.Search(url, Keyword)
        self.Page_Info()
        
#%%
if __name__ == '__main__':
    url = 'http://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=E65JakUBNv8yD5zlWbn&preferencesSaved='
    Keyword = '"learning analytics"'
    Review = "y"
    # Keyword = input("請輸入查詢關鍵字 : ")
    # Review = input("請問是否只要搜尋Review類型(y/n) : ")
    paper = Paper()
    paper.Parse(url, Keyword, Review)