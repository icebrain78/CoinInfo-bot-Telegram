#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pymysql
import time
import re

u1="https://www.binance.com/kr/support/sections/115000202591"
u2="https://www.binance.com/kr/support/sections/115000106672"
def parse_news_init(url):
    try:
        _url=url
        res=requests.get(url)
        soup=BeautifulSoup(res.text,'html.parser')

        items=soup.find_all('li',class_='article-list-item')
        news_list=[]
        for item in items:
            res=requests.get("https://www.binance.com"+item.a['href'])
            article=BeautifulSoup(res.text,'html.parser').find('article',class_='article')

            title=  article.header.h1['title']
            content=article.section.find('div',class_='article-content').find('div',class_='article-body')

            news_list.append([title,content])
            #time.sleep(2)
    except Exception as ex:
        print("Error: ",ex)
    return news_list
def parse_categories_init(url):
    try:
        _url=url
        res=requests.get(url)
        soup=BeautifulSoup(res.text,'html.parser')

        items=soup.find_all('li',class_='article-list-item')
        news_list=[]
        for item in items:
            res=requests.get("https://www.binance.com"+item.a['href'])
            article=BeautifulSoup(res.text,'html.parser').find('article',class_='article')

            title=  article.header.h1['title']
            content=article.section.find('div',class_='article-content').find('div',class_='article-body')

            news_list.append([title,content])
            #time.sleep(2)
    except Exception as ex:
        print("Error: ",ex)
    return news_list
def db_connect(_url,_host,_user,_pwd,_db,_table):
    db=pymysql.connect(host=_host,
                    user=_user,
                    passwd="",
                    db=_db,
                    charset='utf8')
    if _table=="news":
        items=parse_news_init(_url)
    elif _table=="new_listing":
        items=parse_categories_init(_url)
    try:
        with db.cursor() as cursor:
            for item in items:
                title,contents=item
                cursor.execute('select * from '+_table +' where title=%s',pymysql.escape_string(title))
                data='none'
                #for i in data:
                #    data=i
                if data=='none':
                    re_contents=str(contents)
                    idx=re_contents.find("class")
                    re_contents=re_contents.replace(re_contents[idx:idx+5],"className")
                    print(re_contents)
                    sql="insert into "+_table+" (`title`,`contents`,`created`,`type`) values (%s,%s,NOW(),0)"
                    cursor.execute(sql,(pymysql.escape_string(title),re_contents))
                    db.commit()
                else:
                    continue
                #제목이 존재하지 않는 경우 추가 
    finally:
        db.close()
def parse_section():
    return
def parse_categories():
    return 
def check_exists():
    return

#print(parse_news(u))
#db_connect(u1,'localhost','root','056692a','coins','news')
db_connect(u2,'localhost','root','youngjae1!a','coins','new_listing')