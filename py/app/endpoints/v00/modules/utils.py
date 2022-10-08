# Object models import
from math import ceil, sqrt
from tkinter import E
from app.models.fvsion import FvsionModel, MaskImageEnum

# UTILITY LIB
import time
import secrets
from slugify import slugify
import pathlib
from fastapi.encoders import jsonable_encoder
import json
import PIL.ImageOps, PIL.Image
import numpy as np

# UTILITY: create prefixes to filename to try to increase uniqueness of filename 
def prefix():
    # timestr = time.strftime("%Y%m%d_%H%M%S")
    secstr = secrets.token_hex(6)
    # return timestr+"_"+secstr
    return secstr # shorten prefix, exclude timestr

def filenameUnique(p):
    # prompt cut in front to avoid too long prompt text, os path limit 
    # return file-name-from-prompt-cut (i.e. no path or extension)
    return f"{prefix()}_{slugify(p)[0:30]}" 


# UTILITY: create folder if it doesn't exist yet
def createFolder(path):
    pathlib.Path(path.strip('/')).mkdir(parents=True, exist_ok=True) 

# UTILITY: image resize, to ensure it is always a multiple of 64
def resizeImg(image: PIL.Image):
    width, height = image.size
    new_width = round(width/64)*64
    new_height = round(height/64)*64
    return image.resize((new_width, new_height))

# UTILITY: saving files
# required, otherwise len(images)
def isList(l):
    return isinstance(l, list) and not isinstance(l, str)

def saveJson(j: FvsionModel):
    with open(f"{j.out_image.path}/{j.out_image.name}.json", "w") as f:
        f.write(json.dumps(jsonable_encoder(j)))

def saveImage(fv: FvsionModel, image):
    fpname = f"{fv.out_image.path}/{fv.out_image.name}.{fv.out_image.type}" 
    image.save(fpname)

def saveOutput(fv: FvsionModel, path_to_outputs, image):
    if(isList(fv.prompt)):
        # if image is multiprompts and thus a list, save files individually & in grid as well
        for idx in range(len(image)):
            fv.out_image.name = filenameUnique(fv.prompt[idx])
            fv.out_image.path = f"{path_to_outputs.strip('/')}"
            fv.out_image.type = "webp" #smaller than png

            saveImage(fv, image[idx])        
            if(fv.doJSON):
                saveJson(fv)
        # save the grid as well
        grid = image_grid(image)
        print("built grid")
        # save grid using last prompts name 
        grid.save(f"{fv.out_image.path}/{fv.out_image.name}_grid.{fv.out_image.type}")
    else:
        fv.out_image.name = filenameUnique(fv.prompt)
        fv.out_image.path = f"{path_to_outputs.strip('/')}"
        fv.out_image.type = "webp" #smaller than png

        saveImage(fv, image[0])        
        if(fv.doJSON):
            saveJson(fv)

def save(fv: FvsionModel, images: PIL.Image):
    # UTILITY: saving the file to a unique name, if fails, try one more time, which will generate a new secret
    try:
        # print(fv) # diagnostic
        saveOutput(fv=fv, path_to_outputs=fv.path_to_outputs, image=images)
        print(f"successfully saved {len(images)} files")
    except:
        try:
            saveOutput(fv=fv, path_to_outputs=fv.path_to_outputs, image=images)
            print(f"successfully saved {len(images)} files")
        except Exception as e:
            print(e)


# enable/disable safety (NSFW) checker
def dummy(images, **kwargs):
    return images, False


def maskProcessing(fv: FvsionModel):
    init_image_pfname = f"{fv.init_image.path}/{fv.init_image.name}.{fv.init_image.type}"
    init_image = PIL.Image.open(init_image_pfname) 

    if(fv.mask_image_type == MaskImageEnum.default):
        print('using mask_image (separate file) as mask')
        mask_image_pfname = f"{fv.mask_image.path}/{fv.mask_image.name}.{fv.mask_image.type}"
        mask_image = PIL.Image.open(mask_image_pfname).convert("RGB") 

    elif(fv.mask_image_type == MaskImageEnum.alpha):
        print('using alpha channel from init_image as mask')
        # first take out alpha channel
        mask_image = init_image.convert('RGBA').split()[-1]
        # has to invert via RGB mode to get Alpha area to be white
        mask_image = PIL.ImageOps.invert(mask_image.convert('RGB'))

    elif(fv.mask_image_type == MaskImageEnum.white):
        print('using white from init_image as mask')
        mask_image = init_image.convert("RGBA")
        # create a dummy image as black background
        black = PIL.Image.new("RGBA", mask_image.size, "BLACK")
        # paste our partially transparent image on top
        black.paste(mask_image, (0, 0), mask_image)
        mask_image = black.convert("RGB")

    elif(fv.mask_image_type == MaskImageEnum.color):
        print(f'using specific color ({fv.mask_color}) from init_image as mask')
        mask_image = init_image.convert("RGBA")

        # create a dummy image as black background, to handle alpha scenario
        black = PIL.Image.new("RGBA", mask_image.size, "BLACK")
        # paste our partially transparent image on top
        black.paste(mask_image, (0, 0), mask_image)
        mask_image = black.convert("RGB")
    # else:
    #     TODO, maybe use another technique such as custom color?
    
    # ensure width and height a multiple of 64 and same as per init_image
    init_image = resizeImg(init_image)
    mask_image = mask_image.resize(init_image.size)
    # mask_image.save(f'output/example/diagnostic_mask_{fv.mask_image_type}.png') # for diagnostic
    return(mask_image.convert("RGB"))

def initProcessing(fv: FvsionModel):
    init_image_pfname = f"{fv.init_image.path}/{fv.init_image.name}.{fv.init_image.type}"
    print(f'set {init_image_pfname} as init_image')
    init_image = PIL.Image.open(init_image_pfname).convert("RGBA")
    # create a dummy image as black background
    white = PIL.Image.new("RGBA", init_image.size, "WHITE")
    # paste our partially transparent image on top
    white.paste(init_image, (0, 0), init_image)
    # ensure width and height a multiple of 8
    white = resizeImg(white)
    # white.save(f'output/example/diagnostic_init_{fv.mask_image_type}.png') # for diagnostic
    return(white.convert("RGB"))

# handling multi-prompt

# def breakpoints(n):
#     if n == 1:
#         return (1,1)
#     if n >1 and n <= 4:
#         return (2,2)

def breakpointsSQRT(n: int):
    num = ceil(sqrt(n))
    return (num, num)
     
def image_grid(imgs):
    # assign number of columns based on square root, e.g. 2 to 4 image will have grid 2x2, then 3x3 etc
    rows, cols = breakpointsSQRT(len(imgs))

    w, h = imgs[0].size
    grid = PIL.Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

# TODO INCOMPLETE
def RGBColorReplacement(img, orig_color, replacement_color ):
    # orig_color = (255,255,255)
    # replacement_color = (0,0,0)
    data = np.array(img)
    # data[(data == orig_color).all(axis = -1)] = replacement_color
    # data[(data >= (100,100,100) and data<= (120,120,120)).all(axis = -1)] = replacement_color
    mask = np.logical_and((data >= (100,100,100)).all(axis = -1), (data >= (200,200,200)).all(axis = -1))
    data[mask] = replacement_color
    # data[np.where(data == orig_color)] = replacement_color
    img2 = PIL.Image.fromarray(data, mode='RGB')
    img2.show()
