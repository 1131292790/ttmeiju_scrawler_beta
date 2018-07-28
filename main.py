import requests
import lxml
from bs4 import BeautifulSoup
import json
import re

#proxies = {'http': '127.0.0.1:80', 'https': '127.0.0.1:80'}
headers={
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
'Cookie':'PHPSESSID="p7v171q8inqj0uq2hstnvsin94"; Hm_lvt_b173122a0f5eae3f22f6ff0c7fe6d701="1532585918,1532592996"; OWtE_544f_saltkey="p2SE7pTn"; OWtE_544f_lastvisit="1532591184"; OWtE_544f_sid="q1BEBV"; OWtE_544f_lastact="1532594784%09uc.php%09"; OWtE_544f_auth="538bDIXafDvFc1QyJo1iQtM5m1eUyEfc84JUzESIkZzZ6fcVGbbhGgtB5SlEGodhkKWBW14PdCvd%2BHjGntUGyqovePc"; Hm_lpvt_b173122a0f5eae3f22f6ff0c7fe6d701="1532610915"',
'Host':'www.ttmeiju.vip',
'Connection': 'keep-alive',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

'''get source code from host'''	
def write_to_file(name,content):
	with open(name+'.txt','w',encoding='utf-8') as n:
		n.write(content)

def parse_one_page():
	css_selects = bs.select("#seedlist .Scontent1, .Scontent")
	#pattern = re.compile('<input.*?>',re.S)
	#for per_selected in css_selects:
	for per_selected in css_selects:
		result = per_selected.find(attrs={'align':"left"}).find(name='a')
		baidus = per_selected.find(attrs={'ectype':'linklist','align':'left'}).find(name='a')
		baidu_addr = baidus.attrs['href']
		#can store////datatype str
		addr = 'http://www.ttmeiju.vip'+result.attrs['href']
		name = result.get_text().strip()

		#see if password visible
		information = per_selected.find_all(name='td')[4:6]
		password = information[0].get_text()
		size = information[1].get_text()
		if password:
			#execute function to enter netdisk page and store data
			print(name)
			print('password found,we pass')
		else:
			#get password
			print(name)
			headers['Referer']='http://www.ttmeiju.vip/summary.html'
			rq = requests.get(addr,headers=headers)
			seedbs = BeautifulSoup(rq.text,'lxml')
			per_password = seedbs.select('.newstxt p')[2].get_text().strip()
			print(per_password)

#how many you want to scrawl
def change_page(page):
	headers['Referer']='http://www.ttmeiju.vip/meiju/Movie.html'
	
	rq = requests.get('http://www.ttmeiju.vip/index.php/meiju/index/engename/Movie/p/'+
		str(page)+'.html',headers=headers)
	write_to_file('page'+str(page),rq.text)
	parse_one_page()

def main():
	rq = requests.get('http://www.ttmeiju.vip/meiju/Movie.html',headers=headers)
	write_to_file('home_page',rq.text)
	bs = BeautifulSoup(open('home_page.txt'),'lxml')
	bs.prettify()
	parse_one_page()
