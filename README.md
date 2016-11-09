#Grabby
Grabba is a python tool that allows you to copy files from a machine based on a simple filter system. Grabby takes in a user configuration file that allows you to specify what directories you want to search, what file name patterns to exclude, and what file types you want to grab. It then copies files and directories that meet these filters into a user-specified output directory.

```json
{
    /* Where we are copying to */
    "output":"/Volumes/usb/copied",
    /* Directories we are grabbing stuff from */
    "search":["/Users/*/Desktop","/Users/*/Downloads"],
    /* Only grabbing files that match these patterns */
    "include":[".*\\.docx$",".*\\.txt$",".*\\.pdf$"],
    /* Ignoring files that match these patterns */
    "exclude":["$(old|archive)","bitter*melon$"],
    /* If the output directory or any of the sub-directories already exist should we prompt
    to replace them?*/
    "prompt":false
}
```