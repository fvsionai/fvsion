# AI ML imports
from torch import autocast, Generator, float16
from diffusers import StableDiffusionPipeline

# Object models import
from app.models.fvsion import FvsionModel


# Utility imports
from app.endpoints.modules import utils
from fastapi.encoders import jsonable_encoder


def wrapper(fv: FvsionModel):
    
    # Parameters and settings
    # Need to find a way to make this more robust... , e.g. join?
    pathToLocalModel = "models/stable-diffusion-v1-4"
    pathToOutput = "output"

    utils.createFolder(pathToOutput)


    # DIFFUSERS: setup diffusers pipe
    gen = Generator("cuda").manual_seed(fv.seed)

    pipe = StableDiffusionPipeline.from_pretrained(pathToLocalModel, revision="fp16", torch_dtype=float16, use_auth_token=False)


    # enable/disable safety (NSFW) checker
    if(fv.allowNSFW):
        pipe.safety_checker = utils.dummy

    # send to CUDA for NVIDIA GPU
    pipe = pipe.to("cuda")

    # the actual generation happens here.
    with autocast("cuda"):
        image = pipe(fv.prompt,  height=fv.height, width=fv.width, num_inference_steps=fv.num_inference_steps, 
        guidance_scale = fv.guidance_scale,  generator=gen, eta = fv.eta).images[0]  

    print(f"Completed Generation. Attempting to save file")   

    # UTILITY: saving the file to a unique name, if fails, try one more time, which will generate a new secret

    try:
        utils.saveOutput(fv=fv, pathToOutput=pathToOutput, image=image)
        print("successfully saved files")
        return jsonable_encoder(fv)
    except:
        try:
            utils.saveOutput(fv=fv, pathToOutput=pathToOutput, image=image)
            print("successfully saved files after second attempt")
            return jsonable_encoder(fv)
        except Exception as e:
            print(e)
