# Object models import
from app.models.fvsion import FvsionModel

# UTILITY LIB
import time
import secrets
from slugify import slugify
import pathlib
from fastapi.encoders import jsonable_encoder
import json


# UTILITY: create prefixes to filename to try to increase uniqueness of filename 
def prefix():
    timestr = time.strftime("%Y%m%d_%H%M%S")
    secstr = secrets.token_hex(8)
    return timestr+"_"+secstr

def filenameUnique(p):
    # prompt cut in front to avoid too long prompt text, os path limit 
    # return file-name-from-prompt-cut (i.e. no path or extension)
    return f"{prefix()}_{slugify(p)[0:30]}" 


# UTILITY: create folder if it doesn't exist yet
def createFolder(path):
    pathlib.Path(path.strip('/')).mkdir(parents=True, exist_ok=True) 

def saveJson(j: FvsionModel):
    with open(f"{j.out_image.path}/{j.out_image.name}.json", "w") as f:
        f.write(json.dumps(jsonable_encoder(j)))

def saveImage(fv, image):
    fpname = f"{fv.out_image.path}/{fv.out_image.name}.{fv.out_image.type}" 
    image.save(fpname)

def saveOutput(fv, pathToOutput, image):
    fv.out_image.name = filenameUnique(fv.prompt)
    fv.out_image.path = f"{pathToOutput.strip('/')}"
    fv.out_image.type = "png"

    saveImage(fv, image)        
    saveJson(fv)

# enable/disable safety (NSFW) checker
def dummy(images, **kwargs):
    return images, False