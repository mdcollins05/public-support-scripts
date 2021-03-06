#!/usr/bin/env python
import json
import requests
import sys


def get_all_schedule_ids(headers):
    r = requests.get('https://MYSUBDOMAIN.pagerduty.com/api/v1/schedules', headers=headers)
    return [each_id['id'] for each_id in r.json()['schedules']]


def get_user_id_by_name(headers, name):
    final = False
    params = {'query': name}
    r = requests.get('https://MYSUBDOMAIN.pagerduty.com/api/v1/users', 
                    params=params,
                    headers=headers)
    if not r.json()['users']:
        print 'no users found by the name: {0}'.format(name)
    elif len(r.json()['users']) > 1:
        print 'more than one user found for "{0}", please enter the *exact*, full, name of the user, enclosed in quotes'.format(name)
    elif r.json()['users'][0]['name'] == name:
        return r.json()['users'][0]['id']
    return final


def get_all_schedule_ids_which_vacationing_user_is_in(headers, *args):
    vacationing_user_id = get_user_id_by_name(headers, args[0])
    overriding_user_id = get_user_id_by_name(headers, args[1])
    if not vacationing_user_id or not overriding_user_id:
        return
    sched_id_list = get_all_schedule_ids(headers)
    final_dict = {}
    for each_sched_id in sched_id_list:
        r = requests.get('https://MYSUBDOMAIN.pagerduty.com/api/v1/schedules/{0}/entries'.format(each_sched_id), 
                        headers=headers, 
                        params=args[2])
        final_dict[each_sched_id] = [(each_entry['start'], each_entry['end']) for each_entry in r.json()['entries']]
    return final_dict, vacationing_user_id, overriding_user_id


def create_overrides(*args):
    """
        Example CLI-usage on OSX/Linux:
        './create_vacation_overrides.py "Vacationing User's Exact Full Name" "Overriding User's Exact Full Name" "vacation-start-date" "vacation-end-date"'
        e.g.:
        './create_vacation_overrides.py "Joe Vaca" "Bob Over" "2014-01-09" "2099-01-01"'
        NAMES MUST BE IN QUOTES
        QUOTES ARE OPTIONAL FOR DATES
    """
    headers = {
        'Authorization': 'Token token=MY_API_ACCESS_KEY',
        'Content-type': 'application/json',
    }
    cli_params = {"since": args[2], "until": args[3]}
    all_sched_data = get_all_schedule_ids_which_vacationing_user_is_in(headers, args[0], args[1], cli_params)
    for each_sched in all_sched_data[0]:
        for each_date_pair in all_sched_data[0][each_sched]:
            params = {
                "override": {
                    "start": each_date_pair[0],
                    "end": each_date_pair[1],
                    "user_id": all_sched_data[2],
                }
            }
            r = requests.post('https://MYSUBDOMAIN.pagerduty.com/api/v1/schedules/{0}/overrides'.format(each_sched), 
                            headers=headers, 
                            data=json.dumps(params))
            #optional check:
            #print r.status_code


if __name__ == '__main__':
    create_overrides(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
