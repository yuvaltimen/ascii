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
    
    
    downsampled_img = block_reduce(img, block_size=(13, 5, 1), func=np.max)
    print(img.shape)
    print(downsampled_img.shape)
    
    # plt.imshow(downsampled_img)
    # plt.show()
    
    return downsampled_img

def dist(p: tuple, q: tuple) -> float:
    return math.sqrt(sum([math.pow(p[i] - q[i], 2) for i in range(len(p))]))
    
def image_to_ascii(img: np.array) -> str:
    
    cmap = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/()1{}[]?-_+~<>i!lI;:,"^`'."""
    
    out = ""
    
    max_dist = dist((255, 255, 255), (0, 0, 0))
    print("max:" + str(max_dist))

    for w in range(img.shape[0]):
        
        for h in range(img.shape[1]):
            color = img[w][h]
            print("color:" + str(color))
            distance = dist(color, (0, 0, 0))
            print("dist:" + str(distance))
            thresh = int(np.interp((distance - 1) / max_dist, [0, 1], [0, len(cmap)]))
            print("thresh:" + str(thresh))
            out += cmap[thresh]
                
        out += "\n"
        
    return out



if __name__ == "__main__":
    main("/Users/yuvaltimen/Coding/ascii_art/emoji.png")
    
