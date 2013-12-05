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

import collections
import csv
import json
import requests


def process_users():
    url = 'https://mysubdomain.pagerduty.com/api/v1/users'
    headers = {'Authorization': 'Token token=MYSECRETKEY','content-type': 'application/json',}
    reader=csv.DictReader(open('users.csv','r'), fieldnames=('name','email','role','address','type'))
    phone_reader=csv.DictReader(open('users.csv','r'), fieldnames=('name','email','role','address','$
    reader.next()
    phone_reader.next()
    user_id_list = []
    for row in reader:
        row.pop('address')
        row.pop('type')
        myjson = json.dumps(row)
        myjson = myjson.replace('}',', "requester_id":"PJR28TQ",}')
        r = requests.post(url, data=myjson, headers=headers)
        response_dict = collections.OrderedDict(r.json())
        user_id_list.append(response_dict[u'user'][u'id'])
    contact_urls = []
    notification_rule_list = []
    for id in user_id_list:
            contact_urls.append('https://mysubdomain.pagerduty.com/api/v1/users/{0}/contact_methods'$
            notification_rule_list.append('https://mysubdomain.pagerduty.com/api/v1/users/{0}/notifi$
    i=0
    contact_method_list = []
    for row2 in phone_reader:
        row2.pop('name')
        row2.pop('email')
        row2.pop('role')
        myjson2 = json.dumps(row2)
        myjson2 = myjson2.replace('{"type"', '{"contact_method":{"type"').replace('"}','"}}')
        new_r = requests.post(contact_urls[i], data=myjson2, headers=headers)
        res_dict2 = collections.OrderedDict(new_r.json())
        i+=1
        contact_method_list.append(res_dict2[u'contact_method'][u'id'])
    j=0
    for ea_id in contact_method_list:
        dct = {'notification_rule': {'contact_method_id': "{0}".format(ea_id), 'start_delay_in_minut$
        jj = json.dumps(dct)
        rq = requests.post(notification_rule_list[j], data=jj, headers=headers)
        j+=1


if __name__ == '__main__':
    process_users()