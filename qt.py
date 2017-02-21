#!/usr/bin/env python  
# encoding: utf-8  
 
import cookielib
import urllib2
import urllib
from pyquery import PyQuery as pq
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import commands
 
 
def setup_cookie():
    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
    urllib2.install_opener(opener);

 
#login bugzilla
def login_bugzilla():
    username = 'lming'
    password = 'Vlmm@666'
 
    url = r'https://bugzilla.eng.vmware.com/index.cgi'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'
    }
 
    data = urllib.urlencode({"Bugzilla_login":username,"Bugzilla_password":password, "GoAheadAndLogIn":"Log In"})
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)

    the_page = response.read()
 
    #determin if we log in succeed
    if re.findall(r'Log out lming',the_page) != []:
        print 'login succeed!'
    else:
        print 'login failed~'
        sys.exit()

    response.close()


#parse the searched page and return the buglist table in html
def parse_bugzilla():
    #target_url='https://bugzilla.eng.vmware.com/buglist.cgi?cmdtype=runnamed&namedcmd=triaging&buglistsort=id,asc'
    base_url = 'https://bugzilla.eng.vmware.com/'
    #res = urllib2.urlopen(target_url) 
    #d = pq(res.read())
    #table = d('table').html()
    d = pq(filename = 'data.html')
    table = d('table').html()

    print table
    commands.getstatusoutput('cat ')
    print table
    return table

def gen_email_body(table):
    header = '''
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
</head>
<body>

<table id="buglistSorter"
         class="bz_buglist tablesorter" cellspacing="0"
         cellpadding="4" width="100%">
'''
    tail = '''
</table>

</body>
</html>
'''
    email_body = header + table + tail
    return email_body

 
#send html format email
def send_email(email_body):
    me = 'lming@mingrhel.com'
    to = 'lming@vmware.com'
    #cc = 'ljhuang@vmware.com'
    cc = 'lming@vmware.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily Triage Bugs"
    msg['From'] = me
    msg['To'] = to
    msg['CC'] = cc
    part = MIMEText(email_body, 'html')
    msg.attach(part)
    s = smtplib.SMTP('localhost')
    s.sendmail(me, to, msg.as_string())
    s.quit()



def main():
#    setup_cookie()
# 
#    try:
#        login_bugzilla()
#    except Exception, e:
#        print 'fail to login bugzilla'
#        print e
#        sys.exit()
 
    table = parse_bugzilla()
    #email_body = gen_email_body(table) 
    #send_email(email_body)
    print 'ok'
 
if __name__=='__main__':
    main()
