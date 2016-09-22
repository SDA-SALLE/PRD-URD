# RESUSPENDED
Resuspended paved and unpaved. </br>
Programing in python 2.7 import directories xlrd, json, csv, sys. </br>
To import xlrd preview install pip: 
<ul>
<li>$ sudo apt-get install pip 
<li>$ pip install xlrd
</ul>

Execute for paved archive in folder src/mainVP.py 
<ul>
<li>$ python mainVP.py
</ul>

Execute for unpaved archive in folder src/mainVNP.py 
<ul>
<li>$ python mainVNP.py
</ul>


##Como correr el programa

```python
  cd src
  python mainVP.py 
  python mainVNP.py
```

#PRD – URD (Paved Roads – Unpaved Roads)
</br>
Este sub-modulo corresponde a Material Resuspendido (RPM); su estructura consiste en:
<ul>
<li>data: Archivos de entrada y salida</li>
<ul>
<li>in: archivos de entrada</li>
<ul>
<li>constants: Aloja las constantes las cuales no cambian durante las corridas</li>

<ul>
<li>Uncertain_2014.xlsx: Incertidumbres por estación para el año 2014.</li>
<li>Uncertain_2030.xlsx: Incertidumbres por estación para el año 2030.</li>
<li>Resuspeded_2014.xlsx: Valores constantes, los cuales contienen, Días Hábiles, Días No Hábiles; Porcentajes de distribución horaria; Pesos Vehiculares; valores exponenciales. Esto es utilizado dentro de los cálculos de emisiones.</li>
<li>Resuspeded_2030: Valores constantes, los cuales contienen, Días Hábiles, Días No Hábiles; Porcentajes de distribución horaria; Pesos Vehiculares; valores exponenciales. Esto es utilizado dentro de los cálculos de emisiones.</li>
</ul>

<li>flows: Aloja los flujos vehiculares que salen del módulo PRE > FLX se identifican por la fecha.</li>

<ul>
<li>RPM_2014.csv: Archivo .csv que aloja los datos de los flujos vehiculares 2014, este es el resultado del módulo PRE > FLX.</li>
<li>RPM_2030.csv: Archivo .csv que aloja los datos de los flujos vehiculares 2030, este es el resultado del módulo PRE > FLX.</li>
</ul>

<li>VP: Aloja los links correspondientes que provienen de ArcGis.</li>

<ul>
<li>PRINCIPALES: Aloja los links de vías principales, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares.</li>
 
  <ul>
      <li>PRINCIPALES_2014.xlsx: Archivo que contiene la información de links para las vías principales al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
      <li>PRINCIPALES_2030.xlsx: Archivo que contiene la información de links para las vías principales al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
  </ul>

<li>SECUNDARIAS: Aloja los links de vías secundarias, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares. </li>
 
  <ul>
      <li>SECUNDARIAS_2014.xlsx: Archivo que contiene la información de links para las vías secundarias al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
      <li>SECUNDARIAS_2030.xlsx: Archivo que contiene la información de links para las vías secundarias al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
  </ul>

<li>TM: Aloja los links de vías para Transmilenio, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares. </li>
  
  <ul>
      <li>TM_2014.xlsx: Archivo que contiene la información de links para troncales Transmilenio al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
      <li>TM_2030.xlsx: Archivo que contiene la información de links para troncales transmilenio al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
  </ul>
</ul>

<li>VNP: Aloja los links correspondientes que provienen de ArcGis.</li>

<ul>
<li>INDUSTRIAL: Aloja los links de vías industriales, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares.</li>
  
  <ul>
      <li>INDUSTRIAL_2014.xlsx: Archivo que contiene la información de links para las vías industriales al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
      <li>INDUSTRIAL_2030.xlsx: Archivo que contiene la información de links para las vías industriales al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
  </ul>

<li>PUBLICO: Aloja los links de vías públicas, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares. </li>
  
  <ul>
      <li> PUBLICO_2014.xlsx: Archivo que contiene la información de links para las vías públicas al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
      <li>PUBLICO_2030.xlsx: Archivo que contiene la información de links para las vías públicas al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
  </ul>
</ul>  

<li>speciation: Aloja los archivos con los datos para el proceso de especiación de las emisiones VNP y VP, procesadas.</li>

<ul>
<li>VNP_SCP_PROF_2014.xlsx: contiene los perfiles de especiación para VNP (vías no pavimentadas) del año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
<li>VNP_SCP_PROF_2030.xlsx: contiene los perfiles de especiación para VNP (vías no pavimentadas) del año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
<li>VP_SPC_PROF_2014.xlsx: contiene los perfiles de especiación para VP (vías pavimentadas) del año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
<li>VP_SPC_PROF_2030.xlsx: contiene los perfiles de especiación para VP (vías pavimentadas) del año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
</ul>
</ul>

<li>out: archivos de salida </li>
<ul>
<li>EmissionDay: Contienen los resultados por día de las emisiones. </li>
<li>EmissionGrid: Contienen los resultados de VP y VNP de las emisiones por Grilla.</li>
<li>EmissionYear: Contiene las emisiones por año, por grilla.</li>
<li>speciation: Contiene los archivos resultantes del proceso de especiación, para VP y VNP, estos se entregan g/s.</li>
<li>TotalEmisions: Contiene los totales de las emisiones, Tonelada año.</li>
</ul>
</ul>

<li>src: Códigos de programación, y su ejecutable mainVP.py / mainVNP.py</li>
<ul>
<li>core: Aloja los códigos que se reutilizan en todos los módulos. Es decir que se encuentran escritos como funciones generales.</li>
<ul>
<li>binding.py: Se encarga de unir los flujos con los links, de la misma forma que de unir algunos datos intermedios.</li>
<li>clear.py: Realiza una limpieza de la carpeta y subcarpetas out para tener más confianza en los resultados de salida.</li>
<li>matriz.py: Realiza las operaciones de pasar de Excel a csv y también de convertir de csv a matriz para realizar operaciones.</li>
<li>operaciones.py: Realiza las operaciones, tanto para VP como para VNP.</li>
<li>promegd.py: Realiza el promedio para gramo día.</li>
<li>PMC.py: Calcula el PMC, donde es la resta de PM10 – PM2.5</li>
<li>wcsv.py: Realiza la escritura de los datos, o resultados.</li>
</ul>

<li>VPP.py: Realiza las operaciones para calcular emisiones de vías pavimentadas principales.</li>
<li>VPS.py: Realiza las operaciones para calcular emisiones de vías pavimentadas secundarias.</li>
<li>VNP.py: Realiza las operaciones para calcular emisiones de vías no pavimentadas.</li>
<li>speciation.py: Realiza el cálculo de especiación.</li>
<li>mainVP.py: Ejecutable, el cual contiene las instrucciones y rutas, para Vías Pavimentadas.</li>
<li>mainVNP.py: Ejecutable, el cual contiene las instrucciones y rutas, para Vías No Pavimentadas.</li>
<li>uncertain.py: Realiza la operación para sacar las incertidumbres.</li>
<li>flowsdays.py: Realiza sumas, y cálculos de emisiones año, día.</li>
</ul>
