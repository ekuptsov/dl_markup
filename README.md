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

2. Create and setup virtualenv
```
python3 -m venv /path/to/new/virtual/environment
source <venv>/bin/activate
pip install -r requirements.dev.txt
```

3. Install package
```
pip install -e .
```
Now you can run app with
```
dl_markup
```

## Run tests

```
pytest --cov=dl_markup
```

## Check flake8 and pydocstyle

```
flake8 dl_markup
pydocstyle dl_markup
```

## Update localization
```
pylupdate5 dl_markup/*.py -ts dl_markup.ru.ts
lrelease dl_markup.ru.ts
```

## Build a wheel

```
python -m build .
```

This command generate two files in the `dist` directory:
```
dist\
    dl_markup-0.0.1-py3-none-any.whl
    dl_markup-0.0.1.tar.gz
```
