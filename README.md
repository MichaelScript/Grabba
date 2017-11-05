# Grabby
Grabby is a python tool that allows you to copy files from a machine based on a simple filter system. Grabby takes in a user configuration file that allows you to specify what directories you want to search, what file name patterns to exclude, and what file types you want to grab. It then copies files and directories that meet these filters into a user-specified output directory.

I have no idea if this works anymore. I wrote it a long time ago but the repo was private, just making it public in case anyone wants to use/fix this up.

## Installation
> pip install grabby

## Configuring Grabby
Option Name | Type | Default Value | Description
------------ | ------------- | ------------ | ------------- 
**output** | string | *Current Directory* | Where we are copying to 
**search** | list | *Current Directory* | Directories we are grabbing stuff from 
**include** | list | *All* | Only grabbing files that match these regex patterns
**exclude** | list | *None* | Ignoring files that match these regex patterns
**prompt** | boolean | *False* | Enables/Disables prompting replacing directories

### Example Configuration File
```json
{
    "output":"/Volumes/usb/copied",
    "search":["/Users/*/Desktop","/Users/*/Downloads"],
    "include":[".*\\.docx$",".*\\.txt$",".*\\.pdf$"],
    "exclude":["$(old|archive)","bitter*melon$"],
    "prompt":false
}
```
## Command Line Usage
You can run Grabby in your terminal with your default configuration by just typing `grabby` or you can reconfigure grabby on the fly by using it's command line options. For example if you wanted to change what directories you are searching you could do the following: `grabby -s /etc /usr/share`  A full list of command line options is given below.
```
usage: grabby [-h] [-s --search [S __SEARCH [S __SEARCH ...]]]
              [-t --include [T __INCLUDE [T __INCLUDE ...]]]
              [-e --exclude [E __EXCLUDE [E __EXCLUDE ...]]]
              [-c --config [C __CONFIG]] [-o --output [O __OUTPUT]]
              [-p --prompt [P __PROMPT]]

Grabby is a python tool that allows you to find, filter, and grab files from
any machine.

optional arguments:
  -h, --help            show this help message and exit
  -s --search [S __SEARCH [S __SEARCH ...]]
                        Directories you want to search and grab files from.
  -t --include [T __INCLUDE [T __INCLUDE ...]]
                        Only grab files that have filenames that match these
                        patterns.
  -e --exclude [E __EXCLUDE [E __EXCLUDE ...]]
                        Don't grab files that have names that match these
                        patterns
  -c --config [C __CONFIG]
                        Alternative config file.
  -o --output [O __OUTPUT]
                        Alternate output directory
  -p --prompt [P __PROMPT]
                        Prompt for overriding output directories.
```
