"""Hooks to modify the Cat's flow of execution.

Here is a collection of methods to hook into the Cat execution pipeline.

"""

from cat.mad_hatter.decorators import hook
from cat.log import log


# Called when a user message arrives.
# Useful to edit/enrich user input (e.g. translation)
@hook(priority=1)
def before_cat_reads_message(user_message_json: dict, cat) -> dict:
    # Delete task from working memory if exists
    if "task" in cat.working_memory:
        cat.working_memory.pop("task")

    # Get task
    if "prompt_settings" in user_message_json and "task" in user_message_json["prompt_settings"]:
        cat.working_memory["task"] = user_message_json["prompt_settings"]["task"]

    return user_message_json


@hook(priority=1)
def before_cat_sends_message(message: dict, cat):
    # Add valid code check in JSON response
    if "task" in cat.working_memory and cat.working_memory["task"] == "comment":
        answer = cat.llm(
            f"""Structure the sentence in a JSON with this format:
                    {{  
                        'language': the programming language name
                        'code': the code
                    }}
                Sentence
                --------
                {message["content"]}
            """)

        message["content"] = answer

    log(message, "ERROR")

    return message
