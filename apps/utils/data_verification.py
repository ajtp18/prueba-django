import re

def contains_special_characters(s):
    return bool(re.search(r'[#$%^&*@!]', s))