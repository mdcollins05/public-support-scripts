require 'json'

subdomain="change_this"
service_id="change_this"
api_key="change_this"

id="change_this"

endpoint="https://#{subdomain}.pagerduty.com/api/v1/incidents/#{id}/log_entries"

def curl_command_string(tokennum,endpoint)
  curl_command='curl -H "Content-type: application/json" -H "Authorization: Token token='+tokennum+'" -X GET -G "'+endpoint+'"'
end

def print_results(curl_get_all)
  IO.popen(curl_get_all).each do |line|
    parsed=JSON.parse(line)
    puts parsed
  end
end

curl_one=curl_command_string(api_key,endpoint)
puts curl_one
print_results(curl_one)