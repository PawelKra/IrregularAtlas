import os
import pytest
from qgis.testing import start_app

from qgis.core import QgsVectorLayer, QgsProject
from qgis.utils import iface

from ..engine.enum import EnumerateAtlas
from ..engine.gener import Generate

start_app()


@pytest.fixture
def add_ready_layer():
    QgsProject.instance().removeAllMapLayers()
    dir_path = os.path.dirname(__file__)

    atlas = QgsVectorLayer(
        os.path.join(dir_path, '..', 'tests_data', "ATLAS_AFT.shp"),
        'ATLAS_AFT', 'ogr'
    )
    line = QgsVectorLayer(
        os.path.join(dir_path, '..', 'tests_data', "line_ok.shp"),
        'LineAtlas', 'ogr'
    )
    QgsProject.instance().addMapLayer(atlas)
    QgsProject.instance().addMapLayer(line)


@pytest.fixture
def gen_all_atlas():
    QgsProject.instance().removeAllMapLayers()
    dir_path = os.path.dirname(__file__)
    lyr = QgsVectorLayer(
        os.path.join(dir_path, '..', 'tests_data', "layer.shp"),
        'layer', 'ogr'
    )
    gg = Generate(iface)
    gg.SHOW_WARNINGS = False
    gg.inter_only = False
    gg.gsize = [900, 1334]  # A4
    gg.choose_reference_layer(lyr)
    gg.create_atlas_layer()

    gg.generate_panes()
    gg.save_layers()
    return lyr


@pytest.fixture
def gen_intersect_atlas():
    QgsProject.instance().removeAllMapLayers()
    dir_path = os.path.dirname(__file__)
    lyr = QgsVectorLayer(
        os.path.join(dir_path, '..', 'tests_data', "layer.shp"),
        'layer', 'ogr'
    )
    gg = Generate(iface)
    gg.SHOW_WARNINGS = False
    gg.inter_only = True
    gg.gsize = [900, 1334]  # A4
    gg.choose_reference_layer(lyr)
    gg.create_atlas_layer()

    gg.generate_panes()
    gg.save_layers()
    return lyr


# WARNING! Test order does matter!!!
# They generate layers to test_data dir

def test_finding_layers_in_all_atlas(gen_all_atlas):
    en = EnumerateAtlas(iface)
    en.SHOW_WARNINGS = False

    assert en.find_layers()


def test_finding_layers_in_inter_atlas(gen_intersect_atlas):
    en = EnumerateAtlas(iface)
    en.SHOW_WARNINGS = False

    assert en.find_layers()


def test_finding_ready_layers(add_ready_layer):
    en = EnumerateAtlas(iface)
    en.SHOW_WARNINGS = False

    assert en.find_layers()


def test_proper_vertices_placement(add_ready_layer):
    en = EnumerateAtlas(iface)
    en.SHOW_WARNINGS = False

    en.find_layers()
    assert en.check_proper_vertices_placement()


def test_enumerate_atlas(add_ready_layer):
    en = EnumerateAtlas(iface)
    en.SHOW_WARNINGS = False

    en.find_layers()
    en.check_proper_vertices_placement()

    en.enumerate_sites()

    # check if values were written do neighbours panes
    left = {x['Left'] for x in en.atlas.getFeatures()}
    right = {x['Right'] for x in en.atlas.getFeatures()}
    up = {x['Up'] for x in en.atlas.getFeatures()}
    down = {x['Down'] for x in en.atlas.getFeatures()}

    assert len(right) > 4
    assert len(left) > 4
    assert len(right) > 4
    assert len(up) > 4
    assert len(down) > 4
    assert en.num_sites == 25
