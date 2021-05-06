import cv2
import numpy as np
import os
from tqdm import tqdm
from PIL import Image, ImageFont, ImageDraw
import argparse
from multiprocessing import Pool, get_context
import multiprocessing as mp

def get_font_dim(font):
    """
    expects an ImageFont and returns the width and height of a single symbol.
    """
    # create a tmp image
    _img = Image.fromarray(np.zeros((500, 500, 3), dtype=np.uint8))
    _ed = ImageDraw.Draw(_img)

    # get the pixel dims corresponding to the selected font
    width, height = _ed.textsize(".", font=font)
    width_, height_ = _ed.textsize("M", font=font)
    
    #assert width == width_ # check if mono
    #assert height == height_ # check if mono
    return width, height


def convert_intensity_to_symbol(pixel_val):
    """
    takes an intensity and returns a suitable char.
    """
    # invert the intensity
    pixel_val = 255 - pixel_val

    # list of possible chars ordered roughly by numbers of pixels
    char_list = [(".", "'", "´", ","), (":", ";", '"', "-", "~", "_"), ("<", ">", "+", "*", "i", "/", "\\", "(", ")"),
                 ("o", "a", "e", "5", "p", "d", "A"), ("&", "%", "#", "§", "8", "ß", "@")]

    # convert the intensity to an char
    if(pixel_val < 10):
        return " "
    else:
        idx = pixel_val//(int((255-10)/len(char_list)))
        if idx > len(char_list) - 1:
            idx = len(char_list) - 1
        return np.random.choice(char_list[idx])


def ASCIIfy(img, resize, font_path, font_size, stroke_width, verbose=1):
    """
    expects a numpy array encoding an image and returns 
    an PIL image containing an asciified version
    """
    # load the font
    font = ImageFont.truetype(font_path, font_size)
    # get the dimensions of a single symbol
    symbol_width, symbol_height = get_font_dim(font)
    # calc stretching factor
    stretch = symbol_height / symbol_width

    # get the dimensions of the input
    height, width, _  = img.shape

    # if resize = -1 it depends on the symbol size
    if resize == -1:
        new_width = width // symbol_width
        new_height = height // symbol_height
    else:
        new_width = int((width // resize) * stretch)
        new_height = height // resize

    # resize the input
    img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    # get a gray scale version of the input
    img_resized_gray = np.mean(img_resized, axis=2, dtype=np.uint8)

    # create the array that corresponds to the ascii image
    ascii_img = np.zeros((img_resized.shape[0]*symbol_height, img_resized.shape[1]*symbol_width, 3), dtype=np.uint8)

    # create the corresponding PILLOW objects
    pil_ascii_img = Image.fromarray(ascii_img, 'RGB')
    editable_ascii_img = ImageDraw.Draw(pil_ascii_img)

    # iterate over the pixels
    if verbose > 0:
        it = tqdm(np.ndindex(img_resized.shape[:2]), total=img_resized.shape[0]*img_resized.shape[1])
    else:
        it = np.ndindex(img_resized.shape[:2])

    for idx in it:
        # get the color
        color = tuple(img_resized[idx])
        # get the position of the letter in the new image
        anchor = (idx[1]*symbol_width, idx[0]*symbol_height)
        # draw a suitable char
        char = convert_intensity_to_symbol( img_resized_gray[idx] )

        # render the text
        editable_ascii_img.text( anchor, char, fill=color, font=font, stroke_width=stroke_width )

    return pil_ascii_img


def ASCIIfy_(in_path, out_path, resize, font_path, font_size, stroke_width, verbose=1):
    """
    loads the image under in_path and outputs the image with
    the minimun psnr to out_path.
    """
    ASCIIfy(np.array(Image.open(in_path)), resize, font_path, font_size, stroke_width, verbose=verbose).save(out_path)


class ASCIIfier(object):
    """
    Function object to multiprocess the asciification.
    """
    def __init__(self, resize, font_path, font_size, stroke_width, verbose=1):
        self.resize = resize
        self.font_path = font_path
        self.font_size = font_size
        self.stroke_width = stroke_width
        self.verbose = verbose

    def __call__(self, paths):
        in_path, out_path = paths
        ASCIIfy_(in_path, out_path, self.resize, self.font_path, self.font_size, self.stroke_width, verbose=self.verbose)


def parse_args():
    """
    parses the commandline arguments.
    """
    parser = argparse.ArgumentParser(description="A script that can be used to asciify one image or multiple images.")
    parser.add_argument('in_path', type=str, help='Path to the raw data. Can be a single image or a directory containing multiple images.')
    parser.add_argument('out_path', type=str, help='Path to where you want to save the converted image(s).')
    parser.add_argument('--font', default=os.path.join("fonts","MajorMonoDisplay-Regular.ttf"), type=str, help='Path to font file, USE MONO!')
    parser.add_argument('--fontsize', default=10, type=int, help='Which font size should be used?')
    parser.add_argument('--boldness', default=0, type=int, help='How bold should the letters be? Increase, if the image is too dark.')
    parser.add_argument('--resize', default=-1, type=int, help='By how much should the image be resized before asciifying it. If -1 it will choose a resize corresponding to the fontsize so that the resulting image has approximately the same dimensions as the input.')
    parser.add_argument('--n_workers', default=-1, type=int, help='How many processes should be started? If -1 it uses the number of cores.')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    if os.path.isfile(args.in_path):
        ASCIIfy_(args.in_path, args.out_path, args.resize, args.font, args.fontsize, args.boldness)
    else:
        if not os.path.isdir(args.out_path):
            os.makedirs(args.out_path)

        if args.n_workers == 1:
            for f in tqdm(os.listdir(args.in_path)):
                try:
                    ASCIIfy_(os.path.join(args.in_path, f), os.path.join(args.out_path, f), args.resize, args.font, args.fontsize, args.boldness, verbose=0)
                except Exception as e:
                    print(e)
        else:
            asciifier = ASCIIfier(args.resize, args.font, args.fontsize, args.boldness, verbose=0)
            if args.n_workers < 0:
                args.n_workers = mp.cpu_count()

            paths = [(os.path.join(args.in_path, f), os.path.join(args.out_path, f)) for f in os.listdir(args.in_path)]

            print(f"Start multiprocessing with {args.n_workers} workers.")

            with get_context("spawn").Pool(args.n_workers) as p:
                list(tqdm(p.imap(asciifier, paths), total=len(paths)))