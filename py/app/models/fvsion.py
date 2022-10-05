from distutils import extension
from turtle import width
from pydantic import BaseModel, validator
from pydantic.color import Color

from enum import Enum
import uuid, os

# mode to follow diffusers pipeline functions, relatively specific
class ModeEnum(str, Enum):
    txt2img = 'txt2img'
    img2img = 'img2img'
    inpainting = 'inpainting'
    lowvram = 'lowvram'

class MaskImageEnum(str, Enum):
    default = 'default' # use separate file (white as area to be changed)
    alpha = 'alpha' # use same file as init, but using alpha channel as mask
    white = 'white' # use same file as init, but using color white as mask
    color = 'color' # use pydantic color, as input to select mask

class FileModel(BaseModel):
    name: str | None = "init" # exclude extension
    type: str | None = "png" # eg. png, jpg, webp, 
    path: str | None = "outputs/tmp" # might be better changed to pathlib.path later


class ImageModel(BaseModel):
    image: str
    draw_image: FileModel | None 

# when a value is given for the parameters, type is auto assigned and will be used as default when not given 
class FvsionModel(BaseModel):
    # important data
    prompt: str | list[str] # required, for now, might give a default value in wrapper function, allow for list of string for multi prompts
    unique: uuid.UUID = uuid.uuid4()
    mode: ModeEnum = ModeEnum.txt2img 
    mode_isChain = False

    # this is for pipe input
    height = 512
    width = 512
    num_inference_steps = 16
    guidance_scale = 7.5
    eta = 0.0
    strength = 0.85 #for img2img, higher more variation especially useful for inpainting, other default is 0.75

    # this is for pipe input specific to img2img / inpainting
    init_image: FileModel | None 
    init_image_base64: str | None #for base64 test
    mask_image_type: MaskImageEnum = MaskImageEnum.default  # whether to use other files or not 
    mask_image: FileModel | None
    mask_color: Color | None = Color('white')

    # other 
    seed = int.from_bytes(os.urandom(2), "big")
    allowNSFW = False

    # other utilities
    out_image: FileModel | None # filename and path
    api_github: str = "https://github.com/FvsionAI/fvsion"
    api_version: str = "v00"
    pathToLocalModel = "models/stable-diffusion-v1-4-fp16"
    pathToOutput = "outputs"

    # doYAML = False # if True generate a YAML file that save all config
    doJSON = True # if True generate a JSON file that save all config

    @validator('height', 'width')
    def h_and_w_must_be_multiple_of_8(cls, v):
        if v % 8 != 0:
            raise ValueError('height and weight must be multiple of 8')
        return v

    @validator('strength')
    def between_n_include_zero_to_one(cls, v):
        if v>1 or v<0:
            raise ValueError('strength must be between 0 <= x <= 1')
        return v




## https://github.com/huggingface/diffusers/blob/main/src/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion.py
# prompt (`str` or `List[str]`):
#     The prompt or prompts to guide the image generation.
# height (`int`, *optional*, defaults to 512):
#     The height in pixels of the generated image.
# width (`int`, *optional*, defaults to 512):
#     The width in pixels of the generated image.
# num_inference_steps (`int`, *optional*, defaults to 50):
#     The number of denoising steps. More denoising steps usually lead to a higher quality image at the
#     expense of slower inference.
# guidance_scale (`float`, *optional*, defaults to 7.5):
#     Guidance scale as defined in [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598).
#     `guidance_scale` is defined as `w` of equation 2. of [Imagen
#     Paper](https://arxiv.org/pdf/2205.11487.pdf). Guidance scale is enabled by setting `guidance_scale >
#     1`. Higher guidance scale encourages to generate images that are closely linked to the text `prompt`,
#     usually at the expense of lower image quality.
# eta (`float`, *optional*, defaults to 0.0):
#     Corresponds to parameter eta (η) in the DDIM paper: https://arxiv.org/abs/2010.02502. Only applies to
#     [`schedulers.DDIMScheduler`], will be ignored for others.

