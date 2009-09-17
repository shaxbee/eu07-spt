'''
Created on 2009-08-09

@author: gfirlejczyk
'''

class Element(object):
	"""
	Virtual Dispatcher basic element
	"""
	
	def __init__(self, name = ""):
		self.__name = name
		
    def __repr__(self):
	   return 'Element(name="%s")' % self.__name;
		
	def size(self):
		"""
		Returns number of RailTrackings contained in this class
		"""
		return 0
	
	def insert(self, tracking):
		'''
		Add new RailTracking instance
		'''
		pass
