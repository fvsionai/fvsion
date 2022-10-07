from app.endpoints.v00.modules.external import upscaler_gfpgan 
from app.models.fvsion import FvsionModel

def wrapper(fv: FvsionModel):
    if(fv.upscaler.face == "gfpgan"):
        return upscaler_gfpgan.upscaler(fv)
    else:
        raise ValueError(f"Wrong upscaler model selected: {fv.upscaler.face}. Default option is 'gfpgan'")