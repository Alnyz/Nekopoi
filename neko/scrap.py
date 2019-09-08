import re
from bs4 import BeautifulSoup
from .connect import Connection
from .download import Download
from .models import *
from .neko_exceptions import *
from typing import Union, List

class Scraper(Connection):
	def __init__(self, *args, **kwgs):
		super().__init__(*args, **kwgs)
	
	def new_release(self, page):
		self.url(self.PAGE.format(page))
		parse = self.parse()
		soup = BeautifulSoup(parse.text, 'lxml')
		body = soup.find_all('div', class_ = "eropost")
		lists = []
		for i in body:
			h2 = i.h2
			sp = i.find_all('span')
			img = self.BASE_URI+i.img.get("src", None)
			title, url = h2.text.strip(), h2.a.get("href", None)
			date, creator = sp[0].text, sp[1].text if len(sp) > 1 else "Unknown"
			res = NewReleases(title=title, date=date, creator=creator, img=img, url=url)
			lists.append(res)
		return lists
	
	def get_detail(self, url):
		self._url = url
		parse = self.parse()
		soup = BeautifulSoup(parse.text, 'lxml')
		artic = soup.find('div', class_='articles')
		seen = artic.find('div', class_='headpost').find('p').text
		content = artic.find('div', class_='contentpost')
		streams = artic.find('div', class_='show-stream')
		streams = [x.iframe.get('src') for x in streams.find_all('div', id=re.compile(r'stream(\d)'))]
		detail = self.parse_detail(content)
		detail.update({'streams': streams, 'seen': seen, "url": parse.url})
		extras = self.parse_extras(detail)
		[extras.pop(i) if i in extras.keys() \
			else {k:v for k, v in {'sinopsis': None, 'size': None}.items()} \
			for i in ['sinopsis', 'size', 'streams']]
		result = DetailPoi(**extras)
		return result
	
	def _search(self,
				page,
				query = None,
				jav = False,
				hentai = False,
				_3d = False,
				cosplay = False):
		if query:
			self.url(self.SEARCH.format(query))
		elif cosplay and not (hentai or jav or _3d):
			self.url(self.CATEGORY['cosplay'].format(page))
		elif jav and not (hentai or cosplay or _3d):
			self.url(self.CATEGORY['jav'].format(page))
		elif hentai and not (jav or cosplay or _3d):
			self.url(self.CATEGORY['hentai'].format(page))
		elif _3d and not (hentai or cosplay or hentai):
			self.url(self.CATEGORY['3d'].format(page))
		else:
			raise ValueError('Only can parse once of category')
		parse = self.parse()
		if parse.status_code > 400 and page > 1:
			raise OverPage(parse.status_code, "Page limit exceeded %s" % page)
		soup = BeautifulSoup(parse.text, 'lxml')
		content = soup.find('div', id='content')
		result_detail = content.find('div', class_='result').find_all('div', class_='top')
		result = []
		img_list = []
		for i in result_detail:
			detail = self.parse_detail(i)
			img_list.append(self.BASE_URI+i.img.get('src', ""))
			imgs = {'imgs': img_list}
			detail.update({'url': self.BASE_URI+i.a.get('href', "")})
			detail.update(imgs)
			extras = self.parse_extras(detail)
			poi = DetailPoi(**extras)
			result.append(poi)
		return result
	
	def get_video_stream(self, url_stream) :
		self._url = url_stream
		parse = self.parse()
		soup = BeautifulSoup(parse.text, 'lxml')
		try:
			uri = soup.find('div', id='vplayer')
			source = uri.find('source')
			uri = source.get('src', None)
		except AttributeError:
			scrp = soup.find_all('script', attrs={'type': 'text/javascript'})[-1]
			pttrn = re.compile(r'sources:\s\[(\W+.*)\]')
			match = re.findall(pttrn, str(scrp))
			uri = match[0].split(",")[-1].strip('"')
		finally:
			if "streamcherry" in url_stream:
				raise NotSupportStreamUrl(parse.status_code, "This url not support stream for now.")
			elif parse.status_code > 400:
				raise UnknownError(parse.status_code, "Unknown Exception.")
			
		return uri