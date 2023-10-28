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
Write a maze program that receives txt files which represents a maze, and source and destination coordinates
For example, the following maze is represented as a txt file:
(Read this sample from sth/magent/maze.txt)
```txt
#######
#....b#
#.###.#
#.#...#
#...#.#
#.#.#.#
#....a#
#######
```
The # represents a wall, and the . represents a path. The a and b represents the source and destination coordinates, respectively.
The program should convert this txt file to a grid of 0s and 1s, where 0 represents a wall and 1 represents a path. 2 represents the source and 3 represents the destination.
For example, the above maze should be converted to the following grid:
```python
maze = [
    [0,0,0,0,0,0,0]
    [0,1,1,1,1,3,0]
    [0,1,0,1,0,1,0]
    [0,1,0,0,0,1,0]
    [0,1,0,1,0,1,0]
    [0,1,0,1,0,1,0]
    [0,1,1,1,1,2,0]
    [0,0,0,0,0,0,0]
]
```
"""

user_proxy_agent.initiate_chat(assistant_agent, message=message)
