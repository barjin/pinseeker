#!/usr/bin/python3

import cv2 as cv
import numpy as np
import os, json

# def print(x):
#     __builtins__.print(f"[PYnSeeker] {x}")

"""
    Contrast/brightness parameters for the first phase 
        (basically boosting the contrast of the image).
"""
alpha = 2.5
beta = -2.5*128 + 50

"""
    cv.matchTemplate() threshold for registering a pin.
    Decrease in case of unregistered pins.
    Increase in case of false positives.
"""
threshold = 0.65

"""
    Minimal distance (in pixels in both directions) between two pins.
    Decrease if the pins are close to each other.
"""
distance = 10

with open(0, 'rb') as f:
    img_data = np.asarray(bytearray(f.read()), dtype=np.uint8)

    # print(img_data)
    
    img_color = cv.imdecode(img_data, 1)

    # print(f"Image loaded, size {len(img_data)}")
    # print(f"Map shape: {img_color.shape[:2]}")

    img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
    img_boosted = cv.convertScaleAbs(img_gray, alpha=alpha, beta=beta)

    # print("Phase 1/3 (boosting) finished...")

    # print("Loading pin and matching...")
    pinfile = os.path.dirname(os.path.realpath(__file__)) + "/pin.png"
    template = cv.imread(pinfile,0)
    w, h = template.shape[::-1]


    res = cv.matchTemplate(img_boosted,template,cv.TM_CCOEFF_NORMED)

    # print("Phase 2/3 (lookup) finished...")
    # print("Deduplicating matches...")

    loc = zip(*np.where(res >= threshold)[::-1])

    dedup = []
    for pt in loc:
        if(len([x for x in dedup if abs(x['x'] - pt[0]) < distance and abs(x['y'] - pt[1]) < distance]) == 0):
            dedup.append({'x': int(pt[0]), 'y': int(pt[1])})

    # print("Phase 3/3 (deduplication) finished...")
    # print(f"Found {len(dedup)} unique pins...")

    # print(dedup)

    print(json.dumps({
        "length": len(dedup),
        "points": dedup
    }))