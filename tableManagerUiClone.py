# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableManagerUiClone.ui'
#
# Created: Wed Jul 23 07:13:41 2014
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

class Ui_Clone(object):
    def setupUi(self, Clone):
        Clone.setObjectName(_fromUtf8("Clone"))
        Clone.resize(375, 210)
        self.gridlayout = QtGui.QGridLayout(Clone)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.vboxlayout.addItem(spacerItem)
        self.label = QtGui.QLabel(Clone)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.lineDsn = QtGui.QLineEdit(Clone)
        self.lineDsn.setMouseTracking(False)
        self.lineDsn.setInputMask(_fromUtf8(""))
        self.lineDsn.setMaxLength(10)
        self.lineDsn.setFrame(True)
        self.lineDsn.setObjectName(_fromUtf8("lineDsn"))
        self.vboxlayout.addWidget(self.lineDsn)
        self.label_3 = QtGui.QLabel(Clone)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.vboxlayout.addWidget(self.label_3)
        self.comboDsn = QtGui.QComboBox(Clone)
        self.comboDsn.setObjectName(_fromUtf8("comboDsn"))
        self.vboxlayout.addWidget(self.comboDsn)
        self.gridlayout.addLayout(self.vboxlayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Clone)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridlayout.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(Clone)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Clone.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Clone.reject)
        QtCore.QMetaObject.connectSlotsByName(Clone)
        Clone.setTabOrder(self.lineDsn, self.comboDsn)
        Clone.setTabOrder(self.comboDsn, self.buttonBox)

    def retranslateUi(self, Clone):
        Clone.setWindowTitle(_translate("Clone", "Clone field", None))
        self.label.setText(_translate("Clone", "A name for the new field:", None))
        self.label_3.setText(_translate("Clone", "Insert at position:", None))

