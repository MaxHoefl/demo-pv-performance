import json
import numpy

sizes = {
    "mini": {
        "x": 1,
        "y": 1000,
        "z": 40
    },
    "small_40mb": {
        "x": 40,
        "y": 1000,
        "z": 132
    },
    "small": {
        "x": 10,
        "y": 10000,
        "z": 400
    },
    "medium": {
        "x": 100,
        "y": 10000,
        "z": 400
    }
}

def generate_cube(id: str, target_dir):
    x, y, z = sizes[id].values()
    cube = numpy.random.random(size=(x, y, z))
    cube.tofile(f"{target_dir}/cube_{id}.bin")
    with open(f"{target_dir}/cube_{id}.json", "w") as f:
        f.write(json.dumps({"x": x, "y": y, "z": z}))
    return x * y * z * 8 / (1024 * 1024)