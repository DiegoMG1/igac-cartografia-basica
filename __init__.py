# -*- coding: utf-8 -*-
"""
IGAC Cartografía Básica 1:25.000
Plugin para QGIS — punto de entrada obligatorio.
"""

def classFactory(iface):
    from .plugin_main import IGACCartografiaPlugin
    return IGACCartografiaPlugin(iface)
