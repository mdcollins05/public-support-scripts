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

def get_incident_count(since, until, headers):
    payload = {'since': since, 'until': until}
    get_incident_count_url = 'https://mysubdomain.pagerduty.com/api/v1/incidents/count'
    r = requests.get(get_incident_count_url, params=payload, headers=headers)
    return int(r.json()['total'])

def get_incident_ids(since, until, headers):
    id_list = []
    count = get_incident_count(since, until, headers)
    get_incident_ids_url = 'https://mysubdomain.pagerduty.com/api/v1/incidents'
    payload = {'since': since, 'until': until}
    for ea_hun in xrange(0,count+100,100):
        payload['offset'] = ea_hun
        r = requests.get(get_incident_ids_url, params=payload, headers=headers, stream=True)
        id_list = id_list + [ea_inc['id'] for ea_inc in r.json()['incidents']]
    return id_list

def get_log_entries_by_incident(since, until):
    headers = {
        'Authorization': 'Token token=MY_API_ACCESS_KEY',
        'Content-type': 'application/json',
    }
    id_list = get_incident_ids(since, until, headers)
    fin_file = open('incidents_and_notes_{0}_to_{1}_details.csv'.format(since, until), 'w')
    fin_file.write('IncidentID,Created-At,Type,Agent/User,NotificationType,ChannelType,Notes\n')
    for ea_id in id_list:
        r1 = requests.get('https://mysubdomain.pagerduty.com/api/v1/incidents/{0}/log_entries?include[]=channel'.format(ea_id), headers=headers, stream=True)
        for ea_entry in reversed(r1.json()['log_entries']):
            if ea_entry['type'] == 'trigger':
                try:
                    fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"{0}"'.format(ea_entry['agent']['name']), 'N.A.', ea_entry['channel']['type'], '"N.A."\n']))
                except KeyError:
                    fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"N.A.",N.A.', ea_entry['channel']['type'], '"N.A."\n']))
            elif ea_entry['type'] in ['assign', 'escalate']:
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"{0}"'.format(ea_entry['assigned_user']['name']), 'N.A.', ea_entry['channel']['type'], '"N.A."\n']))
            elif ea_entry['type'] == 'notify':
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"{0}"'.format(ea_entry['user']['name']), ea_entry['notification']['type'], 'N.A.,"N.A."\n']))
            elif ea_entry['type'] == 'repeat_escalation_path':
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"N.A.",N.A.', ea_entry['channel']['type'], '"N.A."\n']))
            elif ea_entry['type'] == 'acknowledge':
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"{0}"'.format(ea_entry['agent']['name']), 'N.A.', ea_entry['channel']['type']+'*', '"N.A."\n']))
            elif ea_entry['type'] == 'unacknowledge':
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"N.A.",N.A.', ea_entry['channel']['type'], '"N.A."\n']))
            elif ea_entry['type'] == 'resolve':
                try:
                    fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"{0}"'.format(ea_entry['agent']['name']), 'N.A.', ea_entry['channel']['type'], '"N.A."\n']))
                except KeyError:
                    fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"N.A.",N.A.', ea_entry['channel']['type'], '"N.A."\n']))
            elif ea_entry['type'] == 'annotate':
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], '"{0}"'.format(ea_entry['agent']['name']), 'N.A.', ea_entry['channel']['type'], '"{0}"\n'.format(ea_entry['channel']['content'])]))
            else:
                print ea_entry
    fin_file.close()

if __name__ == '__main__':
    get_log_entries_by_incident(sys.argv[1], sys.argv[2])
