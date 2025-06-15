import pandas as pd
import seaborn as sns
import os
import re
import funciones.funciones_adicionales as fa

ruta_archivo = 'INTEGRADO.csv'

fa.delete_file(ruta_archivo)

df_s1_inicial = pd.read_csv('Data_analytics_SECOP_1.csv')

cols=list(df_s1_inicial.columns)
cols=[x.upper().strip() for x in cols]
df_s1_inicial.columns=cols

df_s1 = df_s1_inicial

estado_proceso_agrupados = pd.DataFrame(df_s1.groupby('ESTADO DEL PROCESO')['NUMERO DE CONTRATO'].count()).sort_values('NUMERO DE CONTRATO',ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['NUMERO DE CONTRATO'] / x['NUMERO DE CONTRATO'].sum()) * 100)

df_s1 = df_s1[~(df_s1['ESTADO DEL PROCESO'] == 'Convocado')]

modalidad_s1_agrupados = pd.DataFrame(df_s1.groupby('MODALIDAD DE CONTRATACION')['NUMERO DE CONTRATO'].count()).sort_values('NUMERO DE CONTRATO',ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['NUMERO DE CONTRATO'] / x['NUMERO DE CONTRATO'].sum()) * 100)

# Al hacer esta verificación se puede evidenciar que diferentes modalidades se podrían agrupar en categorías para facilidad de análisis,  
# (i) La categorías de 'Contratación Directa (Ley 1150 de 2007)' y 'Otras Formas de Contratación Directa' se dejarán como 'Contratación Directa'.  
# (ii) Las diferentes selecciones abreviadas y la subasta y las agruparemos en una gran categoría llamada "Selección Abreviada". 
# (iii) Agruparemos los diferentes concursos de méritos en una sóla categoría llamada "Concurso de Méritos".
# (iv) Unificaremos la licitación obra pública junto con la licitación pública y la dejaremos como una única categoría de licitación pública.
# Sin embargo, no dejaremos perder la columna original con las modalidades de contratación, por lo cual crearemos una nueva llamada "MODALIDAD GENERAL"

df_s1['MODALIDAD GENERAL'] = df_s1['MODALIDAD DE CONTRATACION']

reemplazos_modalidad_s1 = {'Contratación Directa (Ley 1150 de 2007)': 'Contratación Directa',
    'Otras Formas de Contratación Directa':'Contratación Directa',
    'Selección Abreviada de Menor Cuantía (Ley 1150 de 2007)': 'Selección Abreviada',
    'Selección Abreviada del literal h del numeral 2 del artículo 2 de la Ley 1150 de 2007': 'Selección Abreviada',
    'Subasta': 'Selección Abreviada', 'Selección Abreviada servicios de Salud': 'Selección Abreviada',
    'Concurso de Méritos Abierto':'Concurso de Méritos' , 'Concurso de Méritos con Lista Corta':'Concurso de Méritos',
    'Licitación obra pública':'Licitación Pública'
}

df_s1['MODALIDAD GENERAL'].replace(reemplazos_modalidad_s1, inplace=True)

tipo_contrato_s1_agrupados = pd.DataFrame(df_s1.groupby('TIPO DE CONTRATO')['NUMERO DE CONTRATO'].count()).sort_values('NUMERO DE CONTRATO', ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['NUMERO DE CONTRATO'] / x['NUMERO DE CONTRATO'].sum()) * 100)

# Para el presente ejercicio vamos a considerar la totalidad de los tipos de contrato, la única categoría que debe estudiarse a detalle es la de "No definido", debido a que puede ser cualquiera de las demás categorías, esto se verifica de manera manual para cada objeto contractual.
# Es importante que la base de datos no cuente con información imprecisa, algunos contratos puede que aùn en un estado activo pueda que no tengan un proveedor adjudicado, por lo cual se debe verificar esto ya que requerimos informaciòn de los proveedores o contratistas para nuestro problema a resolver. 
# Inicialmente, debemos revisar el tipo de datos para la columna 'NOM RAZON SOCIAL CONTRATISTA'

