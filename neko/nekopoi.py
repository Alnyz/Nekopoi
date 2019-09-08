from .scrap import *
from .download import Download
from .models import *
from typing import Union, List

class Nekopoi(Scraper):
	def __init__(self, *args, **kwrgs):
		super().__init__(*args, **kwrgs)
	
	def new_releases(self, page: Union[int, str]= 1) -> List[NewReleases]:
		return self.new_release(page=page)
	
	def search(self, query: str, page=1) -> List[DetailPoi]:
		return self._search(query=query, page=page)
	
	def jav(self, page: int = 1) -> List[DetailPoi]:
		return self._search(jav=True, page=page)
	
	def _3d(self, page: int = 1) -> List[DetailPoi]:
		return self._search(_3d=True, page=page)
	
	def hentai(self, page: int = 1) -> List[DetailPoi]:
		return self._search(hentai=True, page=page)
	
	def cosplay(self, page: int = 1) -> List[DetailPoi]:
		return self._search(cosplay=True, page=page)
	
	def detail(self, url_neko: str) -> DetailPoi:
		return self.get_detail(url_neko)
	
	def get_stream(self, stream_url: str) -> str:
		return self.get_video_stream(stream_url)
	
	def download(self, stream_url: str, path: str = None) -> Download:
		return Download(dw_url=stream_url, path=path)