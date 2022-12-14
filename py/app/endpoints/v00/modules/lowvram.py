# AI ML imports
from torch import autocast, Generator, float16, cuda
from app.endpoints.v00.modules.external.minimal_gpu import StableDiffusionLowVRAMPipeline

# Object models import
from app.models.fvsion import FvsionModel


# Utility imports
from app.endpoints.v00.modules import utils


def wrapper(fv: FvsionModel):
    
    # Parameters and settings
    # Need to find a way to make this more robust... , e.g. join?
    path_to_local_model = fv.path_to_local_model
    path_to_outputs = fv.path_to_outputs

    utils.createFolder(path_to_outputs)

    cuda.reset_peak_memory_stats()
    # DIFFUSERS: setup diffusers pipe
    # manual seed disabled for min vram mode
    # gen = Generator("cuda").manual_seed(fv.seed)

    pipe = StableDiffusionLowVRAMPipeline.from_pretrained(path_to_local_model, revision="fp16", use_auth_token=False)

    # safety (NSFW) checker is disabled for min vram mode

    # reduce VRAM requirement
    pipe.set_progress_bar_config(disable=None)
    pipe.enable_minimal_memory_usage()
    pipe.enable_attention_slicing()

    # disabled to allow for custom cuda allocation and thus allow for some to cpu
    # # send to CUDA for NVIDIA GPU
    # pipe = pipe.to("cuda")

    print("Complete pipe setup. Starting image generation.")

    # print(fv) # diagnostic

    # the actual generation happens here.
    try:
        with autocast("cuda"):
            images = pipe(fv.prompt,  height=fv.height, width=fv.width, num_inference_steps=fv.num_inference_steps, 
            guidance_scale = fv.guidance_scale, eta = fv.eta).images

        print(f"Completed Generation. Attempting to save {len(images)} file(s)")

 

        mem_bytes = float(cuda.max_memory_allocated()) / (10**9)
        print("{:.1f}".format(mem_bytes) + " GB of VRAM used by cuda directly")
        cuda.reset_peak_memory_stats()

        # delete variables and empty cache
        # delete variables and empty cache
        del pipe, mem_bytes
        cuda.empty_cache() 
    except Exception as e:
        print(e)
        return {"error": str(e)}   

    utils.save(fv, images)
    del images
    cuda.empty_cache()
    # if successful return fv
    return fv