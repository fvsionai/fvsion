# AI ML imports
from torch import autocast, Generator, float16
from diffusers import StableDiffusionImg2ImgPipeline

# Object models import
from app.models.fvsion import FvsionModel

# Utility imports
import PIL

import pathlib
import time
import secrets
from slugify import slugify
from fastapi.encoders import jsonable_encoder
import json

def wrapper(fv: FvsionModel):
    
    # Parameters and settings
    # Need to find a way to make this more robust... , e.g. join?
    pathToLocalModel = "models/stable-diffusion-v1-4"
    pathToOutput = "output"

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
    pathlib.Path(pathToOutput.strip('/')).mkdir(parents=True, exist_ok=True) 


    # DIFFUSERS: setup diffusers pipe
    gen = Generator("cuda").manual_seed(fv.seed)

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(pathToLocalModel, revision="fp16", torch_dtype=float16, use_auth_token=False)

    # enable/disable safety (NSFW) checker
    def dummy(images, **kwargs):
        return images, False
    
    if(fv.allowNSFW):
        pipe.safety_checker = dummy

    # send to CUDA for NVIDIA GPU
    pipe = pipe.to("cuda")

    fpname_input = f"{fv.filepath}/{fv.filename}.{fv.filetype}"
    print(f"will be using input file = {fpname_input} and prompt = {fv.prompt}")

    try:
        init_image = PIL.Image.open(fpname_input)
        init_image = init_image.resize((512, 512))
    except Exception as e:
        print(f"failed to load data from {fpname_input}")
        print(e)

    # the actual generation happens here.
    with autocast("cuda"):
        image = pipe(fv.prompt, init_image=init_image, strength=fv.strength, num_inference_steps=fv.num_inference_steps, 
        guidance_scale = fv.guidance_scale).images[0] 

    print("passed image creation")
    # UTILITY: saving the file to a unique name, if fails, try one more time, which will generate a new secret

    def saveJson(j):
        print(j.json())
        print(str(jsonable_encoder(j)))

        with open(f"{j.filepath}/{j.filename}.json", "w") as f:
            f.write(json.dump(jsonable_encoder(j)))

    def saveImage():
        fv.filename = filenameUnique(fv.prompt)
        fv.filepath = f"{pathToOutput.strip('/')}"

        # save image
        print(f"Completed Generation. Attempting to save file as {fv.filepath}/{fv.filename}")   
        fpname = f"{fv.filepath}/{fv.filename}.png" 
        image.save(fpname)

    try:
        saveImage()
        saveJson(fv)

        return jsonable_encoder(fv)
    except:
        try:
            saveImage()
            saveJson(fv)
            return jsonable_encoder(fv)
        except Exception as e:
            print(e)
