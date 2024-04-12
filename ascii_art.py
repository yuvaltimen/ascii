import sys
import argparse
import math
import numpy as np

from skimage.measure import block_reduce

from PIL import Image


def main(path: str = None, use_alpha: bool = False) -> None:
    img = np.asarray(Image.open(path))
    if use_alpha:
        # Check whether image has alpha channel
        img_alpha = img.shape[-1] == 4
        map_pixels_to_ascii_with_alpha(img) if img_alpha else map_pixels_to_ascii(img)
    else:
        map_pixels_to_ascii(img)


def map_pixels_to_ascii_with_alpha(img: np.array) -> None:
    img_no_alpha = img[:, :, :3]
    alpha_values = img[:, :, 3:]
    print(alpha_values.shape)

    small_img = do_downsample(img_no_alpha)
    small_alpha = do_downsample(alpha_values)

    print("small alphas" + str(small_alpha))

    text = image_to_ascii_alpha(small_img, small_alpha)

    print(text)


def map_pixels_to_ascii(img: np.array) -> np.array:
    small_img = do_downsample(img)
    text = image_to_ascii(small_img)

    print(text)


def do_downsample(img: np.array) -> np.array:
    
    print(img.shape)
    
    downsampled_img_1 = block_reduce(img, block_size=(5, 2, 1), func=np.max)
    print(downsampled_img_1.shape)
    
    downsampled_img_2 = block_reduce(downsampled_img_1, block_size=(2, 2, 1), func=np.mean)
    print(downsampled_img_2.shape)

    return downsampled_img_2


def dist(p: tuple, q: tuple) -> float:
    return math.sqrt(sum([math.pow(p[i] - q[i], 2) for i in range(len(p))]))


def load_cmap(path: str) -> np.array:
    with open(path, "r") as cmap_file:
        lines = cmap_file.readlines()
        lines = [list(line) for line in lines]

    return np.array(lines)


def image_to_ascii_alpha(img: np.array, alphas: np.array) -> str:
    cmap = load_cmap("/Users/yuvaltimen/Coding/ascii-art/ascii/cmap.txt")

    out = ""

    max_dist = dist((255, 255, 255), (0, 0, 0))
    print("max:" + str(max_dist))

    for w in range(img.shape[0]):

        for h in range(img.shape[1]):
            color = img[w][h]
            alph = alphas[w][h]
            # print("color:" + str(color))
            distance = dist(color, (0, 0, 0))
            # print("dist:" + str(distance))
            thresh = int(np.interp((distance - 1) / max_dist, [0, 1], [0, cmap.shape[0] - 1]))
            alph_thresh = int(np.interp(alph, [0, 255], [0, cmap.shape[0] - 1]))
            # print("thresh:" + str(thresh))
            out += cmap[alph_thresh][thresh]

        out += "\n"

    return out


def image_to_ascii(img: np.array) -> str:
    with open("/Users/yuvaltimen/Coding/ascii-art/ascii/cmap.txt", "r") as f:
        cmap = f.read()

    out = ""

    max_dist = dist((255, 255, 255), (0, 0, 0))
    print("max:" + str(max_dist))

    for w in range(img.shape[0]):

        for h in range(img.shape[1]):
            color = img[w][h]

            # print("color:" + str(color))
            distance = dist(color, (0, 0, 0))
            # print("dist:" + str(distance))
            thresh = int(np.interp((distance - 1) / max_dist, [0, 1], [0, len(cmap) - 1]))
            # print("thresh:" + str(thresh))
            out += cmap[thresh]

        out += "\n"

    return out


def validate_args(inputs: dict) -> None:
    print("validating: " + str(inputs))




if __name__ == "__main__":
    description = """
    Usage:
        asciify [-a | --alpha] [-s | --size <height,width>] path
    
    Options:
        -a | --alpha: flag to use alpha values if they exist
        -s | --size: comma-separated integers for output image size (height,width)
    
    Arguments:
        path: absolute path to the image file, supports *.png and *.jpeg
    """

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('path')
    parser.add_argument('-a', '--alpha', action='store_true')
    parser.add_argument('-s', '--size', dest='size', action='store')

    args = vars(parser.parse_args())

    validate_args(args)

    img_path = args['path']  # "/Users/yuvaltimen/Coding/ascii-art/ascii/lego.png"
    output_img_size = (30, 30)
    main(img_path)
