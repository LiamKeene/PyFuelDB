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
        sessionmaker=sessionmaker, edit=options.edit, delete=options.delete
    )
    myapp.show()
    sys.exit(app.exec_())


class FuelTypeDialog(QtGui.QDialog):
    """FuelTypeDialog.

    Qt QDialog that allows the user to add a FuelType object
    to a database.

    """
    def __init__(self, sessionmaker=None, edit=None, delete=None, parent=None):

        QtGui.QDialog.__init__(self, parent)

        self.ui = Ui_FuelTypeDialog()
        self.ui.setupUi(self)

        self.sessionmaker = sessionmaker

        # Connect QDialog signals
        QtCore.QObject.connect(self,
            QtCore.SIGNAL('accepted()'),
            self.accept_fueltype
        )
        QtCore.QObject.connect(self,
            QtCore.SIGNAL('rejected()'),
            self.reject_fueltype
        )

    def accept_fueltype(self):
        """Accept FuelType.

        Called when the QDialog recieves the accepted signal, usually
        from a button on the dialog.

        Creates a bound session object, a new FuelType object
        and saves it.

        """
        session = self.sessionmaker()
        fuel_type = FuelType(
            name=unicode(self.ui.name_line_edit.text()),
            vendor=unicode(self.ui.vendor_line_edit.text()),
            ron=unicode(self.ui.ron_line_edit.text())
        )
        session.add(fuel_type)
        session.commit()

    def reject_fueltype(self):
        """Reject FuelType.

        Called when the QDialog recieves the rejected signal, usually
        from a button on the dialog.

        """
        print 'Rejected FuelType'


if __name__ == '__main__':
    run_dialog()