# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:38:25 2021

@author: User
"""
import random
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd 


headers = {
   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41'
   }
restaurant_name = "貝思諾" #113評論 #存擋用
url_prefix = "https://www.google.com/async/reviewDialog?ei=TS4hYOX2JvOJr7wPjLu46AY&yv=3&async=feature_id:0x346e05e739267f8f%3A0xfebc44443f2cf20,review_source:All%20reviews,sort_by:qualityScore,start_index:0,is_owner:false,filter_text:,associated_topic:,next_page_token:,async_id_prefix:,_pms:s,_fmt:pc"


#建立author, grade, comment來存放資料
author =[]
grade = []
comment = []
sorting_method = "newestFirst,"  #排序方式用最新


for i in range(0,12):  #由上圖，判斷range上限，控制在小於等於 <= [(最大評論數/10)-1]
    start_index_value = i*10 #開始評論序
    next_page_token_value = start_index_value +10 #下一頁評論序
#把完整url組裝起來
    url =  url_prefix + sorting_method + "start_index:" + str(start_index_value) + ",is_owner:false,filter_text:,associated_topic:,next_page_token:" + str(next_page_token_value)  + ",_pms:s,_fmt:pc"
# 發送get請求
    sleep_time=random.uniform(0,2)
    print(f"先停留{sleep_time}秒...")
    time.sleep(sleep_time)
    try:
        text = requests.get(url,headers=headers).text
        soup = BeautifulSoup(text,'lxml')
        
        for s in soup.find_all(class_='jxjCjc'):
            #先過濾評論長度不為空：
                if s.find(class_="Jtu6Td").text != "":
                 #print(s.find(class_="Jtu6Td").text)
                 comment.append(s.find(class_="Jtu6Td").text)
                 author.append(s.find(class_="TSUbDb").text)
                 #print(author)
                 grade.append(s.find(class_='Fam1ne')['aria-label'].split("：")[1].split(" ")[0])
                 #print(grade)
        print(f"已抓取完第{start_index_value}到{next_page_token_value}項目..")
    except:
        print("已經抓不到資料了....")
        break
                                        
print(f"已抓取完畢..")
#整體成pd
google_comment_df = pd.DataFrame({
    "評論者":author,
    "評等":grade,
    "評語":comment,    
    })

    
#存出
#先去掉評語重複的rows，再存出
#google_comment_df.drop_duplicates(subset=["評語"])
#google_comment_df.to_csv(f"./google_{restaurant_name}_comment.csv",encoding='utf-8-sig')