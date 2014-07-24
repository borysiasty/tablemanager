# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableManagerUiInsert.ui'
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

class Ui_Insert(object):
    def setupUi(self, Insert):
        Insert.setObjectName(_fromUtf8("Insert"))
        Insert.resize(420, 425)
        self.gridlayout = QtGui.QGridLayout(Insert)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label = QtGui.QLabel(Insert)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.lineName = QtGui.QLineEdit(Insert)
        self.lineName.setMouseTracking(False)
        self.lineName.setInputMask(_fromUtf8(""))
        self.lineName.setMaxLength(10)
        self.lineName.setFrame(True)
        self.lineName.setObjectName(_fromUtf8("lineName"))
        self.vboxlayout.addWidget(self.lineName)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(Insert)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout.addWidget(self.label_2)
        self.comboType = QtGui.QComboBox(Insert)
        self.comboType.setMaxVisibleItems(5)
        self.comboType.setObjectName(_fromUtf8("comboType"))
        self.vboxlayout.addWidget(self.comboType)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(Insert)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.vboxlayout.addWidget(self.label_3)
        self.comboPos = QtGui.QComboBox(Insert)
        self.comboPos.setObjectName(_fromUtf8("comboPos"))
        self.vboxlayout.addWidget(self.comboPos)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem2)
        self.label_4 = QtGui.QLabel(Insert)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.vboxlayout.addWidget(self.label_4)
        self.lineLength = QtGui.QLineEdit(Insert)
        self.lineLength.setObjectName(_fromUtf8("lineLength"))
        self.vboxlayout.addWidget(self.lineLength)
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem3)
        self.label_5 = QtGui.QLabel(Insert)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.vboxlayout.addWidget(self.label_5)
        self.linePrecision = QtGui.QLineEdit(Insert)
        self.linePrecision.setObjectName(_fromUtf8("linePrecision"))
        self.vboxlayout.addWidget(self.linePrecision)
        self.gridlayout.addLayout(self.vboxlayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Insert)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem4, 1, 0, 1, 1)

        self.retranslateUi(Insert)
        self.comboType.setCurrentIndex(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Insert.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Insert.reject)
        QtCore.QMetaObject.connectSlotsByName(Insert)
        Insert.setTabOrder(self.lineName, self.comboType)
        Insert.setTabOrder(self.comboType, self.comboPos)
        Insert.setTabOrder(self.comboPos, self.buttonBox)

    def retranslateUi(self, Insert):
        Insert.setWindowTitle(_translate("Insert", "Insert field", None))
        self.label.setText(_translate("Insert", "Field name:", None))
        self.label_2.setText(_translate("Insert", "Field type:", None))
        self.label_3.setText(_translate("Insert", "Insert at position:", None))
        self.label_4.setText(_translate("Insert", "Length:", None))
        self.label_5.setText(_translate("Insert", "Precision:", None))

