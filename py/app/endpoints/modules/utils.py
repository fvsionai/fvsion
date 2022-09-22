import time
import secrets
from slugify import slugify

# UTILITY: create prefixes to filename to try to increase uniqueness of filename 
def prefix():
    timestr = time.strftime("%Y%m%d_%H%M%S")
    secstr = secrets.token_hex(8)
    return timestr+"_"+secstr

def filenameUnique(p):
    # prompt cut in front to avoid too long prompt text, os path limit 
    # return file-name-from-prompt-cut (i.e. no path or extension)
    return f"{prefix()}_{slugify(p)[0:30]}" 