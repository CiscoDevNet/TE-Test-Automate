"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Kareem Iskander, DevNet Developer Advocate"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
import json
from configparser import ConfigParser
source_agent = "San Jose, CA (AWS us-west-1)"
target_agents = [
    'London, England (AWS eu-west-2)', 'Paris, France (AWS eu-west-3)', 'Columbus, OH (AWS us-east-2)',
    'Ashburn, VA (AWS us-east-1)', 'Sydney, Australia (AWS ap-southeast-2)', 'Frankfurt, Germany (AWS eu-central-1)'
                ]

def main():
    global token, base_url
    te_api_config = ConfigParser()
    te_api_config.read("config.ini")
    token = te_api_config['TE']['token']
    base_url = te_api_config['TE']['base_url']
    get_agents()


def get_agents():
    filtered_target_agents = {"agents":[]}
    target_agend_id_list= []
    hdr = {"Authorization": token, "Content-Type": "application/json", "Accept": "application/json"}
    print(hdr)
    resp = requests.get(url=base_url+'/agents.json?agentTypes=CLOUD', headers=hdr)
    agents = resp.json()
    filtered_source_agent = [x for x in agents['agents'] if x['agentName'] == source_agent]
    source_agent_id = filtered_source_agent[0]['agentId']
    for target_agent in target_agents:
        filtered_target_agents['agents'].append([x for x in agents['agents'] if x['agentName'] == target_agent])
    create_tests(hdr, filtered_source_agent, filtered_target_agents)


def create_tests(headers, source_agent, target_agents):
    payload = {"interval": 900, "agents": [{"agentId": source_agent[0]['agentId']}], "alertsEnabled": 0}
    for agents in target_agents["agents"]:
        for target_agent in agents:
            payload["testName"] = 'FROM ' + source_agent[0]['location'] + ' TO ' + target_agent['location']
            payload["targetAgentId"] = target_agent['agentId']
            json_object = json.dumps(payload)
            print(json_object)
            resp = requests.post(url=base_url+"/tests/agent-to-agent/new.json", headers=headers, data=json_object)
            print(resp.content)


if __name__ == '__main__':
    main()
