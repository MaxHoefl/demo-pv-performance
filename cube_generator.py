import json
import numpy

sizes = {
    "mini": {
        "x": 1,
        "y": 1000,
        "z": 40
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

id = "mini"
x, y, z = sizes[id].values()
cube = numpy.random.random(size=(x, y, z))
cube.tofile(f"resources/cube_{id}.bin")
with open(f"resources/cube_{id}.json", "w") as f:
    f.write(json.dumps({"x": x, "y": y, "z": z}))

print(f'File Size in MegaBytes is {x * y * z * 8 / (1024 * 1024)}')