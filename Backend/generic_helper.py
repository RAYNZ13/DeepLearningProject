#extract sessionID
import re

def extract_sessionID(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""

#test case
# if __name__ == "__main__":
#     print(extract_sessionID("projects/restobot-for-restaurent-w-yvie/agent/sessions/9e4816dd-9ec5-eb5a-8b78-0ca4ea369bee/contexts/ongoing-order"))