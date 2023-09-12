import re
import requests
import random
import os
import argparse
import time
from pyfiglet import Figlet

ip_re = re.compile(r'((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)(\.((25[0-5])|(2[0-4]\d)|(1\d\d)|([1-9]\d)|\d)){3}')
sub_re = re.compile('<a href=".*?" rel="nofollow" target="_blank">(.*?)</a>')


def ip_check(ip):
    # 添加随机UA头
    with open('user-agents.txt', 'r') as f_UA:
        user_agents = f_UA.readlines()
    headers = {
        'User-Agent': random.choice(user_agents).strip(),
        'Cookie': '_csrf=fa92ea01771153f2debd27716be824d1635b4c6f08e3f23eb4ff1c975c1b3b1fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%2298Zz585MxIVPvA1jKauNWXFQLl0Rlij-%22%3B%7D; PHPSESSID=k557a7ii9r4igr9vavjj3etrl5; Hm_lvt_b37205f3f69d03924c5447d020c09192=1694483938; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1694484211; userId=1485893; userName=WX64ffc5fba9782%40aizhan.com; userGroup=1; userSecure=ef1K1F4kOUy30Y%2BX6LO6Sp%2BMbQZf%2FLY4Dm3nxtRyGIMO4XRQSuwkW%2Bq6XmhB1OgOkxzy74%2BRS1CrYX7s37eLgEMq58yk1zu2GB%2F77RAZpPuWG2xsDGKnldDeyOjhiDQo9Z49Ggh28p6ctJKyPrwaB9XdEn0%3D'
    }
    with open('result.txt', 'a', encoding='utf-8') as res:
        url = "https://dns.aizhan.com/" + ip 
        response = requests.get(url=url, headers=headers).text
        sub = sub_re.findall(response)
        time.sleep(1.5) #防止被ban
        if len(sub) > 0:
            target = ip.replace('\n', '') + "      -----IP：" + \
                ip + " 域名为：" + sub[0]
            print(target)
            res.write(target + '\n')
        else:
            print(f'{ip} 不存在域名')


if __name__ == '__main__':
    print(Figlet(font='slant').renderText('IP Domain'))
    print('         Author: Hungs        HomePage: www.hungs.cn\n')
    parser = argparse.ArgumentParser(description='IP Domain')

    parser.add_argument('-u', '--url', dest='url', required=False, help='target url')
    parser.add_argument('-f', '--file', dest='file', required=False, help='url file')

    Usage = "Usage:\npython3 {0} -u url\npython3 {0} -f url.txt".format(
        os.path.basename(__file__))
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as readlist:
            urls = readlist.readlines()
            for url in urls:
                url = url.strip('\n')
                try:
                    dir = ip_re.search(url).group()
                    ip_check(dir)
                except:
                    print(f'{dir} IP查询异常')
                    continue
        readlist.close()
        

    elif args.url:
        ip_check(args.url)

    else:
        print(Usage)
