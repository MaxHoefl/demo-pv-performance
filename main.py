import os
import random
import numpy as np
import uvicorn
from fastapi import FastAPI

app = FastAPI()

cube_path = os.environ.get("CUBE_PATH", "resources/cube.bin")
cube_data = np.fromfile(cube_path, dtype=np.float64)
A, S, T = 10, 10000, 400
cube_array = cube_data.reshape((A, S, T))


@app.get("/cube")
async def read_random_slice():
    # Generate random indices for the slice
    rdm_1 = random.randint(0, A-1)
    rdm_2 = random.randint(0, S-1)

    random_slice = cube_array[rdm_1, rdm_2, :]

    return {"random_slice": random_slice.tolist()}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0")