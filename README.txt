Para correr esta interfaz es necesario instalar las paqueterias:
-PyQt5, pyqtgraph,numpy, pandas, time

Se han heredado métodos para cargar/cortar una señal de una 
interfaz ya existente. Varios métodos de la super clase necesitan
archivos de esta carpeta para correr, sin embargo no se han utilizado 
para este proyecto más que los 2 ya mencionados. 

Los métodos relacionados a la detección 
de puntos R, intervalos R-R y Variabilidad de Frecuencia Cardiaca
han sido creados desde cero.

Los métodos relacionados a mi interfaz inician desde la 
linea 420, lo anterior a esa linea es la clase de la que
se esta heredando.

En el método "initUI" se han dejado algunas lineas de la 
clase que se hereda, ya que la super clase necesita 
estas variables para correr.

Se añadieron los Botones/Labels/LineEdit/Layouts 
necesarios para los nuevos métodos de mi interfaz, estos inician
desde la linea 743 de este método.

En la carpeta: Señales, se encuentran archivos .txt para 
probar el programa, todos estos Electrocardiogramas
tienen frecuencia f=512 Hz (valor a ingresar en frecuencia)

Se puede encontrar más información en trabajo escrito.

Cualquier Duda: diego.ngzru@gmail.com
Diego Noguez Ruiz