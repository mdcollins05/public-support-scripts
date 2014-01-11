require 'json'

filename="IncidentLog.txt"

subdomain="change_this"
service_id="change_this"
api_key="change_this"

id="change_this"

endpoint="https://#{subdomain}.pagerduty.com/api/v1/log_entries/#{id}"

def curl_command_string(tokennum,endpoint)
    curl_command="curl -H \"Content-type: application/json\" -H \"Authorization: Token token=#{tokennum}\" -X GET -G \
    --data-urlencode \"include[]=channel\" \
    \"#{endpoint}\""
end

def print_results_to_file(curl_get_all,filename)
  file=File.open(filename,"a")
  IO.popen(curl_get_all).each do |line|
    parsed=JSON.parse(line)
    puts parsed
    #parsed["incidents"].each do |hash| 
    #  hash.each_pair {|key,value| file.puts "#{key},#{value}"}
    #  file.puts
    #end
  end
  file.close
end

curl_one=curl_command_string(api_key,endpoint)
puts curl_one
print_results_to_file(curl_one,filename)