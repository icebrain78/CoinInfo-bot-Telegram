import requests
from parsel import Selector
import os
import telegram
import time

my_token=''
bot=telegram.Bot(token = my_token)

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

if not os.path.exists("binance_latest.txt"):
    f=open("binance_latest.txt","w+")
    f.write("Initate")
    f.close()
HEADERS={}
url="https://support.binance.com/hc/en-us/sections/115000106672-New-Listings"
for i in range(0,44):
    try:
        r=requests.get(url,timeout=0.5)
        sel=Selector(text=r.text)
        notice=sel.xpath('//li[contains(@class,"article-list-item")]/a/@href').extract()[0]
        #print(sel.xpath('//li[contains(@class,"article-list-item")]/a/@href'))
        notice_url="https://support.binance.com"+notice
        try:
            rr=requests.get(notice_url,timeout=0.5)
            se=Selector(text=rr.text)
            #print(se.xpath('//h1[contains(@class,"article-title")]/text()').extract())
            title=se.xpath('//h1[contains(@class,"article-title")]/text()').extract()[0].strip('\n \n')
            begin=se.xpath('//div[contains(@class,"article-body")]/p/strong/text()').extract()[0]
            bodys=se.xpath('//div[contains(@class,"article-body")]/p/span/text()').extract()
            #print(title)
            body=begin
            for content in bodys:
                body=body+content
            latest=title+'\n'+body+'\n'
            with open(os.path.join(BASE_DIR,'binance_latest.txt'),'r+',encoding='utf-8') as f_read:
                b_title=f_read.readlines()[0].strip('\n \n')
                f_read.close()
                #print(b_title==title)
                if b_title!=title:
                    bot.sendMessage(chat_id='@hkcoin', text="#Binance 새 글이 올라왔습니다\n"+latest)
                    with open(os.path.join(BASE_DIR,'binance_latest.txt'),'w+',encoding='utf-8') as f_write:
                        f_write.write(latest)
                        f_write.close()
            time.sleep(1)
        except requests.exceptions.ConnectionError:
           # print('')
            time.sleep(1)
    except requests.exceptions.ConnectionError:
        #print('')
        time.sleep(2)