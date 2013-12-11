require 'json'


subdomain="change_this"
api_key="change_this"


schedule_id="change_this"
endpoint="https://#{subdomain}.pagerduty.com/api/v1/schedules/#{schedule_id}"

def curl_command_post_schedules(token_string,endpoint)
    curl_command="curl -H \"Content-type: application/json\" -H \"Authorization: Token token=#{token_string}\" -X GET -G \
    \"#{endpoint}\""
end

curl_string = curl_command_post_schedules(api_key,endpoint)
puts curl_string

IO.popen(curl_string).each do |line|
  parsed=JSON.parse(line)
  puts parsed
end