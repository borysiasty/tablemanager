# -*- coding: utf-8 -*-

# ***************************************************************************
#
# TableManager
#
# Copyright (C) 2008 Borys Jurgiel
#
# ***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources_rc
import tableManager_gui
import os.path

class tableManager:

 def __init__(self, iface):
  self.iface = iface
  #i18n
  pluginPath = QFileInfo(os.path.realpath(__file__)).path()  # patch by Régis Haubourg
  localeName = QLocale.system().name()
  if QFileInfo(pluginPath).exists():
    self.localePath = pluginPath+"/i18n/tablemanager_" + localeName + ".qm"
  if QFileInfo(self.localePath).exists():
    self.translator = QTranslator()
    self.translator.load(self.localePath)
    if qVersion() > '4.3.3':
      QCoreApplication.installTranslator(self.translator)


 def setCurrentTheme(self, theThemeName):
    """ Set icons to the current theme """
    self.action.setIcon(self.getThemeIcon("tableManagerIcon.png"))


 def getThemeIcon(self, theName):
    """ get the icon from the best available theme """
    myCurThemePath = QgsApplication.activeThemePath() + "/plugins/" + theName;
    myDefThemePath = QgsApplication.defaultThemePath() + "/plugins/" + theName;
    myQrcThemePath = ":/plugins/tableManager/icons/" + QgsApplication.themeName() + "/" + theName;
    myQrcPath = ":/plugins/tableManager/icons/" + theName;
    if QFile.exists(myCurThemePath):
      return QIcon(myCurThemePath)
    elif QFile.exists(myDefThemePath):
      return QIcon(myDefThemePath)
    elif QFile.exists(myQrcThemePath):
      return QIcon(myQrcThemePath)
    elif QFile.exists(myQrcPath):
      return QIcon(myQrcPath)
    else:
      return QIcon()


 def initGui(self):
  # create action
  self.action = QAction(self.getThemeIcon("tableManagerIcon.png"), QCoreApplication.translate('TableManager','Table manager'), self.iface.mainWindow())
  #self.action = QAction(QIcon(':/plugins/tableManager/icons/tableManagerIcon.png'), QCoreApplication.translate('TableManager','Table manager'), self.iface.mainWindow())
  self.action.setWhatsThis(QCoreApplication.translate('TableManager','Manages attribute table structure'))
  self.action.triggered.connect(self.run)
  self.iface.currentThemeChanged.connect(self.setCurrentTheme)
  # add toolbar button and menu item
  if hasattr( self.iface, 'addVectorToolBarIcon' ):
    self.iface.addVectorToolBarIcon(self.action)
  else:
    self.iface.addToolBarIcon(self.action)
  if hasattr( self.iface, 'addPluginToVectorMenu' ):
    self.iface.addPluginToVectorMenu( u"&Table Manager", self.action )
  else:
    self.iface.addPluginToMenu("&Table", self.action)


 def unload(self):
  # remove the plugin menu item and icon
  if hasattr( self.iface, 'removePluginVectorMenu' ):
    self.iface.removePluginVectorMenu( u"&Table", self.action )
  else:
    self.iface.removePluginMenu( u"&Table", self.action )
  if hasattr( self.iface, 'removeVectorToolBarIcon' ):
    self.iface.removeVectorToolBarIcon(self.action)
  else:
    self.iface.removeToolBarIcon(self.action)


 def run(self):
  # create and show a configuration dialog or something similar
  layer = self.iface.activeLayer()
  if layer == None or layer.type() != layer.VectorLayer:
    QMessageBox.warning(self.iface.mainWindow(), QCoreApplication.translate('TableManager','Table manager'), QCoreApplication.translate('TableManager','Please select a vector layer'))
  elif layer.isEditable():
    QMessageBox.warning(self.iface.mainWindow(), QCoreApplication.translate('TableManager','Table manager'), QCoreApplication.translate('TableManager','The selected layer is currently in editing mode.\nPlease exit this mode before managing the table.'))
  else:
    dialoga = tableManager_gui.TableManager(self.iface)
    dialoga.exec_()
