# -*- coding: utf-8 -*-
import sys

from optparse import OptionParser

from PyQt4 import QtCore, QtGui

from lib import *
from models import FuelType
from ui_fueltype import Ui_FuelTypeDialog


def run_dialog():
    """Run the dialog.

    Create the QApplication (before modifying sys.argv)
    then parse sys.argv for acceptable command line
    parameters.

    """
    app = QtGui.QApplication(sys.argv)

    # Create an OptionParser
    usage = '%prog [OPTIONS] [FILE...]'
    description = 'Create, Edit or Delete a FuelType.'
    parser = OptionParser(usage=usage, description=description)
    parser.add_option('-e', action='store', type='int', dest='edit',
        metavar='ID', help='Edit an existing fueltype'
    )
    parser.add_option('-d', action='store', type='int', dest='delete',
        metavar='ID', help='Delete an existing fueltype'
    )
    (options, args) = parser.parse_args(sys.argv[1:])

    if not args:
        parser.error('No database file was specified.')

    db_file = args[0]

    if options.edit and options.delete:
        parser.error('Cannot edit and delete at the same time!')

    # Create a database connection
    sessionmaker = get_sessionmaker(get_engine(db_file))
    myapp = FuelTypeDialog(
        sessionmaker, edit=options.edit, delete=options.delete
    )
    myapp.show()
    sys.exit(app.exec_())


class FuelTypeDialog(QtGui.QDialog):
    """FuelTypeDialog.

    Qt QDialog that allows the user to add a FuelType object
    to a database.

    """
    def __init__(self, sessionmaker, edit=None, delete=None, parent=None):

        QtGui.QDialog.__init__(self, parent)

        self.ui = Ui_FuelTypeDialog()
        self.ui.setupUi(self)

        # Create a bound session for the QDialog
        self.session = sessionmaker()

        if edit:
            self.setWindowTitle('Edit FuelType')

            self.fuel_type = self.get_fueltype(edit)
            accept_method = self.update_fueltype

        elif delete:
            self.setWindowTitle('Delete FuelType')

            self.fuel_type = self.get_fueltype(delete)
            accept_method = self.delete_fueltype

        else:
            accept_method = self.add_fueltype

        # Connect QDialog signals
        QtCore.QObject.connect(self,
            QtCore.SIGNAL('accepted()'),
            accept_method
        )
        QtCore.QObject.connect(self,
            QtCore.SIGNAL('rejected()'),
            self.reject_dialog
        )

    def add_fueltype(self):
        """Add FuelType.

        Create a new FuelType object and save it.

        """
        fuel_type = FuelType(
            name=unicode(self.ui.name_line_edit.text()),
            vendor=unicode(self.ui.vendor_line_edit.text()),
            ron=unicode(self.ui.ron_line_edit.text())
        )
        self.session.add(fuel_type)
        self.session.commit()

    def delete_fueltype(self):
        """Delete FuelType.

        Delete the FuelType from the database.

        """
        self.session.delete(self.fuel_type)
        self.session.commit()

    def get_fueltype(self, id):
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

    def update_fueltype(self):
        """Update FuelType.

        Update the FuelType with values from the QDialog's widgets.

        TODO: Only update fields that have been modified.

        """
        self.fuel_type.name = unicode(self.ui.name_line_edit.text())
        self.fuel_type.vendor = vendor=unicode(self.ui.vendor_line_edit.text())
        self.fuel_type.ron=unicode(self.ui.ron_line_edit.text())
        self.session.commit()

    def reject_dialog(self):
        """Reject Dialog.

        Called when the QDialog recieves the rejected signal, usually
        from a button on the dialog.

        """
        print 'Rejected changes'


if __name__ == '__main__':
    run_dialog()