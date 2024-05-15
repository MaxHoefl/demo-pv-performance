import glob
import json
import os
import random
from typing import List

import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from cube_generator import generate_cube

app = FastAPI()

CUBE_ROOT_DIR = os.environ.get("CUBE_ROOT_DIR", "resources/")


class CubeShape(BaseModel):
    x: int
    y: int
    z: int


def load_cube_shape(id: str) -> CubeShape:
    meta_path = os.path.join(CUBE_ROOT_DIR, f"cube_{id}.json")
    with open(meta_path, "r") as f:
        return CubeShape(**json.load(f))


def load_cube(id: str) -> np.ndarray:
    cube_shape = load_cube_shape(id)
    cube_path = os.path.join(CUBE_ROOT_DIR, f"cube_{id}.bin")
    cube_data = np.fromfile(cube_path, dtype=np.float64)
    cube_array = cube_data.reshape((cube_shape.x, cube_shape.y, cube_shape.z))
    return cube_array


@app.get("/cubes")
def get_cube_ids() -> List[str]:
    paths = glob.glob(os.path.join(CUBE_ROOT_DIR, "*.bin"))
    return [os.path.basename(p).replace(".bin", "").replace("cube_", "") for p in paths]


@app.get("/cube/{id}")
async def random_cube_slice(id: str):
    cube_array = load_cube(id)
    x, y, _ = cube_array.shape
    rdm_1 = random.randint(0, x-1)
    rdm_2 = random.randint(0, y-1)
    random_slice = cube_array[rdm_1, rdm_2, :]
    return {"random_slice": random_slice.tolist()}


@app.post("/cube/{id}")
async def create_cube(id: str):
    cube_size = generate_cube(id, CUBE_ROOT_DIR)
    return JSONResponse(content={
        "id": id,
        "size_mb": cube_size
    }, status_code=201)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0")