# A continuación, se verificará si algún contrato no tiene un contratista adjudicado, debemos eliminarlo de la base de datos, pero se debe pasar primero a cadena de texto

df_s1['NOM RAZON SOCIAL CONTRATISTA'] = df_s1['NOM RAZON SOCIAL CONTRATISTA'].astype(str)

valores_vacios = df_s1[df_s1['NOM RAZON SOCIAL CONTRATISTA'] == '']

df_s1['FECHA DE FIRMA DEL CONTRATO'] = pd.to_datetime(df_s1['FECHA DE FIRMA DEL CONTRATO'], format='%d/%m/%Y')
df_s1['FECHA DE CARGUE EN EL SECOP'] = pd.to_datetime(df_s1['FECHA DE CARGUE EN EL SECOP'], format='%d/%m/%Y')

# Estos archivos csv se descargaron en marzo de 2024 por lo cual debemos filtrar la información para analizar el comportamiento para 2023 únicamente

df_s1 = df_s1[df_s1['FECHA DE FIRMA DEL CONTRATO'].dt.year == 2023]
df_s1['FECHA DE FIRMA DEL CONTRATO'].fillna(df_s1['FECHA DE CARGUE EN EL SECOP'], inplace=True)

# Ahora, por algunos aspectos de la paltaforma es probable que algunos contratos se dupliquen en la base de datos inicial, por lo cual debemos eliminar todos los contratos duplicados para evitar inconsistencias en nuestro análisis. Tendremos la columna 'NUMERO DE CONTRATO' para verificar los datos duplicados. Este paso prefereiblemente se debe realizar al principio, ya que algunas depuraciones o transformaciones que se hicieron inicialmente a la base de datos no las hubieramos tenido que hacer al eliminar valores duplicados. 
# Es importante aclarar que los nùmeros de contrato pueden ser iguales para distintas entidades estatales, por ejemplo, una entidad estatal puede generar el contrato de prestación de servicios CPS-001-2023, por lo cual si eliminamos los repetidos, nos puede eliminar contratos reales de otras entidades y nos sesgan el análsiis. Necesitamos entonces generar un identificador por entidad para cada contrato, concatenando las columnas del nombre de la entidad con el número de contrato registrado.

df_s1['NUMERO DE CONTRATO UNICO'] = df_s1['NOMBRE ENTIDAD'] + df_s1['NUMERO DE CONTRATO']

# Ahora podremos eliminar los numeros de contrato duplicados con base en la nueva columna 'NUMERO DE CONTRATO UNICO' 

df_s1.drop_duplicates(subset='NUMERO DE CONTRATO UNICO', keep='first', inplace=True)

# En cuanto al valor de los contratos, se debe revisar si alguna entidad ha cometido alguna impresición en el valor del contrato registrado, por lo cual debemos revisar en un diagrama de caja (boxplot), y sirve para visualizar la distribución de un conjunto de datos numéricos y para identificar la presencia de valores atípicos
# Identificamos una concentración mayoritariamente entre 0 y 100 mil millones de pesos para el valor de los contratos, debemos verificar los valores que no estén dentro de este rango para cerciorarnos que las cifras no presentan inconsistencias

df_s1_out = df_s1[df_s1['CUANTIA CONTRATO']>=100000000000]
df_s1['DETALLE DEL OBJETO A CONTRATAR']=df_s1['DETALLE DEL OBJETO A CONTRATAR'].astype(str)
df_s1['OBJETO CONTRACTUAL'] = df_s1['DETALLE DEL OBJETO A CONTRATAR'].apply(fa.limpiar_texto)
df_s1['PLATAFORMA'] = 'SECOP I'

# Finalmente, seleccionaremos las columnas que identificamos para unificar una base de datos consolidada junto con SECOP 2 y TVEC

df_s1_integrar=df_s1[['NOMBRE ENTIDAD' , 'ESTADO DEL PROCESO', 'NUMERO DE PROCESO','NUMERO DE CONTRATO', 'OBJETO CONTRACTUAL', 'FECHA DE FIRMA DEL CONTRATO', 'NOM RAZON SOCIAL CONTRATISTA', 'CUANTIA CONTRATO', 'MODALIDAD GENERAL','TIPO DE CONTRATO','RUTA PROCESO EN SECOP I','PLATAFORMA']]

