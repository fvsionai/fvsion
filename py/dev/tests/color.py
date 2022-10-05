# AI ML imports
from mimetypes import init
from torch import autocast, Generator, float16
from diffusers import StableDiffusionImg2ImgPipeline

# Object models import
from app.models.fvsion import FvsionModel


# Utility imports
import PIL
from app.endpoints.v00.modules import utils
from fastapi.encoders import jsonable_encoder

# Object models import
from app.models.fvsion import FvsionModel, MaskImageEnum, FileModel
from app.endpoints.v00.modules import utils

# Utility imports
import PIL.Image, PIL.ImageOps

import torch
# from transformers import pipeline

# speech_recognizer = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")


img = PIL.Image.open('output/example/color_spectrum.png').convert("RGB")
utils.RGBColorReplacement(img, (255,255,255), (0, 0, 0))

