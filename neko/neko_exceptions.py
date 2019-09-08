class DefaultException(Exception):
	def __init__(self, code=None, msg=None):
		self.code, self.msg = code, msg
	
	def __str__(self):
		return self.__repr__()
		
	def __repr__(self):
		return "<%s Exception(code=%s, msg=%s)>" % (type(self).__name__, self.code, self.msg)

class OverLimit(DefaultException):
	def __init__(self, *args, **kwgs):
		super().__init__(*args, **kwgs)
		
class NotSupportStreamUrl(DefaultException):
	def __init__(self, *args, **kwgs):
		super().__init__(*args, **kwgs)

class UnknownError(DefaultException):
	def __init__(self, *args, **kwgs):
		super().__init__(*args, **kwgs)
