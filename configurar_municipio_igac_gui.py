"""
=============================================================================
CONFIGURADOR CARTOGRAFÍA BÁSICA IGAC 1:25.000
=============================================================================
Autor:       Diego Andrés Muñoz Guerrero
             Doctor en Geografía IGAC-UPTC
             Profesor Tiempo Completo — Universidad de Nariño, Colombia
Institución: Departamento de Recursos Naturales y Sistemas Agroforestales
             Universidad de Nariño — Colombia
Catálogo:    Cartografía Básica Digital IGAC 1:25.000
             Resoluciones 471 y 529 de 2020
CRS:         EPSG:9377 (MAGNA-SIRGAS / Origen Nacional CTM12)
Formatos:    Shapefile (.shp), File Geodatabase (.gdb),
             Personal Geodatabase (.mdb)
=============================================================================
Ejecutar en la Consola Python de QGIS.
No es necesario editar el código.
=============================================================================
"""

import os
import processing

# --- DEFINICIONES GLOBALES ---
PT = 0.352778
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# -----------------------------

from qgis.core import (
    QgsProject, QgsVectorLayer, QgsCoordinateReferenceSystem,
    QgsLineSymbol, QgsSimpleLineSymbolLayer,
    QgsMarkerSymbol, QgsSimpleMarkerSymbolLayer, QgsFillSymbol,
    QgsCategorizedSymbolRenderer, QgsRendererCategory,
    QgsSingleSymbolRenderer,
    QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
    QgsVectorLayerSimpleLabeling, QgsRuleBasedLabeling, QgsProperty,
    QgsUnitTypes,
)
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog,
    QProgressBar, QTextEdit, QGroupBox, QMessageBox,
    QFrame, QApplication, QCheckBox, QScrollArea, QWidget,
)

# =============================================================================
# CAPAS OPCIONALES — Superficies de Agua con simbología IGAC verificada
# Catálogo Resoluciones 471 y 529 de 2020 (pág. 91-108)
# =============================================================================
# Estructura: nombre_interno → (shp, grupo_GDB, capa_GDB, tipo_geom, simbología)
# tipo_geom: "poligono", "linea", "punto"
# simbologia: diccionario con parámetros verificados del catálogo

CAPAS_OPCIONALES = {
    "Laguna": {
        "shp": "Laguna.shp", "grupo": "Superficies_Agua", "capa": "Laguna",
        "geom": "poligono",
        "fill": (214,237,255), "stroke": (0,112,255), "stroke_pt": 0.13,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Embalse": {
        "shp": "Embalse.shp", "grupo": "Superficies_Agua", "capa": "Embalse",
        "geom": "poligono",
        "fill": (219,247,255), "stroke": (115,178,254), "stroke_pt": 0.13,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Cienaga": {
        "shp": "Cienaga.shp", "grupo": "Superficies_Agua", "capa": "Cienaga",
        "geom": "poligono",
        "fill": (214,237,255), "stroke": (0,112,255), "stroke_pt": 0.13,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Cienaga_P": {
        "shp": "Cienaga_P.shp", "grupo": "Superficies_Agua", "capa": "Cienaga_P",
        "geom": "punto",
        "fill": (0,112,255), "stroke": (0,112,255), "stroke_pt": 2.0,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Jaguey_P": {
        "shp": "Jaguey_P.shp", "grupo": "Superficies_Agua", "capa": "Jaguey_P",
        "geom": "punto",
        "fill": (0,169,230), "stroke": (0,169,230), "stroke_pt": 3.74*PT,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Jaguey_R": {
        "shp": "Jaguey_R.shp", "grupo": "Superficies_Agua", "capa": "Jaguey_R",
        "geom": "poligono",
        "fill": (219,246,255), "stroke": (115,178,254), "stroke_pt": 0.13,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Pantano": {
        "shp": "Pantano.shp", "grupo": "Superficies_Agua", "capa": "Pantano",
        "geom": "poligono",
        "fill": (255,255,255), "stroke": (102,205,171), "stroke_pt": 0.5,
        "trama": True, "trama_color": (102,205,171),
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (60,150,100),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Humedal": {
        "shp": "Humedal.shp", "grupo": "Superficies_Agua", "capa": "Humedal",
        "geom": "poligono",
        "fill": (255,255,255), "stroke": (102,205,171), "stroke_pt": 0.5,
        "trama": True, "trama_color": (102,205,171),
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (60,150,100),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Manglar": {
        "shp": "Manglar.shp", "grupo": "Superficies_Agua", "capa": "Manglar",
        "geom": "poligono",
        "fill": (255,255,255), "stroke": (56,168,0), "stroke_pt": 0.4,
        "trama": True, "trama_color": (112,168,4),
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (60,150,100),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Morichal": {
        "shp": "Morichal.shp", "grupo": "Superficies_Agua", "capa": "Morichal",
        "geom": "poligono",
        "fill": (255,255,255), "stroke": (102,204,172), "stroke_pt": 0.5,
        "trama": True, "trama_color": (82,169,148),
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (60,150,100),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Isla": {
        "shp": "Isla.shp", "grupo": "Superficies_Agua", "capa": "Isla",
        "geom": "poligono",
        "fill": (240,230,180), "stroke": (180,160,80), "stroke_pt": 0.13,
        "label_font": "Arial Narrow", "label_tam": 9, "label_neg": False,
        "label_cur": True, "label_color": (150,100,0),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Manantial": {
        "shp": "Manantial.shp", "grupo": "Superficies_Agua", "capa": "Manantial",
        "geom": "punto",
        "fill": (0,112,255), "stroke": (0,112,255), "stroke_pt": 7.69*PT,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Madrevieja_L": {
        "shp": "Madrevieja_L.shp", "grupo": "Superficies_Agua", "capa": "Madrevieja_L",
        "geom": "linea",
        "fill": (0,115,255), "stroke": (0,115,255), "stroke_pt": 0.45,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Madrevieja_R": {
        "shp": "Madrevieja_R.shp", "grupo": "Superficies_Agua", "capa": "Madrevieja_R",
        "geom": "poligono",
        "fill": (214,237,255), "stroke": (0,112,255), "stroke_pt": 0.13,
        "label_font": "Book Antiqua", "label_tam": 8, "label_neg": True,
        "label_cur": True, "label_color": (0,112,255),
        "label_campo": ["NOMBRE_GEO","NOMBRE_GEOGRAFICO","NOMBRE","NMG"],
    },
    "Linea_de_Mar": {
        "shp": "Linea_Costera.shp", "grupo": "Superficies_Agua", "capa": "Linea_Costera",
        "geom": "linea",
        "fill": (0,112,255), "stroke": (0,112,255), "stroke_pt": 0.57,
        "label_font": "Arial Narrow", "label_tam": 8, "label_neg": False,
        "label_cur": False, "label_color": (0,112,255),
        "label_campo": [],
    },
}

def aplicar_simbologia_opcional(lyr, info, nombre):
    """Aplica simbología IGAC verificada a una capa opcional."""
    r_f, g_f, b_f = info["fill"]
    r_s, g_s, b_s = info["stroke"]
    w = info["stroke_pt"] * PT

    if info["geom"] == "poligono":
        sym = QgsFillSymbol.createSimple({
            "color": f"{r_f},{g_f},{b_f}",
            "outline_color": f"{r_s},{g_s},{b_s}",
            "outline_width": str(w),
        })
        lyr.setRenderer(QgsSingleSymbolRenderer(sym))

    elif info["geom"] == "linea":
        sl = QgsSimpleLineSymbolLayer()
        sl.setColor(QColor(r_s, g_s, b_s))
        sl.setWidth(info["stroke_pt"] * PT)
        sym = QgsLineSymbol(); sym.deleteSymbolLayer(0); sym.appendSymbolLayer(sl)
        lyr.setRenderer(QgsSingleSymbolRenderer(sym))

    elif info["geom"] == "punto":
        sym = marcador("circle", r_f, g_f, b_f, info["stroke_pt"])
        lyr.setRenderer(QgsSingleSymbolRenderer(sym))

    # Etiqueta
    if info.get("label_campo"):
        campo = detectar_campo(lyr, info["label_campo"])
        if campo:
            lbl = make_label(
                campo,
                fuente=info["label_font"],
                tam=info["label_tam"],
                neg=info["label_neg"],
                cur=info["label_cur"],
                color=info["label_color"],
                filtro=f'"{campo}" IS NOT NULL AND "{campo}" != \'\''
            )
            lyr.setLabeling(QgsVectorLayerSimpleLabeling(lbl))
            lyr.setLabelsEnabled(True)

    lyr.triggerRepaint()



