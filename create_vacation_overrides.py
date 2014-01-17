#!/usr/bin/env python
import json
import requests
import sys


def get_all_schedule_ids(headers):
    get_schedule_ids_url = 'https://MYSUBDOMAIN.pagerduty.com/api/v1/schedules'
    r = requests.get(get_schedule_ids_url, headers=headers)
    return [id['id'] for id in r.json()['schedules']]


def get_user_id_by_name(headers, name):
    final = False
    params = {'query': name}
    get_user_by_name_url = 'https://MYSUBDOMAIN.pagerduty.com/api/v1/users'
    r = requests.get(get_user_by_name_url, params=params, headers=headers)
    if not r.json()['users']:
        print 'no users found by the name: {0}'.format(name)
    elif len(r.json()['users']) > 1:
        print 'more than one user found for "{0}", please enter the *exact*, full, name of the user, enclosed in quotes'.format(name)
    elif r.json()['users'][0]['name'] == name:
        return r.json()['users'][0]['id']
    return final


def get_all_schedule_ids_which_user_is_in(headers, *args):
    vacationing_user_id = get_user_id_by_name(headers, args[0])
    overriding_user_id = get_user_id_by_name(headers, args[1])
    if not vacationing_user_id or not overriding_user_id:
        return
    sched_id_list = get_all_schedule_ids(headers)
    final_dict = {}
    for each_sched_id in sched_id_list:
        get_schedule_ids_url = 'https://MYSUBDOMAIN.pagerduty.com/api/v1/schedules/{0}/entries'.format(each_sched_id)
        r = requests.get(get_schedule_ids_url, headers=headers, params=args[2])
        final_dict[each_sched_id] = [(each_entry['start'], each_entry['end']) for each_entry in r.json()['entries']]
    return final_dict, vacationing_user_id, overriding_user_id


def create_overrides(*args):
    headers = {
        'Authorization': 'Token token=MY_API_ACCESS_KEY',
        'Content-type': 'application/json',
    }
    cli_params = {"since": args[2], "until": args[3]}
    all_sched_data = get_all_schedule_ids_which_user_is_in(headers, args[0], args[1], cli_params)
    for each_sched in all_sched_data[0]:
        create_override_url = 'https://MYSUBDOMAIN.pagerduty.com/api/v1/schedules/{0}/overrides'.format(each_sched)
        print create_override_url
        for each_date_pair in all_sched_data[0][each_sched]:
            params = {
                "override": {
                    "start": each_date_pair[0],
                    "end": each_date_pair[1],
                    "user_id": all_sched_data[2],
                }
            }
            r = requests.post(create_override_url, headers=headers, data=json.dumps(params))


if __name__ == '__main__':
    create_overrides(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
