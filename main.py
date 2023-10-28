#!/usr/bin/env python

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.teachable_agent import TeachableAgent


config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST", filter_dict={"model": ["gpt-4"]}
)


def ask_expert_assistant(message):
    assistant_agent = AssistantAgent(
        name="ask_expert_assistant::AssistantAgent",
        llm_config={
            "temperature": 0,
            "config_list": config_list,
        },
    )
    user_proxy_agent = UserProxyAgent(
        name="ask_expert_assistant::UserProxyAgent",
        human_input_mode="NEVER",
        code_execution_config={"work_dir": "./.tmp/code/expert_user"},
        system_message=""""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    )

    user_proxy_agent.initiate_chat(assistant_agent, message=message)
    user_proxy_agent.stop_reply_at_receive(assistant_agent)
    user_proxy_agent.send(
        "Only send the final output.",
        assistant_agent,
    )
    return user_proxy_agent.last_message()["content"]


teachable_agent = TeachableAgent(
    name="TeachableAgent",
    teach_config={
        "path_to_db_dir": "./.tmp/interactive/teachable_agent_db",
        "recall_threshold": 1.5,
    },
    llm_config={
        "config_list": config_list,
        "request_timeout": 600,
        "seed": 42,
        "temperature": 0,
        "functions": [
            {
                "name": "ask_expert_assistant",
                "description": "ALWAYS ask expert when you can't solve the problem or answer the question satisfactorily first, then answer whether you know the answer or not.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "question to ask expert. Ensure the question includes enough context, such as the code and the execution result. The expert does not know the conversation between you and the user unless you share the conversation with the expert.",
                        },
                    },
                    "required": ["message"],
                },
            }
        ],
    },
)

user_proxy_agent = UserProxyAgent(
    "UserProxyAgent",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    function_map={
        "ask_expert_assistant": ask_expert_assistant,
    },
)

teachable_agent.initiate_chat(
    user_proxy_agent,
    message="I am a teachable agent. I can learn from your feedback.",
)

teachable_agent.learn_from_user_feedback()

teachable_agent.close_db()
