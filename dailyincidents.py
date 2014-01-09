import os
import subprocess
import json

subdomain="change_this"
service_id="change_this"
api_key="change_this"

start="2014-01-04"
stop="2014-01-05"

endpoint="https://"+subdomain+".pagerduty.com/api/v1/incidents/"

def curl_command_string(tokennum,start,stop,url,service_number):
    curl_command='curl -H "Content-type: application/json" -H "Authorization: Token token='+tokennum+'" -X GET -G \
    --data-urlencode "since='+start+'" \
    --data-urlencode "until='+stop+'" \
    --data-urlencode "service='+service_number+'" \
    "'+url+'"'
    return curl_command

cs=curl_command_string(api_key,start,stop,endpoint,service_id)

output = subprocess.check_output(cs, shell=True)
decoded_data=json.loads(output)
print decoded_data
incidents= decoded_data['incidents']
f=open('incidents_file.txt', 'w+')
for incident in incidents:
  f.write(str(incident))
f.close