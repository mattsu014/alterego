import re

def extract_reaction(response):
    match = re.search(r"Reaction:\s*(\w+)", response)
    return match.group(1).lower() if match else None


def remove_reaction(response):
    return re.sub(r"Reaction:\s*\w+", "", response).strip()