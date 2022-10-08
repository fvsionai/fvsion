# AI ML imports
import os
from torch import autocast, Generator, float16, float32, cuda
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, StableDiffusionInpaintPipeline

# Object models import
from app.models.fvsion import FvsionModel

# Utility imports
from app.endpoints.v00.modules import utils
from app.endpoints.v00.modules.external.minimal_gpu import StableDiffusionLowVRAMPipeline

def wrapper(fv: FvsionModel):
    
    # Parameters and settings
    # TODO might, need to find a way to make this more robust... , e.g. join?
    path_to_local_model = fv.path_to_local_model
    path_to_outputs = fv.path_to_outputs

    # if folder has fp16 mentioned, use fp16
    if "fp16" in path_to_local_model:
        revision = "fp16"
    else:
        revision = "main"

    utils.createFolder(path_to_outputs)

    # reset track stats, used in conjunction with mem_bytes 
    cuda.reset_peak_memory_stats()

    # if seed is provided, use manual seed, else random seed
    if(fv.seed is not None):
        gen = Generator("cuda").manual_seed(fv.seed)
    else:
        fv.seed = int.from_bytes(os.urandom(2), byteorder="big")
        gen = Generator("cuda")
            
    
    # DIFFUSERS: setup diffusers pipe
    if(fv.mode == "txt2img"):
        pipe = StableDiffusionPipeline.from_pretrained(path_to_local_model, revision=revision, torch_dtype=float16, use_auth_token=False)
        kwargs = {"prompt": fv.prompt, "generator": gen, "height":fv.height, "width":fv.width, "num_inference_steps":fv.num_inference_steps, 
            "guidance_scale" : fv.guidance_scale, "eta" : fv.eta }

    elif(fv.mode == "img2img"):
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(path_to_local_model, revision=revision, torch_dtype=float16, use_auth_token=False)
        init_image = utils.initProcessing(fv)
        kwargs = {"prompt": fv.prompt, "generator": gen, "num_inference_steps":fv.num_inference_steps, 
            "guidance_scale" : fv.guidance_scale, "eta" : fv.eta, "init_image":init_image, "strength":fv.strength, }

    elif(fv.mode == "inpainting"):
        pipe = StableDiffusionInpaintPipeline.from_pretrained(path_to_local_model, revision=revision, torch_dtype=float16, use_auth_token=False)
        init_image = utils.initProcessing(fv)
        mask_image = utils.maskProcessing(fv)
        kwargs = {"prompt": fv.prompt, "generator": gen, "num_inference_steps":fv.num_inference_steps, 
            "guidance_scale" : fv.guidance_scale, "eta" : fv.eta, "init_image":init_image, "strength":fv.strength, "mask_image":mask_image}
    
    elif(fv.mode == "lowvram"):
        pipe = StableDiffusionLowVRAMPipeline.from_pretrained(path_to_local_model, revision=revision, torch_dtype=float32, use_auth_token=False)
        pipe.enable_minimal_memory_usage()
        pipe.enable_attention_slicing()
        kwargs = {"prompt": fv.prompt, "height":fv.height, "width":fv.width, "num_inference_steps":fv.num_inference_steps, 
            "guidance_scale" : fv.guidance_scale, "eta" : fv.eta}
    
    else:
        print("No mode found for "+fv.mode)
        del pipe, gen, kwargs
        cuda.empty_cache() 
        return {"error": "No mode found for "+fv.mode}


    # delete variables and empty cache
    del gen
    cuda.empty_cache()

    pipe.set_progress_bar_config(disable=None)

    # enable/disable safety (NSFW) checker
    if(fv.allowNSFW and fv.mode != "lowvram"):
        pipe.safety_checker = utils.dummy

    if(fv.mode != "lowvram"):
        # reduce VRAM requirement
        # print("not lowvram mode")
        pipe.enable_attention_slicing()
        # send to CUDA for NVIDIA GPU
        pipe = pipe.to("cuda")

    print("Complete pipe setup. Starting image generation.")

    # print(fv) # diagnostic

    # the actual generation happens here.
    # following https://github.com/huggingface/diffusers/pull/740, no longer need to use autocast
    try:
        images = pipe(**kwargs).images

        print(f"Completed Generation. Attempting to save {len(images)} file(s)")

        # display stats tracked
        mem_bytes = float(cuda.max_memory_allocated()) / (10**9)
        print("{:.1f}".format(mem_bytes) + " GB of VRAM used by cuda directly")
        cuda.reset_peak_memory_stats()

        # delete variables and empty cache
        del pipe, mem_bytes, kwargs
        cuda.empty_cache() 
    except Exception as e:
        print(e)
        del pipe, kwargs
        return {"error": str(e)}   

    utils.save(fv, images)
    del images
    cuda.empty_cache()
    # if successful return fv
    return fv
