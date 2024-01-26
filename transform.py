from image import Image
import numpy as np


def adjust_brightness(image, factor):
    # when we brighten, we just want to make each channel higher by some amount
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)

    # x, y pixels and channels(R, G, B) if the image
    x_pixels, y_pixels, num_channels = image.array.shape
    # create a new image so that we don't modify the original image
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                      num_channels=num_channels)

    # this is the non vectorized version
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor

    # adjust brightness (using numpy)
    new_image.array = image.array * factor

    return new_image


def adjust_contrast(image, factor, mid=0.5):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount

    # x, y pixels and channels(R, G, B) if the image
    x_pixels, y_pixels, num_channels = image.array.shape
    # create a new image so that we don't modify the original image
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                      num_channels=num_channels)

    new_image.array = (image.array - mid) * factor + mid

    return new_image


def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an 'odd' number

    # x, y pixels and channels(R, G, B) if the image
    x_pixels, y_pixels, num_channels = image.array.shape
    # create a new image so that we don't modify the original image
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels,
                      num_channels=num_channels)

    # number of neighbors we considered
    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                # prevent out of range
                for i in range(
                    max(0, x - neighbor_range),
                    min(new_image.x_pixels - 1, x + neighbor_range) + 1,
                ):
                    for j in range(
                        max(0, y - neighbor_range),
                        min(new_image.y_pixels - 1, y + neighbor_range) + 1,
                    ):
                        total += image.array[i, j, c]
                    new_image.array[x, y, c] = total / (kernel_size ** 2)
                    
    return new_image


if __name__ == "__main__":
    lake = Image(filename="lake.png")
    city = Image(filename="city.png")

    # brightening
    brightened_im = adjust_brightness(lake, 1.7)
    brightened_im.write_image("brightened.png")

    # darkening
    darkened_im = adjust_brightness(lake, 0.3)
    darkened_im.write_image("darkened.png")

    # increase contrast
    incr_contrast = adjust_contrast(lake, 2, 0.5)
    incr_contrast.write_image("increased_contrast.png")

    # decrease contrast
    decr_contrast = adjust_contrast(lake, 0.5, 0.5)
    decr_contrast.write_image("decreased_contrast.png")
    
    # blur using kernel 3
    blur_3 = blur(city, 3)
    blur_3.write_image('blur_k3.png')

    # blur using kernel size of 15
    blur_15 = blur(city, 15)
    blur_15.write_image('blur_k15.png')
