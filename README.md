# Proyecto-an-lisis-de-datos---Contrataci-n-estatal - Parte 1

Se requiere realizar un estudio general sobre la compra pública en Colombia para el año 2023 a la fecha (2 de marzo de 2024), por lo cual se determinó consolidar la información que registra para las tres plataformas que componen el Sistema Electrónico de Contratación Pública - SECOP: (i) SECOP I, SECOP II y Tienda Virtual del Estado Colombiano – TVEC. 
Principal problema a resolver:
Este procedimiento inicial contempla la manipulación de bases de datos con un gran volumen de información, por lo cual necesitaremos usar un lenguaje de programación, para este caso Python y sus librerías de manipulación de bases de datos y herramientas gráficas para determinación de valores atípicos.
En consecuencia, este primer ejercicio consiste en realizar los siguientes procedimientos a las bases de datos en formato csv.: 

-	Eliminación de contratos duplicados en cada plataforma.
-	Verificación de los estados de los contratos en SECOP, eliminar los estados que no corresponden con contratos firmados.
-	Agrupaciones de las modalidades de contratación y tipos de contrato identificados
-	La identificación de valores atípicos.
-	Integración de las tres bases de datos para hacer un análisis integral.
Fuentes de datos:

	Portal de datos abiertos, conjunto de datos SECOP I - Procesos de Compra Pública
Se descarga un archivo csv llamado Data_analytics_SECOP_1.csv.
https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-I-Procesos-de-Compra-P-blica/f789-7hwg/data
 

	Portal de datos abiertos, conjunto de datos SECOP II - Contratos Electrónicos
https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h/data
Se descarga un archivo csv llamado Data_analytics_SECOP_2.csv. 
 

	Portal de datos abiertos, conjunto de datos Tienda Virtual del Estado Colombiano – TVEC
https://www.datos.gov.co/Gastos-Gubernamentales/Tienda-Virtual-del-Estado-Colombiano-Consolidado/rgxm-mmea/data
Se descarga un archivo csv llamado Data_analytics_TVEC.csv 

 
 Nota: La calidad de los datos depende de cada entidad estatal
