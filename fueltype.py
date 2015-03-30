# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui

from dialog import BaseDialog, run_dialog
from lib import *
from models import FuelType
from ui_fueltype import Ui_FuelTypeDialog


class FuelTypeDialog(BaseDialog):
    """FuelTypeDialog.

    Qt QDialog that allows the user to add, edit or delete a FuelType.

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
        """Create FuelType.

        Create a new FuelType object and save it.

        """
        kwargs = {}
        for widget, field in self.widget_field_map.items():
            kwargs[field] = self._get_widget_value(widget)

        fueltype = FuelType(**kwargs)

        self.session.add(fueltype)

        self.session.commit()

    def delete_object(self):
        """Delete FuelType.

        Delete the FuelType from the database.

        """
        self.session.delete(self.fueltype)

        self.session.commit()

    def get_object(self, id):
        """Get FuelType.

        Query the database using the given FuelType id, and populate
        the QDialog's widgets.

        """
        fueltype = self.session.query(FuelType).get(id)

        if not fueltype:
            raise Exception('FuelType %s was not found!' % (id, ))

        return fueltype

    def update_object(self):
        """Update FuelType.

        Update the FuelType with values from the QDialog's widgets.

        #TODO Only update fields that have been modified.

        """
        for widget, field in self.widget_field_map.items():
            value = self._get_widget_value(widget)
            self._set_field_value(field, value)

        self.session.commit()


if __name__ == '__main__':
    run_dialog(FuelTypeDialog)