# =============================================================================
# CONSTANTES
# =============================================================================
PT       = 0.352778   # 1 punto tipográfico en mm
CRS_DEST = "EPSG:9377"

# Mapeo: nombre interno → (shp, grupo_GDB/MDB, nombre_capa_GDB/MDB)
CAPAS_IGAC = {
    "Curvas_Nivel":     ("Curva_Nivel.shp",      "Relieve",
                         "Curva_Nivel"),
    "Drenaje_Sencillo": ("Drenaje_Sencillo.shp",  "Superficies_Agua",
                         "Drenaje_Sencillo"),
    "Drenaje_Doble":    ("Drenaje_Doble.shp",     "Superficies_Agua",
                         "Drenaje_Doble"),
    "Vias":             ("Via.shp",               "Transporte_Terrestre",
                         "Via"),
    "Construcciones":   ("Construccion_P.shp",    "Edificacion_ObraCivil",
                         "Construccion_P"),
    "Orografia":        ("Orografia.shp",         "Toponimos",
                         "Orografia"),
    "Administrativo":   ("Administrativo_P.shp",
                         "Entidades_Territoriales_y_Unidades_Administrativas",
                         "Administrativo_P"),
}

# Detección inteligente de campos — soporta múltiples versiones del catálogo IGAC
CAMPOS_CANDIDATOS = {
    "Curvas_Nivel": {
        "tipo":   ["TIPO_CURVA", "TIPO_CURVA_NIVEL", "TIPO", "TYPE",
                   "COD_CURVA", "CURVA_TIP"],
        "altura": ["ALTURA_SOB", "ALTURA_SOBRE_NIVEL_MAR", "ALTURA",
                   "ELEV", "COTA", "ALT"],
    },
    "Drenaje_Sencillo": {
        "estado": ["ESTADO_DRE", "ESTADO_DRENAJE", "ESTADO", "TYPE",
                   "TIPO", "CLASE"],
        "nombre": ["NOMBRE_GEO", "NOMBRE_GEOGRAFICO", "NOMBRE",
                   "NMG", "NAME", "NOM"],
    },
    "Drenaje_Doble": {
        "tipo":   ["TIPO", "TYPE", "CLASE", "CLASS", "TIPO_CUERPO"],
        "nombre": ["NOMBRE_GEO", "NOMBRE_GEOGRAFICO", "NOMBRE",
                   "NMG", "NAME", "NOM"],
    },
    "Vias": {
        "tipo":   ["TIPO_VIA", "TIPO", "TYPE", "CLASS",
                   "CLASE_VIA", "VIA_TIPO"],
        "nombre": ["NOMBRE_GEO", "NOMBRE_GEOGRAFICO", "NOMBRE",
                   "NMG", "NAME", "NOM"],
    },
    "Construcciones": {
        "codigo": ["CODIGO_USO", "CODIGO_USO_EDIFICACION", "CODIGO",
                   "CODE", "USO", "COD_USO"],
        "nombre": ["NOMBRE_GEO", "NOMBRE_GEOGRAFICO", "NOMBRE",
                   "NMG", "NAME", "NOM"],
    },
    "Orografia": {
        "codigo": ["CODIGO_NOM", "CODIGO_NOMBRE", "CODIGO",
                   "CODE", "COD_NOM", "COD"],
        "nombre": ["NOMBRE_GEO", "NOMBRE_GEOGRAFICO", "NOMBRE",
                   "NMG", "NAME", "NOM"],
    },
    "Administrativo": {
        "codigo": ["CODIGO_NOM", "CODIGO_NOMBRE", "CODIGO",
                   "CODE", "COD_NOM", "COD"],
        "nombre": ["NOMBRE_GEO", "NOMBRE_GEOGRAFICO", "NOMBRE",
                   "NMG", "NAME", "NOM"],
    },
}

# Mapeo de campos largos MDB → nombres truncados SHP (10 caracteres)
CAMPOS_MDB_A_SHP = {
    "TIPO_CURVA_NIVEL":       "TIPO_CURVA",
    "ALTURA_SOBRE_NIVEL_MAR": "ALTURA_SOB",
    "ESTADO_DRENAJE":         "ESTADO_DRE",
    "NOMBRE_GEOGRAFICO":      "NOMBRE_GEO",
    "CODIGO_USO_EDIFICACION": "CODIGO_USO",
    "CODIGO_NOMBRE":          "CODIGO_NOM",
    "FECHA_MODIFICACION":     "FECHA_MODI",
    "ESTADO_SUPERFICIE":      "ESTADO_SUP",
    "NUMERO_CARRILES":        "NUMERO_CAR",
    "ACCESIBILIDAD":          "ACCESIBILI",
}

# =============================================================================
# CATÁLOGOS DE SIMBOLOGÍA IGAC (verificados del PDF oficial pág 50-142)
# =============================================================================
CURVAS = {
    "1000": ("Curva Índice",     (168,112,0),  0.71),
    "1010": ("Curva Intermedia", (230,159,18), 0.35),
    "1030": ("Suplementaria",    (252,173,20), 0.18),
}

ORO = {
    "8101":("Arial Narrow",9,(150,100,0)),  "8103":("Arial Narrow",9,(150,100,0)),
    "8106":("Arial Narrow",10,(150,100,0)), "8107":("Arial Narrow",9,(150,100,0)),
    "8108":("Arial Narrow",9,(150,100,0)),  "8109":("Arial Narrow",9,(150,100,0)),
    "8110":("Arial Narrow",9,(150,100,0)),  "8111":("Arial Narrow",9,(150,100,0)),
    "8112":("Arial Narrow",9,(150,100,0)),  "8114":("Arial Narrow",9,(150,100,0)),
    "8134":("Book Antiqua",9,(0,112,255)),  "8116":("Arial Narrow",9,(150,100,0)),
    "8115":("Arial Narrow",9,(150,100,0)),  "8117":("Arial Narrow",9,(150,100,0)),
    "8118":("Arial Narrow",9,(150,100,0)),  "8119":("Arial Narrow",9,(150,100,0)),
    "8132":("Book Antiqua",9,(0,112,255)),  "8121":("Arial Narrow",9,(150,100,0)),
    "8135":("Book Antiqua",9,(60,150,100)), "8122":("Arial Narrow",9,(150,100,0)),
    "8123":("Arial Narrow",9,(150,100,0)),  "8125":("Arial Narrow",9,(150,100,0)),
    "8126":("Arial Narrow",9,(150,100,0)),  "8127":("Arial Narrow",9,(150,100,0)),
    "8128":("Arial Narrow",9,(150,100,0)),  "8129":("Arial Narrow",9,(150,100,0)),
    "8104":("Arial Narrow",9,(150,100,0)),  "8130":("Arial Narrow",9,(150,100,0)),
    "8136":("Arial Narrow",9,(150,100,0)),
}

ADMIN = {
    "8301":("Bookman Old Style",11,True, False),
    "8302":("Arial Narrow",     9, True, False),
    "8303":("Zurich LtCn BT",   9, False,False),
    "8304":("Arial Narrow",     10,True, False),
    "8305":("Palatino Linotype",8, True, False),
    "8325":("Bookman Old Style",7, True, False),
    "8328":("Palatino Linotype",10,True, False),
    "8307":("Palatino Linotype",10,True, False),
    "8308":("Arial Narrow",     9, True, False),
    "8309":("Bookman Old Style",13,False,False),
    "8310":("Bookman Old Style",11,False,False),
    "8323":("Palatino Linotype",9, True, False),
    "8311":("Arial Narrow",     8, False,False),
    "8312":("Bookman Old Style",11,False,False),
    "8313":("Arial Narrow",     9, True, False),
    "8314":("Arial Narrow",     9, True, False),
    "8315":("Bookman Old Style",11,False,False),
    "8316":("Arial Narrow",     9, False,False),
    "8317":("Bookman Old Style",13,False,False),
    "8318":("Arial Narrow",     9, False,False),
    "8319":("Arial Narrow",     9, False,False),
    "8320":("Arial Narrow",     9, False,False),
    "8321":("Arial Narrow",     9, False,False),
    "8322":("Arial Narrow",     9, False,False),
    "8326":("Arial Narrow",     9, False,False),
    "8327":("Zurich LtCn BT",   9, False,False),
    "8351":("Palatino Linotype",8, True, False),
    "8306":("Arial Narrow",     8, False,False),
    "8350":("Arial Narrow",     8, False,False),
}

