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

    def create_object(self):
        """Create a new FuelType object using values from the QDialog's widgets.

        Adds it to the bound SQLAlchemy session and calls `QDialog.accept`.

        """
        kwargs = {}
        for widget, field in self.widget_field_map.items():
            kwargs[field] = self._get_widget_value(widget)

        fueltype = FuelType(**kwargs)

        self.session.add(fueltype)

        self.session.commit()

        self.accept()

    def delete_object(self):
        """Delete the FuelType from the database.

        Get user to confirm deletion then call `QDialog.accept`.

        """
        ret = QtGui.QMessageBox.warning(
            self, 'Delete FuelType?',
            'Do you really want to delete this FuelType?\n%s' % self.fueltype,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        )
        if ret == QtGui.QMessageBox.Yes:
            self.session.delete(self.fueltype)

            self.session.commit()

            self.accept()


    def get_object(self, id):
        """Query the database using the given id and return the matching
        FuelType.

        """
        fueltype = self.session.query(FuelType).get(id)

        if not fueltype:
            raise Exception('FuelType %s was not found!' % (id, ))

        return fueltype

    def update_object(self):
        """Update the FuelType object using values from the QDialog's widgets
        and call `QDialog.accept`.

        #TODO Only update fields that have been modified.

        """
        for widget, field in self.widget_field_map.items():
            value = self._get_widget_value(widget)
            self._set_field_value(field, value)

        self.session.commit()

        self.accept()


if __name__ == '__main__':
    run_dialog(FuelTypeDialog)