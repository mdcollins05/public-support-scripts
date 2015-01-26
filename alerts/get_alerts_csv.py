#!/usr/bin/env python

#
# Copyright (c) 2011-2012, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of PagerDuty Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL PAGERDUTY INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
