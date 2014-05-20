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
from qgis.gui import *
from tableManagerUi import Ui_Dialog
from tableManagerUiRename import Ui_Rename
from tableManagerUiClone import Ui_Clone
from tableManagerUiInsert import Ui_Insert
import sys

########## CLASS DialogRename ##############################

class DialogRename(QDialog, Ui_Rename):
  def __init__(self, iface, fields, selection):
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)
    self.fields = fields
    self.selection = selection
    self.setWindowTitle(self.tr('Rename field: {0}').format(fields[selection].name()))
    self.lineEdit.setValidator(QRegExpValidator(QRegExp('[\w\ _]{,10}'),self))
    self.lineEdit.setText(fields[selection].name())


  def accept(self):
    if self.newName() == self.fields[self.selection].name():
      QDialog.reject(self)
      return
    for i in self.fields.values():
      if self.newName().upper() == i.name().upper() and i != self.fields[self.selection]:
        QMessageBox.warning(self,self.tr('Rename field'),self.tr('There is another field with the same name.\nPlease type different one.'))
        return
    if not self.newName():
      QMessageBox.warning(self,self.tr('Rename field'),self.tr('The new name cannot be empty'))
      self.lineEdit.setText(self.fields[self.selection].name())
      return
    QDialog.accept(self)

  def newName(self):
    return self.lineEdit.text()



########## CLASS DialogClone ##############################

class DialogClone(QDialog, Ui_Clone):
  def __init__(self, iface, fields, selection):
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)
    self.fields = fields
    self.selection = selection
    self.setWindowTitle(self.tr('Clone field: ')+fields[selection].name())
    self.comboDsn.addItem(self.tr('at the first position'))
    for i in range(len(fields)):
      self.comboDsn.addItem(self.tr('after the {0} field').format(fields[i].name()))
    self.comboDsn.setCurrentIndex(selection+1)
    self.lineDsn.setValidator(QRegExpValidator(QRegExp('[\w\ _]{,10}'),self))
    self.lineDsn.setText(fields[selection].name()[:8] + '_2')

  def accept(self):
    if not self.result()[1]:
      QMessageBox.warning(self,self.tr('Clone field'),self.tr('The new name cannot be empty'))
      return
    if self.result()[1] == self.fields[self.selection].name():
        QMessageBox.warning(self,self.tr('Clone field'),self.tr('The new field\'s name must be different then source\'s one!'))
        return
    for i in self.fields.values():
      if self.result()[1].upper() == i.name().upper():
        QMessageBox.warning(self,self.tr('Clone field'),self.tr('There is another field with the same name.\nPlease type different one.'))
        return
    QDialog.accept(self)

  def result(self):
    return self.comboDsn.currentIndex(), self.lineDsn.text()



########## CLASS DialogInsert ##############################

class DialogInsert(QDialog, Ui_Insert):
  def __init__(self, iface, fields, selection):
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)
    self.fields = fields
    self.selection = selection
    self.setWindowTitle(self.tr('Insert field'))
    self.lineName.setValidator(QRegExpValidator(QRegExp('[\w\ _]{,10}'),self))
    self.comboType.addItem(self.tr('Integer'))
    self.comboType.addItem(self.tr('Real'))
    self.comboType.addItem(self.tr('String'))
    self.comboType.addItem(self.tr('Date'))

    self.comboPos.addItem(self.tr('at the first position'))
    for i in range(len(fields)):
      self.comboPos.addItem(self.tr('after the {0} field').format(fields[i].name()))
    self.comboPos.setCurrentIndex(selection+1)

  def accept(self):
    if not self.result()[0]:
      QMessageBox.warning(self,self.tr('Insert new field'),self.tr('The new name cannot be empty'))
      return
    for i in self.fields.values():
      if self.result()[0].upper() == i.name().upper():
        QMessageBox.warning(self,self.tr('Insert new field'),self.tr('There is another field with the same name.\nPlease type different one.'))
        return
    QDialog.accept(self)

  def result(self):
    return self.lineName.text(), self.comboType.currentIndex(), self.comboPos.currentIndex()



########## CLASS TableManager ##############################

