from turtle import width
from pydantic import BaseModel, validator

# when a value is given for the parameters, type is auto assigned and will be used as default when not given 
class FvsionModel(BaseModel):
    # this is for pipe input
    prompt: str # required, for now, might give a default value in wrapper function
    height = 512
    width = 512
    num_inference_steps = 16
    guidance_scale = 7.5
    eta = 0.0
    # other 
    seed = 1024
    allowNSFW = False
    # other utilities
    filename: str | None = None

    @validator('height', 'width')
    def h_and_w_must_be_multiple_of_8(cls, v):
        if v % 8 != 0:
            raise ValueError('height and weight must be multiple of 8')
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

