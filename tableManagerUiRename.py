# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableManagerUirename.ui'
#
# Created: Wed Jul 23 07:13:42 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Rename(object):
    def setupUi(self, Rename):
        Rename.setObjectName(_fromUtf8("Rename"))
        Rename.resize(397, 126)
        self.gridlayout = QtGui.QGridLayout(Rename)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label = QtGui.QLabel(Rename)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(Rename)
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setInputMask(_fromUtf8(""))
        self.lineEdit.setMaxLength(10)
        self.lineEdit.setFrame(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.vboxlayout.addWidget(self.lineEdit)
        self.gridlayout.addLayout(self.vboxlayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Rename)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(Rename)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Rename.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Rename.reject)
        QtCore.QMetaObject.connectSlotsByName(Rename)

    def retranslateUi(self, Rename):
        Rename.setWindowTitle(_translate("Rename", "Rename field", None))
        self.label.setText(_translate("Rename", "Enter new field name:", None))

