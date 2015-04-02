# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui

from dialog import BaseDialog, run_dialog
from lib import *
from models import FuelType
from ui_fueltype import Ui_FuelTypeDialog


class FuelTypeDialog(BaseDialog):
    """Qt QDialog that allows the user to add, edit or delete a FuelType.

    """
    object_class = FuelType
    object_name = 'FuelType'

    widget_field_map = {
        'name_line_edit': 'name',
        'vendor_line_edit': 'vendor',
        'ron_line_edit': 'ron',
    }

    def __init__(self, sessionmaker, edit=None, delete=None, parent=None):

        BaseDialog.__init__(
            self, sessionmaker, edit=edit, delete=delete, parent=parent
        )

    def _setup_ui(self):
        """Setup UI.

        """
        self.ui = Ui_FuelTypeDialog()
        self.ui.setupUi(self)


if __name__ == '__main__':
    run_dialog(FuelTypeDialog)