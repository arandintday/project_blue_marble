import requests
import os
import time
import random
import shutil
import PIL.Image as im
from datetime import datetime,timedelta

cache_path = "cache_img"
gif_path = "out_gifs"
isCacheExists=os.path.exists(cache_path)
if isCacheExists:
    shutil.rmtree(cache_path)
    print("[*] Cache cleared successfully")
    os.makedirs(cache_path)
else:
    os.makedirs(cache_path)
isGifdirExists=os.path.exists(gif_path)
if not isGifdirExists:
    os.makedirs(gif_path)

def isLegal(_time_str):
    try:
        time_formatted = datetime(int(_time_str[:4]),int(_time_str[4:6]),int(_time_str[6:8]),int(_time_str[8:10]),int(_time_str[10:]))
        return 0
    except Exception as e:
        print("[-] E:{}".format(e))
        #print("[!] Please input legal time!")
        return 1

def bjt2utc(_bjt_str):
    bjt_formatted = datetime(int(_bjt_str[:4]),int(_bjt_str[4:6]),int(_bjt_str[6:8]),int(_bjt_str[8:10]),int(_bjt_str[10:]))
    utc_formatted =bjt_formatted - timedelta(hours=8)
    utc_str = utc_formatted.strftime("%Y%m%d%H%M")
    return utc_str

def utc2bjt(_utc_str):
    utc_formatted = datetime(int(_utc_str[:4]),int(_utc_str[4:6]),int(_utc_str[6:8]),int(_utc_str[8:10]),int(_utc_str[10:]))
    bjt_formatted =utc_formatted + timedelta(hours=8)
    bjt_str = bjt_formatted.strftime("%Y%m%d%H%M")
    return bjt_str

def isFuture(_time_str):
    time_formatted = datetime(int(_time_str[:4]),int(_time_str[4:6]),int(_time_str[6:8]),int(_time_str[8:10]),int(_time_str[10:]))
    now_time = datetime.now()
    tdelta = now_time - time_formatted
    if tdelta.days<0:
        #print("[-] E:Invalid time, please try again")
        return 1
    else:
        return 0

def compareTime(_atime_str,_btime_str):
    atime_formatted = datetime(int(_atime_str[:4]),int(_atime_str[4:6]),int(_atime_str[6:8]),int(_atime_str[8:10]),int(_atime_str[10:]))
    btime_formatted = datetime(int(_btime_str[:4]),int(_btime_str[4:6]),int(_btime_str[6:8]),int(_btime_str[8:10]),int(_btime_str[10:]))
    tdelta = btime_formatted - atime_formatted
    if tdelta.days<0:
        #print("[-] E:Invalid time, please try again")
        return 1
    else:
        return 0

def time_plus(_time_str):
    time_formatted = datetime(int(_time_str[:4]),int(_time_str[4:6]),int(_time_str[6:8]),int(_time_str[8:10]),int(_time_str[10:]))
    time_formatted_plus = time_formatted + timedelta(minutes=10)
    time_str_plus = time_formatted_plus.strftime("%Y%m%d%H%M")
    return time_str_plus

def get_img(utc_time_str):
    utc_time_str = utc_time_str[:-1]+"0"
    img_link = "https://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}00/00/000_000.png".format(utc_time_str[:8],utc_time_str)
    #print(img_link)
    r = requests.get(img_link,timeout=10)
    try:
        if r.status_code == 200:
            f = open("{}//{}.png".format(cache_path,utc2bjt(utc_time_str)),'wb')
            f.write(r.content)
            f.close()
            print("[*] Downloaded {}.png".format(utc2bjt(utc_time_str)))
            return 0
        else:
            print("[-] 404 Not found")
            return 1
    except Exception as e:
        print("[-] E:{}, retrying...".format(e))
        return 2

def cvtGif(_dir_path,_gif_path):
    img_list = os.listdir(_dir_path)
    img_obj_list=[]
    for img in img_list:
        img_tmp = im.open("{}//{}".format(_dir_path,img))
        img_obj_list.append(img_tmp)
    img_obj_list[0].save("{}//{}_{}.gif".format(_gif_path,img_list[0][:-4],img_list[-1][:-4]), save_all=True, append_images=img_obj_list, duration=3)
    return "{}/{}_{}.gif".format(_gif_path,img_list[0][:-4],img_list[-1][:-4])

print("Please input start time:")
print("Example: 202104061330")
while True:
    fst_time = input()
    if isLegal(fst_time)!=1:
        if isFuture(fst_time)!=1:
            break
        else:
            print("[-] E:Invalid time, please try again")
    else:
        print("[!] Please input legal time!")
utc_time_start = bjt2utc(fst_time)
print("Please input stop time:")
print("Example: 202104061950")
while True:
    fin_time = input()
    if isLegal(fin_time)!=1:
        if isFuture(fin_time)!=1:
            if compareTime(fst_time,fin_time)!=1:
                break
            else:
                print("[-] E:Please input a latter time!")
        else:
            print("[-] E:Invalid time, please try again")
    else:
        print("[!] Please input legal time!")
utc_time_stop = bjt2utc(fin_time)
while True:
    while True:
        if get_img(utc_time_start)!=2:
            break
        time.sleep(random.randint(0,4))
    utc_time_start = time_plus(utc_time_start)
    if compareTime(utc2bjt(utc_time_start),utc2bjt(utc_time_stop))==1:
        break
print("[*] All images downloaded successfully")
print("[*] Converting to GIF, please wait...")
gif_info = cvtGif(cache_path,gif_path)
print("[*] GIF is saving to {}".format(gif_info))
os.system("pause")




