#!/usr/bin/env python

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST", filter_dict={"model": ["gpt-4"]}
)


assistant_agent = AssistantAgent(
    name="AssistantAgent",
    llm_config={
        "temperature": 0,
        "config_list": config_list,
    },
)
user_proxy_agent = UserProxyAgent(
    name="UserProxyAgent",
    human_input_mode="ALWAYS",
    code_execution_config={"work_dir": "./.tmp/code/coder"},
)


message = """
Write a tick tack toe game in python.
The game must be web based and must be playable by two players.
It should run on localhost. must have restart button.
and it should look pretty
"""

user_proxy_agent.initiate_chat(assistant_agent, message=message)
