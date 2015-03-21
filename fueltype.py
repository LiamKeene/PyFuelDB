# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore, QtGui

from lib import *
from models import FuelType
from ui_fueltype import Ui_FuelTypeDialog


class FuelTypeDialog(QtGui.QDialog):
    """FuelTypeDialog.

    Qt QDialog that allows the user to add a FuelType object
    to a database.

    """
    def __init__(self, parent=None, sessionmaker=None):

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
    # Create a database connection
    sessionmaker = get_sessionmaker(get_engine(sys.argv[1]))

    app = QtGui.QApplication(sys.argv)
    myapp = FuelTypeDialog(sessionmaker=sessionmaker)
    myapp.show()
    sys.exit(app.exec_())