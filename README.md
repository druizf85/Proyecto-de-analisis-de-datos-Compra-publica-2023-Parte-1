# Proyecto de análisis de datos – Compra pública 2023 – Parte 1

Se requiere realizar un estudio general sobre la compra pública en Colombia para el año 2023, por lo cual se determinó consolidar la información que registra para las tres plataformas que componen el Sistema Electrónico de Contratación Pública - SECOP: 

(i) SECOP I.
(ii) SECOP II. 
(iii) Tienda Virtual del Estado Colombiano – TVEC. 

Fuentes de datos:

Se tomó como fuente de datos la información de los conjuntos de datos de datos abiertos que son administrados por Colombia Compra Eficiente, se descargó información contractual desde el 1 de enero de 2023 a la fecha (2 de marzo de 2024).

	Portal de datos abiertos, conjunto de datos SECOP I - Procesos de Compra Pública
https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-I-Procesos-de-Compra-P-blica/f789-7hwg/data
Se descarga un archivo csv llamado Data_analytics_SECOP_1.csv. peso 500 MB aprox.

	Portal de datos abiertos, conjunto de datos SECOP II - Contratos Electrónicos
https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h/data
Se descarga un archivo csv llamado Data_analytics_SECOP_2.csv. peso 1,5 GB aprox.
 
	Portal de datos abiertos, conjunto de datos Tienda Virtual del Estado Colombiano – TVEC
https://www.datos.gov.co/Gastos-Gubernamentales/Tienda-Virtual-del-Estado-Colombiano-Consolidado/rgxm-mmea/data
Se descarga un archivo csv llamado Data_analytics_TVEC.csv. peso 500 MB aprox.

Cabe mencionar que al ser esta base de datos diligenciada por entidades estatales, hay mucha información que se debe analizar al detalle dependiendo del modelo del negocio y del mercado. Por lo cual, los criterios que se generen como un error o datos que no fueron registrados por las entidades fueron modificados con el fin de poder realizar este ejercicio. En consecuencia, las conclusiones que de aquí se realicen van a ser de una muestra de contratos, mas no necesariamente reflejarán la realidad absoluta del mercado. 

Principal problema a resolver en esta primera parte del proyecto:

Este procedimiento inicial contempla la manipulación de bases de datos con un gran volumen de información, por lo cual necesitaremos usar un lenguaje de programación, para este caso Python y sus librerías de manipulación de bases de datos y herramientas gráficas para determinación de valores atípicos.
En consecuencia, este primer ejercicio consiste en realizar los siguientes procedimientos a las bases de datos en formato csv: 

-	Eliminación de contratos duplicados en cada plataforma.
-	Verificación de los estados de los contratos en SECOP, eliminar los estados que no corresponden con contratos firmados.
-	Agrupaciones de las modalidades de contratación y tipos de contrato identificados
-	La identificación de valores atípicos.
-	Integración de las tres bases de datos para hacer un análisis consolidado.
