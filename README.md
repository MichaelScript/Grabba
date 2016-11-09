#Grabby
Grabba is a python tool that allows you to copy files from a machine based on a simple filter system. Grabby takes in a user configuration file that allows you to specify what directories you want to search, what file name patterns to exclude, and what file types you want to grab. It then copies files and directories that meet these filters into a user-specified output directory.

##Configuring Grabby
Option Name | Type | Default Value | Description
------------ | ------------- | ------------ | ------------- 
output | string | Current Directory | Where we are copying to 
search | list | Current Directory | Directories we are grabbing stuff from 
include | list | All | Only grabbing files that match these patterns 
exclude | list | None | Ignoring files that match these patterns 
prompt | boolean | False | Enables/Disables prompting replacing directories

####Example Configuration
```json
{
    "output":"/Volumes/usb/copied",
    "search":["/Users/*/Desktop","/Users/*/Downloads"],
    "include":[".*\\.docx$",".*\\.txt$",".*\\.pdf$"],
    "exclude":["$(old|archive)","bitter*melon$"],
    "prompt":false
}
```
