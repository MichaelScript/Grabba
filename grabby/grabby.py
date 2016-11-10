#!/usr/bin/env python
import os
import argparse
import json
import shutil
import sys
import re

parser = argparse.ArgumentParser(prog="grabby",description="Grabby is a python tool that allows you to find, filter, and grab files from any machine.")
def parse_cli():
	parser.add_argument("-s","--search",nargs="*",help="Directories you want to search and grab files from.")
	parser.add_argument("-t","--include",nargs="*",help="Only grab files that have filenames that match these patterns.")
	parser.add_argument("-e","--exclude",nargs="*",help="Don't grab files that have names that match these patterns")
	parser.add_argument("-c","--config",nargs="?",help="Alternative config file.")
	parser.add_argument("-o","--output",nargs="?",help="Alternate output directory")
	parser.add_argument("-p","--prompt",nargs="?",help="Prompt for overriding output directories.")
	args = parser.parse_args()
	return args

# Reading in our command line options and creating a temporary config to honor command line args specified
def config_gen(options):
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
	config.update(filter(lambda k: options[k] is not None,options))
	return config


def copy(config):
	try:
		input_dirs = map(os.path.abspath,config["search"])
		output_dir = os.path.abspath(config["output"])
		# Amalgamating our lists of regular expressions into single expressions
		include_patterns = "|".join(map(lambda exc: "(" + exc + ")",config["include"]))
		# We exclude our output path so we don't go into an infinite loop
		exclude_patterns = "|".join(map(lambda exc: "(" + exc + ")",config["exclude"] + [str(output_dir)]))

		# We filter files with copytree by returning a list of all the "invalid files" in other words
		# we basically need to invert all of our inclusion and exclusion patterns 
		def check_file(directory,file_names):
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
			# Finally putting it all together and recursively copying the directory
			shutil.copytree(directory, output_subdir, ignore=check_file)
		return True
	except Exception as e:
		print(e)
		return False


def grabby():
	config = config_gen(parse_cli())
	if copy(config):
		print("Successively grabbed files.")
	else:
		print("Something went horribly wrong while grabbing files!")


