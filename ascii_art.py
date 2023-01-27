import math
import numpy as np

import matplotlib.pyplot as plt
from skimage.measure import block_reduce
from PIL import Image

def main(path: str = None) -> None:
    
    image = np.asarray(Image.open(path))
    
    img_no_alpha = image[:, :, :3]
    
    small_img = do_downsample(img_no_alpha)
    
    text = image_to_ascii(small_img)
    
    print(text)
    
    
    
def do_downsample(img: np.array) -> np.array:
    
    
    downsampled_img = block_reduce(img, block_size=(19, 19, 1), func=np.max)
    print(img.shape)
    print(downsampled_img.shape)
    
    # plt.imshow(downsampled_img)
    # plt.show()
    
    return downsampled_img
    
def image_to_ascii(img: np.array) -> str:
    
    EMPTY = "."
    LIGHT = "+"
    DARK = "#"
    
    
    
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
    
            color = img[x][y]
            print(color)
        
    return "hit ascii"



if __name__ == "__main__":
    main("/Users/yuvaltimen/Coding/ascii_art/emoji.png")
    
