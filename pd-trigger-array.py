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

