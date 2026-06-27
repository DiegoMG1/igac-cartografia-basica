# IGAC Cartografía Básica 1:25.000 — Plugin para QGIS

![QGIS](https://img.shields.io/badge/QGIS-3.16%2B-green)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Licencia](https://img.shields.io/badge/Licencia-GPL%20v2-orange)
![Colombia](https://img.shields.io/badge/Pa%C3%ADs-Colombia-yellow)

[

![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20969292.svg)

](https://doi.org/10.5281/zenodo.20969292)


Plugin para QGIS que automatiza la configuración de cartografía básica digital IGAC 1:25.000 para cualquier zona de estudio en Colombia. Procesa planchas en formato SHP, GDB o MDB, aplica la simbología oficial del **Catálogo de Objetos IGAC (Resoluciones 471 y 529 de 2020)** y reproyecta automáticamente a **EPSG:9377 (MAGNA-SIRGAS / CTM12 Origen Nacional)**.

---

## Autor

**Diego Andrés Muñoz Guerrero**  
Doctor en Geografía — IGAC-UPTC  
Profesor Tiempo Completo — Universidad de Nariño, Colombia  
Departamento de Recursos Naturales y Sistemas Agroforestales  
📧 dmunoz@udenar.edu.co

---

## Características principales

- ✅ Interfaz gráfica intuitiva — sin necesidad de editar código
- ✅ Soporte para **SHP** (Shapefile), **GDB** (File Geodatabase) y **MDB** (Personal Geodatabase)
- ✅ Planchas en distintos formatos mezcladas en el mismo proyecto
- ✅ Simbología oficial verificada del **Catálogo de Objetos IGAC 2020**
- ✅ Detección inteligente de campos — compatible con todas las versiones del catálogo
- ✅ Reproyección automática a **EPSG:9377 (CTM12 / Origen Nacional)**
- ✅ Reparación automática de geometrías inválidas
- ✅ Etiquetado tipográfico diferenciado por jerarquía según el catálogo
- ✅ Capas opcionales de Superficies de Agua activables con checkboxes
- ✅ Funciona con cualquier zona de estudio: municipios, cuencas, áreas protegidas, etc.

---

## Capas procesadas

### Capas base (siempre incluidas)

| Capa | Shapefile | Grupo GDB/MDB |
|---|---|---|
| Curvas de Nivel | `Curva_Nivel.shp` | `Relieve` |
| Drenaje Sencillo | `Drenaje_Sencillo.shp` | `Superficies_Agua` |
| Drenaje Doble | `Drenaje_Doble.shp` | `Superficies_Agua` |
| Vías | `Via.shp` | `Transporte_Terrestre` |
| Construcciones | `Construccion_P.shp` | `Edificacion_ObraCivil` |
| Orografía | `Orografia.shp` | `Toponimos` |
| Administrativo | `Administrativo_P.shp` | `Entidades_Territoriales_y_Unidades_Administrativas` |

### Capas opcionales — Superficies de Agua (activar con checkbox)

Laguna · Embalse · Ciénaga · Jagüey P · Jagüey R · Pantano · Humedal · Manglar · Morichal · Isla · Manantial · Madrevieja L · Madrevieja R · Línea de Mar / Costera

---

## Requisitos

- **QGIS** 3.16 o superior (recomendado 3.28+)
- **Python** 3.9 o superior (incluido con QGIS)
- Conexión a internet (solo la primera vez, para instalar fuentes tipográficas si faltan)
- Para planchas en formato **MDB**: instalar **Microsoft Access Database Engine 2016** (gratuito)  
  👉 https://www.microsoft.com/en-us/download/details.aspx?id=54920

---

## Instalación

### Opción A — Desde el repositorio de QGIS (recomendado)

1. Abrir QGIS
2. Ir a **Complementos → Administrar e instalar complementos**
3. Buscar: `IGAC Cartografía Básica`
4. Hacer clic en **Instalar**

### Opción B — Instalación manual desde ZIP

1. Descargar el archivo `igac_cartografia_basica.zip` desde este repositorio
2. En QGIS ir a **Complementos → Administrar e instalar complementos → Instalar desde ZIP**
3. Seleccionar el archivo descargado
4. Hacer clic en **Instalar complemento**

### Opción C — Script directo (sin instalar plugin)

1. Descargar `configurar_municipio_igac_gui.py`
2. En QGIS abrir **Complementos → Consola Python**
3. Hacer clic en el ícono **Mostrar editor**
4. Abrir el archivo descargado con el ícono de carpeta
5. Hacer clic en **▶ Ejecutar**

---

## Preparación de los datos

Antes de usar el plugin es necesario organizar los datos en la siguiente estructura de tres carpetas:

```
MI_PROYECTO/
|
+-- PLANCHAS/                  <- Carpeta principal que contiene las planchas
|   |
|   +-- 410IIID/               <- Subcarpeta nombrada con el codigo de la plancha
|   |   +-- Curva_Nivel.shp    <- Archivos SHP descomprimidos directamente aqui
|   |   +-- Curva_Nivel.dbf
|   |   +-- Curva_Nivel.shx
|   |   +-- Drenaje_Sencillo.shp
|   |   +-- Via.shp
|   |   +-- Construccion_P.shp
|   |   +-- Orografia.shp
|   |   +-- Administrativo_P.shp
|   |
|   +-- 410IVC/                <- Otra plancha en SHP
|   |   +-- Curva_Nivel.shp
|   |   +-- ... (resto de shapefiles)
|   |
|   +-- 429IB/                 <- Plancha en MDB (Personal Geodatabase)
|   |   +-- 429IB.mdb          <- Archivo MDB descomprimido directamente aqui
|   |
|   +-- 429ID/                 <- Plancha en GDB (File Geodatabase)
|       +-- 429ID.gdb/         <- Carpeta GDB descomprimida directamente aqui
|
+-- LIMITE/                    <- Limite de la zona de estudio
|   +-- Limite_Pasto.shp
|   +-- Limite_Pasto.dbf
|   +-- Limite_Pasto.shx
|   +-- Limite_Pasto.prj
|
+-- SALIDAS/                   <- Carpeta de resultados (puede estar vacia al inicio)
```

### Reglas para nombrar las carpetas de planchas

> ⚠️ Seguir estas reglas es fundamental para que el plugin detecte correctamente las planchas.

- El nombre de cada subcarpeta debe ser **exactamente el código de la plancha IGAC**
- Usar **MAYÚSCULAS** siempre
- **Sin espacios**, sin guiones, sin puntos, sin caracteres especiales
- El código va **pegado**, sin separadores entre letras y números

| Correcto | Incorrecto |
|---|---|
| `410IIID` | `410 IIID` |
| `410IVC` | `plancha-410IVC` |
| `429IB` | `429ib` |
| `448IIA` | `448_IIA` |
| `430IIIC` | `430-IIIC` |

### Reglas para los archivos dentro de cada subcarpeta

**Para planchas en Shapefile (SHP):**
- Descomprimir el ZIP del IGAC **directamente** dentro de la subcarpeta de la plancha
- Deben estar todos los archivos asociados: `.shp`, `.dbf`, `.shx`, `.prj`
- **No crear subcarpetas adicionales** dentro de la carpeta de la plancha

**Para planchas en Personal Geodatabase (MDB):**
- Copiar el archivo `.mdb` directamente dentro de la subcarpeta
- El archivo debe estar descomprimido — no dentro de un ZIP
- Requiere tener instalado **Microsoft Access Database Engine 2016**

**Para planchas en File Geodatabase (GDB):**
- Copiar la carpeta `.gdb` completa dentro de la subcarpeta de la plancha
- La carpeta `.gdb` debe estar descomprimida

### ¿Se pueden mezclar formatos?

**Sí.** El plugin detecta automáticamente si cada plancha viene en SHP, GDB o MDB. Es válido tener unas planchas en SHP y otras en MDB dentro del mismo proyecto.

---

## Uso

### Paso 1 — Abrir el configurador

Si instalaste el plugin:
- Ir a **Vectorial → IGAC Cartografía Básica 1:25.000 → Configurar Cartografía**

Si usas el script directo:
- Ejecutar `configurar_municipio_igac_gui.py` en la Consola Python de QGIS

### Paso 2 — Llenar los datos de la zona de estudio

| Campo | Descripción | Ejemplo |
|---|---|---|
| Nombre de la zona | Nombre del municipio, cuenca o área | `Pasto` |
| Departamento / Región | Departamento donde se ubica | `Nariño` |

### Paso 3 — Seleccionar las rutas

Usar los botones 📁 para seleccionar:

| Campo | Qué seleccionar |
|---|---|
| Carpeta de planchas IGAC | La carpeta `PLANCHAS/` que contiene las subcarpetas |
| Límite zona de estudio | El archivo `.shp` del límite del área de estudio |
| Carpeta de salida | La carpeta `SALIDAS/` donde se guardarán los resultados |

### Paso 4 — Detectar las planchas

Hacer clic en **🔍 Detectar planchas automáticamente** para que el plugin liste las subcarpetas disponibles. También se pueden escribir manualmente separadas por comas:

```
410IIID, 410IVC, 429IB, 429ID
```

### Paso 5 — Seleccionar capas opcionales (si aplica)

En la sección **Capas adicionales opcionales** activar con checkbox las capas de Superficies de Agua presentes en la zona de estudio. Si una capa está marcada pero no existe en las planchas, el plugin lo indica en el log y continúa sin error.

### Paso 6 — Ejecutar

Hacer clic en **▶ Ejecutar**. El proceso puede tardar varios minutos dependiendo del número de planchas. El log muestra el avance en tiempo real.

### Resultado

Al finalizar se generan en la carpeta de salida:
- Los **shapefiles procesados**, reproyectados a EPSG:9377 y recortados al límite
- Un **proyecto QGIS** (`.qgz`) con todas las capas cargadas y la simbología aplicada
- Una carpeta `_tmp/` con archivos intermedios que puede eliminarse

---

## Simbología aplicada

La simbología sigue estrictamente el **Catálogo de Objetos para Cartografía Básica 1:25.000 del IGAC** (Resoluciones 471 y 529 de 2020), verificada página por página del documento oficial.

| Capa | Símbolo | Colores RGB |
|---|---|---|
| Curva Índice | Línea continua 0.71pt | 168, 112, 0 |
| Curva Intermedia | Línea continua 0.35pt | 230, 159, 18 |
| Curva Suplementaria | Línea continua 0.18pt | 252, 173, 20 |
| Drenaje Permanente | Línea continua 0.45pt | 0, 112, 255 |
| Drenaje Intermitente | Línea discontinua 0.46pt | 0, 112, 255 |
| Vía Panamericana | Línea roja 2.0pt | 230, 0, 0 |
| Vía Pavimentada | Línea roja 1.0pt | 230, 0, 0 |
| Vía Carreteable | Línea discontinua 0.18pt | 230, 0, 0 |
| Cementerio / Iglesia / Salud | Cruz negra 2.0pt | 0, 0, 0 |
| Otras Construcciones | Cuadrado gris 1.5pt | 104, 104, 104 |
| Laguna / Embalse | Polígono azul claro | 214, 237, 255 |
| Límite zona de estudio | Contorno rojo 0.66pt | 200, 0, 0 |

### Tipografía del catálogo

| Fuente IGAC | Uso en el catálogo | Alternativa gratuita |
|---|---|---|
| Bookman Old Style | Entidades administrativas mayores | Libre Baskerville |
| Palatino Linotype | Corregimientos, caseríos | IM Fell English |
| Book Antiqua | Drenajes, cuerpos de agua | Cormorant Garamond |
| Arial Narrow | Curvas de nivel, veredas, construcciones | (nativa de Windows) |
| Zurich LtCn BT | Barrios, sectores | Barlow Condensed |

---

## Compatibilidad de versiones del catálogo IGAC

El plugin detecta automáticamente el nombre correcto de los campos en cada capa, siendo compatible con versiones antiguas y nuevas del catálogo:

| Campo en SHP | Campo en MDB/GDB | Descripción |
|---|---|---|
| `TIPO_CURVA` | `TIPO_CURVA_NIVEL` | Tipo de curva de nivel |
| `ALTURA_SOB` | `ALTURA_SOBRE_NIVEL_MAR` | Cota de la curva |
| `ESTADO_DRE` | `ESTADO_DRENAJE` | Tipo de drenaje |
| `NOMBRE_GEO` | `NOMBRE_GEOGRAFICO` | Nombre del objeto geográfico |
| `CODIGO_USO` | `CODIGO_USO_EDIFICACION` | Tipo de construcción |
| `CODIGO_NOM` | `CODIGO_NOMBRE` | Código del topónimo |

---

## Solución de problemas frecuentes

**El plugin no encuentra las planchas:**  
Verificar que las subcarpetas están nombradas con el código exacto de la plancha en MAYÚSCULAS y sin caracteres especiales, espacios ni guiones.

**Error con archivos MDB:**  
Instalar Microsoft Access Database Engine 2016 (64 bits):  
https://www.microsoft.com/en-us/download/details.aspx?id=54920

**Las curvas de nivel no aparecen:**  
El campo puede tener un nombre diferente. Verificar en la tabla de atributos que existe alguno de estos campos: `TIPO_CURVA`, `TIPO_CURVA_NIVEL` o `TIPO`.

**Las fuentes tipográficas se ven como Arial:**  
El plugin usa las fuentes del catálogo si están instaladas (con Microsoft Office) o sus equivalentes gratuitas de Google Fonts. Las etiquetas funcionan en cualquier caso.

**QGIS se cierra durante el procesamiento:**  
Puede ocurrir con muchas planchas si el equipo tiene poca RAM. Cerrar otras aplicaciones antes de ejecutar.

**Geometría inválida:**  
El plugin repara automáticamente las geometrías inválidas antes del recorte. Si el error persiste, verificar la integridad de los datos originales del IGAC.

---

## Estructura del repositorio

```
igac-cartografia-basica/
+-- __init__.py                      <- Punto de entrada del plugin QGIS
+-- plugin_main.py                   <- Clase principal y registro de botones
+-- configurar_municipio_igac_gui.py <- Configurador con interfaz grafica
+-- metadata.txt                     <- Metadatos del plugin para QGIS
+-- icon.png                         <- Icono del plugin (64x64 px)
+-- README.md                        <- Este archivo
```

---

## Licencia

Este proyecto está bajo la **Licencia GNU General Public License v2.0**.  
Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## Cómo citar

Si usas este plugin en investigaciones o trabajos académicos, por favor citar como:

```
Muñoz Guerrero, D.A. (2026). IGAC Cartografía Básica 
1:25.000 — Plugin para QGIS. Zenodo. 
https://doi.org/10.5281/zenodo.20969292

---

## Agradecimientos

- **IGAC** — Instituto Geográfico Agustín Codazzi, por el Catálogo de Objetos para Cartografía Básica 1:25.000 (Resoluciones 471 y 529 de 2020)
- **QGIS Development Team** — por la plataforma de código abierto
- **Universidad de Nariño** — Departamento RENSAF, por el apoyo institucional

---

*Desarrollado con ❤️ para la comunidad GIS de Colombia*
