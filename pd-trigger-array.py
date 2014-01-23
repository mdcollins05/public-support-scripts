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

subdomain="insert_here"
api_key="insert_here"

endpoint="https://events.pagerduty.com/generic/2010-04-15/create_event.json"
service_access_array=["change_for_one_service","change_for_second_service","change_or_keep_adding_services"]

incident_key="JMYDNSPRA"
subject="Emergency notification from the server."
details_dict={"ping time":"1200ms", "load average":"200ms"} 

def curl_command_post_schedules(token_string,schedule_json,endpoint):
    #curl_command="curl -H \"Content-type: application/json\" -X POST \ -d #{schedule_json} \"#{endpoint}\""
    curl_command="curl -H \"Content-type: application/json\" -X POST -d " + schedule_json + " \"" + endpoint + "\""
    return curl_command

def dict_to_json(hash):
  string=""
  for key in details_dict:
    #string+="\"#{key}\": \"#{value}\", "
    string+="\"" + key + "\": \"" + details_dict[key] + "\", "
  return string
    
sched_dict=dict_to_json(details_dict)

for service_entry in service_access_array:
  sched_json= "'{ \
              \"service_key\": \""  + service_entry + "\", \
              \"incident_key\": \"" + incident_key + "\", \
              \"event_type\": \"trigger\", \
              \"description\": \"" + subject + "\", \
              \"details\": {" + sched_dict + "}   }'"

  print sched_json
               
  curl_string = curl_command_post_schedules(api_key,sched_json,endpoint)
  print curl_string

  os.system(curl_string)

