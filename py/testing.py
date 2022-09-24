# Object models import
from app.models.fvsion import FvsionModel, MaskImageEnum, FileModel
from app.endpoints.modules import utils

# Utility imports
import PIL.Image, PIL.ImageOps


img = PIL.Image.open('output/example/color_spectrum.png').convert("RGB")
utils.RGBColorReplacement(img, (255,255,255), (0, 0, 0))
