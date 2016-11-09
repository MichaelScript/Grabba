import os
import argparse
import json
import shutil
import sys
import re

parser = argparse.ArgumentParser(prog="grabba",description="Grabba is a python tool that allows you to grab files from a machine based on a simple filter system.")
def parse_cli():
	parser.add_argument("--search","-s",nargs="*",help="Directories you want to search and grab files from.")
	parser.add_argument("--types","-t",nargs="*",help="File types you want to grab.")
	parser.add_argument("--exclude","-e",nargs="*",help="Don't grab files that have names that contain these patterns in their names.")
	parser.add_argument("--config","-c",nargs="?",help="Alternative config file.")
	parser.add_argument("--output","-o",nargs="?",help="Alternate output directory")
	parser.add_argument("--prompt","-p",nargs="?",help="Prompt for overriding output directories.")
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

valid_types = tuple(config["types"])
exclude_patterns = "|".join(map(lambda exc: "(" + exc + ")",config["exclude"]))
# We filter files with copytree by returning a list of all the "invalid files" in other words
# all of the files that aren't of the correct type or contain any of our exclusion paterns
def check_file(directory,file_names):
	invalid_files = filter(lambda file_name: not os.path.isdir(os.path.join(directory,file_name)) and (re.search(exclude_patterns,file_name) or not file_name.endswith(valid_types)),file_names)
	return invalid_files

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




