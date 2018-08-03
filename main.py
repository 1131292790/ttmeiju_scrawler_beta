import requests
from bs4 import BeautifulSoup
import re
import threading

# proxies = {'http': '127.0.0.1:80', 'https': '127.0.0.1:80'}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie': 'PHPSESSID="p7v171q8inqj0uq2hstnvsin94"; Hm_lvt_b173122a0f5eae3f22f6ff0c7fe6d701="1532585918,1532592996"; OWtE_544f_saltkey="p2SE7pTn"; OWtE_544f_lastvisit="1532591184"; OWtE_544f_sid="q1BEBV"; OWtE_544f_lastact="1532594784%09uc.php%09"; OWtE_544f_auth="538bDIXafDvFc1QyJo1iQtM5m1eUyEfc84JUzESIkZzZ6fcVGbbhGgtB5SlEGodhkKWBW14PdCvd%2BHjGntUGyqovePc"; Hm_lpvt_b173122a0f5eae3f22f6ff0c7fe6d701="1532610915"',
    'Host': 'www.ttmeiju.vip',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}
thread_list=[]

def write_to_file(name, content):
    with open(name + '.txt', 'w', encoding='utf-8') as n:
        n.write(content)

def parse_one_page(target):
    css_selects = target.select("#seedlist .Scontent1, .Scontent")
    for per_selected in css_selects:
        result = per_selected.find(attrs={'align': "left"}).find(name='a')
        baidus = per_selected.find(attrs={'ectype': 'linklist', 'align': 'left'}).find(name='a')
        baidu_addr = baidus.attrs['href']
        addr = 'http://www.ttmeiju.vip' + result.attrs['href']
        name = result.get_text().strip()
        information = per_selected.find_all(name='td')[4:6]
        password = information[0].get_text()
        #size = information[1].get_text()
        check_baidu_addr_exist(baidu_addr, password, name, addr)

def change_page(page):
    """换页爬取"""
    headers['Referer'] = 'http://www.ttmeiju.vip/meiju/Movie.html'
    rq = requests.get('http://www.ttmeiju.vip/index.php/meiju/index/engename/Movie/p/'
                      + str(page) + '.html', headers=headers, timeout=20)
    # print(rq.status_code)
    bs = BeautifulSoup(rq.text, 'lxml')
    # print(bs)
    parse_one_page(bs)

def check_baidu_addr_exist(content, password, name, addr):
    """检查百度网盘地址是否存在"""
    result = re.match('^https://pan.baidu.com/s.*', content, re.S)
    if result:
        check_password(password, name, addr)
        print(result.group())
    else:
        pass

def check_password(password, name, addr):
    """检查网盘地址是否有密码"""
    if password:
        # execute function to enter netdisk page and store data
        print(name + " " + password)
    else:
        print(name + 'No password')

def thread_running(func,page):
    for i in range(page):
        per_thread = threading.Thread(target=func,args=(i,))#args括号里面要有逗号，不然报错
        thread_list.append(per_thread)
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()

thread_running(change_page,6)