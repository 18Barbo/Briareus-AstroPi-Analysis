# Import libraries necessary for the code
import cv2
from PIL import Image
import numpy as np

# Applies a canny filter to 'image'
def cannyFilter(image, threshold1, threshold2):
    # Read the image
    image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv2.Canny(image, threshold1, threshold2)

    return edges

# Changes white pixels to the respective colours
def colourImage(image, output, colour, index):
    # Get the dimensions of the image
    height, width = image.shape

    # Create a new RGB image with the same dimensions
    imageBGR = np.zeros((height, width, 3), dtype=np.uint8)

    # Iterate through each pixel in the black and white image
    for i in range(height):
        for j in range(width):
            # Check if the pixel is white (255)
            if image[i, j] == 255:
                # Set the corresponding pixel in the RGB image to the specified color
                imageBGR[i, j] = colour[str(2 - index)]

    # Save the resulting RGB image
    cv2.imwrite(output, imageBGR)

# Combines the images
def combineImages(image1, image2, output, colour, i):
    # Open the images
    image1 = Image.open(image1)
    image2 = Image.open(image2)

    # Get the image sizes
    width, height = image1.size

    # Create a new blank image
    new_image = Image.new("RGB", (width, height), color=0)

    # Iterate over each pixel position
    for y in range(height):
        for x in range(width):

            # Adds the correct pixel values to the new Image
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))


            if pixel2 != (0, 0, 0):
                new_image.putpixel((x, y), pixel2)

            if pixel1 != (0, 0, 0):
                new_image.putpixel((x, y), pixel1)



    # Save the combined image
    new_image.save(output)

# Sets up a function called 'main' where all the code runs
def main():
    # For loop to repeat all the code 10 times
    for r in range(10):
        # Sets thresholds for the function 'cannyFilter'
        threshold1 = 0
        threshold2 = 0

        # Saves images to the variables 'image', 'imageA', 'imageB'
        image = f"images/{r + 1}.png"
        imageA = f"images/a{r + 1}.png"
        imageB = f"images/b{r + 1}.png"

        funcList = {'0': cannyFilter(image, threshold1, threshold2),
                    '1': cannyFilter(imageA, threshold1, threshold2),
                    '2': cannyFilter(imageB, threshold1, threshold2)}

        colourList = {'0': (255, 0, 0),
                      '1': (0, 255, 0),
                      '2': (0, 0, 255),}
        pathList = []

        # Iterates over the 3 images
        for i in range(3):

            output = f'images/temp/{i}.png'
            
            # Creates an outline and then apllies colour
            lineImage = funcList[str(i)]
            colourImage(lineImage, output, colourList, i)
           
            pathList.append(output)

        print(pathList)

        print(pathList)

        for i in range(2):

            output = f'images/final/{r}{i}.png'
            combineImages(pathList[i], pathList[i+1], output, colourList, i)

if __name__ == '__main__':
    main()
