import glob
import json
import os
import random
from typing import List

import numpy as np
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from cube_generator import generate_cube

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

app = FastAPI()

CUBE_ROOT_DIR = os.environ.get("CUBE_ROOT_DIR", "resources/")


class CubeShape(BaseModel):
    x: int
    y: int
    z: int


def load_cube_shape(name: str) -> CubeShape:
    meta_path = os.path.join(CUBE_ROOT_DIR, f"{name}.json")
    with open(meta_path, "r") as f:
        return CubeShape(**json.load(f))


def load_cube(name: str) -> np.ndarray:
    cube_shape = load_cube_shape(name)
    cube_path = os.path.join(CUBE_ROOT_DIR, f"{name}.bin")
    cube_data = np.fromfile(cube_path, dtype=np.float64)
    cube_array = cube_data.reshape((cube_shape.x, cube_shape.y, cube_shape.z))
    return cube_array


def find_cube_names(name_pattern: str = "*") -> List[str]:
    paths = glob.glob(os.path.join(CUBE_ROOT_DIR, f"{name_pattern}.bin"))
    return [os.path.basename(p).replace(".bin", "") for p in paths]


def get_random_cube_slice(cube_array: np.ndarray) -> np.ndarray:
    x, y, _ = cube_array.shape
    rdm_1 = random.randint(0, min(10, x - 1))
    rdm_2 = random.randint(0, min(10, y - 1))
    random_slice = cube_array[rdm_1, rdm_2, :]
    return random_slice

@app.get("/cubes")
def get_cube_ids(name_pattern: str = "*") -> List[str]:
    return find_cube_names(name_pattern)


@app.get("/cubes/{name}")
async def random_cube_slice(name: str, prefix: bool = False):
    if prefix:
        cube_names = find_cube_names(name + "*")
        if len(cube_names) == 0:
            raise HTTPException(status_code=404, detail=f"No cubes with name prefix {name}")
        for cube_name in cube_names:
            logging.info(f"Loading cube {cube_name}")
            cube_array = load_cube(cube_name)
            get_random_cube_slice(cube_array)
        name = cube_names[0]
    cube_array = load_cube(name)
    random_slice = get_random_cube_slice(cube_array)
    return {"random_slice": random_slice.tolist()}


@app.post("/cubes")
async def create_cube(x: int, y: int, z:int, n: int = None):
    if n is not None:
        generated_chunks = []
        for i in range(n):
            name = f"cube-{x}-{y}-{z}_{i}"
            cube_size = generate_cube(x, y, z, name=name, target_dir=CUBE_ROOT_DIR)
            generated_chunks.append({"name": name, "size_mb": cube_size})
        return JSONResponse(content=generated_chunks, status_code=201)
    name = f"cube-{x}-{y}-{z}"
    cube_size = generate_cube(x, y, z, name=name, target_dir=CUBE_ROOT_DIR)
    return JSONResponse(content={
        "name": name,
        "size_mb": cube_size
    }, status_code=201)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0")