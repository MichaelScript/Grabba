import os
import argparse
import json
import shutil
import sys
import re

parser = argparse.ArgumentParser(prog="grabby",description="Grabby is a python tool that allows you to find, filter, and grab files from any machine.")
def parse_cli():
	parser.add_argument("-s --search",nargs="*",help="Directories you want to search and grab files from.")
	parser.add_argument("-t --include",nargs="*",help="Only grab files that have filenames that match these patterns.")
	parser.add_argument("-e --exclude",nargs="*",help="Don't grab files that have names that match these patterns")
	parser.add_argument("-c --config",nargs="?",help="Alternative config file.")
	parser.add_argument("-o --output",nargs="?",help="Alternate output directory")
	parser.add_argument("-p --prompt",nargs="?",help="Prompt for overriding output directories.")
	args = parser.parse_args()
	return args

options = parse_cli()
# If no path is specified we default to the config path within this file's directory.
config_path = options.config or os.path.join(os.path.dirname(os.path.realpath(__file__)),"config","config.json")
with open(config_path,"r") as config:
	try:
		config = json.load(config)
	except:
		raise ValueError("Something went wrong when trying to read the configuration file.")
# Converting our args namespace into a dictionary that we can iterate over.
options = options.__dict__
del options["config"]
# Altering our configuration (temporarily) to honor our command line arguments
config.update(filter(lambda k: options[k] is not None,options))
# Might want to look into checking for directory duplicates / directories that are parents/children of each other
# input_dirs = map(os.path.abspath,input_dirs)
# output_dir = os.path.abspath(config["output"])
# For testing.
test_dir = os.path.abspath(os.path.join(os.path.realpath(__file__),os.pardir,os.pardir,'tests'))
input_dirs = [os.path.join(test_dir,"input")]
output_dir = os.path.join(test_dir,"output")

include_patterns = "|".join(map(lambda exc: "(" + exc + ")",config["include"]))
exclude_patterns = "|".join(map(lambda exc: "(" + exc + ")",config["exclude"]))
# We filter files with copytree by returning a list of all the "invalid files" in other words
# we basically need to invert all of our inclusion and exclusion patterns 
def check_file(directory,file_names):
	# Ugliness.
	return filter(lambda file_name: not os.path.isdir(os.path.join(directory,file_name)) and\
	 (re.search(exclude_patterns,file_name) or not re.search(include_patterns,file_name)),\
	 file_names)

prompt = config["prompt"]

for directory in input_dirs:
	# We create a new directory within our output directory based on the name of the directory we are copying from.
	output_subdir = os.path.join(output_dir,os.path.relpath(directory,os.pardir).replace("/","__"))
	if os.path.exists(output_subdir):
		if prompt:
			print("The output sub-directory (" + output_subdir + ") already exists would you like to delete this?")
			if raw_input() not in ["true","yes","y"]:
				print("Skipping...")
				continue
		shutil.rmtree(output_subdir)

	shutil.copytree(directory, output_subdir, ignore=check_file)




