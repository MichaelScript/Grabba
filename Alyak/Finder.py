#!/usr/bin/env python
import os
import re

class Finder:
	def __init__(self,include=None,exclude=None):
		self.include = include or "\S+"
		self.exclude = exclude or "!^"

	# By default our file checker will include all patterns and exclude no patterns
	def gen_file_checker(self,include,exclude):
		return lambda file_path: re.search(include,file_path) and not re.search(exclude,file_path)


	def getValidFiles(self,*search_dirs):
		checker = self.gen_file_checker(self.include,self.exclude)
		valid = []
		for input_dir in search_dirs:
			for root,dirs,files in os.walk(input_dir,topdown=False):
				valid.extend(map(lambda file_name: os.path.join(root,file_name),filter(checker,files)))
		return valid

	def setInclude(self,include):
		self.include = include

	def setExclude(self,exclude):
		self.exclude = exclude