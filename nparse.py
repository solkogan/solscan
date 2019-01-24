import subprocess
import inspect
import sys, os, codecs, re
import webbrowser
import requests

stopwords=['403 Forbidden', 'Not Found', 'Welcome to nginx on Debian!']

dic={
"\\xD0\\xB0":"а", "\\xD0\\x90":"А",
"\\xD0\\xB1":"б", "\\xD0\\x91":"Б",
"\\xD0\\xB2":"в", "\\xD0\\x92":"В",
"\\xD0\\xB3":"г", "\\xD0\\x93":"Г",
"\\xD0\\xB4":"д", "\\xD0\\x94":"Д",
"\\xD0\\xB5":"е", "\\xD0\\x95":"Е",
"\\xD1\\x91":"ё", "\\xD0\\x81":"Ё",
"\\xD0\\xB6":"ж", "\\xD0\\x96":"Ж",
"\\xD0\\xB7":"з", "\\xD0\\x97":"З",
"\\xD0\\xB8":"и", "\\xD0\\x98":"И",
"\\xD0\\xB9":"й", "\\xD0\\x99":"Й",
"\\xD0\\xBA":"к", "\\xD0\\x9A":"К",
"\\xD0\\xBB":"л", "\\xD0\\x9B":"Л",
"\\xD0\\xBC":"м", "\\xD0\\x9C":"М",
"\\xD0\\xBD":"н", "\\xD0\\x9D":"Н",
"\\xD0\\xBE":"о", "\\xD0\\x9E":"О",
"\\xD0\\xBF":"п", "\\xD0\\x9F":"П",
"\\xD1\\x80":"р", "\\xD0\\xA0":"Р",
"\\xD1\\x81":"с", "\\xD0\\xA1":"С",
"\\xD1\\x82":"т", "\\xD0\\xA2":"Т",
"\\xD1\\x83":"у", "\\xD0\\xA3":"У",
"\\xD1\\x84":"ф", "\\xD0\\xA4":"Ф",
"\\xD1\\x85":"х", "\\xD0\\xA5":"Х",
"\\xD1\\x86":"ц", "\\xD0\\xA6":"Ц",
"\\xD1\\x87":"ч", "\\xD0\\xA7":"Ч",
"\\xD1\\x88":"ш", "\\xD0\\xA8":"Ш",
"\\xD1\\x89":"щ", "\\xD0\\xA9":"Щ",
"\\xD1\\x8A":"ъ", "\\xD0\\xAA":"Ъ",
"\\xD1\\x8B":"ы", "\\xD0\\xAB":"Ы",
"\\xD1\\x8C":"ь", "\\xD0\\xAC":"Ь",
"\\xD1\\x8D":"э", "\\xD0\\xAD":"Э",
"\\xD1\\x8E":"ю", "\\xD0\\xAE":"Ю",
"\\xD1\\x8F":"я", "\\xD0\\xAF":"Я",
}

urls=[]

f=open('output.txt', 'r')
f2=open('output.html', 'w')

f2.write('''<html lang="ru"><head><title>Scan results</title><meta charset="utf-8">
         <style>
         td {
         padding: 7px;
         }
         td a {
         color: navy;
         }
         </style>
         </head><body><table border=1>''')

for x in f:
    if('Nmap scan report for' in x):
        hosts = re.search('(\d+\.\d+\.\d+\.\d+)', x)
        host=hosts.group(1).strip()
    if('Anonymous FTP login allowed' in x):
        urls.append('<tr><td>Открытый FTP</td><td><a href="ftp://'+host+'" target="_blank"><b>ftp://'+host+'</b></a></td><td></td></tr>')
    if('http-title:' in x):
        x=x.replace('|_http-title:','')
        x=x.replace('| http-title: ','')
        w=x.strip()
        for k in dic:      
            if (k in w):
                w=w.replace(k, dic[k])
        htmlcode=''
        # s=requests.get('http://'+host)
        # htmlcode=s.text
        htmltype=''
        ff=open(u'fingerprints.txt', 'r')
        color='#eaeaea'
        for keyword in ff:
            ms=keyword.split('|')
            if(ms[0].strip() in w):
                htmltype=ms[1]
                color='white'
        if('password' in htmlcode):
            htmltype='Форма авторизации'
        if('location.href' in htmlcode):
            htmltype='Переадресация'
        if not(w in stopwords):
            urls.append('<tr style="background: '+color+';"><td>'+w+'</td><td><a href="http://'+host+'" target="_blank"><b>'+host+'</b></a></td><td>'+htmltype+'</td></tr>')
urls=list(set(urls))
urls.sort()
for s in urls:
    f2.write(s)
f2.write('</table></body></html>')
f2.close()
f.close()
        
webbrowser.open('output.html')	
