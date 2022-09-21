from fastapi import APIRouter
from app.models.fvsion import FvsionModel
from app.endpoints.modules import txt2img


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
    txt2img.wrapper(fv)
    return {"done": "done"}


@router.get("/fvsionModel")
async def shareFvsionModel():
    return FvsionModel.schema_json(indent=2)