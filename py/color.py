# Object models import
from app.models.fvsion import FvsionModel, MaskImageEnum, FileModel


# Utility imports
import PIL.Image, PIL.ImageOps

initImage = FileModel(path='output/example', name='ori_bwa_512', type='png')
maskImage = FileModel(path='output/example', name='bw_512', type='png')

fv = FvsionModel(prompt="test", init_image=initImage, mask_image=maskImage)

for idx, mask_image_type in enumerate([MaskImageEnum.default, MaskImageEnum.alpha, MaskImageEnum.white ]):
    try:
        init_image_pfname = f"{fv.init_image.path}/{fv.init_image.name}.{fv.init_image.type}"
        print(f'set {init_image_pfname} as init_image')
        init_image = PIL.Image.open(init_image_pfname) 

        if(mask_image_type == MaskImageEnum.default):
            mask_image_pfname = f"{fv.mask_image.path}/{fv.mask_image.name}.{fv.mask_image.type}"
            mask_image = PIL.Image.open(mask_image_pfname) 
        else:
            
            if(mask_image_type == MaskImageEnum.alpha):
                print('using alpha channel from init_image as mask')
                # first take out alpha channel
                mask_image = init_image.convert('RGBA').split()[-1]
                # has to invert via RGB mode to get Alpha area to be white
                mask_image = PIL.ImageOps.invert(mask_image.convert('RGB'))
            elif(mask_image_type == MaskImageEnum.white):
                print('using white from init_image as mask')
                mask_image = init_image.convert("RGBA")
                # create a dummy image as black background
                black = PIL.Image.new("RGBA", mask_image.size, "BLACK")
                # paste our partially transparent image on top
                black.paste(mask_image, (0, 0), mask_image)
                mask_image = black.convert("RGB")
            # else:
            #     print('using black from init_image as mask')

        mask_image.save(f'output/example/{idx}_{mask_image_type}.png')
    except Exception as e:
        print(e)