#!/bin/sh

pyuic4 -o tableManagerUi.py tableManagerUi.ui
pyuic4 -o tableManagerUiClone.py tableManagerUiClone.ui
pyuic4 -o tableManagerUiInsert.py tableManagerUiInsert.ui
pyuic4 -o tableManagerUiRename.py tableManagerUirename.ui
pyrcc4 -o resources_rc.py resources.qrc
