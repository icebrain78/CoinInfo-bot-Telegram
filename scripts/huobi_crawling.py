import requests
import os,sys,os.path
import telegram
from parsel import Selector
import time

my_token=''
bot=telegram.Bot(token=my_token)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
HEADERS={
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
'accept': 'application/json, text/plain, */*',
}

url="https://api.huobi.co.kr/v1/notice/list?language=ko-KR&limit=15&currPage=1"
for s in range(0,58):
    try:
        r=requests.get(url,headers=HEADERS,timeout=0.5)
        print(s)
        id_list=[]
        for i in r.json()['data']['list']:
            id_list.append(i['id'])
        title_id=max(id_list)
        id_idx=id_list.index(title_id)
        title=r.json()['data']['list'][id_idx]['title']
        content=r.json()['data']['list'][id_idx]['content']
        sel=Selector(text=content)
        content="\n".join(sel.xpath('//text()').extract())
        latest=str(title_id)+'\n'+title+'\n'+content+'\n'

        with open(os.path.join(BASE_DIR,'huobi_latest.txt'),'r+',encoding='utf-8') as f_read:
            before_list=f_read.readlines()[0:2]
            before=before_list[1].strip('\n')
            b_id=before_list[0].strip('\n')
            f_read.close()
            if int(b_id)<=title_id:
                if before!=title:
                    bot.sendMessage(chat_id='@hkcoin',text="Huobi 새 글이 올라왔습니다\n"+latest)
                    with open(os.path.join(BASE_DIR,'huobi_latest.txt'),'w+',encoding='utf-8') as f_write:
                        f_write.write(latest)
                        f_write.close()
            time.sleep(1)
    except requests.exceptions.ConnectionError:
        print("Connection Error--Please wait")