df_s2_inicial=pd.read_csv('Data_analytics_SECOP_2.csv')

cols = list(df_s2_inicial.columns)
cols = [x.upper().strip() for x in cols]

df_s2_inicial.columns = cols
df_s2 = df_s2_inicial


# Para este conjunto de datos vamos a eliminar inicialmente los contratos repetidos

df_s2['NUMERO DE CONTRATO UNICO'] = df_s2['NOMBRE ENTIDAD'] + df_s2['REFERENCIA DEL CONTRATO']
df_s2.drop_duplicates(subset='REFERENCIA DEL CONTRATO', keep='first', inplace=True)

# Verificamos los estados de los contratos que se pueden ver para esta base de datos de SECOP II

estado_contrato_s2_agrupados = pd.DataFrame(df_s2.groupby('ESTADO CONTRATO')['REFERENCIA DEL CONTRATO'].count()).sort_values('REFERENCIA DEL CONTRATO',ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['REFERENCIA DEL CONTRATO'] / x['REFERENCIA DEL CONTRATO'].sum()) * 100)

df_s2 = df_s2[(df_s2['ESTADO CONTRATO'] != 'Cancelado') & (df_s2['ESTADO CONTRATO'] != 'Borrador') & (df_s2['ESTADO CONTRATO'] != 'enviado Proveedor')]

modalidad_s2_agrupados = pd.DataFrame(df_s2.groupby('MODALIDAD DE CONTRATACION')['REFERENCIA DEL CONTRATO'].count()).sort_values('REFERENCIA DEL CONTRATO',ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['REFERENCIA DEL CONTRATO'] / x['REFERENCIA DEL CONTRATO'].sum()) * 100)
# Se puede evidenciar que hay modalidades que se pueden agrupar:
# (i) Contratación Directa - Contratación Directa (con ofertas) - Contratación directa
# (ii) Selección Abreviada - Selección abreviada subasta inversa - Selección Abreviada de Menor Cuantía - Seleccion Abreviada Menor Cuantia Sin Manifestacion Interes	
# (iii) Contratación régimen especial - Contratación régimen especial (con ofertas)
# (iv) Licitación Pública - Licitación pública Obra Publica - Licitación Pública Acuerdo Marco de Precios
# (v) Concurso de Méritos - CCE-20-Concurso_Meritos_Sin_Lista_Corta_1Sobre - Concurso de méritos abierto - CCE-19-Concurso_Meritos_Con_Lista_Corta_1Sobre	

# Se crea otra columna para la modalidad general

df_s2['MODALIDAD GENERAL'] = df_s2['MODALIDAD DE CONTRATACION']

reemplazos_modalidad_s2 = {
    'Contratación Directa (con ofertas)': 'Contratación Directa', 'Contratación directa':'Contratación Directa',
    'Selección abreviada subasta inversa': 'Selección Abreviada', 'Selección Abreviada de Menor Cuantía': 'Selección Abreviada', 'Seleccion Abreviada Menor Cuantia Sin Manifestacion Interes': 'Selección Abreviada', 'Contratación régimen especial (con ofertas)':'Contratación régimen especial',
    'Licitación pública Obra Publica':'Licitación pública','Licitación Pública Acuerdo Marco de Precios':'Licitación pública',
    'CCE-20-Concurso_Meritos_Sin_Lista_Corta_1Sobre':'Concurso de Méritos', 'Concurso de méritos abierto':'Concurso de Méritos',
    'CCE-19-Concurso_Meritos_Con_Lista_Corta_1Sobre':'Concurso de Méritos'
}

df_s2['MODALIDAD GENERAL'].replace(reemplazos_modalidad_s2, inplace=True)

modalidad_s2_agrupados = pd.DataFrame(df_s2.groupby('MODALIDAD GENERAL')['REFERENCIA DEL CONTRATO'].count()).sort_values('REFERENCIA DEL CONTRATO',ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['REFERENCIA DEL CONTRATO'] / x['REFERENCIA DEL CONTRATO'].sum()) * 100)

