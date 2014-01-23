require 'json'

filename="IncidentsInService.txt"

subdomain="change-this"
service_id="change-this"
api_key="change-this"

start="2013-01-01"
stop="2013-05-01"

endpoint="https://#{subdomain}.pagerduty.com/api/v1/incidents/"

def curl_command_string(tokennum,start,stop,endpoint,service_number)
    curl_command='curl -H "Content-type: application/json" -H "Authorization: Token token='+tokennum+'" -X GET -G \
    --data-urlencode "since='+start+'" \
    --data-urlencode "until='+stop+'" \
    --data-urlencode "service='+service_number+'" \
    "'+endpoint+'"'
end

def print_results_to_file(curl_get_all,filename)
  file=File.open(filename,"a")
  IO.popen(curl_get_all).each do |line|
    parsed=JSON.parse(line)
    puts parsed
    parsed["incidents"].each do |hash| 
      hash.each_pair {|key,value| file.puts "#{key},#{value}"}
      file.puts
    end
  end
  file.close
end

curl_first_half_year=curl_command_string(api_key,start,stop,endpoint,service_id)
print_results_to_file(curl_first_half_year,filename)

start="2013-05-02"
stop="2013-10-09"

curl_second_half_year=curl_command_string(api_key,start,stop,endpoint,service_id)
print_results_to_file(curl_second_half_year,filename)