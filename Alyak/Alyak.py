#!/usr/bin/env python
from Finder import Finder
import os
import json
import shutil

class Alyak:
	def __init__(self,config=None):
		config = config or os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir,"config","config.json")
		self.config = self.load_config(config)

	def load_config(self,config_path):
		with open(config_path) as config:
			try:
				return json.load(config)
			except Exception as e:
				raise ValueError(e + "\nSomething went wrong when trying to read the configuration file.")

	# Calls provided function on all found files that match specified patterns
	def apply(self,search_dirs,func=None):
		if not func:
			def func(x):
				print(x)
		config = self.config
		finder = Finder(config["include"],config["exclude"])
		for validFile in finder.getValidFiles(search_dirs):
			try:
				func(validFile)
			except:
				print("Couldn't execute function on file: " + validFile + ", skipping.")


alyak = Alyak()
copy = lambda input_file: shutil.copy2(input_file,"/Users/Michael/Desktop/output")
alyak.apply("/Users/Michael/Desktop/")

if __name__ == "__main__":
	parser.add_argument("-s","--search",nargs="*",help="Directories you want to search and grab files from.")
	parser.add_argument("-t","--include",nargs="*",help="Only grab files that have filenames that match these patterns.")
	parser.add_argument("-e","--exclude",nargs="*",help="Don't grab files that have names that match these patterns")
	parser.add_argument("-c","--config",nargs="?",help="Alternative config file.")
	parser.add_argument("-o","--output",nargs="?",help="Alternate output directory")
	parser.add_argument("-p","--prompt",nargs="?",help="Prompt for overriding output directories.")
	args = parser.parse_args()
	print(args)