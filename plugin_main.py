# -*- coding: utf-8 -*-
"""
IGAC Cartografía Básica 1:25.000
Plugin principal — registra el botón en la barra de herramientas.
"""

import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

class IGACCartografiaPlugin:
    """Clase principal del plugin."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action_configurar = None

    def initGui(self):
        """Crear la entrada en la interfaz de QGIS."""
        icon_path = os.path.join(self.plugin_dir, "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()

        # Botón único: Configurador
        self.action_configurar = QAction(
            icon,
            "Configurar Cartografía IGAC 1:25.000",
            self.iface.mainWindow()
        )
        self.action_configurar.setToolTip(
            "Configura la cartografía básica IGAC 1:25.000 para una zona de estudio"
        )
        self.action_configurar.triggered.connect(self.abrir_configurador)

        # Agregar al menú Vector y a la barra de herramientas
        self.iface.addToolBarIcon(self.action_configurar)
        self.iface.addPluginToVectorMenu(
            "IGAC Cartografía Básica 1:25.000",
            self.action_configurar
        )

    def unload(self):
        """Eliminar entradas de la interfaz al desactivar el plugin."""
        self.iface.removeToolBarIcon(self.action_configurar)
        self.iface.removePluginVectorMenu(
            "IGAC Cartografía Básica 1:25.000",
            self.action_configurar
        )

    def abrir_configurador(self):
        """Abrir la ventana del configurador IGAC."""
        from .configurar_municipio_igac_gui import VentanaIGAC
        self.ventana = VentanaIGAC(self.iface.mainWindow())
        self.ventana.show()