# Ahora se verificarán los tipos de contrato que se encuentran en la base de datos SECOP II

tipo_contrato_s2_agrupados = pd.DataFrame(df_s2.groupby('TIPO DE CONTRATO')['REFERENCIA DEL CONTRATO'].count()).sort_values('REFERENCIA DEL CONTRATO',ascending=False).assign(Porcentaje_de_Participacion=lambda x: (x['REFERENCIA DEL CONTRATO'] / x['REFERENCIA DEL CONTRATO'].sum()) * 100)

df_s2['FECHA DE FIRMA'] = pd.to_datetime(df_s2['FECHA DE FIRMA'])
df_s2 = df_s2[df_s2['FECHA DE FIRMA'].dt.year == 2023]

# Ahora haremos el reemplazo de las fechas nulas en fecha de firma con fechas de inicio de contrato
df_s2['FECHA DE FIRMA'].fillna(df_s2['FECHA DE INICIO DEL CONTRATO'], inplace=True)

plot= sns.set_style("whitegrid")
ax=sns.boxplot(x=df_s2['VALOR DEL CONTRATO'])

# Identificamos una concentración mayoritariamente entre 0 y 100 mil millones de pesos para el valor de los contratos, debemos verificar los valores que no estén dentro de este rango para cerciorarnos que las cifras no presentan inconsistencias

df_s2_out = df_s2[df_s2['VALOR DEL CONTRATO']>=100000000000]

# Una vez verificados se continúa con el análisis.
# Aplicamos el mismo procedimiento a los objetos contractuales que generamos para corregir errores en los objetos contractuales

df_s2['DESCRIPCION DEL PROCESO'] = df_s2['DESCRIPCION DEL PROCESO'].astype(str)
df_s2['OBJETO CONTRACTUAL'] = df_s2['DESCRIPCION DEL PROCESO'].apply(fa.limpiar_texto)
df_s2['PLATAFORMA'] = 'SECOP II'
df_s2['PROVEEDOR ADJUDICADO'] = df_s2['PROVEEDOR ADJUDICADO'].astype(str)
df_s2_integrar=df_s2[['NOMBRE ENTIDAD', 'ESTADO CONTRATO','PROCESO DE COMPRA','REFERENCIA DEL CONTRATO', 'OBJETO CONTRACTUAL', 'FECHA DE FIRMA', 'PROVEEDOR ADJUDICADO', 'VALOR DEL CONTRATO','MODALIDAD GENERAL','TIPO DE CONTRATO','URLPROCESO','PLATAFORMA']]

tvec_inicial=pd.read_csv('Data_analytics_TVEC.csv')

cols = list(tvec_inicial.columns)
cols = [x.upper().strip() for x in cols]
tvec_inicial.columns=cols

tvec = tvec_inicial


# Para esta base de datos, a diferencia de las otras, los contratos se identifican como número de orden de compra, por lo cual siempre serán valores distintos para cada contrato, independientemente de la entidad estatal. Por lo cual se hará la verificación de los duplicados de manera directa con la columna "IDENTIFICADOR DE LA ORDEN". 
# Hay que tener presente que la totalidad de las filas que registran en esta base de datos se ve alterada ya que cada item que se registra en una orden de compra se crea una nueva fila, por lo cual vamos a ver que reduce considerablemente el número de órdenes de compra de la base de datos con la eliminación de duplicados.

tvec.drop_duplicates(subset='IDENTIFICADOR DE LA ORDEN', keep="first", inplace=True)
tvec['FECHA'] = pd.to_datetime(tvec['FECHA'])
tvec = tvec[tvec['FECHA'].dt.year == 2023]

# Para este conjunto de datos no tenemos reemplazo de las fechas nulas, por lo cual para aquellos que no contengan información vamos a eliminarlo del conjunto de datos
tvec.dropna(subset=['FECHA'], inplace=True)

tvec['TOTAL'] = pd.to_numeric(tvec['TOTAL'], errors='coerce')

