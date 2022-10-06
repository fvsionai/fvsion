import base64
from fastapi import APIRouter
from app.models.fvsion import FvsionModel, ImageModel
from app.endpoints.v00.modules import diffusers_pipe, lowvram
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os

#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/api/v00",
    tags=["v00"],
    responses={404: {"description": "Not found"}},
)


@router.post("/pipe")
async def generate_pipe(fv: FvsionModel):
    try:
        newFV = diffusers_pipe.wrapper(fv)
        content = jsonable_encoder(newFV)        
        return JSONResponse(content=content, status_code=200)
    except Exception as e:
        # TODO improve error handling
        print(e)
        return JSONResponse(content={"error": "image generation error", "message": str(e)}, status_code=500)


@router.post("/lowvram")
async def generate_pipe(fv: FvsionModel):
    try:
        newFV = lowvram.wrapper(fv)
        content = jsonable_encoder(newFV)        
        return JSONResponse(content=content, status_code=200)
    except Exception as e:
        # TODO improve error handling
        print(e)
        return JSONResponse(content={"error": "image generation error", "message": str(e)}, status_code=500)

# utilities
# get PID, use to check system is online
@router.get("/pid")
# Get the python child of child pid, for kill instructions
async def read_root():
    return {"pid": str(os.getpid())}

# get the fvsion model as json schema
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