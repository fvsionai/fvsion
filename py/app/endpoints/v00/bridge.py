from fastapi import APIRouter
from app.models.fvsion import FvsionModel
from app.endpoints.v00.modules import txt2img, img2img, inpainting
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