CONSTRUCCIONES = {
    "2302":("Instalación Minera",        "square",          104,104,104,1.5),
    "2320":("Sitio de Interés",          "square",          104,104,104,1.5),
    "3413":("Faro",                      "star",            0,  0,  0,  2.0),
    "3680":("Industria",                 "square",          104,104,104,1.5),
    "3686":("Cementerio",                "cross",           0,  0,  0,  2.0),
    "3692":("Instalación Minera",        "square",          104,104,104,1.5),
    "4101":("Otras Construcciones",      "square",          104,104,104,1.5),
    "4112":("Establecimiento Educativo", "filled_arrowhead",0,  0,  0,  2.0),
    "4119":("Salud",                     "cross",           0,  0,  0,  2.0),
    "4129":("Iglesia",                   "cross",           0,  0,  0,  2.0),
    "4131":("Hotel",                     "square",          104,104,104,1.5),
    "4165":("Monumento",                 "triangle",        0,  0,  0,  2.0),
    "4166":("Seguridad",                 "square",          104,104,104,1.5),
    "5608":("Silo",                      "square",          104,104,104,1.5),
    "5610":("Tanque",                    "square",          104,104,104,1.5),
    "5620":("Pozo",                      "circle",          0,  0,  0,  2.0),
    "5684":("Molino",                    "star4",           0,  0,  0,  2.0),
}

# =============================================================================
# FUENTES TIPOGRÁFICAS
# =============================================================================
FUENTES_REQUERIDAS = {
    "Palatino Linotype": {"alternativa": "IM Fell English",
        "url": "https://fonts.google.com/download?family=IM+Fell+English"},
    "Zurich LtCn BT":   {"alternativa": "Barlow Condensed",
        "url": "https://fonts.google.com/download?family=Barlow+Condensed"},
    "Bookman Old Style": {"alternativa": "Libre Baskerville",
        "url": "https://fonts.google.com/download?family=Libre+Baskerville"},
    "Book Antiqua":      {"alternativa": "Cormorant Garamond",
        "url": "https://fonts.google.com/download?family=Cormorant+Garamond"},
}

def fuente_disponible(nombre):
    db = QFontDatabase(); instaladas = db.families()
    if nombre in instaladas: return nombre
    if nombre in FUENTES_REQUERIDAS:
        alt = FUENTES_REQUERIDAS[nombre]["alternativa"]
        if alt in instaladas: return alt
    return "Arial"

# =============================================================================
# DETECCIÓN INTELIGENTE DE CAMPOS
# =============================================================================
def detectar_campo(lyr, candidatos):
    """Busca el primer campo disponible de la lista de candidatos."""
    nombres = {c.name().upper(): c.name() for c in lyr.fields()}
    for cand in candidatos:
        if cand.upper() in nombres:
            return nombres[cand.upper()]
    return None

def obtener_campos(lyr, nombre_capa):
    """Retorna los campos detectados para una capa. Admite cualquier versión del catálogo."""
    if nombre_capa not in CAMPOS_CANDIDATOS:
        return {}
    resultado = {}
    for campo_interno, candidatos in CAMPOS_CANDIDATOS[nombre_capa].items():
        campo = detectar_campo(lyr, candidatos)
        resultado[campo_interno] = campo
    return resultado

# =============================================================================
# BÚSQUEDA DE CAPAS EN PLANCHA (SHP / GDB / MDB)
# =============================================================================
def buscar_uri(carpeta_plancha, nombre_interno):
    shp_nombre, grupo_gdb, capa_gdb = CAPAS_IGAC[nombre_interno]
    # 1. SHP directo
    fp = os.path.join(carpeta_plancha, shp_nombre)
    if os.path.exists(fp):
        return fp
    # 2. GDB
    for entry in os.listdir(carpeta_plancha):
        if entry.lower().endswith(".gdb") and \
           os.path.isdir(os.path.join(carpeta_plancha, entry)):
            ruta = os.path.join(carpeta_plancha, entry)
            for uri in [f"{ruta}|layername={capa_gdb}",
                        f"{ruta}|layername={grupo_gdb}/{capa_gdb}"]:
                if QgsVectorLayer(uri, "t", "ogr").isValid():
                    return uri
    # 3. MDB
    for entry in os.listdir(carpeta_plancha):
        if entry.lower().endswith(".mdb"):
            ruta = os.path.join(carpeta_plancha, entry)
            uri  = f"{ruta}|layername={capa_gdb}"
            if QgsVectorLayer(uri, "t", "ogr").isValid():
                return uri
    return None

def normalizar_campos(uri, tmp_dir, nombre):
    """Renombra campos largos MDB→SHP y elimina campos Binary."""
    from PyQt5.QtCore import QVariant
    lyr = QgsVectorLayer(uri, "x", "ogr")
    if not lyr.isValid(): return uri
    campos = lyr.fields()
    necesita = any(c.name() in CAMPOS_MDB_A_SHP or
                   c.type() in [QVariant.ByteArray, QVariant.UserType]
                   for c in campos)
    if not necesita: return uri
    mapping = []
    for c in campos:
        if c.type() in [QVariant.ByteArray, QVariant.UserType]:
            continue
        nuevo = CAMPOS_MDB_A_SHP.get(c.name(), c.name())
        mapping.append({"name": nuevo, "type": c.type(),
                        "length": c.length(), "precision": c.precision(),
                        "expression": f'"{c.name()}"'})
    gpkg = os.path.join(tmp_dir, f"{nombre}_norm.gpkg")
    processing.run("native:refactorfields",
                   {"INPUT": uri, "FIELDS_MAPPING": mapping, "OUTPUT": gpkg})
    return gpkg

# =============================================================================
# FUNCIONES DE SIMBOLOGÍA
# =============================================================================
def linea_sl(rgb, w_pt, patron=None):
    sl = QgsSimpleLineSymbolLayer()
    sl.setColor(QColor(*rgb)); sl.setWidth(w_pt * PT)
    if patron:
        sl.setUseCustomDashPattern(True)
        sl.setCustomDashVector([p * PT for p in patron])
    return sl

def marcador(forma_str, r, g, b, tam_mm, br=None, bg=None, bb=None):
    formas = {
        "square":           QgsSimpleMarkerSymbolLayer.Square,
        "circle":           QgsSimpleMarkerSymbolLayer.Circle,
        "cross":            QgsSimpleMarkerSymbolLayer.Cross,
        "triangle":         QgsSimpleMarkerSymbolLayer.Triangle,
        "star":             QgsSimpleMarkerSymbolLayer.Star,
        "star4":            QgsSimpleMarkerSymbolLayer.Star,
        "filled_arrowhead": QgsSimpleMarkerSymbolLayer.ArrowHead,
    }
    sl = QgsSimpleMarkerSymbolLayer()
    sl.setShape(formas.get(forma_str, QgsSimpleMarkerSymbolLayer.Square))
    sl.setColor(QColor(r, g, b))
    sl.setSize(tam_mm); sl.setSizeUnit(QgsUnitTypes.RenderMillimeters)
    sl.setStrokeColor(QColor(br or r, bg or g, bb or b))
    sl.setStrokeWidth(0.2)
    sym = QgsMarkerSymbol(); sym.deleteSymbolLayer(0); sym.appendSymbolLayer(sl)
    return sym

