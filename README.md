# cyanide

Cyanide is a tool to poison request logs by injecting a payload in the user-agent. It has 3 payloads ready for now.

This is a BadByte, my hacking team, Official Tool. You can join our hacking community [here](https://discord.gg/CDACNFg).

## Installation
For now, the only way of downloading this project is by cloning this repo. PyPi support will be added in the next update, hopefully!

## Usage

```
usage: cyanide.py [-h] [-q] [-Pl] [-pl PAYLOAD] [-m METHOD] [-P PARAMETER]
                  [-e] [-E] [-p PREFIX] [-s SUFFIX] [-u URL]

Log poisoner. Turns a Local File Inclusion to a Remote Code Execution. Counts
3 different payloads for now.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet, --no-banner
                        Quiet mode. No banner.
  -Pl, --payloads, --list
                        List all possible payloads.
  -pl PAYLOAD, --payload PAYLOAD, --set-payload PAYLOAD
                        Set payload (by index or ID). Use -Pl to list
                        available payloads.
  -m METHOD, --method METHOD
                        HTTP request method. Ex.: POST
  -P PARAMETER, --par PARAMETER, --parameter PARAMETER
                        Query parameter name. Ex.: '-P view' => '?view='
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

Payloads:
```
[0] PHPCMD (72 chars) -> PHP Simple Command Injection: [PHP] Simple command injection with query variable 'c'. Ex.: ?c=ls
[1] PHPB64CMD (102 chars) -> PHP Simple Base64 Command Injection: [PHP] Simple command injection with query variable 'b', but the command is base64 and
URL encoded. Ex.: ?b=bHM%3D
[2] PHPREADFILE (130 chars) -> PHP File Reader: [PHP] Read a file's contents. Using parameter 'f' to specificy a filename. Ex.: ?f=filename.ext
```
