class Config:
	BASE_URI = 'https://3z094n2681j06q8k14w31cu4q80d5p.com'
	PAGE = '/page/{}/'
	SEARCH = '?s={}&post_type=anime'
	CATEGORY = {
		'hentai': '/category/hentai'+PAGE,
		'jav': '/category/jav'+PAGE,
		'3d': '/category/3d-hentai/'+PAGE , 
		'cosplay': '/tag/jav-cosplay/'+PAGE
	}
	
	def parse_detail(self, data):
		sdata = {}
		try:
			sdata["title"] = data.a.text
		except AttributeError:
			sdata['title'] = data.img.get('alt', None)
		for i in data.find_all("p"):
			tt = i.text
			if "\xa0" in tt:
				text = tt.split(":\xa0", 1)
			if "size" or "duration" in tt.lower():
				text = tt.split(": ", 1)
			if "anime" in tt.lower() and sdata["title"] == "" or None:
				sdata["title"] = tt.split(":", 1)[1].strip()
			if "sinopsis" in tt.lower():
				text = ""
			else:
				text = tt.split(":",1)		
			if len(text) <= 1:
				sdata["sinopsis"] = "".join(text)
			else:				
				sdata[text[0].lower().strip().replace(" ", "_")] = text[1].strip().replace("\xa0", "")
		return sdata
	
	def parse_extras(self, data):
		key_list = ['sinopsis', 'size', 'streams', 'imgs', 'movie_id', 'artist']
		ex = {'extras':{}}
		for k, v in data.items():
			if k in key_list:
				ex['extras'].update({k: v})
		data.update(ex)
		return data
			