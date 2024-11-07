from qdarktheme.qtpy import QtCore, QtGui, QtWidgets

class NumericDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(parent, option, index)
        if isinstance(editor, QtWidgets.QLineEdit):
            reg_ex =  QtCore.QRegularExpression("[0-9]+.?[0-9]{,2}")
            validator = QtCore.QRegularExpressionVa QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor