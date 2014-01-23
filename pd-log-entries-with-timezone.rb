require 'json'
require 'date'

time_zone="change_this"
subdomain="change_this"
service_id="change_this"
api_key="change_this"

id="PROE3A2"

endpoint="https://#{subdomain}.pagerduty.com/api/v1/log_entries/#{id}"

def curl_command_string(tokennum,endpoint,place)
    curl_command="curl -H \"Content-type: application/json\" -H \"Authorization: Token token=#{tokennum}\" -X GET -G \
    --data-urlencode \"include[]=channel\" --data-urlencode \"time_zone=#{place}\" \
    \"#{endpoint}\""
end

def print_results(curl_get_all)
  IO.popen(curl_get_all).each do |line|
    parsed=JSON.parse(line)
    log=parsed["log_entry"]
    time=log["created_at"]
    puts time
  end
end

run_this=curl_command_string(api_key,endpoint,time_zone)
puts run_this
print_results(run_this)

