from PyQt5.QtWidgets import QDialog, QMessageBox

from ..ui.ui_atlas import Ui_Dialog


class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        # setup ui
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.paper_sizes = {
            'A4': [210, 297],
            'A3': [297, 410],
        }

        # user cancelled calculation of atlas panes, exit and do nothing
        self.abandon = True

        # size of pane on paper [mm]
        self.size = [0, 0]

        # size of pane on ground [m]
        self.ground_size = [0, 0]

        # signals
        self.ui.pushButton_ok.clicked.connect(self.accepted)
        self.ui.pushButton_cancel.clicked.connect(self.aborted)

    def accepted(self):
        """ calculate size of atlas pane selected bu user"""
        self.abandon = False
        if self.read_size_from_dialog():
            if self.calculate_size_on_ground():
                self.abandon = False
                self.hide()

    def aborted(self):
        """hide and die"""
        self.hide()

    def read_size_from_dialog(self):
        """take size of atlas pane from user choice"""

        if self.ui.radioButton_a3.isChecked():
            self.size = self.paper_sizes['A3']
        elif self.ui.radioButton_a4.isChecked():
            self.size = self.paper_sizes['A4']
        if self.ui.radioButton_other.isChecked():
            size = self.decode_other_value(self.ui.lineEdit_other.text())
            if not size:
                self.show_warning('Someting goes wrong, check your size!')
                return False
            self.size = size

        # chech if user wants horizontal mode
        if not self.ui.radioButton_other.isChecked():
            if self.size[0] in [x[0] for x in self.paper_sizes.values()] \
                    and self.ui.radioButton_horizontal.isChecked():
                self.size = self.size[::-1]

        return True

    def calculate_size_on_ground(self):
        """ Calculate size of pane in field
        return True or False
        """

        # take 15 mm from every side of pane to maintain overlapping area
        # between panes (readers can easily locate their ROI)
        scale = self.ui.spinBox_scale.value()
        self.ground_size = [
            (((self.size[0]-30)/10)*int(scale))/100,
            (((self.size[1]-30)/10)*int(scale))/100,
        ]

        # size should be greater than one meter
        if min(self.ground_size) < 1:
            self.show_warning(
                'Size of pane on ground shoul be greater than one meter'
            )
            self.ground_size = [0, 0]
            return False

        return True

    def decode_other_value(self, val):
        """ uncode string to 2 int values
        'intxint' -> [int, int] or False
        """
        if 'x' not in val:
            self.show_warning('there should be x betwen values')
        elif ' ' in val:
            self.show_warning('there shouldn\'t be <space> here')
        elif '\t' in val:
            self.show_warning('there shouldn\'t be <TAB> here')
        elif '.' in val or ',' in val:
            self.show_warning('Only integers values are respected')
        else:
            tab = val.split('x')
            if len(tab) != 2:
                self.show_warning('There should be only one x!')
            elif tab[0].isdigit() and tab[1].isdigit():
                return [int(tab[0]), int(tab[1])]

        return False

    def show_warning(self, text):
        """Show warning to user if something is wrong"""
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('Błąd')
        message.setText(text)
        message.addButton("Close", QMessageBox.ActionRole)
        message.exec_()