plot= sns.set_style("whitegrid")
ax=sns.boxplot(x=tvec['TOTAL'])
plot


# Se identifica entonces, al igual que en las demás bases de datos que hay valores atípicos desde los 100 mil millones de pesos, los cuales se deben revisar directamente en la fuente de datos
# Este conjunto de datos no tiene enlace de la orden de compra, por lo cual se debe crearlo, se identifica que el enlace principal para la consulta de las órdenes de compra es siempre este
# https://www.colombiacompra.gov.co/tienda-virtual-del-estado-colombiano/ordenes-compra
# Por lo cual se concatenará el enlace con el número de la orden de compra, para esto crearemos primero la columna 'ENLACE'

tvec['ENLACE'] = "https://www.colombiacompra.gov.co/tienda-virtual-del-estado-colombiano/ordenes-compra/"

# Ahora concatenamos esta nueva columna con el identificador de la orden y creamos el 'ENLACE DE OC'

tvec['IDENTIFICADOR DE LA ORDEN'] = tvec['IDENTIFICADOR DE LA ORDEN'].astype(str)
tvec['ENLACE DE OC'] = tvec['ENLACE'] + tvec['IDENTIFICADOR DE LA ORDEN']

# Finalmente identificamos las columnas que se usarán para el análisis de los datos
# En esta base de datos no existen las columnas modalidad de contratación ni tipo de contrato, por lo cual vamos a crear unas que digan 'AMP - Orden de compra'

tvec['MODALIDAD'] = 'AMP - Orden de compra'
tvec['TIPO DE CONTRATO'] = 'AMP - Orden de compra'

# Aplicamos el procedimiento de los objetos contractuales, en este caso será la columna "ITEMS"

tvec['ITEMS'] = tvec['ITEMS'].astype(str)
tvec['OBJETO CONTRACTUAL'] = tvec['ITEMS'].apply(fa.limpiar_texto)
tvec['PLATAFORMA'] = 'TVEC'

tvec_integrar=tvec[['ENTIDAD', 'ESTADO', 'AGREGACION','IDENTIFICADOR DE LA ORDEN', 'OBJETO CONTRACTUAL','FECHA', 'PROVEEDOR', 'TOTAL', 'MODALIDAD','TIPO DE CONTRATO','ENLACE DE OC','PLATAFORMA']]

# Una vez definidas estas columnas ahora vamos a integrar las tres bases de datos en una única llamada INTEGRADO

columnas = df_s2_integrar.columns
df_s1_integrar.columns = columnas
tvec_integrar.columns = columnas

INTEGRADO = pd.concat([df_s1_integrar, df_s2_integrar,tvec_integrar])

# Finalmente, tenemos una base de datos con 935.696 filas y 13 columnas.
# Se puede verificar el tipo de datos que trae cada una de las columnas.

# Sin embargo, es necesario establecer las cadenas de texto para confirmar que estamos trabajando sobre el mismo formato

columnas_a_convertir = ['NOMBRE ENTIDAD', 'ESTADO CONTRATO', 'PROCESO DE COMPRA',
                        'REFERENCIA DEL CONTRATO', 'OBJETO CONTRACTUAL',
                        'PROVEEDOR ADJUDICADO',
                        'MODALIDAD GENERAL', 'TIPO DE CONTRATO',
                        'URLPROCESO', 'PLATAFORMA']

INTEGRADO[columnas_a_convertir] = INTEGRADO[columnas_a_convertir].astype(str)

# Convertimos las cadenas de texto vacías a "No definido"

INTEGRADO[columnas_a_convertir] = INTEGRADO[columnas_a_convertir].fillna('No definido')

# Convertimos valores de contratos nulos por 0.

INTEGRADO['VALOR DEL CONTRATO'].fillna(0, inplace=True)

csv_file_path = 'INTEGRADO.csv'

INTEGRADO.to_csv(csv_file_path,index=False)

# Ya hemos generado el archivo csv en la carpeta, ahora procedemos a analizar y dar respuesta a nuestro ejercicio a través de Power Bi en la segunda parte del proyecto.
