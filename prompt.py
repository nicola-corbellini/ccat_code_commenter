"""Hooks to modify the prompts.

Here is a collection of methods to hook the prompts components that instruct the *Agent*.

"""

from typing import List, Dict

from cat.mad_hatter.decorators import hook


@hook(priority=1)
def agent_prompt_prefix(prefix, cat) -> str:
    prefix = ""

    return prefix


@hook(priority=1)
def agent_prompt_suffix(suffix, cat) -> str:
    using_vs_ext = "task" in cat.working_memory

    if using_vs_ext:
        task = cat.working_memory["task"]

    if using_vs_ext and task == "comment":
        suffix = """{episodic_memory}

{declarative_memory}

{tools_output} 

{chat_history}
    Add comments this code.
     Code
     ----
     {input}
    
    Only answer with commented code"""
    elif using_vs_ext and task == "function":
        suffix = """{episodic_memory}

{declarative_memory}

{tools_output}

{chat_history}

    {input}"""

    else:
        suffix = """
        # Context

        {episodic_memory}

        {declarative_memory}
        
        {tools_output}

        ## Conversation until now:{chat_history}
         - Human: {input}
         - AI: """

    return suffix

"""
#Temporarily commented out because the new version don't use this anymore
@hook(priority=1)
def agent_prompt_chat_history(chat_history: List[Dict], cat) -> str:
    history = ""
    if "task" not in cat.working_memory:
        for turn in chat_history:
            history += f"\n - {turn['who']}: {turn['message']}"

    return history

"""
