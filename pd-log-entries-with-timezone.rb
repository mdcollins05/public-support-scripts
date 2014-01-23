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

