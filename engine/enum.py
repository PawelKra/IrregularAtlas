from qgis.core import Qgis, QgsProject


class EnumerateAtlas:
    SHOW_WARNINGS = True

    def __init__(self, iface):
        self.iface = iface

        self.atlas = False  # atlas vector layer
        self.line = False  # line vector layer

        self.line_dict = {}  # dict with ordered point from line
        self.atlas_cent = {}  # dict centroids {atlas_pane_id: PointXY()}
        self.atlas_order = {}  # dict {feature_atlas.id(): site_number}

        self.num_sites = 0  # count of numerated sites

    def paginate(self):
        """ perform all steps to enumerate atlas.
        find, check and process
        """

        # find needed layers
        if not self.find_layers():
            return

        # check if user do the right job
        if not self.check_layers() or \
                not self.check_proper_vertices_placement():
            return

        # enumerate atlas tiles
        self.enumerate_sites()

    def find_layers(self):
        """check if ATLAS and AtlasLine layer is TOC"""
        lyrs = [x for x in QgsProject.instance().mapLayers().values()]
        if len(lyrs) == 0:
            self.show_meesage('critical', "ERROR", 'No Layers in TOC')
            return False

        atlas = [x for x in lyrs if x.name()[:9].upper() == 'ATLAS_AFT']
        line = [x for x in lyrs if x.name()[:9] == 'LineAtlas']

        if len(atlas) != 1 or len(line) != 1:
            self.show_meesage(
                'critical', "ERROR", 'Missing ATLAS_AFT and/or LineAtlas'
            )
            return False

        self.atlas = atlas[0]
        self.line = line[0]
        return True

    def check_layers(self):
        """ check linestring vector layer if there is only one line in it,
        and it has the same number of vertices that there is panes in atlas
        layer
        """

        # there should be only one feature in line layer
        if self.line.featureCount() != 1:
            self.show_meesage(
                'critical',
                'ERROR',
                'There should be only one line in Line Vector Layer!'
            )
            return False

        # number of vertices in line feature == count of atlas tiles
        line = [x for x in (self.line.getFeatures())][0]
        if self.atlas.featureCount() != len(line.geometry().asPolyline()):
            self.show_meesage(
                'critical',
                'ERROR',
                'Number of vertices in line should be equal to '
                'atlas tiles count '
                '   Panes count: '+str(self.atlas.featureCount()) +
                ', Line vertices: ' + str(len(self.line_dict))
            )
            return False

        # check if we have all the columns
        fnm = self.atlas.dataProvider().fieldNameMap()
        oblig = ['SITE', 'Up', 'Left', 'Down', 'Right', ]
        flds = [x for x in fnm.keys() if x in oblig]
        if len(flds) != len(oblig):
            self.show_meesage(
                'critical',
                'ERROR',
                'ATLAS_AFT is lack of columns: ['
                ','.join([x for x in oblig if x not in flds]) + ']',
            )
            return False

        return True

    def process_line(self):
        """ convert line to dict
        {id: QgsPoint(), }
        """
        line = [x for x in self.line.getFeatures()][0]
        if line.geometry().wkbType() == 5:  # MultiLineString
            self.line_dict = {
                i+1: val for i, val in
                enumerate([y for y in line.geometry().asMultiPolyline()][0])
            }
        if line.geometry().wkbType() == 2:  # LineString
            self.line_dict = {i+1: val for i, val in
                              enumerate(line.geometry().asPolyline())}

    def check_proper_vertices_placement(self):
        """check if vertices will select only one tile of atlas, if not
        return False
        """
        self.process_line()
        for feat in self.atlas.getFeatures():
            bbox = feat.geometry().boundingBox()
            num = [x for x, pnt in self.line_dict.items()
                   if bbox.xMinimum() < pnt.x() < bbox.xMaximum() and
                   bbox.yMinimum() < pnt.y() < bbox.yMaximum()]

            self.atlas_cent[feat.id()] = [
                feat.geometry().centroid().boundingBox().xMinimum(),
                feat.geometry().centroid().boundingBox().yMinimum(),
            ]

            if len(num) != 1:
                if len(num) > 1:
                    text = 'with more than one vertices'
                else:
                    text = 'with no vertices'

                self.show_meesage(
                    'critical', "ERROR", 'Check vertices, found tile '+text
                )
                return False
            self.atlas_order[feat.id()] = num[0]

        if len(self.atlas_order) == len(self.line_dict):
            return True

        return False

    def enumerate_sites(self):
        """enumerate tiles of atlas in order of line verices and add neigbours
        tiles to apropriate columns
        """
        fnm = self.atlas.dataProvider().fieldNameMap()
        for i, feat in enumerate(self.atlas.getFeatures()):
            bbox = feat.geometry().boundingBox()
            width = bbox.width() / 2
            height = bbox.height() / 2

            val = {fnm['SITE']: str(self.atlas_order[feat.id()])}

            # check if there is another tile on left, if there is add it
            # to column to show it on edge of atlas site
            L = [x for x, point in self.atlas_cent.items()
                 if bbox.xMinimum()-width-50 < point[0] <
                 bbox.xMinimum()+width-1
                 and
                 bbox.yMinimum()-height+50 < point[1] <
                 bbox.yMaximum()+height-50
                 and feat.id() != x
                 ]
            val[fnm['Left']] = str('0')
            if len(L) > 0:
                val[fnm['Left']] = str(self.atlas_order[L[0]])

            # check if there is another tile on up, if there is add it
            # to column to show it on edge of atlas site
            U = [x for x, point in self.atlas_cent.items()
                 if bbox.xMinimum()-width/3 < point[0] <
                 bbox.xMaximum()+width/3
                 and
                 bbox.yMaximum()-height/3 < point[1] <
                 bbox.yMaximum()+height+50
                 and feat.id() != x
                 ]
            val[fnm['Up']] = str('0')
            if len(U) > 0:
                val[fnm['Up']] = str(self.atlas_order[U[0]])

            # check if there is another tile on rigth, if there is add it
            # to column to show it on edge of atlas site
            R = [x for x, point in self.atlas_cent.items()
                 if bbox.xMaximum()-width+50 < point[0] <
                 bbox.xMaximum()+width+50
                 and
                 bbox.yMinimum()-height+50 < point[1] <
                 bbox.yMaximum()+height-50
                 and feat.id() != x
                 ]
            val[fnm['Right']] = str('0')
            if len(R) > 0:
                val[fnm['Right']] = str(self.atlas_order[R[0]])

            # check if there is another tile on down, if there is add it
            # to column to show it on edge of atlas site
            D = [x for x, point in self.atlas_cent.items()
                 if bbox.xMinimum()-width/3 < point[0] <
                 bbox.xMaximum()+width/3
                 and
                 bbox.yMinimum()-height-50 < point[1] <
                 bbox.yMinimum()+height/3
                 and feat.id() != x
                 ]
            val[fnm['Down']] = str('0')
            if len(D) > 0:
                val[fnm['Down']] = str(self.atlas_order[D[0]])

            self.atlas.dataProvider().changeAttributeValues({feat.id(): val})
            self.num_sites += 1

        self.show_meesage('success', 'OK',
                          'Total processed sites: ' + str(self.num_sites)
                          )

    def show_meesage(self, t, title, mess):
        """Show message bat with specified type, title ans message on it
        t - type of message ('success', 'error', warning')
        title, mess  -> str
        """
        # omit for testing
        if not self.SHOW_WARNINGS:
            return

        mess_type = Qgis.Success
        if t == 'error':
            mess_type = Qgis.Critical
        elif t == 'warning':
            mess_type = Qgis.Warning

        self.iface.messageBar().pushMessage(title, mess, mess_type, 10)
