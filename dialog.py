# -*- coding: utf-8 -*-
import sys

from optparse import IndentedHelpFormatter, OptionParser

from PyQt4 import QtCore, QtGui

from lib import *


class RawIndentedHelpFormatter(IndentedHelpFormatter):
    """RawIndentedHelpFormatter.

    Overrides IndentedHelpFormatter to return help elements without any special
    formatting, textwrap, etc.

    """
    def format_epilog(self, epilog):
        """format_epilog.

        Return the epilog without formatting.

        """
        return '\n%s\n' % (epilog, )


def run_dialog(klass):
    """Run the dialog.

    Create the QApplication (before modifying sys.argv)
    then parse sys.argv for acceptable command line
    parameters.

    """
    app = QtGui.QApplication(sys.argv)

    # Create an OptionParser
    usage = '%prog [OPTIONS] [FILE...]'
    description = 'Create, Edit or Delete a %s.' % (klass.object_name, )
    epilog = """Examples:

  Create a new %(object_name)s in the given SQLite database

    python %(prog_name)s.py pyfueldb.db

  Edit an existing %(object_name)s in the given SQLite database

    python %(prog_name)s.py -e 1 pyfueldb.db

  Delete an existing %(object_name)s from the given SQLite database

    python %(prog_name)s.py -d 1 pyfueldb.db

  The SQLite database file should be specified otherwise changes
  will not be recorded.
    """ % {
            'object_name': klass.object_name.lower(),
            'prog_name': sys.argv[0],
        }

    parser = OptionParser(
        usage=usage, description=description, epilog=epilog,
        formatter=RawIndentedHelpFormatter()
    )
    parser.add_option('-e', action='store', type='int', dest='edit',
        metavar='ID', help='Edit an existing %s' % (klass.object_name.lower(), )
    )
    parser.add_option('-d', action='store', type='int', dest='delete',
        metavar='ID', help='Delete an existing %s' % (klass.object_name.lower(), )
    )
    (options, args) = parser.parse_args(sys.argv[1:])

    if not args:
        parser.error('No database file was specified.')

    db_file = args[0]

    if options.edit and options.delete:
        parser.error('Cannot edit and delete at the same time!')

    # Create a database connection
    sessionmaker = get_sessionmaker(get_engine(db_file))
    myapp = klass(
        sessionmaker, edit=options.edit, delete=options.delete
    )
    myapp.show()
    sys.exit(app.exec_())


class BaseDialog(QtGui.QDialog):
    """BaseDialog.

    Abstract base class for PyFuelDB QDialogs.  Subclasses of the BaseDialog
    will allow a user to create, edit or delete objects associated with
    the subclass.

    :object_name - string representing the name of the associated object.

    """
    object_name = 'Object'

    def __init__(self, sessionmaker, edit=None, delete=None, parent=None):
        """Initialise an instance of this QDialog.

        :sessionmaker - a sessionmaker instance bound to a database.

        :edit - optional integer representing the object to edit.

        :delete - optional integer representing the object to delete.

            If the edit and delete parameters are omitted, the dialog will assume
            that the user is trying to add a new object.

            The edit and delete parameters cannot be called at the same time,
            for obvious reasons.

        :parent - optional QWidget representing the owner of this QDialog.

        """
        QtGui.QDialog.__init__(self, parent)

        self._setup_ui()

        # Create a bound session for the QDialog
        self.session = sessionmaker()

        if edit:
            self.setWindowTitle('Edit %s' % (self.object_name, ))

            setattr(self, self.object_name.lower(), self.get_object(edit))
            accept_method = self.update_object

        elif delete:
            self.setWindowTitle('Delete %s' % (self.object_name, ))

            setattr(self, self.object_name.lower(), self.get_object(delete))
            accept_method = self.delete_object

        else:
            accept_method = self.create_object

        # Connect QDialog signals
        QtCore.QObject.connect(self,
            QtCore.SIGNAL('accepted()'),
            accept_method
        )
        QtCore.QObject.connect(self,
            QtCore.SIGNAL('rejected()'),
            self.reject_dialog
        )

    def _setup_ui(self):
        """Setup the UI.

        Must be implemented by subclasses.

        """
        raise NotImplementedError

    def create_object(self):
        """Create Object.

        Must be implemented by subclasses.

        """
        raise NotImplementedError

    def delete_object(self):
        """Delete Object.

        Must be implemented by subclasses.

        """
        raise NotImplementedError

    def get_object(self, id):
        """Get Object.

        Must be implemented by subclasses.

        """
        raise NotImplementedError

    def update_object(self):
        """Update Object.

        Must be implemented by subclasses.

        """
        raise NotImplementedError

    def reject_dialog(self):
        """Reject Dialog.

        Called when the QDialog recieves the rejected signal, usually
        from a button on the dialog.

        """
        print 'Rejected changes'


if __name__ == '__main__':
    run_dialog(BaseDialog)