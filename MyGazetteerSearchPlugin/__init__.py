# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MyGazetteerSearchPlugin
                                 A QGIS plugin
 A search plugin that queries a local SQLite database
                             -------------------
        begin                : 2013-09-20
        copyright            : (C) 2013 by Tim Martin
        email                : Tim.Martin@ordnancesurvey.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "Gazetteer Search Plugin"


def description():
    return "A search plugin that queries a local SQLite database"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Tim Martin"

def email():
    return "Tim.Martin@ordnancesurvey.co.uk"

def classFactory(iface):
    # load MyGazetteerSearchPlugin class from file MyGazetteerSearchPlugin
    from mygazetteersearchplugin import MyGazetteerSearchPlugin
    return MyGazetteerSearchPlugin(iface)
