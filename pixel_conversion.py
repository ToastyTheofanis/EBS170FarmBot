import math
import numpy as np

def pixelConvert(coords):
    results = []
    
    cameraX = 500
    cameraY = 350
    scaleFactor = 0.35
    photoWidth = 1920
    photoHeight = 1080
    thetaCAM = math.radians(3.14)

    for i in range(coords.shape[0]):
        yoloX = coords[i, 0]
        yoloY = coords[i, 1]

        # Rotates the photo to be the same axes as the farmbed
        rotatedX = yoloX * math.cos(thetaCAM) + yoloY * math.sin(thetaCAM)
        rotatedY = -yoloX * math.sin(thetaCAM) + yoloY * math.cos(thetaCAM)

        # Changes origin from top left to the bottom left
        # x position does not flip only y does
        mirroredX = rotatedX
        mirroredY = rotatedY - 2 * (rotatedY - 0.5)

        # Finds the distance from the mushroom to the center of the photo where the gripper should be
        distanceFromCameraPixelsX = mirroredX - 0.443
        distanceFromCameraPixelsY = mirroredY - 0.5
    
        distanceFromCameraMMX = distanceFromCameraPixelsX * scaleFactor * photoWidth
        distanceFromCameraMMY = distanceFromCameraPixelsY * scaleFactor * photoHeight

        absoluteMushroomX = distanceFromCameraMMX + cameraX
        absoluteMushroomY = distanceFromCameraMMY + cameraY

        results.append((absoluteMushroomX, absoluteMushroomY))
    
    results_array = np.array(results)
    
    for result in results_array:
        print(f"Mushroom is located at location ({result[0]}, {result[1]})")

    return results_array

normalized_coords = np.array([
    [0.503346, 0.277321],
    [0.236388, 0.152616],
    [0.446385, 0.504069],
    [0.149752, 0.495847],
    [0.614795, 0.233091],
    [0.602019, 0.755422],
    [0.313624, 0.394774],
    [0.293891, 0.851433],
    [0.480935, 0.954736],
    [0.803946, 0.102615]
])

results_array = pixelConvert(normalized_coords)
print("Results array:\n", results_array)