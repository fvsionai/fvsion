# AI ML imports
from cmath import log
from torch import autocast, Generator, float16
from diffusers import StableDiffusionPipeline

# Object models import
from app.models.fvsion import FvsionModel


# Utility imports
from app.endpoints.modules import utils
import pathlib
from fastapi.encoders import jsonable_encoder
import json

def wrapper(fv: FvsionModel):
    
    # Parameters and settings
    # Need to find a way to make this more robust... , e.g. join?
    pathToLocalModel = "models/stable-diffusion-v1-4"
    pathToOutput = "output"




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
        guidance_scale = fv.guidance_scale,  generator=gen, eta = fv.eta).images[0]  


    # UTILITY: saving the file to a unique name, if fails, try one more time, which will generate a new secret

    def saveJson(j: FvsionModel):
        with open(f"{j.out_image.path}/{j.out_image.name}.json", "w") as f:
            f.write(json.dumps(jsonable_encoder(j)))

    def saveImage():
        fv.out_image.name = utils.filenameUnique(fv.prompt)
        fv.out_image.path = f"{pathToOutput.strip('/')}"
        fv.out_image.type = "png"

        # save image
        print(f"Completed Generation. Attempting to save file as {fv.out_image.path}/{fv.out_image.name}.{fv.out_image.type}")   
        fpname = f"{fv.out_image.path}/{fv.out_image.name}.{fv.out_image.type}" 
        image.save(fpname)

    try:
        saveImage()
        saveJson(fv)
        print("check 2")
        return jsonable_encoder(fv)
    except:
        try:
            saveImage()
            saveJson(fv)
            return jsonable_encoder(fv)
        except Exception as e:
            print(e)
