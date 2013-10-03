#!/usr/bin/env python

import requests
import sys

def get_incident_count(since, until, headers):
    payload = {'since': since, 'until': until}
    get_incident_count_url = 'https://pdt-dank.pagerduty.com/api/v1/incidents/count'
    r = requests.get(get_incident_count_url, params=payload, headers=headers)
    return int(r.json()['total'])

def get_incident_ids(since, until, headers):
    #id_str = ''
    id_list = []
    count = get_incident_count(since, until, headers)
    get_incident_ids_url = 'https://pdt-dank.pagerduty.com/api/v1/incidents'
    payload = {'since': since, 'until': until}
    for ea_hun in xrange(0,count):
        if int(ea_hun)%100==1:
            payload['offset'] = ea_hun
            r = requests.get(get_incident_ids_url, params=payload, headers=headers, stream=True)
            id_list = id_list + [ea_inc['id'] for ea_inc in r.json()['incidents']]
    return id_list

def get_details_by_incident(since, until):
    headers = {
        'Authorization': 'Token token=rcz1JzsqjcKhbEgXgY4z',
        'Content-type': 'application/json',
    }
    id_list = get_incident_ids(since, until, headers)
    fin_file = open('incident_report_{0}_to_{1}_details.csv'.format(since, until), 'w')
    fin_file.write('IncidentID,Created-At,Type,Agent/User,NotificationType,ChannelType,Subject,Summary\n')
    for ea_id in id_list:
        r = requests.get('https://pdt-dank.pagerduty.com/api/v1/incidents/{0}/log_entries?include[]=channel'.format(ea_id), headers=headers, stream=True)
        for ea_entry in reversed(r.json()['log_entries']):
            if ea_entry['type'] != 'notify':
                if ea_entry['channel']['type'] not in ['auto','timeout','website','note'] and ea_entry['channel'].get('subject'):
                    if ea_entry.get('agent') and ea_entry['agent'].get('name'):
                        fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], ea_entry['agent']['name'], 'N.A', ea_entry['channel']['type'], '"' + ea_entry['channel']['subject'] + '"', '"' + ea_entry['channel']['details'] + '"']).replace('\n','') + '\n')
                    elif ea_entry.get('assigned_user'):
                        fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], ea_entry['assigned_user']['name'], 'N.A.', ea_entry['channel']['type'], '"' + ea_entry['channel']['subject'] + '"', '"' + ea_entry['channel']['details'] + '"']).replace('\n','') + '\n')
                else:
                    if ea_entry.get('agent') and ea_entry['agent'].get('name'):
                        fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], ea_entry['agent']['name'], 'N.A', ea_entry['channel']['type']]).replace('\n','') + ',N.A.,N.A.\n')
                    elif ea_entry.get('assigned_user'):
                        fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], ea_entry['assigned_user']['name'], 'N.A.', ea_entry['channel']['type']]).replace('\n','') + ',N.A.,N.A.\n')
            else:
                fin_file.write(','.join([ea_id, ea_entry['created_at'], ea_entry['type'], ea_entry['user']['name'], ea_entry['notification']['type']]).replace('\n','') + ',N.A.,N.A.,N.A.\n')
                
    fin_file.close()


if __name__ == '__main__':
    get_details_by_incident(sys.argv[1], sys.argv[2])