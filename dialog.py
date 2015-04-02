# -*- coding: utf-8 -*-
import sys

from optparse import IndentedHelpFormatter, OptionParser

from PyQt4 import QtCore, QtGui

from lib import *


class RawIndentedHelpFormatter(IndentedHelpFormatter):
    """Overrides IndentedHelpFormatter to return help elements without any
    special formatting, textwrap, etc.

    """
    def format_epilog(self, epilog):
        """Return the epilog without formatting.

        """
        return '\n%s\n' % (epilog, )


def run_dialog(klass):
    """Create the QApplication (before modifying sys.argv) then parse sys.argv
    for acceptable command line parameters.

    """
    app = QtGui.QApplication(sys.argv)

    # Create an OptionParser
    usage = '%prog [OPTIONS] [FILE...]'
    description = 'Create, Edit or Delete a %s.' % (klass.object_name, )
    epilog = """Examples:

  Create a new %(object_name)s in the given SQLite database

    python %(prog_name)s pyfueldb.db

  Edit an existing %(object_name)s in the given SQLite database

    python %(prog_name)s -e 1 pyfueldb.db

  Delete an existing %(object_name)s from the given SQLite database

    python %(prog_name)s -d 1 pyfueldb.db

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
    """Base class for PyFuelDB QDialogs.

    Subclasses of the BaseDialog will allow a user to create, edit or delete
    objects associated with the subclass.

    :object_class - actual class model representing the object.  This must be
        set by inheriting subclasses for create, edit and delete methods to work.

    :object_name - string representing the name of the associated object.  This
        should be set by inheriting classes for UI strings, dialog titles, etc.

    :widget_field_map - dictionary that maps widget names to object attributes.
        This must be set by inheriting classes otherwise DB methods will not be
        able to interact with the UI.

    # TODO - enforce setting of appropriate attributes by subclasses.
    # TODO - determine if any attributes/widgets are missing from widget_field_map.

    """
    object_class = None
    object_name = 'Object'

    widget_field_map = {}

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
            self._populate_widgets()
            accept_method = self.update_object

        elif delete:
            self.setWindowTitle('Delete %s' % (self.object_name, ))

            setattr(self, self.object_name.lower(), self.get_object(delete))
            self._populate_widgets()
            accept_method = self.delete_object

        else:
            accept_method = self.create_object

        # Connect QDialogButtonBox signals
        QtCore.QObject.connect(
            self.ui.button_box,
            QtCore.SIGNAL('accepted()'),
            accept_method
        )
        QtCore.QObject.connect(
            self.ui.button_box,
            QtCore.SIGNAL('rejected()'),
            self.reject_dialog
        )

    def _setup_ui(self):
        """Setup the UI.

        Must be implemented by subclasses.

        """
        raise NotImplementedError

    def _populate_widgets(self):
        """Populate dialog widgets.

        Using the widget to field mapping, populate the widgets
        from the object's attributes.

        """
        for widget, field in self.widget_field_map.items():
            value = self._get_field_value(field)
            self._set_widget_value(widget, value)

    def _get_field_value(self, field):
        """Get the value of a field.

        :field - string, field to get value of

        """
        #TODO some type checking
        return getattr(
            getattr(self, self.object_name.lower()), field
        )

    def _set_field_value(self, field, value):
        """Set the value of a field.

        :field - string; name of the field (object attribute)

        :value - the value to set

        """
        #TODO Some type checking
        setattr(
            getattr(self, self.object_name.lower()),
            field, unicode(value)
        )

    def _get_widget_value(self, widget):
        """Get the values of a widget.

        :widget - string; name of the QWdiget

        """
        widget = getattr(self.ui, widget)

        if isinstance(widget, (QtGui.QLineEdit, )):
            return unicode(widget.text())

        raise TypeError('Cannot handle widget ' \
            '%(widget_type)s with name `%(widget_name)s`.'
            % {'widget_name': widget.objectName(), 'widget_type': type(widget), }
        )

    def _set_widget_value(self, widget, value):
        """Set the value of a widget.

        :widget - string; name of the QWidget

        :value - the value to set

        """
        widget = getattr(self.ui, widget)

        if isinstance(widget, (QtGui.QLineEdit, )):
            widget.setText(value)

        else:
            raise TypeError('Cannot handle widget ' \
                '%(widget_type)s with name `%(widget_name)s`.'
                % {'widget_name': widget.objectName(), 'widget_type': type(widget), }
            )

    def create_object(self):
        """Create a new object using values from the QDialog's widgets.

        Adds it to the bound SQLAlchemy session and calls `QDialog.accept`.

        """
        if self.object_class is None:
            raise TypeError('Class attribute `object_class` not defined in subclass')

        kwargs = {}
        for widget, field in self.widget_field_map.items():
            kwargs[field] = self._get_widget_value(widget)

        object_instance = self.object_class(**kwargs)

        self.session.add(object_instance)

        self.session.commit()

        self.accept()

    def delete_object(self):
        """Delete the object from the database.

        Get user to confirm deletion then call `QDialog.accept`.

        """
        ret = QtGui.QMessageBox.warning(
            self, 'Delete %(object_name)s?' % {'object_name': self.object_name, },
            'Do you really want to delete this %(object_name)s?\n%(object)s' % {
                'object': getattr(self, self.object_name.lower()),
                'object_name': self.object_name, },
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        )
        if ret == QtGui.QMessageBox.Yes:
            self.session.delete(getattr(self, self.object_name.lower()))

            self.session.commit()

            self.accept()

    def get_object(self, id):
        """Query the database using the given id and return the matching object.

        """
        if self.object_class is None:
            raise TypeError('Class attribute `object_class` not defined in subclass')

        object_instance = self.session.query(self.object_class).get(id)

        if not object_instance:
            raise Exception('%(object_name)s %(object_id)s was not found!' % {
                'object_id': id, 'object_name': self.object_name, })

        return object_instance

    def update_object(self):
        """Update the object using values from the QDialog's widgets and call
        `QDialog.accept`.

        #TODO Only update fields that have been modified.

        """
        for widget, field in self.widget_field_map.items():
            value = self._get_widget_value(widget)
            self._set_field_value(field, value)

        self.session.commit()

        self.accept()

    def reject_dialog(self):
        """Called when the QDialogButtonBox recieves the rejected signal, usually
        from a QDialogButtonBox button with a RejectRole.

        """
        print 'Rejected changes'
        self.reject()


if __name__ == '__main__':
    run_dialog(BaseDialog)