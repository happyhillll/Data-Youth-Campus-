#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import pandas as pd
from selenium import webdriver
import time

def get_posts(query, page_num):
    url_query = quote(query)  # 검색어 형태로 변경해주는 함수

#url
    url = 'https://search.naver.com/search.naver?query=' + url_query + '&nso=&where=blog&sm=tab_opt'

#data 저장
    blog_df = pd.DataFrame(columns=('Title', 'Date', 'Blog Url', 'Post'))
    idx = 0
    # 스크롤을 위한 driver선언
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url=url)

    # 입력한 페이지 수 만큼 스크롤
    for i in range(page_num):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)
        # print(i)

    # 크롤링 과정 : 검색화면 - 글 제목, 작성 날짜(중요x라서 형식에 맞게 변환x),url 스크래핑
    # url-블로그 포스터 전문 확인 가능
    # 크롤링 방지용 iframe 속으로 들어가서, post의 text만 크롤링하여 저장

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.find_all('div', {'class': 'total_wrap api_ani_send'})  # 검색화면의 블로그 목록

    for post in posts:
        # post 제목, 날짜
        title = post.select_one('.api_txt_lines.total_tit').text
        date = post.find('span', {'class': 'sub_time sub_txt'}).get_text()

        # url->블로그 창 연결
        post_url = post.find('a', {'class': 'api_txt_lines total_tit'}).get('href')

        try:
            post_link = urllib.request.urlopen(post_url).read()
            # post_link = req.urlopen(post_url).read()
            post_html = BeautifulSoup(post_link, 'html.parser')
        except:
            continue

        # iframe src를 통해 원본 접근
        for main_frame in post_html.select("iframe#mainFrame"):
            frame_url = "https://blog.naver.com" + main_frame.get('src')
            post_text = urllib.request.urlopen(frame_url).read()
            post_html = BeautifulSoup(post_text, 'html.parser')
            post_content_text = ""

            for post_content in post_html.find_all('div', {'class': 'se-main-container'}):
                post_content_text = post_content.get_text()

            # 형식이 다른 블로그 존재, 예외처리
            if post_content_text == "":
                for post_content in post_html.find_all('div', {'id': 'postViewArea'}):
                    post_content_text = post_content.get_text()
            post_content_text = post_content_text.replace('\n', '')
        blog_df.loc[idx] = [title, date, post_url, post_content_text]
        idx += 1
    return blog_df

query = input("검색: ")
page_num = int(input("page 수: "))  # 한 페이지당 약 30개
blog_df= get_posts(query, page_num)
print(blog_df.head())
blog_df.to_csv('blog_data_info.csv',encoding= 'utf-8-sig')
print("끝")


# In[24]:


from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import pandas as pd
from selenium import webdriver
import time


# In[25]:


def get_posts(query, page_num):
    url_query = quote(query)  # 검색어 형태로 변경해주는 함수

    #url
    url = 'https://search.naver.com/search.naver?query=' + url_query + '&nso=&where=blog&sm=tab_opt'


# In[22]:


#data 저장
blog_df = pd.DataFrame(columns=('Title', 'Date', 'Blog Url', 'Post'))
idx = 0
# 스크롤을 위한 driver선언
driver = webdriver.Chrome(executable_path='/Users/minjikim/Downloads/chromedriver')
driver.get(url=url)

# 입력한 페이지 수 만큼 스크롤
for i in range(page_num):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(1)
# print(i)

# 크롤링 과정 : 검색화면 - 글 제목, 작성 날짜(중요x라서 형식에 맞게 변환x),url 스크래핑
# url-블로그 포스터 전문 확인 가능
# 크롤링 방지용 iframe 속으로 들어가서, post의 text만 크롤링하여 저장


# In[ ]:




