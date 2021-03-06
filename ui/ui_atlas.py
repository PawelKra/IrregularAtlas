# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_atlas.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 340)
        font = QtGui.QFont()
        font.setFamily("Arial")
        Dialog.setFont(font)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.radioButton_a4 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_a4.setGeometry(QtCore.QRect(30, 50, 171, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.radioButton_a4.setFont(font)
        self.radioButton_a4.setChecked(True)
        self.radioButton_a4.setObjectName("radioButton_a4")
        self.radioButton_a3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_a3.setGeometry(QtCore.QRect(30, 80, 181, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.radioButton_a3.setFont(font)
        self.radioButton_a3.setObjectName("radioButton_a3")
        self.radioButton_other = QtWidgets.QRadioButton(Dialog)
        self.radioButton_other.setGeometry(QtCore.QRect(30, 110, 104, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.radioButton_other.setFont(font)
        self.radioButton_other.setObjectName("radioButton_other")
        self.lineEdit_other = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_other.setEnabled(False)
        self.lineEdit_other.setGeometry(QtCore.QRect(140, 110, 101, 32))
        self.lineEdit_other.setObjectName("lineEdit_other")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(250, 120, 41, 18))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(20, 280, 331, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_ok.setFont(font)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(370, 290, 88, 34))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(320, 30, 141, 111))
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.radioButton_portrate = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_portrate.setGeometry(QtCore.QRect(20, 40, 111, 22))
        self.radioButton_portrate.setChecked(True)
        self.radioButton_portrate.setObjectName("radioButton_portrate")
        self.radioButton_horizontal = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_horizontal.setGeometry(QtCore.QRect(20, 70, 111, 22))
        self.radioButton_horizontal.setObjectName("radioButton_horizontal")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 170, 81, 18))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(20, 140, 441, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(20, 200, 441, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(20, 260, 441, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.checkBox_inter = QtWidgets.QCheckBox(Dialog)
        self.checkBox_inter.setGeometry(QtCore.QRect(30, 230, 401, 26))
        self.checkBox_inter.setObjectName("checkBox_inter")
        self.spinBox_scale = QtWidgets.QSpinBox(Dialog)
        self.spinBox_scale.setGeometry(QtCore.QRect(120, 160, 171, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_scale.setFont(font)
        self.spinBox_scale.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_scale.setMaximum(5000000)
        self.spinBox_scale.setProperty("value", 5000)
        self.spinBox_scale.setObjectName("spinBox_scale")

        self.retranslateUi(Dialog)
        self.radioButton_other.toggled['bool'].connect(self.radioButton_portrate.setDisabled)
        self.radioButton_other.toggled['bool'].connect(self.radioButton_horizontal.setDisabled)
        self.radioButton_other.toggled['bool'].connect(self.lineEdit_other.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Atlas options"))
        self.radioButton_a4.setText(_translate("Dialog", "A4   (210x297 mm)"))
        self.radioButton_a3.setText(_translate("Dialog", "A3   (297x420 mm)"))
        self.radioButton_other.setText(_translate("Dialog", "other:"))
        self.lineEdit_other.setText(_translate("Dialog", "900x900"))
        self.label_2.setText(_translate("Dialog", "mm"))
        self.label_4.setText(_translate("Dialog", "Paper size:"))
        self.pushButton_ok.setText(_translate("Dialog", "Generate"))
        self.pushButton_cancel.setText(_translate("Dialog", "Cancel"))
        self.groupBox.setTitle(_translate("Dialog", "Orientation"))
        self.radioButton_portrate.setText(_translate("Dialog", "Portrait"))
        self.radioButton_horizontal.setText(_translate("Dialog", "Horizontal"))
        self.label.setText(_translate("Dialog", "Scale  1:"))
        self.checkBox_inter.setText(_translate("Dialog", "panes only intersecting with layer features (polygons)"))
