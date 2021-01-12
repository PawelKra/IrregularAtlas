# Irregular Atlas

QGIS plugin that create atlas panes in user specified scale and size for selected layer. Gives posibility for easy numerate sites by line and get neighbours sites in columns.


![Alt text](/atlas_steps.png?raw_true)

## Instalation

Place this repo in python plugin directory of QGIS


## How to

Select one layer from TOC, click on genreate panes on Irregular Atlas toolbar.
There will be generated 2 layers:
* **ATLAS_AFT** Which is saved in catalog with selected origin layer (if there exists layer at that name, it will be overriten)
* **LineAtlas** Memory layer for line to numerate panes. There should be only one line in this layer with equal number of vertices to tiles. Every verticle should be placed in way that it could select only one atlas tile


After enumeration of atlas You can see labeled tiles and small numbers shows discovered neighbours panes around every tile.


## Tests

If You want to run tests You need pytest and pytest-qt. Tests area placed in testes directory
