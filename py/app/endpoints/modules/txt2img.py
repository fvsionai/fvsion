# AI ML imports
from turtle import width
from torch import autocast, Generator, float16
from diffusers import StableDiffusionPipeline

# Object models import
from app.models.fvsion import FvsionModel

# Utility imports
import pathlib
import time
import secrets
from slugify import slugify

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
        # return path/to/file/file-name-from-prompt-cut.png
        return f"{pathToOutput.strip('/')}/{prefix()}_{slugify(p)[0:30]}.png" 


    # UTILITY: create folder if it doesn't exist yet
    pathlib.Path(pathToOutput.strip('/')).mkdir(parents=True, exist_ok=True) 

    # DIFFUSERS: setup diffusers pipe
    gen = Generator("cuda").manual_seed(fv.seed)

    pipe = StableDiffusionPipeline.from_pretrained(pathToLocalModel, revision="fp16", torch_dtype=float16, use_auth_token=False)

    # enable/disable safety (NSFW) checker
    def dummy(images, **kwargs):
        return images, False
    
    if(fv.allowNSFW):
        pipe.safety_checker = dummy

    # send to CUDA for NVIDIA GPU
    pipe = pipe.to("cuda")

    # the actual generation happens here.
    with autocast("cuda"):
        image = pipe(fv.prompt,  height=fv.height, width=fv.width, num_inference_steps=fv.num_inference_steps, 
        guidance_scale = fv.guidance_scale,  generator=gen, eta = fv.eta)["sample"][0]  


    # UTILITY: saving the file to a unique name, if fails, try one more time, which will generate a new secret

    try:
        image.save(filenameUnique(fv.prompt))
    except:
        try:
            image.save(filenameUnique(fv.prompt))
        except Exception as e:
            print(e)