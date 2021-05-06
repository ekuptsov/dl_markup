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

1. Download, install and setup [Git LFS](https://git-lfs.github.com/)

2. Setup virtualenv
```
./scripts/setup/dev.sh
source venv/bin/activate
```

3. install package
```
pip install -e .
```
Now you can run app with
```
dl_markup
```

## Update localization

1. Go to the root

2. `pylupdate5 dl_markup/*.py -ts dl_markup.ru.ts`

3. `lrelease dl_markup.ru.ts`

## Run tests

`pytest .`