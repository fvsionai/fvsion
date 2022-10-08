import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..', 'py'))

# AI ML imports
from mimetypes import init
from torch import autocast, Generator, float16

# Object models import
from app.models.fvsion import FvsionModel


# Utility imports
import PIL
from app.endpoints.v00.modules import utils
from fastapi.encoders import jsonable_encoder
import PIL.Image, PIL.ImageOps


# Object models import
from app.models.fvsion import FvsionModel, MaskImageEnum, FileModel
from app.endpoints.v00.modules import utils


# testing tile
from py.app.endpoints.v00.modules.custom_pipe import FvsionPipeline, preprocess_init_image, preprocess_mask


from typing import Optional, List

import torch
import torch.nn as nn
from torch import autocast
from diffusers import PNDMScheduler, LMSDiscreteScheduler
from PIL import Image

def wrapper(fv: FvsionModel):

    # Parameters and settings
    # Need to find a way to make this more robust... , e.g. join?
    path_to_local_model = fv.path_to_local_model
    path_to_outputs = fv.path_to_outputs

    # scheduler = PNDMScheduler(
    #     beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear"
    # )

    # use LMS without init images
    scheduler = LMSDiscreteScheduler(
        beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear"
    )
    
    pipe = FvsionPipeline.from_pretrained(
        path_to_local_model,
        scheduler=scheduler,
        revision="fp16",
        torch_dtype=torch.float16,
    ).to("cuda")

    @torch.inference_mode()
    @torch.cuda.amp.autocast()
    def predict():
        generator = torch.Generator("cuda").manual_seed(fv.seed)

        try:
            images = pipe(
                prompt= fv.prompt,
                width=fv.width,
                height=fv.height,
                prompt_strength=fv.strength,
                guidance_scale=fv.guidance_scale,
                generator=generator,
                num_inference_steps=fv.num_inference_steps,
            ).images

            for i, sample in enumerate(images):
                output_path = f"outputs/out-{i}.png"
                sample.save(output_path)

            print(f"Completed Generation. Attempting to save {len(images)} file(s)")
        except Exception as e:
            print(e) 

        return fv
    
    predict()

# for tiling
def patch_conv(**patch):
    cls = torch.nn.Conv2d
    init = cls.__init__
    def __init__(self, *args, **kwargs):
        return init(self, *args, **kwargs, **patch)
    cls.__init__ = __init__

patch_conv(padding_mode='circular')


fv = FvsionModel(prompt="Stone wall trimsheet, quixel, substance designer, trending on artstation")


wrapper(fv)