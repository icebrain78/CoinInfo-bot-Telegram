import requests
import os,os.path,sys
import telegram
import time

#if os.path.exists(lockfile):
#    sys.exit()
#else:
#    l_file=open(lockfile,"w+")
#    l_file.write("1")
#    l_flie.close()
my_token=''
bot=telegram.Bot(token = my_token)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
if not os.path.exists("bitrex_latest.txt"):
    f=open("bitrex_latest.txt","w+")
    f.write("Initate::0")
    f.close()
url="https://bittrex.com/api/v1.1/public/getmarkets"
for i in range(0,35):
    try:
        r=requests.get(url)
        content=r.json()['result'][-1]
        mar=content['MarketName']
        created=content['Created']
        latest=str(content)+"::"+str(created)
        with open(os.path.join(BASE_DIR,'bitrex_latest.txt'),'r+',encoding='utf-8') as f_read:
            before=f_read.readlines()[0]
            b_created=before.split("::")[1]
            f_read.close()
            if b_created!=str(created):
                print("#new bitrex")
                bot.sendMessage(chat_id='@hkcoin', text="[Bitrex] 업데이트됨\n"+str(mar))
                with open(os.path.join(BASE_DIR,'bitrex_latest.txt'),'w+',encoding='utf-8') as f_write:
                    f_write.write(latest)
                    f_write.close()
                time.sleep(1)
    except requests.exceptions.ConnectionError:
        print("Connection Error--Please wait 3 seconds")
    time.sleep(1)
#os.unlink(lockfi