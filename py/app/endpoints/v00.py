from fastapi import APIRouter
from app.models.fvsion import FvsionModel
from app.endpoints.modules import txt2img, img2img
from fastapi.responses import JSONResponse


#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/api/v00",
    tags=["v00"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root():
    return [{"id": 1}, {"id": 2}]

# @router.post("/txt2img/")
# async def create_item(gen_config: GenModel):
#     return {"done": "done"}


@router.post("/txt2img/")
async def generateT2I(fv: FvsionModel):
    try:
        jsonReturned = txt2img.wrapper(fv)
        return JSONResponse(content=jsonReturned, status_code=200)
    except:
        # TODO improve error handling
        return JSONResponse(content={"error": "image generation error"}, status_code=500)


@router.post("/img2img/")
async def generateT2I(fv: FvsionModel):
    try:
        jsonReturned = img2img.wrapper(fv)
        return JSONResponse(content=jsonReturned, status_code=200)
    except:
        # TODO improve error handling
        return JSONResponse(content={"error": "image generation error"}, status_code=500)


@router.get("/fvsionModel")
async def shareFvsionModel():
    return FvsionModel.schema_json(indent=2)