def make_label(field, fuente="Arial", tam=7, neg=False, cur=False,
               color=(0,0,0), placement=QgsPalLayerSettings.AroundPoint,
               filtro=None):
    if not field: return QgsPalLayerSettings()
    fuente_real = fuente_disponible(fuente)
    cfg = QgsPalLayerSettings(); cfg.fieldName = field
    tf = QgsTextFormat()
    f = QFont(fuente_real); f.setBold(neg); f.setItalic(cur)
    tf.setFont(f); tf.setSize(tam)
    tf.setSizeUnit(QgsUnitTypes.RenderPoints); tf.setColor(QColor(*color))
    b = QgsTextBufferSettings(); b.setEnabled(True); b.setSize(0.5)
    b.setColor(QColor(255,255,255)); tf.setBuffer(b)
    cfg.setFormat(tf); cfg.placement = placement
    if filtro:
        cfg.dataDefinedProperties().setProperty(
            QgsPalLayerSettings.Show, QgsProperty.fromExpression(filtro))
    return cfg

def simbolo_via(tipo):
    s = QgsLineSymbol(); s.deleteSymbolLayer(0); t = str(tipo)
    if t=="1":   s.appendSymbolLayer(linea_sl((230,0,0),2.0))
    elif t=="2": s.appendSymbolLayer(linea_sl((230,0,0),2.0));  s.appendSymbolLayer(linea_sl((255,255,255),1.42,[6,6]))
    elif t=="3": s.appendSymbolLayer(linea_sl((230,0,0),1.0))
    elif t=="4": s.appendSymbolLayer(linea_sl((230,0,0),1.0));  s.appendSymbolLayer(linea_sl((255,255,255),0.57,[5,5]))
    elif t=="5": s.appendSymbolLayer(linea_sl((230,0,0),1.0));  s.appendSymbolLayer(linea_sl((255,255,255),0.57)); s.appendSymbolLayer(linea_sl((255,0,0),0.99,[4,2]))
    elif t=="6": s.appendSymbolLayer(linea_sl((230,0,0),0.18,[4,1.6]))
    elif t=="7": s.appendSymbolLayer(linea_sl((0,0,0),0.16,[6,2,4,2,4,2,2]))
    elif t=="8": s.appendSymbolLayer(linea_sl((142,45,168),0.31))
    else:        s.appendSymbolLayer(linea_sl((120,120,120),0.4))
    return s

# =============================================================================
# SIMBOLOGÍA POR CAPA — usa campos detectados automáticamente
# =============================================================================
def aplicar_simbologia(capas_cargadas, lim_capa, log_fn=None):
    def log(msg):
        if log_fn: log_fn(f"   {msg}")

    def get(n): return capas_cargadas.get(n)

    # Curvas de Nivel
    if get("Curvas_Nivel"):
        l = get("Curvas_Nivel")
        campos = obtener_campos(l, "Curvas_Nivel")
        campo_tipo   = campos.get("tipo")
        campo_altura = campos.get("altura")
        if not campo_tipo:
            log("⚠ Curvas: no se encontró campo de tipo — se aplica símbolo simple")
            sl = QgsSimpleLineSymbolLayer()
            sl.setColor(QColor(168,112,0)); sl.setWidth(0.35*PT)
            sym = QgsLineSymbol(); sym.deleteSymbolLayer(0); sym.appendSymbolLayer(sl)
            l.setRenderer(QgsSingleSymbolRenderer(sym))
        else:
            tipos = sorted(set(str(f[campo_tipo]) for f in l.getFeatures()))
            cats  = []
            for t in tipos:
                if t in CURVAS:
                    lab, rgb, w = CURVAS[t]
                else:
                    lab, rgb, w = f"Curva {t}", (200,140,0), 0.25
                sl = QgsSimpleLineSymbolLayer()
                sl.setColor(QColor(*rgb)); sl.setWidth(w*PT)
                sym = QgsLineSymbol(); sym.deleteSymbolLayer(0); sym.appendSymbolLayer(sl)
                cats.append(QgsRendererCategory(t, sym, lab))
            l.setRenderer(QgsCategorizedSymbolRenderer(campo_tipo, cats))
            log(f"Curvas: campo '{campo_tipo}' | tipos {tipos}")
        if campo_altura and campo_tipo:
            filtro = f'"{campo_tipo}" = 1000' if campo_tipo == "TIPO_CURVA" else None
            l.setLabeling(QgsVectorLayerSimpleLabeling(make_label(
                campo_altura, fuente="Arial Narrow", tam=6, color=(100,68,0),
                placement=QgsPalLayerSettings.Line, filtro=filtro)))
            l.setLabelsEnabled(True)
        l.triggerRepaint()

    # Drenaje Sencillo
    if get("Drenaje_Sencillo"):
        l = get("Drenaje_Sencillo")
        campos = obtener_campos(l, "Drenaje_Sencillo")
        campo_estado = campos.get("estado")
        campo_nombre = campos.get("nombre")
        if campo_estado:
            s_int = QgsLineSymbol(); s_int.deleteSymbolLayer(0)
            s_int.appendSymbolLayer(linea_sl((0,112,255),0.46,[11.9,1.7,0.85,1.7,0.85]))
            sl_p  = QgsSimpleLineSymbolLayer()
            sl_p.setColor(QColor(0,112,255)); sl_p.setWidth(0.45*PT)
            s_p   = QgsLineSymbol(); s_p.deleteSymbolLayer(0); s_p.appendSymbolLayer(sl_p)
            tipos = sorted(set(str(f[campo_estado]) for f in l.getFeatures()))
            cats  = []
            for t in tipos:
                if t in ("5101","1","Permanente"):
                    cats.append(QgsRendererCategory(t, s_p, "Permanente"))
                else:
                    cats.append(QgsRendererCategory(t, s_int, "Intermitente"))
            l.setRenderer(QgsCategorizedSymbolRenderer(campo_estado, cats))
        else:
            sl = QgsSimpleLineSymbolLayer(); sl.setColor(QColor(0,112,255)); sl.setWidth(0.45*PT)
            sym = QgsLineSymbol(); sym.deleteSymbolLayer(0); sym.appendSymbolLayer(sl)
            l.setRenderer(QgsSingleSymbolRenderer(sym))
        if campo_nombre:
            filtro_d = f'"{campo_nombre}" IS NOT NULL AND "{campo_nombre}" != \'\''
            l.setLabeling(QgsVectorLayerSimpleLabeling(make_label(
                campo_nombre, fuente="Book Antiqua", tam=8, neg=True, cur=True,
                color=(0,112,255), placement=QgsPalLayerSettings.Curved,
                filtro=filtro_d)))
            l.setLabelsEnabled(True)
        l.triggerRepaint()

    # Drenaje Doble
    if get("Drenaje_Doble"):
        l = get("Drenaje_Doble")
        campos = obtener_campos(l, "Drenaje_Doble")
        campo_tipo   = campos.get("tipo")
        campo_nombre = campos.get("nombre")
        if campo_tipo:
            tipos = sorted(set(str(f[campo_tipo]) for f in l.getFeatures()))
            cats  = []
            for t in tipos:
                if t in ("0","Cuerpo de Agua","CuerpoAgua"):
                    cats.append(QgsRendererCategory(t, QgsFillSymbol.createSimple({
                        "color":"214,237,255","outline_color":"90,112,255",
                        "outline_width":str(0.13*PT)}), "Cuerpo de Agua"))
                else:
                    cats.append(QgsRendererCategory(t, QgsFillSymbol.createSimple({
                        "color":"255,250,180","outline_color":"255,160,30",
                        "outline_width":str(0.71*PT)}), "Lecho Seco"))
            l.setRenderer(QgsCategorizedSymbolRenderer(campo_tipo, cats))
        else:
            l.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({
                "color":"214,237,255","outline_color":"90,112,255",
                "outline_width":str(0.13*PT)})))
        if campo_nombre:
            l.setLabeling(QgsVectorLayerSimpleLabeling(make_label(
                campo_nombre, fuente="Book Antiqua", tam=8, neg=True, cur=True,
                color=(0,112,255),
                filtro=f'"{campo_nombre}" IS NOT NULL AND "{campo_nombre}" != \'\'')))
            l.setLabelsEnabled(True)
        l.triggerRepaint()

    # Vías
    if get("Vias"):
        l = get("Vias")
        campos = obtener_campos(l, "Vias")
        campo_tipo = campos.get("tipo")
        if campo_tipo:
            labs  = {"1":"Panamericana","2":"Doble calzada","3":"Pavimentada",
                     "4":"Sin pavimentar","5":"Sin pavimentar angosta",
                     "6":"Carreteable","7":"Camino / Sendero","8":"Peatonal urbana"}
            tipos = sorted(set(str(f[campo_tipo]) for f in l.getFeatures()))
            cats  = [QgsRendererCategory(t, simbolo_via(t),
                     labs.get(t, f"Tipo {t}")) for t in tipos]
            l.setRenderer(QgsCategorizedSymbolRenderer(campo_tipo, cats))
        else:
            sl = QgsSimpleLineSymbolLayer(); sl.setColor(QColor(230,0,0)); sl.setWidth(1.0*PT)
            sym = QgsLineSymbol(); sym.deleteSymbolLayer(0); sym.appendSymbolLayer(sl)
            l.setRenderer(QgsSingleSymbolRenderer(sym))
        l.triggerRepaint()

    # Construcciones
    if get("Construcciones"):
        l = get("Construcciones")
        campos = obtener_campos(l, "Construcciones")
        campo_codigo = campos.get("codigo")
        campo_nombre = campos.get("nombre")
        if campo_codigo:
            tipos = sorted(set(str(f[campo_codigo]) for f in l.getFeatures()))
            cats  = []
            for t in tipos:
                if t in CONSTRUCCIONES:
                    desc, forma, r, g, b, tam = CONSTRUCCIONES[t]
                    cats.append(QgsRendererCategory(t, marcador(forma,r,g,b,tam), desc))
                else:
                    cats.append(QgsRendererCategory(t,
                        marcador("square",104,104,104,1.5), f"Construcción {t}"))
            l.setRenderer(QgsCategorizedSymbolRenderer(campo_codigo, cats))
        else:
            l.setRenderer(QgsSingleSymbolRenderer(marcador("square",104,104,104,1.5)))
        if campo_nombre:
            l.setLabeling(QgsVectorLayerSimpleLabeling(make_label(
                campo_nombre, fuente="Arial Narrow", tam=7, neg=True, color=(0,0,0),
                filtro=f'"{campo_nombre}" IS NOT NULL AND "{campo_nombre}" != \'\'')))
            l.setLabelsEnabled(True)
        l.triggerRepaint()

    # Orografía
    if get("Orografia"):
        l = get("Orografia")
        campos = obtener_campos(l, "Orografia")
        campo_codigo = campos.get("codigo")
        campo_nombre = campos.get("nombre")
        l.setRenderer(QgsSingleSymbolRenderer(marcador("triangle",150,90,30,2.5,90,50,10)))
        if campo_nombre and campo_codigo:
            root_o = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            for cod,(fuente,tam,color) in ORO.items():
                cfg = make_label(campo_nombre, fuente=fuente, tam=tam,
                                 neg=False, cur=True, color=color,
                                 placement=QgsPalLayerSettings.AroundPoint)
                r = QgsRuleBasedLabeling.Rule(cfg)
                r.setFilterExpression(f'"{campo_codigo}" = {cod}')
                root_o.appendChild(r)
            l.setLabeling(QgsRuleBasedLabeling(root_o))
            l.setLabelsEnabled(True)
        elif campo_nombre:
            l.setLabeling(QgsVectorLayerSimpleLabeling(make_label(
                campo_nombre, fuente="Arial Narrow", tam=9, cur=True,
                color=(150,100,0))))
            l.setLabelsEnabled(True)
        l.triggerRepaint()

    # Administrativo
    if get("Administrativo"):
        l = get("Administrativo")
        campos = obtener_campos(l, "Administrativo")
        campo_codigo = campos.get("codigo")
        campo_nombre = campos.get("nombre")
        l.setRenderer(QgsSingleSymbolRenderer(marcador("circle",0,0,0,1.8,255,255,255)))
        if campo_nombre and campo_codigo:
            root_a = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            for cod,(fuente,tam,neg,cur) in ADMIN.items():
                cfg = make_label(campo_nombre, fuente=fuente, tam=tam,
                                 neg=neg, cur=cur, color=(0,0,0),
                                 placement=QgsPalLayerSettings.AroundPoint,
                                 filtro=(f'"{campo_codigo}" = {cod} AND '
                                         f'"{campo_nombre}" IS NOT NULL AND '
                                         f'"{campo_nombre}" != \'\''))
                r = QgsRuleBasedLabeling.Rule(cfg)
                r.setDescription(f"{cod}")
                r.setFilterExpression(f'"{campo_codigo}" = {cod}')
                root_a.appendChild(r)
            l.setLabeling(QgsRuleBasedLabeling(root_a))
            l.setLabelsEnabled(True)
        elif campo_nombre:
            l.setLabeling(QgsVectorLayerSimpleLabeling(make_label(
                campo_nombre, fuente="Arial Narrow", tam=9, color=(0,0,0))))
            l.setLabelsEnabled(True)
        l.triggerRepaint()

    # Límite
    if lim_capa:
        lim_capa.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({
            "color":"0,0,0,0","outline_color":"200,0,0",
            "outline_width":str(0.66*PT),"style":"no"})))
        lim_capa.triggerRepaint()

