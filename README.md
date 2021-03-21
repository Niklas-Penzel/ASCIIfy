# ASCIIfy
A simple script to ASCIIfy images using the python image library.

## Examples
Input
![alt text](examples/starry_night.jpg)

ASCIIfied
![alt text](examples/ascii_starry_night.jpg)

## Installation
* pip:
```
pip3 install -r requirements.txt
```
* conda:
```
conda env create -f environment.yml
```

## Usage
```
python ASCIIfy.py -h
```
```
usage: ASCIIfy.py [-h] [--font FONT] [--fontsize FONTSIZE] 
                  [--boldness BOLDNESS] [--resize RESIZE] in_path out_path

A script that can be used to asciify one image or multiple images.

positional arguments:
  in_path              Path to the raw data. Can be a single image or a 
                       directory containing multiple images.
  out_path             Path to where you want to save the converted image(s).

optional arguments:
  -h, --help           show this help message and exit
  --font FONT          Path to font file, USE MONO!
  --fontsize FONTSIZE  Which font size should be used?
  --boldness BOLDNESS  How bold should the letters be? Increase, if the image is too dark.
  --resize RESIZE      By how much should the image be resized before asciifying it. 
                       If -1 it will choose a resize corresponding to the fontsize so 
                       that the resulting image has approximately the same dimensions
                       as the input.
```