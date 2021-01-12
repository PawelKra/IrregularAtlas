import os

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QVariant

from qgis.core import QgsField, QgsVectorLayer, QgsPointXY, QgsGeometry, Qgis,\
    QgsFeature, QgsVectorFileWriter, QgsProject, QgsSpatialIndex, QgsWkbTypes

from .window import Dialog


class Generate:
    # for test purporses
    SHOW_WARNINGS = True

    def __init__(self, iface):
        self.iface = iface
        self.lyr = False  # reference layer to get extent
        self.dir_path = ''  # path to catalog with ref layer

        self.atlas = False  # QgsVectorLayer with atlas
        self.atlasPr = False  # dataProvider
        self.line = False  # QgsVectorLayer with lilne to enumerate panes
        self.linePr = False  # dataProvider

        self.gsize = [0, 0]  # size of pane on the ground withou scale

        self.inter_only = False  # generate only panes that intersect with lyr
        self.si = QgsSpatialIndex()  # spatial index from self.lyr

    def generate(self):
        """Perform all steps and generate layers with atlas"""

        if not self.choose_reference_layer():
            return
        if not self.check_crs_in_meters():
            return

        self.get_data_from_user()
        self.create_atlas_layer()

        self.generate_panes()
        self.save_layers()

    def check_crs_in_meters(self):
        """check if layer source crs is in meters, other way it atlas will
        be generated incorectly"""

        if self.lyr.sourceCrs().mapUnits() != 0:
            self.show_warning(
                'Layer crs map unit is diffret from meters, Aborting'
            )
            return False
        return True

    def get_data_from_user(self):
        """Show dialog to user what size of atlas should be generated"""

        self.dlg = Dialog()
        self.dlg.exec_()

        # get calculated size on ground from dialog
        self.gsize = self.dlg.ground_size
        self. inter_only = self.dlg.ui.checkBox_inter.isChecked()

    def choose_reference_layer(self, lyr=False):
        """ Point to reference layer to get it boundingBox, it should be
        currently selected layer
        there is an option to point to layer - testing
        """

        if lyr is False:
            self.lyr = self.iface.activeLayer()
        else:
            self.lyr = lyr

        if self.lyr in [False, None]:
            self.show_warning('No suitable layer!')
            self.lyr = False
            return False

        # check if layer is valid
        if not self.lyr.isValid():
            self.show_warning('Not valid layer, choose another!')
            self.lyr = False
            return False

        try:
            self.dir_path = os.path.dirname(
                self.lyr.dataProvider().dataSourceUri().split("|")[0])
        except Exception:
            return False

        return True

    def create_atlas_layer(self):
        """Creates atlas layer and save it do disk in catalog with referenced
        layer

        """
        if self.lyr is False:
            return False

        # check what kind of crs is defined in layer
        crs = self.lyr.sourceCrs().authid()
        if 'EPSG:' not in crs:
            crs_txt = ''
        else:
            crs_txt = 'crs=' + crs + '&'

        self.atlas = QgsVectorLayer(
            "Polygon?"+crs_txt+"index=yes", "ATLAS_AFT", "memory"
        )
        self.atlasPr = self.atlas.dataProvider()
        self.atlas.startEditing()
        self.atlasPr.addAttributes([
            QgsField("SITE", QVariant.Int),
            QgsField("Left", QVariant.Int),
            QgsField("Up", QVariant.Int),
            QgsField("Right", QVariant.Int),
            QgsField("Down", QVariant.Int),
            QgsField("ISSUES", QVariant.String, len=50),
            ])
        self.atlas.updateFields()
        self.atlas.commitChanges()

        # Generate line vector layer to easy show order and calculate order
        # from vertex of Line
        self.line = QgsVectorLayer(
            "LineString?"+crs_txt+"&index=yes", "LineAtlas", "memory")
        self.linePr = self.line.dataProvider()

    def generate_si(self):
        """Generate Spatial index from original layer"""
        if self.lyr.geometryType() in [QgsWkbTypes.Polygon,
                                       QgsWkbTypes.PolygonGeometry,
                                       QgsWkbTypes.MultiPolygon]:
            self.si.addFeatures(self.lyr.getFeatures())
        else:
            # if geometry type other than poly, omit spatial index
            self.inter_only = False

    def generate_panes(self):
        """Generate panes of atlas to cover all extent of reference layer
        if layer is Polygon or Multipolygon type it is option to generate
        panes only there panes overlap with references
        """

        # pobierz rozmiary warstwy którą będziemy atlasować
        xmin = self.lyr.extent().xMinimum()
        xmax = self.lyr.extent().xMaximum()
        ymin = self.lyr.extent().yMinimum()
        ymax = self.lyr.extent().yMaximum()

        # generate SpatialIndex only if checkbox in checked and reference layer
        # is at certain type (poly, multipoly)
        if self.inter_only:
            self.generate_si()

        x = xmin
        y = ymin
        panes_poly = []
        ita = 0  # no more than 999 tile in any direction!!!

        while x < xmax and ita < 999:
            while y < ymax and ita < 999:
                f = self.generate_pane(x, y)
                if f is not False:
                    panes_poly.append(f)
                y += self.gsize[1]
                ita += 1

            x += self.gsize[0]
            ita += 1
            y = ymin

        self.atlas.startEditing()
        self.atlas.addFeatures(panes_poly)
        self.atlas.commitChanges()

    def generate_pane(self, x, y):
        """generate one pane of atlas in given x,y position
            if spatialindex is added there will be returning False if pane
            not intersect with SI
        """
        poly = [
            QgsPointXY(x, y),
            QgsPointXY(x, y+self.gsize[1]),
            QgsPointXY(x+self.gsize[0], y+self.gsize[1]),
            QgsPointXY(x+self.gsize[0], y),
            QgsPointXY(x, y),
        ]
        g = QgsGeometry().fromPolygonXY([poly])

        # if SpatialIndex not intersects with generated geometry, return False
        if self.inter_only:
            if len(self.si.intersects(g.boundingBox())) == 0:
                return False

        f = QgsFeature()
        f.setFields(self.atlas.fields())
        f.setGeometry(g)
        return f

    def save_layers(self):
        """Save atlas layer to disk, and add atlas and line vector layer to
        TOC
        """
        crs = self.lyr.sourceCrs()

        QgsVectorFileWriter.writeAsVectorFormat(
            self.atlas,
            os.path.join(os.path.join(self.dir_path, "ATLAS_AFT.shp")),
            "UTF-8",
            crs,
            "ESRI Shapefile")

        self.atlasF = QgsVectorLayer(
            os.path.join(self.dir_path, "ATLAS_AFT.shp"), "ATLAS_AFT", "ogr")

        QgsProject.instance().addMapLayer(self.atlasF)
        QgsProject.instance().addMapLayer(self.line)

        plugin_dir = os.path.dirname(__file__)
        self.atlasF.loadNamedStyle(
            os.path.join(plugin_dir, '..', 'qml', 'ATLAS_AFT_check.qml'))
        self.line.loadNamedStyle(
            os.path.join(plugin_dir, '..', 'qml', 'ATLAS_LINE.qml'))

        self.show_success()

    def show_success(self):
        # show confirmation to user on message bar
        if not self.SHOW_WARNINGS:
            return

        self.iface.messageBar().pushMessage(
                    "OK",
                    'Atlas Panes generated correctly',
                    Qgis.Success,
                    5
        )

    def show_warning(self, text):
        """Show warning to user if something is wrong"""
        if not self.SHOW_WARNINGS:
            return

        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('Błąd')
        message.setText(text)
        message.addButton("Close", QMessageBox.ActionRole)
        message.exec_()
