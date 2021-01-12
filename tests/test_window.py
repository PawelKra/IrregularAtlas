import pytest
from pytestqt import qtbot  # noqa

from ..engine.window import Dialog


def test_check_option_A3(qtbot):
    win = Dialog()
    qtbot.addWidget(win)

    win.ui.radioButton_a3.click()
    win.read_size_from_dialog()

    assert win.size == [297, 410]


def test_check_option_A3_horizontal(qtbot):
    win = Dialog()
    qtbot.addWidget(win)

    win.ui.radioButton_a3.click()
    win.ui.radioButton_horizontal.click()
    win.read_size_from_dialog()

    assert win.size == [410, 297]


def test_check_option_other(qtbot):
    win = Dialog()
    qtbot.addWidget(win)

    win.ui.radioButton_other.click()
    win.ui.lineEdit_other.setText('900x900')

    win.read_size_from_dialog()
    assert win.size == [900, 900]


def test_scale_change(qtbot):
    win = Dialog()
    qtbot.addWidget(win)

    win.ui.spinBox_scale.setValue(9000)

    assert win.ui.spinBox_scale.value() == 9000


def test_size_on_ground_900x900_5000(qtbot):
    win = Dialog()
    qtbot.addWidget(win)

    win.ui.radioButton_other.click()
    win.ui.lineEdit_other.setText('900x900')
    win.read_size_from_dialog()

    assert win.calculate_size_on_ground()
    assert win.ground_size == [4350, 4350]
