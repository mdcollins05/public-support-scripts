#!/usr/bin/env python
import requests
import sys

def get_alerts(since, until):
    """
    A sample script to programatically access the PD alerts csv-page behind the login, via a single-session.
    CLI USAGE: './get_alerts_csv.py SINCE-TIMESTAMP UNTIL-TIMESTAMP'
    Currently, timestamps should be in the format '2013-09-10T00:00:00Z'.
    Also, currently, subdomain, email, and password are all hard-coded, but no reason they can't be passed in as well, if need be.
    """
    login_url = 'https://mysubdomain.pagerduty.com/sign_in'
    login = {'user[email]':'myemail@example.com','user[password]':'MYPASSWORD'}
    s = requests.Session()
    r = s.post(login_url, data=login, stream=True)
    url = 'https://mysubdomain.pagerduty.com/csv/alerts'
    payload = {'since': since, 'until': until}
    r = s.get(url, data=payload)
    f = open('test.csv','w')
    f.write(r.text.encode('utf-8'))
    f.close()


if __name__ == '__main__':
    get_alerts(sys.argv[1], sys.argv[2])
