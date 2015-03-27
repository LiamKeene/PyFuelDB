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
        fuel_type = FuelType(
            name=unicode(self.ui.name_line_edit.text()),
            vendor=unicode(self.ui.vendor_line_edit.text()),
            ron=unicode(self.ui.ron_line_edit.text())
        )
        self.session.add(fuel_type)
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
        fuel_type = self.session.query(FuelType).get(id)

        if not fuel_type:
            raise Exception('FuelType %s was not found!' % (id, ))

        self.ui.name_line_edit.setText(fuel_type.name)
        self.ui.vendor_line_edit.setText(fuel_type.vendor)
        self.ui.ron_line_edit.setText(fuel_type.ron)

        return fuel_type

    def update_object(self):
        """Update FuelType.

        Update the FuelType with values from the QDialog's widgets.

        #TODO Only update fields that have been modified.

        """
        self.fueltype.name = unicode(self.ui.name_line_edit.text())
        self.fueltype.vendor = vendor=unicode(self.ui.vendor_line_edit.text())
        self.fueltype.ron=unicode(self.ui.ron_line_edit.text())
        self.session.commit()

    def reject_dialog(self):
        """Reject Dialog.

        Called when the QDialog recieves the rejected signal, usually
        from a button on the dialog.

        """
        print 'Rejected changes'


if __name__ == '__main__':
    run_dialog(FuelTypeDialog)