import requests
from .config import Config

class Connection(Config):
	def __init__(self, headers = None, timeout = 3000):
		super().__init__()
		self._url = None
		self.headers = headers
		self.timeout = timeout
		self.session = requests.Session()
		if headers:
			self.session.headers.update(self.headers)
		
	def parse(self, method="GET", *args, **kwgs):
		with self.session as session:
			r = session.request(url=self._url,
					method=method,
					timeout = self.timeout / 1000, 
					*args, **kwgs)
			if not r.ok and r.status_code < 400 or r.status_code > 500:
				raise Exception("Connection failure %s with code %s" % (r.url, r.status_code))
			if r.status_code > 400:
				return r
			return r

	def update_headers(self, key_val):
		self.headers.update(key_val)

	def add_headers(self, key_val):
		self.headers = key_val

	def url(self, end = ""):
		self._url = self.BASE_URI + end