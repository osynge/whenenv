import uuid
import base64
import string
import sys

transtbl = None
if sys.version_info < (3,):
    transtbl = string.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )

if sys.version_info > (3,):
    transtbl = str.maketrans(
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
          'ABCEGHJKLMNPRSTVWXYZabcdefghijkl'
        )

def GeneratePrompt():
    match_prompt = uuid.uuid4()
    return base64.b32encode(str(match_prompt).replace('-', '').decode('hex')).rstrip('=').translate(transtbl)
