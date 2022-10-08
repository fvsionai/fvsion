# Adapted from https://github.com/TencentARC/GFPGAN/blob/master/inference_gfpgan.py (MIT)
import cv2
import numpy as np
import os
import torch
from basicsr.utils import imwrite

# Object models import
from app.models.fvsion import FvsionModel

# import customized GFPGANer
from app.endpoints.v00.modules.external.custom_gfpgan import GFPGANer


def upscaler(fv: FvsionModel):
    # ------------------------ input & output ------------------------
    if fv.init_image.path.endswith('/'):
        fv.init_image.path = fv.init_image.path[:-1]

    fpname = f"{fv.init_image.path}/{fv.init_image.name}.{fv.init_image.type}"
    if os.path.isfile(fpname):
        img_list = [fpname]
    else:
        print("Input is not a file. Please re-check spelling of path, name & type")
    # else:
    #     img_list = sorted(glob.glob(os.path.join(args.input, '*')))

    outputs_dir = fv.out_image.path
    os.makedirs(outputs_dir, exist_ok=True)

    # ------------------------ set up background upsampler ------------------------
    if fv.upscaler.bg == 'realesrgan':
        from basicsr.archs.rrdbnet_arch import RRDBNet
        from realesrgan import RealESRGANer

        if(fv.upscaler.bg_version == "RealESRGAN_x2plus"):
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            model_path = 'models/RealESRGAN/RealESRGAN_x2plus.pth'
            netscale = 2
        
        elif(fv.upscaler.bg_version == "RealESRGAN_x4plus"):
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            model_path = 'models/RealESRGAN/RealESRGAN_x4plus.pth'
            netscale = 4
        
        elif(fv.upscaler.bg_version == "RealESRGAN_x4plus_anime_6B"):
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
            model_path = 'models/RealESRGAN/RealESRGAN_x4plus_anime_6B.pth'
            netscale = 4                      
        
        bg_upsampler = RealESRGANer(
            scale=netscale,
            model_path=model_path,
            model=model,
            tile=400,
            tile_pad=10,
            pre_pad=0,
            half=True)  # need to set False in CPU mode
            
        print(f"set {fv.upscaler.bg}:{fv.upscaler.bg_version} as bg upscaler")
    else:
        bg_upsampler = None

    # ------------------------ set up GFPGAN restorer ------------------------

    if fv.upscaler.face_version == 'gfpgan' :
        arch = 'clean'
        channel_multiplier = 2
        model_name = 'GFPGANv1.4'
        print(f"set {fv.upscaler.face} as main upscaler")
    if fv.upscaler.face_version == 'RestoreFormer' :
        arch = 'RestoreFormer'
        channel_multiplier = 2
        model_name = 'RestoreFormer'
        print(f"set {fv.upscaler.face} as main upscaler")
    else:
        raise ValueError(f'Wrong model selected {fv.upscaler.face}.')

    # determine model paths
    model_path = os.path.join('models/gfpgan', model_name + '.pth')
    if not os.path.isfile(model_path):
        model_path = os.path.join('models/gfpgan/weights', model_name + '.pth')
    if not os.path.isfile(model_path):
        # ask user to run download_models.bat
        print("No models found, please run (double click) fvsion/models/download_models.bat")

    # added filter to suppress UserWarning: The parameter 'pretrained' is deprecated since 0.13 and will be removed in 0.15
    # added filter to suppress UserWarning: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and will be removed in 0.15
    # TODO, this both need to be addressed in gfpgan main library
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=UserWarning)

        restorer = GFPGANer(
            model_path=model_path,
            upscale=fv.upscaler.factor,
            arch=arch,
            channel_multiplier=channel_multiplier,
            bg_upsampler=bg_upsampler)
    
    print("Complete upscaler setup. Attempting to upscale image.")
    # ------------------------ restore ------------------------
    for img_path in img_list:
        # read image
        img_name = os.path.basename(img_path)
        print(f'Processing {img_name} ...')
        basename, ext = os.path.splitext(img_name)
        input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)

        # restore faces and background if necessary
        cropped_faces, restored_faces, restored_img = restorer.enhance(
            input_img,
            has_aligned=fv.upscaler.has_aligned,
            only_center_face=fv.upscaler.only_center_face,
            paste_back=True,
            weight=fv.upscaler.weight)

        # save faces
        for idx, (cropped_face, restored_face) in enumerate(zip(cropped_faces, restored_faces)):
            # save cropped face
            save_crop_path = os.path.join(outputs_dir, 'cropped_faces', f'{basename}_{idx:02d}.png')
            imwrite(cropped_face, save_crop_path)
            # save restored face
            if fv.upscaler.suffix is not None:
                save_face_name = f'{basename}_{idx:02d}_{fv.upscaler.suffix}.png'
            else:
                save_face_name = f'{basename}_{idx:02d}.png'
            save_restore_path = os.path.join(outputs_dir, 'restored_faces', save_face_name)
            imwrite(restored_face, save_restore_path)
            # save comparison image
            cmp_img = np.concatenate((cropped_face, restored_face), axis=1)
            imwrite(cmp_img, os.path.join(outputs_dir, 'cmp', f'{basename}_{idx:02d}.png'))

        # save restored img
        if restored_img is not None:
            if fv.upscaler.type == 'auto':
                extension = ext[1:]
            else:
                extension = fv.upscaler.type

            if fv.upscaler.suffix is not None:
                save_restore_path = os.path.join(outputs_dir, f'{basename}_{fv.upscaler.suffix}.{extension}')
            else:
                save_restore_path = os.path.join(outputs_dir, f'{basename}.{extension}')
            imwrite(restored_img, save_restore_path)

            print(f'Results are in the [{outputs_dir}] folder.')

            fv.out_image.name = fv.out_image.name + "_" + fv.upscaler.suffix
            return fv

