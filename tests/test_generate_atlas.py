import os
import pytest
from qgis.testing import start_app

from qgis.core import QgsVectorLayer
from qgis.utils import iface

from ..engine.gener import Generate

start_app()


@pytest.fixture
def layer():
    dir_path = os.path.dirname(__file__)

    lwrite = QgsVectorLayer(
        os.path.join(dir_path, '..', 'tests_data', "layer.shp"), 'layer', 'ogr'
    )

    return lwrite


def test_layer_mapunit_are_not_meters():
    lyr = QgsVectorLayer(
        'Polygon?crs=epsg:4326&field=name:string(20)',
        'test',
        'memory')
    gg = Generate(False)
    gg.SHOW_WARNINGS = False
    gg.lyr = lyr
    assert gg.check_crs_in_meters() is False


def test_layer_mapunit_are_meters():
    lyr = QgsVectorLayer(
        'Polygon?crs=epsg:2180&field=name:string(20)',
        'test',
        'memory')

    gg = Generate(False)
    gg.SHOW_WARNINGS = False
    gg.lyr = lyr
    assert gg.check_crs_in_meters()


def test_add_reference_layer(layer):
    lyr = layer

    gg = Generate(iface)
    gg.SHOW_WARNINGS = False
    assert lyr.featureCount() == 2
    assert len([x for x in lyr.getFeatures()]) == 2
    assert gg.choose_reference_layer(lyr)


def test_generated_atlas_layer(layer):
    lyr = layer

    gg = Generate(iface)
    gg.gsize = [2300, 2300]
    gg.SHOW_WARNINGS = False
    gg.choose_reference_layer(lyr)
    gg.create_atlas_layer()
    gg.save_layers()

    assert sorted(gg.atlas.dataProvider().fieldNameMap().keys()) == \
        sorted(['SITE', 'Up', 'Down', 'Left', 'Right', 'ISSUES'])
    assert gg.lyr.sourceCrs() == gg.atlas.sourceCrs()
    assert os.path.dirname(
        gg.lyr.dataProvider().dataSourceUri().split('|')[0]
    ) == \
        os.path.dirname(
            gg.atlasF.dataProvider().dataSourceUri().split('|')[0]
        )


def test_generate_A4_pane(layer):
    lyr = layer

    gg = Generate(iface)
    gg.gsize = [2300, 2300]
    gg.SHOW_WARNINGS = False
    gg.choose_reference_layer(lyr)
    gg.create_atlas_layer()

    feat = gg.generate_pane(500000, 200000)

    assert feat.geometry().boundingBox().xMinimum() == 500000
    assert feat.geometry().boundingBox().xMaximum() == 502300
    assert feat.geometry().boundingBox().yMaximum() == 202300
    assert feat.geometry().boundingBox().yMinimum() == 200000


def test_atlas_generation_only_intersects_panes(layer):
    lyr = layer

    gg = Generate(iface)
    gg.SHOW_WARNINGS = False
    gg.inter_only = True
    gg.gsize = [850, 1340]  # A4
    gg.choose_reference_layer(lyr)
    gg.create_atlas_layer()

    gg.generate_panes()

    assert gg.atlas.featureCount() == 25


def test_atlas_generation_all_panes(layer):
    lyr = layer

    gg = Generate(iface)
    gg.SHOW_WARNINGS = False
    gg.inter_only = False
    gg.gsize = [850, 1340]  # A4
    gg.choose_reference_layer(lyr)
    gg.create_atlas_layer()

    gg.generate_panes()

    assert gg.atlas.featureCount() == 66
