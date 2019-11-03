import requests
from parsel import Selector
import telegram
import time
import os
my_token=''
bot=telegram.Bot(token = my_token)
#print(bot.getUpdates())
#chat_id=bot.getUpdates()[-1].message.chat.id

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
HEADERS={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}
url="https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20"
for i in range(0,52):
    try:
        r=requests.get(url,headers=HEADERS,timeout=0.5)
        id_list=[]
        for i in r.json()['data']['list']:
            id_list.append(i['id'])
        content_url='https://api-manager.upbit.com/api/v1/notices/'+str(id_list[0])
        try:
            rr=requests.get(content_url,headers=HEADERS,timeout=0.5)
            title=rr.json()['data']['title']
            updated_at=rr.json()['data']['updated_at']
            created_at=rr.json()['data']['created_at']
            body=rr.json()['data']['body']
        #print('----------')
            latest=title+'\n'+updated_at+'\n'+created_at+'\n'+body+'\n'
            with open(os.path.join(BASE_DIR,'upbit_latest.txt'),'r+',encoding='utf-8') as f_read:
                before= f_read.readlines()[0]
                f_read.close()
                if before!=title+'\n':
               # print("#new upbit")
               # print(latest)
                    bot.sendMessage(chat_id='@hkcoin', text="#Upbit 새 글이 올라왔습니다\n"+latest)
                    with open(os.path.join(BASE_DIR,'upbit_latest.txt'),'w+',encoding='utf-8') as f_write:
                        f_write.write(latest)
                        f_write.close()
        except requests.exceptions.ConnectionError:
            print("Connection Error--Pleasw wair 3 seconds")
    except requests.exceptions.ConnectionError:
        print("Connection Error--Please wait 3 seconds")
    time.sleep(1)