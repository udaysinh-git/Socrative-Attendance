# here we will create functions that will check if email , api_key is valid or not

import re
from openai import OpenAI


def check_email(email: str):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_regex, email))
