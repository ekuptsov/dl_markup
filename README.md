# Deep Learning Markup Tool

A tool for images markup for deep learning puproses.

MVP:
Color segmentation masks.

Interface model:
1. Line "Input directory" display absolute path to folder with input images. To change it press "Change" button or edit path manually.
2. Line "Output directory" display absolute path to folder where segmentation mask was saved. To change it press "Change" button or edit path manually.
3. User able to switch between 2 instruments: brush and polygon.
    1. Size of brush can be changed by Ctrl+mouse wheel. Size of brush cursor always fits the width of drawing line.
    2. Polygon item places vertecies on image by mouse clicking. If user press on first-placed vertex, tool draw a polygon with marked verticies. Other verticies can be moved in the markup process by holding mouse button.
4. User able to choose markup color on color Palette. Application provides 12 different colors.
5. User press on image name in list on the left and it is loaded on the screen. If canvas have unsaved changes, application suggest save them before switching image.
6. Button "Save" creates the file with a mask in the output directory. File has the same name as original image has.
7. Button "Clear" remove mark objects from image.
8. Buttons "Undo", "Redo" allow user to move back and forth along markup history.

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