class TableManager(QDialog, Ui_Dialog):

  def __init__(self, iface):
    QDialog.__init__(self)
    self.iface = iface
    self.setupUi(self)
    self.layer = self.iface.activeLayer()
    self.provider = self.layer.dataProvider()
    self.fields = self.readFields( self.provider.fields() )
    self.isUnsaved = False  # No unsaved changes yet
    if self.provider.storageType() == 'ESRI Shapefile': # Is provider saveable?
      self.isSaveable = True
    else:
      self.isSaveable = False

    self.needsRedraw = True # Preview table is redrawed only on demand. This is for initial drawing.
    self.lastFilter = None
    self.selection = -1     # Don't highlight any field on startup
    self.selection_list = [] #Update: Santiago Banchero 09-06-2009

    QObject.connect(self.butUp, SIGNAL('clicked()'), self.doMoveUp)
    QObject.connect(self.butDown, SIGNAL('clicked()'), self.doMoveDown)
    QObject.connect(self.butDel, SIGNAL('clicked()'), self.doDelete)
    QObject.connect(self.butIns, SIGNAL('clicked()'), self.doInsert)
    QObject.connect(self.butClone, SIGNAL('clicked()'), self.doClone)
    QObject.connect(self.butRename, SIGNAL('clicked()'), self.doRename)
    QObject.connect(self.butSave, SIGNAL('clicked()'), self.doSave)
    QObject.connect(self.butSaveAs, SIGNAL('clicked()'), self.doSaveAs)
    QObject.connect(self.buttonBox, SIGNAL('rejected()'), self.doDone)
    QObject.connect(self.fieldsTable, SIGNAL('itemSelectionChanged ()'), self.selectionChanged)
    QObject.connect(self.tabWidget, SIGNAL('currentChanged (int)'), self.drawDataTable)

    self.setWindowTitle(self.tr('Table Manager: {0}').format(self.layer.name()))
    self.progressBar.setValue(0)
    self.restoreCfg()
    self.drawFieldsTable()
    self.readData()



  def readFields(self, providerFields): # Populates the self.fields dictionary with providerFields
    fieldsDict = {}
    i=0
    for field in providerFields:
        fieldsDict.update({i:field})
        i+=1
    return fieldsDict



  def drawFieldsTable(self): # Draws the fields table on startup and redraws it when changed
    fields = self.fields
    self.fieldsTable.setRowCount(0)
    for i in range(len(fields)):
      self.fieldsTable.setRowCount(i+1)
      item = QTableWidgetItem(fields[i].name())
      item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
      item.setData(Qt.UserRole, i) # set field index
      self.fieldsTable.setItem(i,0,item)
      item = QTableWidgetItem(fields[i].typeName())
      item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
      self.fieldsTable.setItem(i,1,item)
    self.fieldsTable.setColumnWidth(0, 128)
    self.fieldsTable.setColumnWidth(1, 64)



  def readData(self): # Reads data from the 'provider' QgsDataProvider into the 'data' list [[column1] [column2] [column3]...]
    fields = self.fields
    self.data = []
    for i in range(len(fields)):
      self.data += [[]]
    steps = self.provider.featureCount()
    stepp = steps / 10
    if stepp == 0:
      stepp = 1
    progress = self.tr('Reading data ') # As a progress bar is used the main window's status bar, because the own one is not initialized yet
    n = 0
    for feat in self.provider.getFeatures():
        attrs = feat.attributes()

        for i in range(len(attrs)):
            self.data[i] += [attrs[i]]

        n += 1
        if n % stepp == 0:
            progress += '|'
            self.iface.mainWindow().statusBar().showMessage(progress)

    self.iface.mainWindow().statusBar().showMessage('')



  def drawDataTable(self,tab): # Called when user switches tabWidget to the Table Preview
    if tab != 1 or self.needsRedraw == False: return
    fields = self.fields
    self.dataTable.clear()
    self.repaint()
    self.dataTable.setColumnCount(len(fields))
    self.dataTable.setRowCount(self.provider.featureCount())
    header = []
    for i in fields.values():
      header.append(i.name())
    self.dataTable.setHorizontalHeaderLabels(header)
    self.progressBar.setRange (0, len(self.data)+1)
    self.progressBar.setFormat(self.tr('Drawing table') +': %p%')
    formatting = True
    if formatting: # slower procedure, with formatting the table items
      for i in range(len(self.data)):
        self.progressBar.setValue(i+1)
        for j in range(len(self.data[i])):
          item = QTableWidgetItem(unicode(self.data[i][j] or 'NULL'))
          item.setFlags(Qt.ItemIsSelectable)
          if fields[i].type() == 6 or fields[i].type() == 2:
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
          self.dataTable.setItem(j,i,item)
    else: # about 25% faster procedure, without formatting
      for i in range(len(self.data)):
        self.progressBar.setValue(i+1)
        for j in range(len(self.data[i])):
          self.dataTable.setItem(j,i,QTableWidgetItem(unicode(self.data[i][j] or 'NULL')))
    self.dataTable.resizeColumnsToContents()
    self.needsRedraw = False
    self.progressBar.reset()



  def setChanged(self): # Called after making any changes
    if self.isSaveable:
      self.butSave.setEnabled(True)
    self.butSaveAs.setEnabled(True)
    self.isUnsaved = True       # data are unsaved
    self.needsRedraw = True     # preview table needs to redraw



  def selectionChanged(self): # Called when user is changing field selection of field
    #self.selection_list = [ i.topRow() for i in self.fieldsTable.selectedRanges() ]
    self.selection_list = [i for i in range(self.fieldsTable.rowCount()) if self.fieldsTable.item(i,0).isSelected()]

    if len(self.selection_list)==1:
        self.selection = self.selection_list[0]
    else:
        self.selection = -1

    self.butDel.setEnabled( len(self.selection_list)>0 )

    item = self.selection
    if item == -1:
      self.butUp.setEnabled(False)
      self.butDown.setEnabled(False)
      self.butRename.setEnabled(False)
      self.butClone.setEnabled(False)
    else:
      if item == 0:
        self.butUp.setEnabled(False)
      else:
        self.butUp.setEnabled(True)
      if item == self.fieldsTable.rowCount()-1:
        self.butDown.setEnabled(False)
      else:
        self.butDown.setEnabled(True)
      if self.fields[item].type() in [2,6,10,14]:
         self.butRename.setEnabled(True)
         self.butClone.setEnabled(True)
      else:
        self.butRename.setEnabled(False)
        self.butClone.setEnabled(False)



  def doMoveUp(self): # Called when appropriate button was pressed
    item = self.selection
    tmp = self.fields[item]
    self.fields[item] = self.fields[item-1]
    self.fields[item-1] = tmp
    for i in range(0,2):
      tmp = QTableWidgetItem(self.fieldsTable.item(item,i))
      self.fieldsTable.setItem(item,i,QTableWidgetItem(self.fieldsTable.item(item-1,i)))
      self.fieldsTable.setItem(item-1,i,tmp)
    if item > 0:
      self.fieldsTable.clearSelection()
      self.fieldsTable.setCurrentCell(item-1,0)
    tmp = self.data[item]
    self.data[item]=self.data[item-1]
    self.data[item-1]=tmp
    self.setChanged()



  def doMoveDown(self): # Called when appropriate button was pressed
    item = self.selection
    tmp = self.fields[item]
    self.fields[self.selection] = self.fields[self.selection+1]
    self.fields[self.selection+1] = tmp
    for i in range(0,2):
      tmp = QTableWidgetItem(self.fieldsTable.item(item,i))
      self.fieldsTable.setItem(item,i,QTableWidgetItem(self.fieldsTable.item(item+1,i)))
      self.fieldsTable.setItem(item+1,i,tmp)
    if item < self.fieldsTable.rowCount()-1:
      self.fieldsTable.clearSelection()
      self.fieldsTable.setCurrentCell(item+1,0)
    tmp = self.data[item]
    self.data[item]=self.data[item+1]
    self.data[item+1]=tmp
    self.setChanged()



  def doRename(self): # Called when appropriate button was pressed
    dlg = DialogRename(self.iface,self.fields,self.selection)
    if dlg.exec_() == QDialog.Accepted:
      newName = dlg.newName()
      self.fields[self.selection].setName(newName)
      item = self.fieldsTable.item(self.selection,0)
      item.setText(newName)
      self.fieldsTable.setItem(self.selection,0,item)
      self.fieldsTable.setColumnWidth(0, 128)
      self.fieldsTable.setColumnWidth(1, 64)
      self.setChanged()



  def doDelete(self): # Called when appropriate button was pressed
    #<---- Update: Santiago Banchero 09-06-2009 ---->
    #self.selection_list = sorted(self.selection_list,reverse=True)
    all_fields_to_del = [self.fields[i].name() for i in self.selection_list if i <> -1]

    warning = '<b>' + self.tr('WARNING! Are you sure you want to remove the following fields?\n{0}').format(", ".join(all_fields_to_del)) + '</b>'
    if QMessageBox.warning(self, self.tr('Delete field'), warning , QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
        return

    self.selection_list.sort(reverse=True) # remove them in reverse order to avoid index changes!!!
    for r in self.selection_list:
        if r <> -1:
            del(self.data[r])
            del(self.fields[r])
            self.fields = dict(zip(range(len(self.fields)), self.fields.values()))
            self.drawFieldsTable()
            self.setChanged()

    self.selection_list = []
    #</---- Update: Santiago Banchero 09-06-2009 ---->


  def doInsert(self): # Called when appropriate button was pressed
    dlg = DialogInsert(self.iface,self.fields,self.selection)
    if dlg.exec_() == QDialog.Accepted:
      (aName, aType, aPos) = dlg.result()
      if aType == 0:
        #Int
        aLength = 10
        aPrec = 0
        aVariant = QVariant.Int
        aTypeName = 'Integer'
      elif aType == 1:
        #Real
        aLength = 32
        aPrec = 3
        aVariant = QVariant.Double
        aTypeName = 'Real'
      elif aType == 3:
        #Date
        aLength = 0
        aPrec = 0
        aVariant = QVariant.Date
        aTypeName = 'Date'
      else:
        # aType 2 means String
        aLength = 80
        aPrec = 0
        aVariant = QVariant.String
        aTypeName = 'String'
      self.data += [[]]
      if aPos < len(self.fields):
        fieldsToMove = range(aPos+1,len(self.fields)+1)
        fieldsToMove.reverse()
        for i in fieldsToMove:
          self.fields[i] = self.fields[i-1]
          self.data[i] = self.data[i-1]
      self.fields[aPos] = QgsField(aName, aVariant, aTypeName, aLength, aPrec, "")
      aData = []
      if aType == 2:
        aItem = None
      else:
        aItem = None
      for i in range(len(self.data[0])):
        aData += [aItem]
      self.data[aPos] = aData
      self.drawFieldsTable()
      self.fieldsTable.setCurrentCell(aPos,0)
      self.setChanged()



  def doClone(self): # Called when appropriate button was pressed
    dlg = DialogClone(self.iface,self.fields,self.selection)
    if dlg.exec_() == QDialog.Accepted:
      (dst, newName) = dlg.result()
      self.data += [[]]
      movedField = QgsField(self.fields[self.selection])
      movedData = self.data[self.selection]
      if dst < len(self.fields):
        fieldsToMove = range(dst+1,len(self.fields)+1)
        fieldsToMove.reverse()
        for i in fieldsToMove:
          self.fields[i] = self.fields[i-1]
          self.data[i] = self.data[i-1]
      self.fields[dst] = movedField
      self.fields[dst].setName(newName)
      self.data[dst] = movedData
      self.drawFieldsTable()
      self.fieldsTable.setCurrentCell(dst,0)
      self.setChanged()



  def doSave(self): # Called when appropriate button was pressed
    # I believe the procedure below is as much safe as possible.
    encoding = self.provider.encoding()
    tmpDir = QDir.tempPath()
    srcPath = self.provider.dataSourceUri().split('|')[0]
    # without this one line code in win xp, srcName return something wrong,see below (patch from Volkan Kepoglu - thanks!)
    srcPath = srcPath.replace("\\","/")
    if srcPath.upper().endswith('.SHP'): # if the path points to the shp file, remove the extension...
      srcName = QFileInfo(srcPath).baseName()
      srcPath = QFileInfo(srcPath).path() + '/' + QFileInfo(srcPath).baseName()
    else: # ...but if it points only to a directory, try to determine the name of the file inside!
      qPath = QDir(srcPath)
      qPath.setNameFilters(['*.shp', '*.SHP'])
      if len(qPath.entryList()) == 1: # there is exactly one shapefile inside
        srcName = qPath.entryList()[0]
        srcName = QFileInfo(srcName).baseName()
        srcPath += '/' + srcName
      else:
        QMessageBox.warning(self, self.tr('Table Manager'), self.tr("I cannot determine the layer source file: {0} !\nThe layer won't be changed, please use the Save As button.").format(srcPath))
        return
    # write the layer to the temporary directory
    if self.writeToFile(tmpDir+'/'+srcName+'.shp', encoding) != 0:
      QMessageBox.warning(self, self.tr('Table Manager'), self.tr("Failed saving the changes to the temporary directory: {0} !\nThe layer won't be changed, please use the Save As button.").format(tmpDir))
      QgsVectorFileWriter.deleteShapeFile(tmpDir+'/'+srcName+'.shp')
      return
    # try to remove the old .dbf~ backup
    QFile(srcPath+'.dbf~').remove()

    ''' 4 lines added : '''
    layerName = self.layer.name()
    QFile.remove( tmpDir+'/'+srcName+'.qml' )
    self.layer.saveNamedStyle( tmpDir+'/'+srcName+'.qml' )
    if hasattr( QgsMapLayerRegistry.instance(), "removeMapLayers" ):
        QgsMapLayerRegistry.instance().removeMapLayers([self.layer.id()])
    else:
        QgsMapLayerRegistry.instance().removeMapLayer(self.layer.getLayerID()) # API <= 1.8
    # rename the oryginal .dbf file to .dbf~
    if not QFile(srcPath+'.dbf').rename(srcPath+'.dbf~'):
      QMessageBox.warning(self, self.tr('Table Manager'), self.tr('Failed backuping the old table to {0}.dbf~\nThe layer won\'t be changed, please use the Save As button.').format(srcPath))
      # we don't return now because layer has to be reloaded'''
    # copy the .dbf from the temp directory to the target location
    elif QFile(tmpDir+'/'+srcName+'.dbf').copy(srcPath+'.dbf'):
      # dbf file copied. Copy also cpg if present
      if QFile(tmpDir+'/'+srcName+'.cpg').exists():
        QFile(srcPath+'.cpg').remove()
        QFile(tmpDir+'/'+srcName+'.cpg').copy(srcPath+'.cpg')
    else:
      # something went wrong with copying the dbf file. Restore the dbf~ file
      if not QFile(srcPath+'.dbf~').rename(srcPath+'.dbf'):
        QMessageBox.warning(self, self.tr('Table Manager'), self.tr('WARNING! I can neither save the new {0}.dbf file\nnor restore it from the {0}.dbf~ backup.\nPlease check it manually!').format(srcName))
        QgsVectorFileWriter.deleteShapeFile(tmpDir+'/'+srcName+'.shp')
        return
      # dbf~ file restored :
      QMessageBox.warning(self, self.tr('Table Manager'), self.tr("Failed saving the changes to {0}.dbf\nThe layer will not be changed, please use the Save As button.").format(srcPath))
      '''
      QgsVectorFileWriter.deleteShapeFile(tmpDir+'/'+srcName+'.shp')
      return
      we don't return now because layer has to be reloaded
      '''
    # clean the temp directory
    QgsVectorFileWriter.deleteShapeFile(tmpDir+'/'+srcName+'.shp')
    # create the new layer
    '''layerName = self.layer.name()'''
    newLayer = QgsVectorLayer(srcPath+'.shp', layerName, 'ogr')
    if not newLayer.isValid():
      QMessageBox.warning(self, self.tr('Table Manager'), self.tr("WARNING! The changes seem to be commited, but I can't reload the layer!\nPlease check it out!\nThe old table is backuped as {0}.dbf~.").format(srcName))
      return
    # copy the style (it's possible only if the clasyfying field was not renamed!)
    if QMessageBox.question(self, self.tr('Saving successful'),self.tr('Saving successful. The old table has been backuped as {0}.dbf~.\nDo you wish to keep the layer style?\n\nNote that if the style depends on an attribute you\'ve renamed, all features on the layer will become invisible. In that case please adjust the style manually.').format(srcName), QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
      '''#newLayer.copySymbologySettings(self.layer)'''
      resp = newLayer.loadNamedStyle( tmpDir+'/'+srcName+'.qml' )
      if not resp[1]:
        QMessageBox.warning(self, self.tr('Table Manager'), self.tr("This layer will be reloaded without its previous style (loading style failed)"))
    QFile.remove( tmpDir+'/'+srcName+'.qml' )
    # set encoding
    newLayer.setProviderEncoding( encoding )
    # reload the layer
    if hasattr( QgsMapLayerRegistry.instance(), 'addMapLayers' ):
        QgsMapLayerRegistry.instance().addMapLayers([newLayer])
    else:
        QgsMapLayerRegistry.instance().addMapLayer(newLayer)  # QPI <= 1.8
    # point the self.layer to the new one.
    self.layer = self.iface.activeLayer()
    self.provider = self.layer.dataProvider()
    self.fields = self.readFields( self.provider.fields() )
    self.butSave.setEnabled(False)
    self.saveCfg() # save cfg only in case of any successfull operations, not when user just plays
    self.isUnsaved = False


  def doSaveAs(self): # Called when appropriate button was pressed
    formats = QgsVectorFileWriter.supportedFiltersAndFormats().keys()
    formats.sort()
    filters = ''
    for i in formats:
      filters += i + ';;'
    fileDialog = QgsEncodingFileDialog(self, self.tr('Save as'), self.lastDirectory, filters, self.lastEncoding)
    fileDialog.setAcceptMode(QFileDialog.AcceptSave)
    if self.lastFilter:
      fileDialog.selectNameFilter( self.lastFilter )
    if fileDialog.exec_() != QDialog.Accepted:
      return
    fileName = fileDialog.selectedFiles()[0]
    encoding = fileDialog.encoding()
    if not fileName:
      return
    filePath = QFileInfo(fileName).absoluteFilePath()
    if not filePath:
      return
    self.lastFilter = fileDialog.selectedNameFilter()
    driverName = QgsVectorFileWriter.supportedFiltersAndFormats()[ self.lastFilter ]

    if driverName == 'ESRI Shapefile' and QFileInfo(filePath).suffix().upper() != 'SHP':
      filePath = filePath + '.shp'
    if driverName == 'KML' and QFileInfo(filePath).suffix().upper() != 'KML':
      filePath = filePath + '.kml'
    if driverName == 'MapInfo File' and QFileInfo(filePath).suffix().upper() not in ['MIF','TAB']:
       filePath = filePath + '.mif'
    if driverName == 'GeoJSON' and QFileInfo(filePath).suffix().upper() != 'GEOJSON':
      filePath = filePath + '.geojson'
    if driverName == 'GeoRSS' and QFileInfo(filePath).suffix().upper() != 'XML':
      filePath = filePath + '.xml'
    if driverName == 'GMT' and QFileInfo(filePath).suffix().upper() != 'GMT':
      filePath = filePath + '.gmt'
    if driverName == 'SQLite' and QFileInfo(filePath).suffix().upper() != 'SQLITE':
      filePath = filePath + '.sqlite'
    if driverName in ['Interlis 1','Interlis 2'] and QFileInfo(filePath).suffix().upper() not in ['ITF','XML','ILI']:
      filePath = filePath + '.itf'
    if driverName == 'GML' and QFileInfo(filePath).suffix().upper() != 'GML':
      filePath = filePath + '.gml'
    if driverName == 'Geoconcept' and QFileInfo(filePath).suffix().upper() not in ['GXT','TXT']:
      filePath = filePath + '.gxt'
    if driverName == 'DXF' and QFileInfo(filePath).suffix().upper() != 'DXF':
      filePath = filePath + '.dxf'
    if driverName == 'DGN' and QFileInfo(filePath).suffix().upper() != 'DGN':
      filePath = filePath + '.dgn'
    if driverName == 'CSV' and QFileInfo(filePath).suffix().upper() != 'CSV':
      filePath = filePath + '.csv'
    if driverName == 'BNA' and QFileInfo(filePath).suffix().upper() != 'BNA':
      filePath = filePath + '.bna'
    if driverName == 'GPX' and QFileInfo(filePath).suffix().upper() != 'GPX':
      filePath = filePath + '.gpx'
    if driverName == 'S57' and QFileInfo(filePath).suffix().upper() != 'S57':
      filePath = filePath + '.s57'

    # if saving to the source layer...
    reloadSourceLayer = False
    if filePath == self.provider.dataSourceUri().split('|')[0]:
      if QMessageBox.question(self, self.tr('Table Manager'), self.tr('You are attemping to save the changes to the original file. Are you sure you want to do this? If yes, the original layer will be removed from the legend.'), QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
        reloadSourceLayer = True
      else:
        return

    if self.writeToFile(filePath,encoding, driverName) != 0:
      return

    # formatting TOC item name and adding to the TOC
    layer = QgsVectorLayer(filePath, QFileInfo(filePath).completeBaseName(), 'ogr')
    if layer.isValid():
        layer.setProviderEncoding( encoding )
        if hasattr( QgsMapLayerRegistry.instance(), 'addMapLayers' ):
            QgsMapLayerRegistry.instance().addMapLayers([layer])
        else:
            QgsMapLayerRegistry.instance().addMapLayer(layer)  # QPI <= 1.8
    else:
      QMessageBox.warning(self, self.tr('Table Manager'), self.tr("WARNING! The new layer seems to be created, but is invalid.\nIt won't be loaded."))
    if reloadSourceLayer:
      if hasattr( QgsMapLayerRegistry.instance(), "removeMapLayers" ):
        QgsMapLayerRegistry.instance().removeMapLayers([self.layer.id()])
      else:
        QgsMapLayerRegistry.instance().removeMapLayer(self.layer.getLayerID()) # API <= 1.8
      self.layer = self.iface.activeLayer()
      self.provider = self.layer.dataProvider()
      self.fields = self.readFields( self.provider.fields() )
      self.setWindowTitle(self.tr('Table Manager: {0}').format(self.layer.name()))
    self.isUnsaved = False
    self.lastDirectory = QFileInfo(fileName).absolutePath()
    self.lastEncoding = encoding
    self.saveCfg() # Store configuration only in case of any successfull operations, not when user is just playing ;)



  def writeToFile(self, filePath, encoding, driverName = 'ESRI Shapefile'): # write data to a shapefile
    if QFile(filePath).exists():
      try:
        QgsVectorFileWriter.deleteShapeFile(filePath)
      except:
        QMessageBox.warning(self, self.tr('Table Manager'), self.tr('Cannot overwrite an existing shapefile.\nPlease remove it manually.'))
        return 1
    self.progressBar.setRange(0, self.provider.featureCount())
    self.progressBar.setFormat(self.tr('Saving data:') + ' %p%')
    self.progressBar.setValue(0)
    # create destination layer
    fields = QgsFields()
    keys = self.fields.keys()
    keys.sort()
    for key in keys:
        fields.append(self.fields[key])
    if driverName == 'ESRI Shapefile':
        #lco = ["ENCODING="+encoding , "SHAPE_ENCODING="+encoding]
        lco = ["ENCODING="+encoding]
        settings = QSettings()
    else:
        lco = []
    writer = QgsVectorFileWriter(filePath, encoding, fields, self.provider.geometryType(), self.provider.crs(), driverName, [], lco)
    if writer.hasError():
      QMessageBox.warning(self, self.tr('Table Manager'), self.tr("Error creating file. The errror message was:") + "<br/>" + writer.errorMessage() )
      self.progressBar.reset()
      return 2
    geom = QgsGeometry()
    n = 0
    for feat in self.provider.getFeatures():
        geom = feat.geometry()
        outFeat = QgsFeature()
        outFeat.setGeometry(geom)
        attrs = []
        for i in range(len(self.fields)):
            try:
                attrs += [self.data[i][n]]
            except:
                attrs += ['']
        outFeat.initAttributes(len(attrs))
        outFeat.setAttributes(attrs)
        writer.addFeature(outFeat)
        self.progressBar.setValue(n)
        n += 1

    del writer
    self.progressBar.reset()
    return 0



  def doDone(self): # Called when 'Done' button pressed
    question = self.tr('The table contains unsaved changes. Do you really want to quit?')
    if not (self.isUnsaved and QMessageBox.question(self, self.tr('Table Manager'), question, QMessageBox.Yes, QMessageBox.No) == QMessageBox.No):
      self.close()



  def restoreCfg(self): # Restores previous session configuration or, if fails, init defaul values
    settings = QSettings()
    self.restoreGeometry(settings.value('/Plugin-TableManager/geometry', QByteArray(), type=QByteArray))
    self.lastDirectory = settings.value('/Plugin-TableManager/lastDirectory', '.', type=unicode)
    self.lastEncoding = settings.value('/Plugin-TableManager/lastEncoding', 'UTF-8', type=unicode)
    self.lastFilter = settings.value('/Plugin-TableManager/lastFilter', '', type=unicode)



  def saveCfg(self): # Saves configuration
    settings = QSettings()
    settings.setValue('/Plugin-TableManager/geometry', self.saveGeometry())
    settings.setValue('/Plugin-TableManager/lastDirectory', self.lastDirectory)
    settings.setValue('/Plugin-TableManager/lastEncoding', self.lastEncoding)
    settings.setValue('/Plugin-TableManager/lastFilter', self.lastFilter)
