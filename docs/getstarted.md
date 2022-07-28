# Getting Started
Cyanide is a tool to poison request logs by injecting a payload in the user-agent. They can then be accessed back using an Local File Inclusion to trigger Remote Code Execution. It currently has a total of 6 great standalone payloads.

## Installation
As of now, the only way of using this project is by cloning the repo or with [this download link](https://github.com/Noxtal/cyanide/archive/refs/heads/master.zip").

## Usage
```
usage: cyanide.py [-h] [-q] [-Pl] [-pl [PAYLOAD ...]] [-m METHOD] [-P PARAMETER]
                  [-C COOKIES] [-e] [-E] [-p PREFIX] [-s SUFFIX] [-u URL]

Log poisoner. Turns a Local File Inclusion to a Remote Code Execution. Counts 6
different payloads for now.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet, --no-banner
                        Quiet mode. No banner.
  -Pl, --payloads, --list
                        List all possible payloads.
  -pl [PAYLOAD ...], --payload [PAYLOAD ...], --set-payload [PAYLOAD ...]
                        Set payload (by index or ID). Use -Pl to list available
                        payloads.
  -m METHOD, --method METHOD
                        HTTP request method. Ex.: POST
  -P PARAMETER, --par PARAMETER, --parameter PARAMETER
                        Query parameter name. Ex.: '-P view' => '?view='
  -C COOKIES, --cookies COOKIES
                        Set request cookies such as PHP session in JSON format (ex.:
                        '{"key":"value", ...}').
  -e, --encode, --dds-encode
                        URL encode ../
  -E, --double-encode, --dds-double-encode
                        Double-encode ../
  -p PREFIX, --prefix PREFIX
                        Query prefix. Ex.: '../../../../../etc/cat/'
  -s SUFFIX, --suffix SUFFIX
                        Query suffix. Ex.: '&other='
  -u URL, --URL URL, --url URL
                        URL to attack.
```


