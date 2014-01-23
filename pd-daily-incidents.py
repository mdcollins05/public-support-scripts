# Copyright (c) 2014, PagerDuty, Inc. <info@pagerduty.com>
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