# =============================================================================
# VENTANA PRINCIPAL
# =============================================================================
class VentanaIGAC(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurador Cartografía IGAC 1:25.000")
        self.setMinimumWidth(620)
        self.setMaximumHeight(850)
        self.setModal(False)
        self._cfg = None
        self._construir_ui()

    def _construir_ui(self):
        # Layout con scroll para que funcione en cualquier resolución de pantalla
        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.setSpacing(0)

        # Área de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_content = QWidget()
        lay = QVBoxLayout(scroll_content)
        lay.setSpacing(8); lay.setContentsMargins(14,14,14,10)
        scroll_area.setWidget(scroll_content)
        main_lay.addWidget(scroll_area)

        # Encabezado institucional nativo PyQt5 — nítido a cualquier resolución
        enc = QFrame()
        enc.setStyleSheet("QFrame{background-color:#1f618d;border-radius:6px;}")
        enc_lay = QVBoxLayout(enc)
        enc_lay.setContentsMargins(0,0,0,0); enc_lay.setSpacing(0)

        # Buscar logos individuales en la carpeta del script
        rutas_buscar = [_SCRIPT_DIR, os.getcwd(), os.path.expanduser("~/Documents")]
        try:
            rutas_buscar.insert(0, os.path.dirname(os.path.abspath(__file__)))
        except NameError:
            pass

        logo_udenar = next((os.path.join(r,"logo_udenar.png")
                            for r in rutas_buscar
                            if os.path.exists(os.path.join(r,"logo_udenar.png"))), None)
        logo_facia  = next((os.path.join(r,"logo_facia.png")
                            for r in rutas_buscar
                            if os.path.exists(os.path.join(r,"logo_facia.png"))), None)

        # Fila superior: logos + texto
        fila_sup = QHBoxLayout()
        fila_sup.setContentsMargins(10,8,10,4); fila_sup.setSpacing(8)

        if logo_udenar:
            lbl_u = QLabel()
            lbl_u.setPixmap(QPixmap(logo_udenar).scaled(
                60,60,Qt.KeepAspectRatio,Qt.SmoothTransformation))
            fila_sup.addWidget(lbl_u)

        if logo_udenar and logo_facia:
            sep = QFrame(); sep.setFrameShape(QFrame.VLine)
            sep.setStyleSheet("color:rgba(255,255,255,80);"); sep.setMaximumWidth(1)
            fila_sup.addWidget(sep)

        if logo_facia:
            lbl_f = QLabel()
            lbl_f.setPixmap(QPixmap(logo_facia).scaled(
                60,60,Qt.KeepAspectRatio,Qt.SmoothTransformation))
            fila_sup.addWidget(lbl_f)

        if logo_udenar or logo_facia:
            sep2 = QFrame(); sep2.setFrameShape(QFrame.VLine)
            sep2.setStyleSheet("color:rgba(255,255,255,60);"); sep2.setMaximumWidth(1)
            fila_sup.addWidget(sep2)

        txt_lay = QVBoxLayout(); txt_lay.setSpacing(3)
        lbl_titulo = QLabel("Configurador Cartografía Básica IGAC 1:25.000")
        lbl_titulo.setStyleSheet(
            "color:white;font-size:15px;font-weight:bold;"
            "font-family:\'Bookman Old Style\',Georgia,serif;")
        lbl_escala = QLabel("Escala 1:25.000  ·  EPSG:9377 CTM12  ·  Colombia")
        lbl_escala.setStyleSheet(
            "color:#d6eaf8;font-size:11px;font-family:\'Arial Narrow\',Arial;")
        txt_lay.addWidget(lbl_titulo); txt_lay.addWidget(lbl_escala)
        fila_sup.addLayout(txt_lay); fila_sup.addStretch()
        enc_lay.addLayout(fila_sup)

        # Línea verde separadora
        linea = QFrame(); linea.setFrameShape(QFrame.HLine)
        linea.setStyleSheet("background-color:#27ae60;max-height:2px;border:none;")
        linea.setMaximumHeight(2)
        enc_lay.addWidget(linea)

        # Footer oscuro con institución y autor
        footer = QFrame()
        footer.setStyleSheet(
            "QFrame{background-color:#154360;border-radius:0 0 6px 6px;}")
        footer_lay = QHBoxLayout(footer)
        footer_lay.setContentsMargins(10,3,10,3)
        lbl_inst = QLabel(
            "Depto. de Recursos Naturales y Sistemas Agroforestales  ·  "
            "Universidad de Nariño  ·  Colombia")
        lbl_inst.setStyleSheet("color:#85c1e9;font-size:9px;font-family:Arial;")
        lbl_autor = QLabel("v1.0  ·  D.A. Muñoz G.")
        lbl_autor.setStyleSheet(
            "color:white;font-size:9px;font-weight:bold;font-family:Arial;")
        footer_lay.addWidget(lbl_inst)
        footer_lay.addStretch()
        footer_lay.addWidget(lbl_autor)
        enc_lay.addWidget(footer)
        lay.addWidget(enc)

        # Datos zona de estudio
        grp1 = QGroupBox("Datos de la zona de estudio")
        grp1.setStyleSheet("QGroupBox{font-weight:bold;}")
        g1 = QGridLayout(grp1); g1.setSpacing(8)
        g1.addWidget(QLabel("Nombre de la zona de estudio:"), 0, 0)
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Ej: La Florida, Cuenca Río Bobo, Área Metropolitana Pasto")
        g1.addWidget(self.txt_nombre, 0, 1)
        g1.addWidget(QLabel("Departamento / Región:"), 1, 0)
        self.txt_depto = QLineEdit(); self.txt_depto.setPlaceholderText("Ej: Nariño")
        g1.addWidget(self.txt_depto, 1, 1)
        lay.addWidget(grp1)

        # Rutas
        grp2 = QGroupBox("Rutas de trabajo")
        grp2.setStyleSheet("QGroupBox{font-weight:bold;}")
        g2 = QGridLayout(grp2); g2.setSpacing(8)
        def fila(label, campo, slot, row):
            g2.addWidget(QLabel(label), row, 0); g2.addWidget(campo, row, 1)
            btn = QPushButton("📁"); btn.setFixedWidth(36); btn.clicked.connect(slot)
            g2.addWidget(btn, row, 2)
        self.txt_planchas = QLineEdit()
        self.txt_planchas.setPlaceholderText("Carpeta con subcarpetas de planchas (SHP, GDB o MDB)")
        self.txt_limite   = QLineEdit()
        self.txt_limite.setPlaceholderText("Shapefile del límite de la zona de estudio")
        self.txt_salida   = QLineEdit()
        self.txt_salida.setPlaceholderText("Carpeta donde se guardarán los resultados")
        fila("Carpeta de planchas IGAC:",      self.txt_planchas, lambda: self._carpeta(self.txt_planchas), 0)
        fila("Límite zona de estudio (.shp):", self.txt_limite,   self._limite,                             1)
        fila("Carpeta de salida:",             self.txt_salida,   lambda: self._carpeta(self.txt_salida),   2)
        lay.addWidget(grp2)

        # Planchas
        grp3 = QGroupBox("Planchas IGAC de la zona de estudio")
        grp3.setStyleSheet("QGroupBox{font-weight:bold;}")
        g3 = QVBoxLayout(grp3)
        lbl_h = QLabel("Escribe los nombres de las subcarpetas, separados por comas.\n"
                        "Cada subcarpeta puede contener SHP, GDB o MDB — se detectan automáticamente.\n"
                        "Ejemplo:  410IIID, 410IVC, 429IB, 429ID")
        lbl_h.setStyleSheet("color:#555;font-size:11px;")
        g3.addWidget(lbl_h)
        self.txt_planchas_nombres = QLineEdit()
        self.txt_planchas_nombres.setPlaceholderText("410IIID, 410IVC, 429IB, 429ID")
        g3.addWidget(self.txt_planchas_nombres)
        btn_det = QPushButton("🔍  Detectar planchas automáticamente")
        btn_det.setStyleSheet("QPushButton{background:#eaf4fb;border:1px solid #aad4f5;"
                               "border-radius:4px;padding:4px 10px;}"
                               "QPushButton:hover{background:#d5eaf7;}")
        btn_det.clicked.connect(self._detectar)
        g3.addWidget(btn_det)
        lay.addWidget(grp3)

        # Capas opcionales
        grp_op = QGroupBox("Capas adicionales opcionales (Superficies de Agua)")
        grp_op.setStyleSheet("QGroupBox{font-weight:bold;}")
        lay_op = QVBoxLayout(grp_op)
        lbl_op = QLabel("Activa las capas adicionales presentes en tu zona de estudio.\n"
                         "El script verificará si existen en las planchas antes de procesarlas.")
        lbl_op.setStyleSheet("color:#555;font-size:11px;")
        lay_op.addWidget(lbl_op)

        # Área con scroll para los checkboxes
        scroll = QScrollArea(); scroll.setMaximumHeight(90)
        scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        scroll_widget = QWidget()
        scroll_grid = QGridLayout(scroll_widget); scroll_grid.setSpacing(4)

        self.checks_opcionales = {}
        capas_nombres = {
            "Laguna":       "Laguna",
            "Embalse":      "Embalse",
            "Cienaga":      "Ciénaga (polígono)",
            "Cienaga_P":    "Ciénaga (punto)",
            "Jaguey_P":     "Jagüey (punto)",
            "Jaguey_R":     "Jagüey (polígono)",
            "Pantano":      "Pantano",
            "Humedal":      "Humedal",
            "Manglar":      "Manglar",
            "Morichal":     "Morichal",
            "Isla":         "Isla",
            "Manantial":    "Manantial",
            "Madrevieja_L": "Madrevieja (línea)",
            "Madrevieja_R": "Madrevieja (polígono)",
            "Linea_de_Mar": "Línea de Mar / Costera",
        }
        col, row = 0, 0
        for key, nombre_display in capas_nombres.items():
            cb = QCheckBox(nombre_display)
            cb.setStyleSheet("font-size:11px;")
            self.checks_opcionales[key] = cb
            scroll_grid.addWidget(cb, row, col)
            col += 1
            if col > 2: col = 0; row += 1

        scroll.setWidget(scroll_widget)
        lay_op.addWidget(scroll)

        # Botones seleccionar/deseleccionar todo
        lay_sel = QHBoxLayout()
        btn_all = QPushButton("Seleccionar todas")
        btn_all.setStyleSheet("QPushButton{background:#eaf4fb;border:1px solid #aad4f5;"
                               "border-radius:4px;padding:3px 8px;font-size:11px;}"
                               "QPushButton:hover{background:#d5eaf7;}")
        btn_all.clicked.connect(lambda: [cb.setChecked(True)
                                          for cb in self.checks_opcionales.values()])
        btn_none = QPushButton("Deseleccionar todas")
        btn_none.setStyleSheet("QPushButton{background:#fef9e7;border:1px solid #f9e79f;"
                                "border-radius:4px;padding:3px 8px;font-size:11px;}"
                                "QPushButton:hover{background:#fef3cd;}")
        btn_none.clicked.connect(lambda: [cb.setChecked(False)
                                           for cb in self.checks_opcionales.values()])
        lay_sel.addWidget(btn_all); lay_sel.addWidget(btn_none); lay_sel.addStretch()
        lay_op.addLayout(lay_sel)
        lay.addWidget(grp_op)

        # Proceso
        grp4 = QGroupBox("Proceso")
        grp4.setStyleSheet("QGroupBox{font-weight:bold;}")
        g4 = QVBoxLayout(grp4)
        self.barra = QProgressBar(); self.barra.setValue(0)
        self.barra.setStyleSheet("QProgressBar{border:1px solid #ccc;border-radius:4px;height:18px;}"
                                  "QProgressBar::chunk{background:#1a7a3a;border-radius:3px;}")
        g4.addWidget(self.barra)
        self.log = QTextEdit(); self.log.setReadOnly(True); self.log.setMaximumHeight(100)
        self.log.setStyleSheet("background:#1e1e1e;color:#d4d4d4;font-family:monospace;"
                                "font-size:11px;border-radius:4px;")
        self.log.setPlaceholderText("El avance del proceso aparecerá aquí...")
        g4.addWidget(self.log)
        lay.addWidget(grp4)

        # Botones
        lay_btn = QHBoxLayout()
        self.btn_cerrar = QPushButton("✖  Cerrar")
        self.btn_cerrar.setStyleSheet("QPushButton{background:#f5f5f5;border:1px solid #ccc;"
                                       "border-radius:4px;padding:6px 16px;}"
                                       "QPushButton:hover{background:#e8e8e8;}")
        self.btn_cerrar.clicked.connect(self.close)
        self.btn_exec = QPushButton("▶   Ejecutar")
        self.btn_exec.setStyleSheet("QPushButton{background:#1a7a3a;color:white;border:none;"
                                     "border-radius:4px;padding:6px 24px;font-size:13px;"
                                     "font-weight:bold;}"
                                     "QPushButton:hover{background:#15612e;}"
                                     "QPushButton:disabled{background:#aaa;}")
        self.btn_exec.clicked.connect(self._ejecutar)
        lay_btn.addWidget(self.btn_cerrar); lay_btn.addStretch(); lay_btn.addWidget(self.btn_exec)
        lay.addLayout(lay_btn)

    def _carpeta(self, campo):
        r = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if r: campo.setText(r)

    def _limite(self):
        r, _ = QFileDialog.getOpenFileName(self, "Seleccionar límite", "", "Shapefiles (*.shp)")
        if r: self.txt_limite.setText(r)

    def _detectar(self):
        carpeta = self.txt_planchas.text().strip()
        if not os.path.isdir(carpeta):
            QMessageBox.warning(self, "Atención", "Primero selecciona la carpeta de planchas.")
            return
        subs = sorted([d for d in os.listdir(carpeta)
                       if os.path.isdir(os.path.join(carpeta, d)) and not d.startswith("_")])
        if subs:
            self.txt_planchas_nombres.setText(", ".join(subs))
            self._log(f"✓ Planchas detectadas: {', '.join(subs)}")
        else:
            QMessageBox.warning(self, "Sin resultados", "No se encontraron subcarpetas.")

    def _log(self, texto):
        self.log.append(texto)
        self.log.ensureCursorVisible()
        QApplication.processEvents()

    def _validar(self):
        err = []
        if not self.txt_nombre.text().strip():   err.append("• Escribe el nombre de la zona de estudio")
        if not self.txt_depto.text().strip():     err.append("• Escribe el departamento o región")
        if not os.path.isdir(self.txt_planchas.text().strip()):
            err.append("• Selecciona la carpeta de planchas IGAC")
        if not os.path.isfile(self.txt_limite.text().strip()):
            err.append("• Selecciona el shapefile del límite")
        if not self.txt_salida.text().strip():    err.append("• Selecciona la carpeta de salida")
        if not self.txt_planchas_nombres.text().strip():
            err.append("• Indica las planchas (o usa Detectar)")
        return err

    def _ejecutar(self):
        err = self._validar()
        if err:
            QMessageBox.warning(self, "Campos incompletos",
                                "Por favor completa:\n\n" + "\n".join(err))
            return
        planchas = [p.strip() for p in
                    self.txt_planchas_nombres.text().split(",") if p.strip()]
        self._cfg = {
            "carpeta_planchas": self.txt_planchas.text().strip(),
            "limite_shp":       self.txt_limite.text().strip(),
            "carpeta_salida":   self.txt_salida.text().strip(),
            "nombre":           self.txt_nombre.text().strip(),
            "departamento":     self.txt_depto.text().strip(),
            "planchas":         planchas,
        }
        try:
            os.makedirs(self._cfg["carpeta_salida"], exist_ok=True)
            os.makedirs(os.path.join(self._cfg["carpeta_salida"], "_tmp"), exist_ok=True)
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"No se pudo crear la carpeta de salida:\n{ex}")
            return
        self.btn_exec.setEnabled(False); self.btn_exec.setText("⏳  Procesando...")
        self.log.clear(); self.barra.setValue(0)
        self._log(f"Zona de estudio: {self._cfg['nombre']} — {self._cfg['departamento']}")
        self._log(f"Planchas: {', '.join(planchas)}\n")
        QTimer.singleShot(100, self._procesar)

    def _procesar(self):
        cfg = self._cfg
        out = cfg["carpeta_salida"]
        tmp = os.path.join(out, "_tmp")
        crs = QgsCoordinateReferenceSystem(CRS_DEST)
        try:
            # Reproyectar límite
            self._log("▶ Reproyectando límite de la zona de estudio...")
            self.barra.setValue(5); QApplication.processEvents()
            limite_9377 = os.path.join(out, "Limite_Zona_Estudio_9377.shp")
            processing.run("native:reprojectlayer", {
                "INPUT": cfg["limite_shp"],
                "TARGET_CRS": crs,
                "OUTPUT": limite_9377})
            lim = QgsVectorLayer(limite_9377, "lim", "ogr")
            e   = lim.extent()
            self._log(f"   OK — {e.width():.0f} m × {e.height():.0f} m")
            self.barra.setValue(10); QApplication.processEvents()

            # Procesar capas
            capas_paths = {}
            total = len(CAPAS_IGAC)
            for i, nombre_interno in enumerate(CAPAS_IGAC.keys()):
                self._log(f"▶ Procesando {nombre_interno}...")
                QApplication.processEvents()
                inputs = []
                for p in cfg["planchas"]:
                    cp = os.path.join(cfg["carpeta_planchas"], p)
                    if not os.path.isdir(cp): continue
                    uri = buscar_uri(cp, nombre_interno)
                    if uri:
                        lyr = QgsVectorLayer(uri, "x", "ogr")
                        if lyr.isValid() and lyr.featureCount() > 0:
                            uri_norm = normalizar_campos(uri, tmp, f"{p}_{nombre_interno}")
                            inputs.append(uri_norm)
                            self._log(f"   + {p}: {lyr.featureCount()} features")
                        else:
                            self._log(f"   - {p}: sin datos")
                    else:
                        self._log(f"   - {p}: capa no encontrada")

                if not inputs:
                    self._log(f"   [sin datos] {nombre_interno}")
                    self.barra.setValue(10+int(60*(i+1)/total))
                    QApplication.processEvents()
                    continue

                merged       = os.path.join(tmp, nombre_interno+"_merge.gpkg")
                reproj       = os.path.join(tmp, nombre_interno+"_9377.gpkg")
                fixed        = os.path.join(tmp, nombre_interno+"_fixed.gpkg")
                clipped_gpkg = os.path.join(tmp, nombre_interno+"_clip.gpkg")
                clipped      = os.path.join(out, nombre_interno+".shp")

                QApplication.processEvents()
                processing.run("native:mergevectorlayers",
                               {"LAYERS": inputs, "CRS": None, "OUTPUT": merged})
                QApplication.processEvents()
                processing.run("native:reprojectlayer",
                               {"INPUT": merged, "TARGET_CRS": crs, "OUTPUT": reproj})
                QApplication.processEvents()
                # Reparar geometrías inválidas antes del clip
                processing.run("native:fixgeometries",
                               {"INPUT": reproj, "OUTPUT": fixed})
                QApplication.processEvents()
                processing.run("native:clip",
                               {"INPUT": fixed, "OVERLAY": limite_9377, "OUTPUT": clipped_gpkg})
                QApplication.processEvents()

                from PyQt5.QtCore import QVariant
                lyr_clip = QgsVectorLayer(clipped_gpkg, "clip_tmp", "ogr")
                if lyr_clip.isValid():
                    campos_ok = [c.name() for c in lyr_clip.fields()
                                 if c.type() not in [QVariant.ByteArray, QVariant.UserType]]
                    processing.run("native:retainfields",
                                   {"INPUT": clipped_gpkg, "FIELDS": campos_ok, "OUTPUT": clipped})
                    QApplication.processEvents()

                n = QgsVectorLayer(clipped,"f","ogr").featureCount() \
                    if os.path.exists(clipped) else 0
                if n > 0:
                    capas_paths[nombre_interno] = clipped
                    self._log(f"   ✓ {nombre_interno}: {n} features")
                else:
                    self._log(f"   [0 features] {nombre_interno}")
                self.barra.setValue(10+int(60*(i+1)/total))
                QApplication.processEvents()

            # Cargar capas y aplicar simbología
            self._log("▶ Cargando capas y aplicando simbología IGAC...")
            self.barra.setValue(75); QApplication.processEvents()

            proj = QgsProject.instance()
            proj.removeAllMapLayers()
            proj.setCrs(crs)

            orden = ["Curvas_Nivel","Drenaje_Doble","Drenaje_Sencillo",
                     "Vias","Construcciones","Orografia","Administrativo"]
            lim_capa = QgsVectorLayer(limite_9377, "Límite Zona de Estudio", "ogr")
            proj.addMapLayer(lim_capa)
            capas_cargadas = {}
            for nc in orden:
                if nc in capas_paths:
                    lyr = QgsVectorLayer(capas_paths[nc], nc.replace("_"," "), "ogr")
                    proj.addMapLayer(lyr)
                    capas_cargadas[nc] = lyr

            self.barra.setValue(85); QApplication.processEvents()
            aplicar_simbologia(capas_cargadas, lim_capa, log_fn=self._log)
            # Procesar capas opcionales activadas por el usuario
            capas_opcionales_activadas = {k: v for k, v in self.checks_opcionales.items()
                                           if v.isChecked()}
            if capas_opcionales_activadas:
                self._log(f"\n▶ Procesando {len(capas_opcionales_activadas)} capa(s) opcional(es)...")
                QApplication.processEvents()

                for nombre_op, _ in capas_opcionales_activadas.items():
                    info = CAPAS_OPCIONALES[nombre_op]
                    self._log(f"  ▶ {nombre_op}...")
                    QApplication.processEvents()

                    inputs_op = []
                    for p in cfg["planchas"]:
                        cp = os.path.join(cfg["carpeta_planchas"], p)
                        if not os.path.isdir(cp): continue

                        # Buscar SHP, GDB o MDB para esta capa opcional
                        uri_op = None
                        fp_shp = os.path.join(cp, info["shp"])
                        if os.path.exists(fp_shp):
                            uri_op = fp_shp
                        else:
                            for entry in os.listdir(cp):
                                ruta_e = os.path.join(cp, entry)
                                if entry.lower().endswith(".gdb") and os.path.isdir(ruta_e):
                                    for u in [f"{ruta_e}|layername={info['capa']}",
                                              f"{ruta_e}|layername={info['grupo']}/{info['capa']}"]:
                                        if QgsVectorLayer(u,"t","ogr").isValid():
                                            uri_op = u; break
                                elif entry.lower().endswith(".mdb"):
                                    u = f"{ruta_e}|layername={info['capa']}"
                                    if QgsVectorLayer(u,"t","ogr").isValid():
                                        uri_op = u; break
                                if uri_op: break

                        if uri_op:
                            lyr_op = QgsVectorLayer(uri_op,"x","ogr")
                            if lyr_op.isValid() and lyr_op.featureCount() > 0:
                                uri_norm = normalizar_campos(uri_op, tmp, f"{p}_{nombre_op}")
                                inputs_op.append(uri_norm)
                                self._log(f"    + {p}: {lyr_op.featureCount()} features")

                    if not inputs_op:
                        self._log(f"    [sin datos] {nombre_op} — no existe en las planchas")
                        QApplication.processEvents()
                        continue

                    merged_op       = os.path.join(tmp, nombre_op+"_merge.gpkg")
                    reproj_op       = os.path.join(tmp, nombre_op+"_9377.gpkg")
                    fixed_op        = os.path.join(tmp, nombre_op+"_fixed.gpkg")
                    clipped_gpkg_op = os.path.join(tmp, nombre_op+"_clip.gpkg")
                    clipped_op      = os.path.join(out, nombre_op+".shp")

                    QApplication.processEvents()
                    processing.run("native:mergevectorlayers",
                                   {"LAYERS": inputs_op, "CRS": None, "OUTPUT": merged_op})
                    QApplication.processEvents()
                    processing.run("native:reprojectlayer",
                                   {"INPUT": merged_op, "TARGET_CRS": crs, "OUTPUT": reproj_op})
                    QApplication.processEvents()
                    # Reparar geometrías inválidas
                    processing.run("native:fixgeometries",
                                   {"INPUT": reproj_op, "OUTPUT": fixed_op})
                    QApplication.processEvents()
                    processing.run("native:clip",
                                   {"INPUT": fixed_op, "OVERLAY": limite_9377,
                                    "OUTPUT": clipped_gpkg_op})
                    QApplication.processEvents()

                    from PyQt5.QtCore import QVariant
                    lyr_clip_op = QgsVectorLayer(clipped_gpkg_op,"clip_op","ogr")
                    if lyr_clip_op.isValid():
                        campos_ok_op = [c.name() for c in lyr_clip_op.fields()
                                        if c.type() not in [QVariant.ByteArray,
                                                             QVariant.UserType]]
                        processing.run("native:retainfields",
                                       {"INPUT": clipped_gpkg_op,
                                        "FIELDS": campos_ok_op,
                                        "OUTPUT": clipped_op})
                        QApplication.processEvents()

                    if os.path.exists(clipped_op):
                        n_op = QgsVectorLayer(clipped_op,"f","ogr").featureCount()
                        if n_op > 0:
                            lyr_nueva = QgsVectorLayer(clipped_op,
                                                        nombre_op.replace("_"," "), "ogr")
                            proj.addMapLayer(lyr_nueva)
                            aplicar_simbologia_opcional(lyr_nueva, info, nombre_op)
                            self._log(f"    ✓ {nombre_op}: {n_op} features")
                        else:
                            self._log(f"    [0 features] {nombre_op}")

            self._log("   ✓ Simbología aplicada correctamente")
            self.barra.setValue(92); QApplication.processEvents()

            # Zoom y guardar
            from qgis.utils import iface
            ext = lim_capa.extent(); ext.scale(1.05)
            iface.mapCanvas().setExtent(ext); iface.mapCanvas().refresh()

            nombre = cfg["nombre"]
            qgz = os.path.join(out, f"{nombre.replace(' ','_')}_IGAC_25000.qgz")
            proj.write(qgz)
            self.barra.setValue(100)
            self._log(f"\n✅ ¡COMPLETADO!")
            self._log(f"   Zona: {nombre} — {cfg['departamento']}")
            self._log(f"   Proyecto: {qgz}")

            self.btn_exec.setEnabled(True); self.btn_exec.setText("▶   Ejecutar")
            QMessageBox.information(self, "¡Completado!",
                f"Cartografía generada correctamente.\n\n"
                f"Zona de estudio: {nombre}\n"
                f"Proyecto guardado en:\n{qgz}")

        except Exception as ex:
            import traceback
            self._log(f"\n❌ ERROR: {str(ex)}")
            self._log(traceback.format_exc())
            self.btn_exec.setEnabled(True); self.btn_exec.setText("▶   Ejecutar")
            QMessageBox.critical(self, "Error",
                f"Ocurrió un error durante el procesamiento:\n\n{str(ex)}")

# =============================================================================
# LANZAR
# =============================================================================
# ventana = VentanaIGAC(iface.mainWindow())
# ventana.show()