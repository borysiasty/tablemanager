# -*- coding: utf-8 -*-
#-----------------------------------------------------------
#
# Table Manager
# Copyright (C) 2008-2013 Borys Jurgiel
# fix for multiple field removing (C) 2009-2010 Santiago Banchero
# fix for saving under Windows and preserving styles (C) 2011 Philippe Desboeufs
#
#-----------------------------------------------------------
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

def name():
    return 'Table Manager'

def description():
    return 'Manages the attribute table structure'

def version():
    return 'Version 0.4.4'

def qgisMinimumVersion():
    return '1.7'

def icon():
    return "icons/tableManagerIcon.png"

def author():
    return 'Borys Jurgiel'

def authorName():
    return 'Borys Jurgiel'

def email():
    return 'spamfilter@borysjurgiel.pl'

def homepage():
    return 'http://hub.qgis.org/projects/tablemanager'

def classFactory(iface):
    from tableManager_plugin import tableManager
    return tableManager(iface)
