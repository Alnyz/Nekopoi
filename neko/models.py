class NewReleases(object):
	def __init__(self, **kwgs):
		self.kw = kwgs
		
		for k, v in self.kw.items():
			setattr(self, k, v)
		
	def __str__(self):
		return self.__unicode__()
			
	def __unicode__(self):
		return u'NewReleases(title={title}, date={date},' \
			u'creator={creator}, img={img}, url={url})'.format(**self.kw)

class DetailPoi(object):
	def __init__(self, **kwgs):
		self.kw = kwgs
		
		for k, v in self.kw.items():
			setattr(self, k, v)
		
	def __str__(self):
		return self.__unicode__()
		
	def __unicode__(self):
		return u'DetailPoi(title={title}, seen={seen}, duration={duration},' \
			u' producer={producer}, url={url}, extras={extras})'.format(
			title=self.kw['title'], seen=self.kw.get('seen', None), duration=self.kw.get('duration', None), \
			producer=self.kw.get('producers', None), url=self.kw.get('url', None), extras= '"' + repr(self.kw['extras'])[:15] + '..."') 