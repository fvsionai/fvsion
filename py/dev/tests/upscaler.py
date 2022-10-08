import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..', 'py'))

# AI ML imports
from mimetypes import init
from torch import autocast, Generator, float16

# Object models import
from app.models.fvsion import FvsionModel, UpscalerModel


# Utility imports
import PIL
from app.endpoints.v00.modules import utils
from fastapi.encoders import jsonable_encoder
import PIL.Image, PIL.ImageOps


# Object models import
from app.models.fvsion import FvsionModel, MaskImageEnum, FileModel
from app.endpoints.v00.modules import utils


# testing tile
from app.endpoints.v00.modules.custom_pipe import FvsionPipeline, preprocess_init_image, preprocess_mask


from typing import Optional, List

import torch
import torch.nn as nn
from torch import autocast
from diffusers import PNDMScheduler, LMSDiscreteScheduler
from PIL import Image

from app.endpoints.v00.modules.external import upscaler_gfpgan 

# fv = FvsionModel(prompt= "A fantasy landscape, trending on artstation", unique= "c0d3bc14-b2be-449d-b227-dffd6e04580d", mode= "txt2img", 
# init_image=FileModel(name= "init", type= "png", path= "F:\\fvsionai\\fvsion\\outputs\\tmp"), 
# init_image_base64=None, mask_image_type= "default", 
# mask_image=FileModel(name= "mask", type= "png", path= "outputs/tmp"), 
# mask_color= "white", 
# out_image=FileModel(name= "99094cd144fe_a-fantasy-landscape-trending-o", type= "webp", path= "outputs"), 
# api_github= "https://github.com/FvsionAI/fvsion", api_version= "v00", mode_isChain= False, height= 512, width= 512, num_inference_steps= 30, guidance_scale= 6.5, eta= 0.0, strength= 0.85, seed= 1024, allowNSFW= True, path_to_local_model= "models/stable-diffusion-v1-4-fp16", path_to_outputs= "outputs", doJSON= True)

fv = FvsionModel(prompt="test", mode="txt2img", upscaler=UpscalerModel(), init_image=FileModel(name="99094cd144fe_a-fantasy-landscape-trending-o", type="webp", path="outputs"), out_image=FileModel(name="99094cd144fe_a-fantasy-landscape-trending-o", type="webp", path="outputs"))

upscaler_gfpgan.upscaler(fv)