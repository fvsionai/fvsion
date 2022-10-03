# AI ML imports
from torch import autocast, Generator, float16, cuda
from app.endpoints.v00.modules.external.minimal_gpu import StableDiffusionPipelineMinMemory

# Object models import
from app.models.fvsion import FvsionModel


# Utility imports
from app.endpoints.v00.modules import utils


def wrapper(fv: FvsionModel):
    
    # Parameters and settings
    # Need to find a way to make this more robust... , e.g. join?
    pathToLocalModel = fv.pathToLocalModel
    pathToOutput = fv.pathToOutput

    utils.createFolder(pathToOutput)

    cuda.reset_peak_memory_stats()
    # DIFFUSERS: setup diffusers pipe
    # manual seed disabled for min vram mode
    # gen = Generator("cuda").manual_seed(fv.seed)

    pipe = StableDiffusionPipelineMinMemory.from_pretrained(pathToLocalModel, revision="main", use_auth_token=False)

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

        # with autocast("cuda"):
        #     _ = pipe(fv.prompt, guidance_scale=7.5, num_inference_steps=10, output_type="numpy")  

        mem_bytes = cuda.max_memory_allocated()
        print(mem_bytes)
        cuda.reset_peak_memory_stats()
    except Exception as e:
        print(e)
        return e   

    # UTILITY: saving the file to a unique name, if fails, try one more time, which will generate a new secret
    try:
        utils.saveOutput(fv=fv, pathToOutput=pathToOutput, image=images)
        print(f"successfully saved {len(images)} files")
    except:
        try:
            utils.saveOutput(fv=fv, pathToOutput=pathToOutput, image=images)
            print(f"successfully saved {len(images)} files")
        except Exception as e:
            print(e)
            return e 

    # if successful return fv
    return fv