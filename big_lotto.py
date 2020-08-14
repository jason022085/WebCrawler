from bs4 import BeautifulSoup
import requests
#%%
winning_Numbers_Sort_lotto = ['Lotto649Control_history_dlQuery_No1_','Lotto649Control_history_dlQuery_No2_',
                              'Lotto649Control_history_dlQuery_No3_','Lotto649Control_history_dlQuery_No4_',
                              'Lotto649Control_history_dlQuery_No5_','Lotto649Control_history_dlQuery_No6_',
                              'Lotto649Control_history_dlQuery_SNo_']

def search_winning_numbers(css_class):#尋找中獎號碼(包括特別號)
    global winning_Numbers_Sort_lotto
    if(css_class != None):
        for i in range(len(winning_Numbers_Sort_lotto )):
            if winning_Numbers_Sort_lotto [i] in css_class:
                return css_class    
def parse_tw_lotto_html(data_Info,number_count):#整理成list和dict
    data_Info_List = []
    data_Info_Dict = {}
    tmp_index = 0
    for index  in range(len(data_Info)) :
        if (index == 0):
            data_Info_List.append(data_Info[index].text)  
        else:
            if(index % number_count != 0):
                data_Info_List.append(data_Info[index].text)
            else:
                data_Info_Dict[str(tmp_index)] = list(data_Info_List)
                data_Info_List= []
                data_Info_List.append(data_Info[index].text)
                tmp_index = tmp_index+1
        data_Info_Dict[str(tmp_index)] = list(data_Info_List)
    return data_Info_List,data_Info_Dict   
def get_term_lotto_result(term):#獲取單期開獎結果
    term = str(term)
    from selenium import webdriver
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument('--headless')#無頭模式(加入此行可讓虛擬瀏覽器不被顯示出來)
    #browser = webdriver.Chrome()
    browser = webdriver.Chrome(chrome_options=chrome_options)
    head_Html_lotto='http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
    browser.get(head_Html_lotto)
    browser.find_element_by_id('Lotto649Control_history_txtNO').click() 
    browser.find_element_by_id('Lotto649Control_history_txtNO').send_keys(term) #搜尋框中輸入
    browser.find_element_by_id('Lotto649Control_history_btnSubmit').click()
    page_result = browser.page_source   
    soup = BeautifulSoup(page_result,'lxml')
    header_Info = soup.find_all(id=search_winning_numbers)
    data_Info_List,data_Info_Dict  = parse_tw_lotto_html(header_Info,7) 
    return data_Info_List
def add_more_years(num):
    import numpy as np
    if num == 0:
        return np.array(range(103000001,103000090))#今天只開到108000089，等2019過完之後，就能調到103000109
    else:
        return np.concatenate((add_more_years(num-1),add_more_years(num-1)+10**6), axis=None)
#%%測試單頁開獎結果
'''        
head_Html_lotto='http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
res = requests.get(head_Html_lotto, timeout=30)
soup = BeautifulSoup(res.text,'lxml')
header_Info = soup.find_all(id=search_winning_numbers)
data_Info_List,data_Info_Dict  = parse_tw_lotto_html(header_Info,7)    
print(data_Info_Dict)
'''
#%%取得所需要的號碼
import numpy as np
all_lotto_results = []
all_terms = add_more_years(5)
for term in all_terms:
    all_lotto_results.append(get_term_lotto_result(term))
#%%將結果存成xlsx
import pandas as pd
df = pd.DataFrame(all_lotto_results)
df.to_excel("lotto_result.xlsx")