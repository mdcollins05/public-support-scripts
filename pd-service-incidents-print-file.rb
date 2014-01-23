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