# Object models import
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
    timestr = time.strftime("%Y%m%d_%H%M%S")
    secstr = secrets.token_hex(8)
    return timestr+"_"+secstr

def filenameUnique(p):
    # prompt cut in front to avoid too long prompt text, os path limit 
    # return file-name-from-prompt-cut (i.e. no path or extension)
    return f"{prefix()}_{slugify(p)[0:30]}" 


# UTILITY: create folder if it doesn't exist yet
def createFolder(path):
    pathlib.Path(path.strip('/')).mkdir(parents=True, exist_ok=True) 

def saveJson(j: FvsionModel):
    with open(f"{j.out_image.path}/{j.out_image.name}.json", "w") as f:
        f.write(json.dumps(jsonable_encoder(j)))

def saveImage(fv: FvsionModel, image):
    fpname = f"{fv.out_image.path}/{fv.out_image.name}.{fv.out_image.type}" 
    image.save(fpname)

def saveOutput(fv: FvsionModel, pathToOutput, image):
    fv.out_image.name = filenameUnique(fv.prompt)
    fv.out_image.path = f"{pathToOutput.strip('/')}"
    fv.out_image.type = "png"

    saveImage(fv, image)        
    if(fv.doJSON):
        saveJson(fv)

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
    #     print('using black from init_image as mask')

    mask_image.save(f'output/example/diagnostic_mask_{fv.mask_image_type}.png')
    return(mask_image.convert("RGB"))

def initProcessing(fv: FvsionModel):
        init_image_pfname = f"{fv.init_image.path}/{fv.init_image.name}.{fv.init_image.type}"
        print(f'set {init_image_pfname} as init_image')
        init_image = PIL.Image.open(init_image_pfname).convert("RGBA")
        # create a dummy image as black background
        white = PIL.Image.new("RGBA", init_image.size, "WHITE")
        # paste our partially transparent image on top
        white.paste(init_image, (0, 0), init_image)
        white.save(f'output/example/diagnostic_init_{fv.mask_image_type}.png')
        return(white.convert("RGB"))


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