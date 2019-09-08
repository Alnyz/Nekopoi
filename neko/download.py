from .connect import Connection
from tqdm import tqdm
import os

class Download(Connection):
	def __init__(self, path = None, dw_url=None, *args, **kwgs):
		super().__init__(*args, **kwgs)
		self._path = path or os.getcwd() + "/test.mp4"
		self._url = dw_url
		
	def __str__(self):
		return self.__repr__()
	
	def __repr__(self):
		return '<%s Response(_url=%s)>' % (type(self).__name__, self._url)

	def download(self, cus_chunk = None):
		self.timeout = 10000
		parse = self.parse("GET", stream=True)
		size = int(parse.headers.get('Content-Length', 0))
		chunks = size if size > 0 else 16*1024*1024 if not cus_chunk else cus_chunk
		tq = tqdm(desc="Downloading",
				total=size,
				unit="B",
				unit_scale=True)
		with open(self._path, 'wb') as fp:
			for chunk in parse.iter_content(chunks):
				if chunk:
					tq.update(len(chunk))
					fp.write(chunk)
				else:
					raise
			tq.close()
			return self._path
		print("Download complete")