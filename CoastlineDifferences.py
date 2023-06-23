# Import needed libraries
import csv
from PIL import Image
import math

# Creates or clears files for each image
for i in range(3):
    for j in range(2):
        data_file = f'Image{i}{j}.csv'
        with open(data_file, 'w') as f:
            writer = csv.writer(f)
            header = 'Distance', ''
            writer.writerow(header)

# Iterates through each image
for i in range(3):
    for j in range(2):
        # Opens the image and gets the dimensions
        img = Image.open(f'{i}{j}.png')
        print(f'{i}{j}.png')
        width, height = img.size
        print(width, height)

        # These lists contain the coordinates of coloured pixels
        red_pixels = []
        green_pixels = []
        blue_pixels = []

        # Iterates through each pixel
        for w in range(width):
            for h in range(height):
                # Gets the pixels rgb colours using its x and y location
                pixel = img.getpixel((w, h))

                # Saves the rgb values of the pixel into separate variables
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                # Adds the pixels coordinates to the corresponding list
                if red == 255:
                    red_pixels.append([w,h])
                if green == 255:
                    green_pixels.append([w,h])
                if blue == 255:
                    blue_pixels.append([w,h])

        # This will check if it's the first image therefore only containing red and green pixels
        if j == 0:
            # These variables are used to check how many times each situation happened e.g. vertical line,
            # horizotal line and sloped line
            n_gradient = 0
            n_x = 0
            n_y = 0

            # This is the list which will hold the distances between the coastlines
            distance = []

            n_pix = 0

            # Iterates through each red pixel
            for k in range(len(red_pixels)):
                pixel_pair = []
                pix_x, pix_y = red_pixels[k]

                # Contains the location of each surrounding pixel
                surrounding_pixels = [
                    [pix_x, (pix_y + 1)],
                    [(pix_x + 1), (pix_y + 1)],
                    [(pix_x + 1), pix_y],
                    [(pix_x + 1), (pix_y - 1)],
                    [pix_x, (pix_y - 1)],
                    [(pix_x - 1), (pix_y - 1)],
                    [(pix_x - 1), pix_y],
                    [(pix_x - 1), (pix_y + 1)]
                ]

                # Iterates through the surrounding pixels
                for l in range(len(surrounding_pixels)):
                    x = surrounding_pixels[l][0]
                    y = surrounding_pixels[l][1]
                    if x < width and y < height:
                        pixel = img.getpixel((x, y))

                        # Saves the pixel location if a surrounding pixel is red
                        if pixel[0] == 255:
                            pixel_pair.append([x, y])

                # Checks to see if there are two surrounding pixels
                if len(pixel_pair) == 2:
                    temp_distance = 0
                    check_length = 10

                    # Calculates the change in y between the surrounding pixels
                    change_y = (pixel_pair[1][1] - pixel_pair[0][1])

                    # Calculates the change in x between the surrounding pixels
                    change_x = (pixel_pair[1][0] - pixel_pair[0][0])

                    # If the change in y is 0 the line is horizontal therefore the perpendicular line is vertical
                    # This will work out the distance between the red and green pixel vertically
                    if change_y == 0:

                        # Gets the x position of the center pixel as this will remain constant
                        x = pix_x

                        for m in range(check_length):
                            y = pix_y + m
                            if y < height:
                                if img.getpixel((x, y))[1] == 255:
                                    temp_distance = y - pix_y
                                    n_y += 1
                                    m = check_length + 1
                        for n in range(check_length):
                            y = pix_y - n
                            if y >= 0:
                                if img.getpixel((x, y))[1] == 255:
                                    if temp_distance != 0:
                                        if n < temp_distance:
                                            temp_distance = y - pix_y
                                    else:
                                        temp_distance = y - pix_y
                                    n_y += 1
                                    n = check_length + 1

                    # If the change in x is 0 the line is vertical therefore the perpendicular line is horizontal
                    # This will work out the distance between the red and green pixel horizontally
                    elif change_x == 0:

                        # Gets the y position of the center pixel as this will remain consatnt
                        y = pix_y
                        for m in range(check_length):
                            x = pix_x + m
                            if x < width:
                                if img.getpixel((x, y))[1] == 255:
                                    temp_distance = m
                                    n_x += 1
                                    break
                        for n in range(check_length):
                            x = pix_x - n
                            if x >= 0:
                                if img.getpixel((x, y))[1] == 255:
                                    if temp_distance != 0:
                                        if n < temp_distance:
                                            temp_distance = x - pix_x
                                    else:
                                        temp_distance = x - pix_x
                                    n_x += 1
                                    break

                    # If the change in x and y is not 0 the line is sloped
                    # This will work out the distance between the red and green pixel using pythagorus
                    else:
                        gradient = change_y / change_x
                        gradient = -1 / gradient

                        c = pix_y - gradient * pix_x
                        for m in range(check_length):
                            x = int(pix_x + m)
                            y = int(gradient * x + c)
                            if x < width and y < height and y >= 0:
                                pixel = img.getpixel((x, y))
                                if pixel[1] == 255:
                                    temp_distance = math.sqrt((change_x * change_x) + (change_y * change_y))
                                    n_gradient += 1
                                    break
                        for n in range(check_length):
                            x = int(pix_x - n)
                            y = int(gradient * x + c)
                            if x < width and x >= 0 and y < height and y >= 0:
                                pixel = img.getpixel((x, y))
                                if pixel[1] == 255:
                                    if temp_distance != 0:
                                        if n < temp_distance:
                                            temp_distance = math.sqrt((change_x * change_x) + (change_y * change_y))
                                    else:
                                        temp_distance = math.sqrt((change_x * change_x) + (change_y * change_y))
                                    n_gradient += 1
                                    break
                    # This adds the distance between pixels to a list
                    if temp_distance != 0:
                        n_pix += 1
                        distance.append(temp_distance)

            # This adds the distances between the red and green pixels to its corresponding file
            file = open(f'Image{i}{j}.csv', 'a')
            for p in range(len(distance)):
                file.write(f'{str(distance[p])}\n')

        # This will check if it's the second image therefore only containing green and blue pixels
        if j == 1:

            # These variables are used to check how many times each situation happened e.g. vertical line,
            # horizotal line and sloped line
            n_gradient = 0
            n_x = 0
            n_y = 0

            # This is the list which will hold the distances between the coastlines
            distance = []

            n_pix = 0

            # Iterates through each green pixel
            for k in range(len(green_pixels)):
                pixel_pair = []
                pix_x, pix_y = green_pixels[k]

                # Contains the location of each surrounding pixel
                surrounding_pixels = [
                    [pix_x, (pix_y + 1)],
                    [(pix_x + 1), (pix_y + 1)],
                    [(pix_x + 1), pix_y],
                    [(pix_x + 1), (pix_y - 1)],
                    [pix_x, (pix_y - 1)],
                    [(pix_x - 1), (pix_y - 1)],
                    [(pix_x - 1), pix_y],
                    [(pix_x - 1), (pix_y + 1)]
                ]

                # Iterates through each surrounding pixel to see if it is green
                for l in range(len(surrounding_pixels)):
                    x = surrounding_pixels[l][0]
                    y = surrounding_pixels[l][1]
                    if x < width and y < height:
                        pixel = img.getpixel((x, y))

                        # Saves the pixel location if a surrounding pixel is green
                        if pixel[1] == 255:
                            pixel_pair.append([x, y])

                # Checks to see if there are two surrounding pixels
                if len(pixel_pair) == 2:
                    temp_distance = 0
                    check_length = 10

                    # Calculates the change in y between the surrounding pixels
                    change_y = (pixel_pair[1][1] - pixel_pair[0][1])

                    # Calculates the change in x between the surrounding pixels
                    change_x = (pixel_pair[1][0] - pixel_pair[0][0])

                    # If the change in y is 0 the line is horizontal therefore the perpendicular line is vertical
                    # This will work out the distance between the green and blue pixel vertically
                    if change_y == 0:

                        # Gets the x position of the center pixel as this will remain constant
                        x = pix_x

                        for m in range(check_length):
                            y = pix_y + m
                            if y < height:
                                if img.getpixel((x, y))[2] == 255:
                                    temp_distance = y - pix_y
                                    n_y += 1
                                    m = check_length + 1
                        for n in range(check_length):
                            y = pix_y - n
                            if y >= 0:
                                if img.getpixel((x, y))[2] == 255:
                                    if temp_distance != 0:
                                        if n < temp_distance:
                                            temp_distance = y - pix_y
                                    else:
                                        temp_distance = y - pix_y
                                    n_y += 1
                                    n = check_length + 1

                    # If the change in x is 0 the line is vertical therefore the perpendicular line is horizontal
                    # This will work out the distance between the green and blue pixel horizontally
                    elif change_x == 0:

                        # Gets the y position of the center pixel as this will remain constant
                        y = pix_y
                        for m in range(check_length):
                            x = pix_x + m
                            if x < width:
                                if img.getpixel((x, y))[2] == 255:
                                    temp_distance = m
                                    n_x += 1
                                    break
                        for n in range(check_length):
                            x = pix_x - n
                            if x >= 0:
                                if img.getpixel((x, y))[2] == 255:
                                    if temp_distance != 0:
                                        if n < temp_distance:
                                            temp_distance = x - pix_x
                                    else:
                                        temp_distance = x - pix_x
                                    n_x += 1
                                    break

                    # If the change in x and y is not 0 the line is sloped
                    # This will work out the distance between the green and blue pixel using pythagorus
                    else:
                        gradient = change_y / change_x
                        gradient = -1 / gradient

                        c = pix_y - gradient * pix_x
                        for m in range(check_length):
                            x = int(pix_x + m)
                            y = int(gradient * x + c)
                            if x < width and y < height and y >= 0:
                                pixel = img.getpixel((x, y))
                                if pixel[2] == 255:
                                    temp_distance = math.sqrt((change_x * change_x) + (change_y * change_y))
                                    n_gradient += 1
                                    break
                        for n in range(check_length):
                            x = int(pix_x - n)
                            y = int(gradient * x + c)
                            if x < width and x >= 0 and y < height and y >= 0:
                                pixel = img.getpixel((x, y))
                                if pixel[2] == 255:
                                    if temp_distance != 0:
                                        if n < temp_distance:
                                            temp_distance = math.sqrt((change_x * change_x) + (change_y * change_y))
                                    else:
                                        temp_distance = math.sqrt((change_x * change_x) + (change_y * change_y))
                                    n_gradient += 1
                                    break
                    # This adds the distance between pixels to a list
                    if temp_distance != 0:
                        n_pix += 1
                        distance.append(temp_distance)

            # This adds the distances between the green and blue pixels to its corresponding file
            file = open(f'Image{i}{j}.csv', 'a')
            for p in range(len(distance)):
                file.write(f'{str(distance[p])}\n')
