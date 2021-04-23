# Deep Learning Markup Tool

A tool for images markup for deep learning puproses.

MVP:
Binary segmentation masks.

Interface model:
1. Button "Images folder" for input folder selection.
2. Button "Output folder" for output folder selection.
3. One instrument - brush. Size of brush can be changed by buttons / mouse wheel.
4. Image is loading on the screen. The brush draws a green semi-transparent mask over the image.
5. Button "OK" creates the file with a mask in the output directory. File has the same name as original image has.
6. Button "Next" loads the next image.

Optional features:
1. "Eraser" instrument.
2. "Undo" button.
3. Multi-class labelling.

## Setup development environment

1. Setup virtualenv
```
./scripts/setup/dev.sh
source venv/bin/activate
```
2. Download, install and setup [Git LFS](https://git-lfs.github.com/)
