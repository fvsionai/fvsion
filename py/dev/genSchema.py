# For relative imports to work in Python 3.6
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'py'))

from app.models.fvsion import FvsionModel


def saveJson():
    with open(f"src/stores/schema.json", "w") as f:
        f.write(FvsionModel.schema_json(indent=2))


saveJson()