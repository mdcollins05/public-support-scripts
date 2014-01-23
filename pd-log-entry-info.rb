require 'json'
require 'date'

subdomain="change_this"
service_id="change_this"
api_key="change_this"

id="PUF0J5S"

endpoint="https://#{subdomain}.pagerduty.com/api/v1/log_entries/#{id}"

def curl_command_string(tokennum,endpoint)
    curl_command="curl -H \"Content-type: application/json\" -H \"Authorization: Token token=#{tokennum}\" -X GET -G \
    --data-urlencode \"include[]=channel\" \
    \"#{endpoint}\""
end

def print_results(curl_get_all)
  IO.popen(curl_get_all).each do |line|
    parsed=JSON.parse(line)
    puts parsed
    log=parsed["log_entry"]
    time=log["created_at"]
    puts time
    
    channel=log["channel"]
    puts channel
    linesstring= channel["body"]
    lines=linesstring.split("\n")
    lines.each {|line| puts line}
  end
end

curl_one=curl_command_string(api_key,endpoint)
puts curl_one
print_results(curl_one)

puts ENV['TZ']