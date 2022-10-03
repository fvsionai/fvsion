import base64
from fileinput import filename
from urllib import request
from fastapi import APIRouter
from app.models.fvsion import FvsionModel, ImageModel
from app.endpoints.v00.modules import txt2img, img2img, inpainting, txt2img_min
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/api/v00",
    tags=["v00"],
    responses={404: {"description": "Not found"}},
)

@router.get("/pid")
# Get the python child of child pid, for kill instructions
async def read_root():
    return {"pid": str(os.getpid())}


@router.post("/txt2img")
async def generateTxt2Img(fv: FvsionModel):
    try:
        newFV = txt2img.wrapper(fv)
        content = jsonable_encoder(newFV)
        print(content)
        return JSONResponse(content=content, status_code=200)
    except:
        # TODO improve error handling
        return JSONResponse(content={"error": "image generation error"}, status_code=500)

# @router.post("/txt2img_min")
# async def generateTxt2ImgMin(fv: FvsionModel):
#     try:
#         newFV = txt2img_min.wrapper(fv)
#         content = jsonable_encoder(newFV)
#         print(content)
#         return JSONResponse(content=content, status_code=200)
#     except:
#         # TODO improve error handling
#         return JSONResponse(content={"error": "image generation error"}, status_code=500)

@router.post("/img2img")
async def generateImg2Img(fv: FvsionModel):
    try:
        newFV = img2img.wrapper(fv)
        content = jsonable_encoder(newFV)
        print(content)
        return JSONResponse(content=content, status_code=200)
    except:
        # TODO improve error handling
        return JSONResponse(content={"error": "image generation error"}, status_code=500)

@router.post("/inpainting")
async def generateInpainting(fv: FvsionModel):
    try:
        newFV = inpainting.wrapper(fv)
        content = jsonable_encoder(newFV)
        print(content)
        return JSONResponse(content=content, status_code=200)
    except:
        # TODO improve error handling
        return JSONResponse(content={"error": "image generation error"}, status_code=500)

@router.get("/fvsionModel")
async def shareFvsionModel():
    return FvsionModel.schema_json(indent=2)

# to allow drawn sketch to download to /outputs/ folder
@router.post("/save-as-base64")
def base64_saver(data: ImageModel):
    fpname = os.path.join(f"{data.draw_image.path}/{data.draw_image.name}.{data.draw_image.type}")
    with open(fpname, "wb") as fh:
        base64_data = data.image.replace('data:image/png;base64,', '')
        fh.write(base64.b64decode(base64_data))
    return { "done": fpname}