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
my_token='537097274:AAGrw2EpxvEfVIqNp2em9lFKYFpMFply4D8'
bot=telegram.Bot(token = my_token)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
if not os.path.exists("amazonenaws_latest.txt"):
    with open(os.path.join(BASE_DIR,'amazonenaws_latest.txt'),'w+',encoding='utf-8') as f_write:
        f_write.write("Initate::0")
        f_write.close()


url="https://s3.ap-northeast-2.amazonaws.com/crix-production/crix_master"
for i in range(0,50):
    try:
        r=requests.get(url)
        content=r.json()[-1]
        timestamp=content['timestamp']
        pair=content['pair']
        latest=str(content)+"::"+str(timestamp)
        with open(os.path.join(BASE_DIR,'amazonenaws_latest.txt'),'r+',encoding='utf-8') as f_read:
            before=f_read.readlines()[0]
            b_timestamp=before.split("::")[1]
            f_read.close()
#            print(b_timestamp==str(timestamp))
            if b_timestamp!=str(timestamp):
                print("#new amazonenaws")
                bot.sendMessage(chat_id='@hkcoin', text="[업비트 신규성장] 업데>이트됨\n"+str(pair))
                with open(os.path.join(BASE_DIR,'amazonenaws_latest.txt'),'w+',encoding='utf-8') as f_write:
                    f_write.write(latest)
                    f_write.close()
                time.sleep(1)
    except requests.exceptions.ConnectionError:
        print("Connection Error--Please wait 3 seconds")
    time.sleep(1)