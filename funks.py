# ths file is for helper functions and other non pycord stuff
import json
import re


def get_config() -> dict:
    with open("config.json", "r") as f:
        jdata = json.load(f)
    return jdata


def data_extractor(msg: str) -> dict:
    # takes the string format of a message then returns the wanted data in a dict

    try:
        # Define regular expressions for extracting relevant data
        streak_pattern = re.compile(r"\[STREAK (\d+)\]")
        days_pattern = re.compile(r"\[DAYS (\d+)\]")
        problems_pattern = re.compile(r"\[PROBLEMS\s+(\d+)\]")
        today_pattern = re.compile(r"TODAY\[(\d+)\]")

        streak_match = streak_pattern.search(msg)
        days_match = days_pattern.search(msg)
        problems_match = problems_pattern.search(msg)
        today_match = today_pattern.search(msg)

        # Create a dictionary with the extracted data
        data_dict = {
            "streak": int(streak_match.group(1)) if streak_match else None,
            "days": int(days_match.group(1)) if days_match else None,
            "problems": int(problems_match.group(1)) if problems_match else None,
            "today": int(today_match.group(1)) if today_match else None,
        }

        return data_dict

    except AttributeError as e:
        print(f"Error extracting data: {e}")
    return {}


def checkisinstance(embed, title, value_title, obj, objx):
    """
    Add fields to the given embed based on the type of obj.

    Parameters:
    - embed (discord.Embed): The embed to which fields are added.
    - title (str): The title for the field.
    - value_title (str): The title for the value field (used when obj is a tuple).
    - obj: The object to check and add fields based on its type.
    - objx: The expected type of obj.

    Returns:
    - discord.Embed: The updated embed with added fields.
    """
    if not isinstance(obj, objx):
        # If obj is not of the expected type, set a default value
        obj = "missing data, try again later"
        embed.add_field(name=title, value=obj)
    else:
        # If obj is a tuple, add fields for the value and additional information
        embed.add_field(name=title, value=obj[1])
        embed.add_field(name=value_title, value=obj[2])

    return embed
