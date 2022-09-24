from bs4 import BeautifulSoup as bsoup
from requests import get
from threading import Thread
from sys import exit
from os import system



#http://proxy.example.com:8080 or 'https://user:password@proxyip:port'


class web_scraper(Thread,object):
	def __init__(self,keyworlds_list=str(),list_dork=str(),list_proxy=str(),out_file=str()):
		self.list_dork = list_dork
		self.list_proxy = list_proxy
		self.out_file = out_file
		self.keyworlds_list = keyworlds_list

		self.blacklist = [
		"facebook",
		"google",
		"pastebin",
		"gist",
		"github",
		"udemy",
		"jetbrains",
		"youtube",
		"whatsapp",
		"telegram",
		"twitter",
		"vuldb",
		"tenable",
		"exploit-db",
		"stackoverflow",
		"bing",
		"w3schools",
		"wikipedia",
		"cvedetails",
		"exploitdb",
		]


	def main(self):

		found_finished = []
		found0         = []


		self.proxies = self.read(str(self.list_proxy))
		self.keys = self.read(str(self.keyworlds_list))
		self.dorks = self.read(str(self.list_dork))

		thrd_bing   = self.thread_bing(self.keys,self.dorks)
		thrd_ask    = self.thread_ask(self.keys,self.dorks)



		list_bing   = list(dict.fromkeys(thrd_bing))
		list_ask    = list(dict.fromkeys(thrd_ask))


		for ii in list_bing and list_ask:
				for i in self.blacklist:
					if ii.find(i) == -1:
						found0.append(ii)



		for ii in found0:
			url = self.scrape_website_url(ii,self.proxies[0])
			for i in self.blacklist:
				if ii.find(i) == -1:
					found_finished.append(ii)

		
		finished_dup = list(dict.fromkeys(found_finished))
		found_finished.clear()
		for ii in finished_dup:
			if ii.find('...') != -1:
				found_finished.append(ii)

		found_len= int(len(found_finished))

		for ii in found_finished:
			self.write(ii)

		return found_len
		exit(1)

#===================================================

	def write(self,line):
		i = open(self.out_file,'a',encoding='utf-8')
		i.write(line+'\n')
		i.close()
		pass


	def read(self,lst):
		tupple = []
		x = open(lst,"r")
		ll = x.readlines()
		for ii in ll:
			a = ii.rstrip("\n\r")
			tupple.append(a)

		return tupple


	

	def thread_ask(self,keyworlds,dorks):
		found = []
		c = 0
		c_max = len(keyworlds)

		while c_max > c:
			for dork in dorks:
				ask = self.search_ask('allinurl:'+str(keyworlds[c])+'/'+str(dork),self.proxies[0])
				if ask[0] == int(0):
					c-=1

				if ask[0] > int(0):
					c+=1

				for req in ask[1]:
					if req.find(str(dorks)) != -1:
						found.append(str(req))

			
		return found

			
	def thread_bing(self,keyworlds,dorks):
		found = []
		
		for keyworld in keyworlds:
			for i in dorks:
				bing = self.bing_search('allinurl:'+str(keyworld)+'/'+str(dorks),self.proxies[0])
				for req in bing:
					if req.find(str(dorks)) != -1 and req.find(str(keyworld)) != -1:
						found.append(str(req))
		return found

	def scrape_website_url(self,url,proxy):

		found = []

		proxies = {'https': proxy }
		base_url = url
		headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' }
		try:
			resp = get(base_url,headers=headers,proxies=proxies,timeout=10)
		except Exception:
			print('ERROR CONN!')
			exit(1)
		soup = bsoup(resp.text, 'html.parser')
		for link in soup.find_all("a"):
			req = link.get('href')
			found.append(str(req))




		return found






	def search_ask(self,query,proxy):
		result = []
		base_url = "https://www.ask.com/web"
		headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' }
		proxies = {'https': proxy }
		for ii in range(1,7):
			params   = {"q": query, "page": ii}
			try:
				resp = get(base_url,proxies=proxies,params=params,headers=headers,timeout=10)
			except Exception:
				print('ERROR CONN!')
				exit(1)
			soup = bsoup(resp.text, 'html.parser')
			links  = soup.findAll('div',{'class':'PartialSearchResults-item-url PartialSearchResults-item-top-url'})
			lenx = len(result)
			for link in links:
				result.append(link.text)
		return lenx,self.finder_url(result)



	def bing_search(self,query,proxy):

		result = []
		base_url = 'https://www.bing.com/search'
		headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0' }
		proxies = {'https': proxy }
		for ii in range(1,57):
			params   = { 'q': query, 'first': ii * 10 + 1 }
			try:
				resp = get(base_url,proxies=proxies, params=params, headers=headers,timeout=10)
			except Exception:
				print('ERROR CONN!')
				exit(1)
			soup = bsoup(resp.text, 'html.parser')
			links  = soup.findAll('cite')
			for link in links:
				result.append(link.text)
		return self.finder_url(result)


	def finder_url(self,listx):
		found = []
		c = 0

		for url in listx:
			for dork in self.dorks:
				if url.find(str(dork)) != -1:
					found.append(url)
			
		return found



