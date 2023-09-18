# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 13:43:38 2022
INTERFAZ EKG
@author: Diego Noguez
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStatusBar,QFileDialog,
                             QWidget,  QSplitter, QPushButton, QVBoxLayout, QToolBar,
                             QMenuBar, QAction, QFormLayout, QLabel
                             ,QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator

from modules.DFA import DFA
from modules.MDFA import MDFA
from modules.Dialog import Dialog
import pyqtgraph as pg  
import time

from numpy import (asarray, transpose,arange,where)
from pandas import (read_csv, DataFrame)
#%%
class Principal(QMainWindow):
    def __init__(self):
        super().__init__() #hereda de QmainWindow el constructor
        self.initUI()
        
    def DFA_boton(self):
        self.DFAWindow = DFA()
        self.DFAWindow.show()
    def MFDFA_boton(self):
        self.MFDFAWindow = MDFA()
        self.MFDFAWindow.show()
#%%
    def cargarSenial(self):
        self.txt_total.setText('')
        self.lbl_inicio.setText('')
        self.lbl_final.setText('')
        self.seg_pos.clear()
        self.btnIniciar.setEnabled(True)
        self.plot1.clear()
        self.nombreSenial= QFileDialog.getOpenFileName(None, 'Open file', '/home')        
        if(len(self.nombreSenial[0])!=0):
            print(self.nombreSenial)
            datos = read_csv(self.nombreSenial[0],sep='\t', header=None)
            lineas= datos.shape[1]
            if(lineas == 1):
                self.y = asarray(datos[0])
                self.y_auto = datos[0]
            elif(lineas == 2):
                self.y = asarray(datos[1])
                self.y_auto = datos[1]
            self.plot1.setLabel('bottom',color='k', **{'font-size':'14pt'})
            self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
            # Y1 axis   
            self.plot1.setLabel('left',color='k', **{'font-size':'14pt'})
            self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
            names=str.split(self.nombreSenial[0],"/")
            t=len(names)
            self.nombre= names[t-1]
            self.plot1.setTitle(self.nombre)
            self.plot1.plot(self.y,pen='k')
            self.btnauto.setEnabled(True)
#%%
    def localizacion(self):
        if(self.aux == True):
            i = self.seg_pos.currentIndex()
            if(i == 0):
                self.lbl_inicio.setText('ini')
                self.lbl_final.setText('end')
            else:
                self.lbl_inicio.setText(str(self.inicio[i-1]))
                self.lbl_final.setText(str(self.final[i-1]))
#%%
    def colocar(self):
        inicio = int(self.lbl_inicio.text())
        final  = int(self.lbl_final.text())
        if(self.aux2 == True):
            self.lr.setRegion([inicio,final])

#%% 
    def autoseg(self):
        self.aux == False
        self.inicio = []
        self.final  = []
        self.seg_pos.clear()
        self.seg_pos.addItem('')
        def group_consecutives(vals, step=1):
            run = []
            result = [run]
            expect = None
            for v in vals:
                if (v == expect) or (expect is None):
                    run.append(v)
                else:
                    run = [v]
                    result.append(run)
                expect = v + step
            return result
        if(len(self.txt_umbral.text())!=0 and len(self.txt_basal.text())!=0 and len(self.txt_ancho.text())!=0 
           and len(self.txt_separacion.text())!=0):
            umbral     = float(self.txt_umbral.text())
            basal      = float(self.txt_basal.text())
            ancho      = float(self.txt_ancho.text())
            separacion = float(self.txt_separacion.text())        
            y = self.y_auto
            
            loc_x = []
            for i in range(len(y)):
                if(y[i]>umbral):
                    loc_x.append(i) 
                    
            pico_range = group_consecutives(loc_x)        
            
            loc_x1 = []
            for i in range(len(pico_range)):
                aux  = pico_range[i]
                pico = list(y[aux])
                pos_aux = pico.index(max(pico))
                loc_x1.append(aux[pos_aux])
                    
            loc = []
            loc.append(loc_x[0])
            for i in range(1,len(loc_x1)):
                if(loc_x1[i]-loc_x1[i-1]>ancho):
                    loc.append(loc_x1[i])
                    
            ini = []
            end = []        
            for i in range(len(loc)):
                if(loc[0]>2*separacion ):
                    x_ini   = arange(loc[i]-separacion,loc[i])
                    y_ini   = y[x_ini]
                    
                    x_end   = arange(loc[i],loc[i] + separacion)
                    y_end   = y[x_end]
                    
                    donde_ini = where(y_ini <= min(y_ini) + basal)[0]
                    donde_fin = where(y_end <= min (y_ini) + basal)[0]
                                
                    if(len(donde_fin)!=0 and len(donde_ini)!=0 ):
                        ini.append(x_ini[max(donde_ini)])
                        end.append(x_end[min(donde_fin)]) 
                elif(loc[0]<separacion):
                    x_ini   = arange(0,loc[i])
                    y_ini   = y[x_ini]
                    
                    x_end   = arange(loc[i],loc[i] + separacion)
                    y_end   = y[x_end]
                    
                    donde_ini = where(y_ini <= min(y_ini) + basal)[0]
                    donde_fin = where(y_end <= min (y_ini) + basal)[0]
                                
                    if(len(donde_fin)!=0 and len(donde_ini)!=0 ):
                        ini.append(x_ini[max(donde_ini)])
                        end.append(x_end[min(donde_fin)]) 
                        
                elif(len(y) - (loc[len(loc)-1] + separacion) < 0 ):
                    x_ini   = arange(loc[i]-separacion,loc[i])
                    y_ini   = y[x_ini]
                    
                    x_end   = arange(loc[i],len(y))
                    y_end   = y[x_end]
                    
                    donde_ini = where(y_ini <= min(y_ini) + basal)[0]
                    donde_fin = where(y_end <= min (y_ini) + basal)[0]
                                
                    if(len(donde_fin)!=0):
                        ini.append(x_ini[max(donde_ini)])
                        end.append(x_end[min(donde_fin)]) 
            ini = list(set(ini))
            end = list(set(end))
            ini = list(sorted(ini))
            end = list(sorted(end))
            names = str.split(self.nombreSenial[0],self.nombre)
            nam   = str.split(self.nombre,'.') 
    
            for i in range(len(ini)):
                self.seg_pos.addItem(str(i+1))
                self.inicio.append(int(ini[i]))
                self.final.append(int(end[i]))
                data = DataFrame(y[int(ini[i]):int(end[i])])
                data.to_csv(names[0]+nam[0]+'_seg_'+ str(i+1) +'.txt',sep ='\t', header = None, index = False)
            self.aux = True
            self.txt_total.setText(str(len(self.inicio)))
            self.btn_loc.setEnabled(True)
            self.btnauto.setEnabled(False)
        elif(len(self.txt_umbral.text())!=0 or len(self.txt_basal.text())!=0 or len(self.txt_ancho.text())!=0 
           or len(self.txt_separacion.text())!=0):
            self.dialogo_error = Dialog('Error: Missing value ','Icons\error.png')
            self.dialogo_error.show()
        elif(len(self.txt_umbral.text())!=0 and len(self.txt_basal.text())!=0 and len(self.txt_ancho.text())!=0 
           and len(self.txt_separacion.text())!=0):
            self.dialogo_error = Dialog('Error: Missing value ','Icons\error.png')
            self.dialogo_error.show()
            
#%%
    def enabledButtons(self):
        self.btnAdd.setEnabled(True)
        self.txtns.setEnabled(True)
        self.plot1.addItem(self.lr)
        self.btnIniciar.setEnabled(False)
        self.aux2 = True
#%%      
    def addInterval(self):
        duracion = []
        contador = 0
        if(len(self.txtns.text())==0):
            self.dialogo_error = Dialog('A segment number must be type() = int ','Icons\error.png')
            self.dialogo_error.show()
        else:
            contador  = int(self.txtns.text())
            regionSelected = self.lr.getRegion()
            ini = int(regionSelected[0])
            fin = int(regionSelected[1])
            duracion.append(self.y[ini:fin])
            duracion = transpose(duracion)
            df = DataFrame(duracion)
            names = str.split(self.nombreSenial[0],self.nombre)
            nam   = str.split(self.nombre,'.')
            df.to_csv(names[0]+nam[0]+'_seg_'+str(contador)+'.txt',index=False,sep='\t', header = None, mode = 'w') 
            duracion = []        
            linea1= pg.InfiniteLine(pos= ini, angle=90, movable=False)
            linea2= pg.InfiniteLine(pos= fin, angle=90, movable=False)
            self.plot1.addItem(linea1)
            self.plot1.addItem(linea2)
            self.lr.setRegion([fin,fin+6000])

#%%
    def reboot(self):
        self.contador=0
        self.valorContador.setText("")

#%%  
    def initUI(self):
        pg.setConfigOption('background', 'w')       
        self.app_name("EKG") #added
        self.app_logo("Icons\multifractal.ico") #added
        ##################################################################
        ### Barra de Herramientas 
        ##################################################################
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        
        barra_herr = QToolBar("Toolbar")
        self.addToolBar(barra_herr)
        
        barra_menu = QMenuBar()
        self.setMenuBar(barra_menu)
 
        #ICONOS DE LA BARRA DE HERRAMIENTAS    
        abrir_action = QAction(QIcon('Icons/open.png'), 'Load Signal', self)
        abrir_action.setToolTip('Load Signal')
        abrir_action.setStatusTip('Load signal to segment')
        abrir_action.triggered.connect(self.cargarSenial)
        barra_herr.addAction(abrir_action)
        barra_herr.addSeparator()
        
        DFA_action = QAction(QIcon('Icons/DFA.ico'), 'Detrended Analysis Fluctuation', self)
        DFA_action.setToolTip('Detrended Analysis Fluctuation')
        DFA_action.setStatusTip('Detrended Analysis Fluctuation')
        DFA_action.triggered.connect(self.DFA_boton)
        barra_herr.addAction(DFA_action)
        
        MDFA_action = QAction(QIcon('Icons/multifractal.ico'), 'Multifractal Detrended Analysis Fluctuation', self)
        MDFA_action.setToolTip('Multifractal Detrended Analysis Fluctuation')
        MDFA_action.setStatusTip('Multifractal Detrended Analysis Fluctuation')
        MDFA_action.triggered.connect(self.MFDFA_boton)
        barra_herr.addAction(MDFA_action)
        #################################################################
        ##     Definición de variables globales
        #################################################################
        self.nombreSenial = ''
        self.y = []
        self.aux = 0
        self.aux2 = False
        #################################################################
        ##     Definición de elementos contenedores
        #################################################################
        contain = QSplitter(Qt.Horizontal)
        graficos = QVBoxLayout()
        botones  = QVBoxLayout()
        results2 = QFormLayout()
        results3 = QFormLayout()
        results  = QFormLayout()
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        #Region for segment in signal
        self.lr = pg.LinearRegionItem([0,6000])
        
        btnLoadSig = QPushButton('Load signal')
        btnLoadSig.clicked.connect(self.cargarSenial)
        btnLoadSig.setStyleSheet("font-size: 18px")
        
        self.btnIniciar = QPushButton('Start segmentation')
        self.btnIniciar.clicked.connect(self.enabledButtons)
        self.btnIniciar.setEnabled(False)
        self.btnIniciar.setStyleSheet("font-size: 18px")

        self.btnAdd = QPushButton('Add segment')
        self.btnAdd.clicked.connect(self.addInterval)
        self.btnAdd.setEnabled(False)
        self.btnAdd.setStyleSheet("font-size: 18px")
        
        txtnumseg  = QLabel("Segment num:")
        txtnumseg.setStyleSheet("font-size: 18px")
                
        validator = QIntValidator()
        validator.setRange(100,999)  
        
        self.txtns = QLineEdit()
        self.txtns.setValidator(validator)
        self.txtns.setEnabled(False)
        
        lbl_umbral = QLabel('Upper threshold:')
        lbl_umbral.setStyleSheet("font-size: 18px")
        self.txt_umbral = QLineEdit()
        
        
        lbl_basal = QLabel('Lower threshold')
        lbl_basal.setStyleSheet("font-size: 18px")
        self.txt_basal = QLineEdit()
        
        lbl_ancho = QLabel('Segment width ')
        lbl_ancho.setStyleSheet("font-size: 18px")
        self.txt_ancho = QLineEdit()
        
        lbl_separacion = QLabel('Distance:')
        lbl_separacion.setStyleSheet("font-size: 18px")
        self.txt_separacion = QLineEdit()
        
        self.btnauto = QPushButton('Start auto-segmentation')
        self.btnauto.clicked.connect(self.autoseg)
        self.btnauto.setStyleSheet("font-size: 18px")
        self.btnauto.setEnabled(False)
        
        lbl_total = QLabel('# of segments:')
        lbl_total.setStyleSheet('font-size: 18px')
        
        self.txt_total = QLabel()
        self.txt_total.setStyleSheet('font-size: 18px')
        
        lbl_file = QLabel('Segment: ')
        lbl_file.setStyleSheet("font-size: 18px")
        self.seg_pos = QComboBox()
        self.seg_pos.currentIndexChanged.connect(self.localizacion)
        
        self.lbl_inicio = QLabel()
        self.lbl_inicio.setStyleSheet("font-size: 18px")
        self.lbl_final = QLabel()
        self.lbl_final.setStyleSheet("font-size: 18px")
        
        self.btn_loc = QPushButton('Find segment')
        self.btn_loc.setStyleSheet("font-size: 18px")
        self.btn_loc.clicked.connect(self.colocar)
        self.btn_loc.setEnabled(False)
        
        lbl_autoseg = QLabel("Auto-Segmentation")
        lbl_autoseg.setStyleSheet("font-size: 20px")
        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom',color='k', **{'font-size':'16pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        self.plot1.setLabel('left',color='k', **{'font-size':'16pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        graficos.addWidget(self.plot1)
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        botones.addWidget(btnLoadSig)
        botones.addWidget(self.btnIniciar)
        results.addRow(txtnumseg, self.txtns)
        results.addRow(self.btnAdd)
        botones.addLayout(results)     
        
        results2.addRow(lbl_autoseg)
        results2.addRow(lbl_umbral, self.txt_umbral)
        results2.addRow(lbl_basal , self.txt_basal)
        results2.addRow(lbl_ancho , self.txt_ancho)
        results2.addRow(lbl_separacion, self.txt_separacion)
        botones.addLayout(results2)        
        botones.addWidget(self.btnauto)
        results3.addRow(lbl_total,self.txt_total)
        results3.addRow(lbl_file,self.seg_pos)
        results3.addRow(self.lbl_inicio,self.lbl_final)
        results3.addRow(self.btn_loc)
        botones.addLayout(results3)
        #################################################################
        ##     Colocar elementos en la ventana
        #################################################################        
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)

        contain.addWidget(gra)
        contain.addWidget(bot)
        self.setCentralWidget(contain)
        self.show()
 
        
 
#%% MODIFICADORES DEL UI   NEW     
    def app_name(self,name):
        self.name=name
        self.setWindowTitle(self.name)
    
    def app_logo(self,path):
        self.path=path
        self.setWindowIcon(QIcon(self.path))
    

#%%   EKG interfaz
class MiInterfaz(Principal):
    def __init__(self):
        super().__init__()
    
    def cargarSenial(self):
        super().cargarSenial()
#%%     
    def R_points(self,x, y_geq_t): #funcion que encuentra los puntos R  
        tam = len(x)
        
        x_max=[] #Aqui se va a guardar la coordenada x de cada punto R
        y_max=[] #Aqui se va a guardar la coordenada y de cada punto R
        
        ini = 0
        fin = 0
        
        max=0
        max_x=0

        for i in range(tam - 1):
            if (x[i + 1] - x[i]) != 1: #Si no son consecutivos
                fin = i
                segmento = x[ini:fin + 1] #Tengo que sumar un uno porque el stop esta en fin, sino no guarda la ultima
                y_segmento = y_geq_t[ini:fin + 1]
                
                for j in range(len(y_segmento)):
                    if y_segmento[j]>max:
                        max = y_segmento[j]
                        max_x = segmento[j]
                
                x_max.append(max_x)
                y_max.append(max)
                
                max=0
                max_x=0

                
                ini = fin + 1 #Inicia en el ultimo indice que me quede
        
        #El if de distancia distinta de 1 no esta contando el ultimo intrervalo, por lo cual se tiene que hacer una vez más.
        
        segmento = x[ini:tam] #Ahora segmento es el indice donde inicié al ultimo 
        y_segmento = y_geq_t[ini:tam]
        
        for j in range(len(y_segmento)):
            if y_segmento[j]>max:
                max = y_segmento[j]
                max_x = segmento[j]
        
        x_max.append(max_x)
        y_max.append(max)
        
        return x_max, y_max
 #%%     
    def imprimir_coordenadas(self,x,y):
        if (len(x) != 0) and  (len(x) == len(y)):
            num=1
            print(f"\nA total of {len(x)} R points were detected \n")
            for j in range(len(x)):
                print(f"The point #{num} have coordinates ({x[j]},{y[j]}) ")
                num=num+1   
 #%%    
    def points_selection(self): #Este metodo selecciona los puntos R
        self.btnPuntos.setEnabled(True)
        
        start_time=time.time() #medir cuanto tiempo tarda en encontrar los puntos R
                
        if len(self.form_umbral_puntos.text())!=0:
            umbral_puntos = float (self.form_umbral_puntos.text())
            x = []
            y_geq_t = []
            tam = len(self.y) #self.y son los puntos del EKG
            
            for i in range (tam):
                if self.y[i]>umbral_puntos:
                    y_geq_t.append(self.y[i]) #coordenada y s.t. 'y' \geq umbral
                    x.append(i)  #coordenada x de la respectiva y
        else:
            dialogo_error_umbral = Dialog('Error: Missing Threshold value','Icons\error.png')
            dialogo_error_umbral.show()
        
        x_max, y_max = self.R_points(x,y_geq_t)
        
        #para poder usar las varibales en otro método
        self.x_max=x_max
        self.y_max=y_max
        
        self.scatterplot = pg.ScatterPlotItem(x_max, y_max, symbol='x', pen ='g', size=30)
        self.plot1.addItem(self.scatterplot)
        
        
        self.imprimir_coordenadas(x_max, y_max)
        
        end_time=time.time()
        final_time=end_time-start_time
        
        print(f"Running time:{final_time} sec")
        
 #%%
    def Reiniciar(self):
        self.btnReiniciar.setEnabled(True)
        
        self.plot1.removeItem(self.scatterplot)

        
 #%%
    def medir_dist(self,x,freq):
        ms=1000 #constante de milisegundo
        
        #La frecuencia es cuantos datos se registra por segundo
        #entonces para calcular el tiempo en ms que transcurrio dado un valor x
        #usare regla de 3
        
        self.x_max_ms=[] #Aqui voy a guardar los tiempos
        
        for i in range(len(x)):
            x_time=(x[i]*ms)/freq
            self.x_max_ms.append(x_time)
        
                
        self.dist_points=[] #aqui se guardan las distancias
        
        for i in range(len(self.x_max_ms)-1):
            distance=self.x_max_ms[i+1]-self.x_max_ms[i]
            self.dist_points.append(distance)
        
        print("\n\n")
        for i in range(len(self.dist_points)):
            print(f"The time between the points {i+1} and {i+2} is {self.dist_points[i]} ms ")
        
        time_sample=(x[len(x)-1]*1/60)/freq

        print(f"\nThe EKG duration was {time_sample} minutes  ")
#%%
    def distance(self): #Este metodo llama a la función que mide distancia
        self.btnConfirm.setEnabled(True)
        
        start_time=time.time() #medir cuanto tiempo tarda en encontrar los puntos R

        
        if len(self.form_freq.text())!=0 :
            freq=float(self.form_freq.text())
            self.medir_dist(self.x_max,freq) 
        else:
            self.dialogo_error_freq = Dialog('Error: Missing Frequency value','Icons\error.png')
            self.dialogo_error_freq.show()  
            
        end_time=time.time()
        final_time=end_time-start_time
            
        print(f"Running time:{final_time} sec")

#%%
    def imprime_HRV(self,distancia,time): #imprime la HRV
        onda=pg.plot(time[1:],distancia, pen=pg.mkPen("k", width=1) )
        
        onda.showGrid(x = True, y = True, alpha = 1.0)
        
        titulo = "Heart Rate Variability"
        
        onda.setWindowTitle(titulo)

#%%
    def HRV_plot(self): #Este metodo imprime la onda R cuando se activa boton
        self.btnOndaR.setEnabled(True)
        start_time=time.time() 
        
        self.imprime_HRV(self.dist_points,self.x_max_ms)

        end_time=time.time()
        final_time=end_time-start_time
            
        print(f"HRV PLOT Running time:{final_time} sec")
#%% 
    def export_hrv(self):
        self.btnExport.setEnabled(True)
        
        name= self.form_export.text()
        f= open(f"{name}.txt","w+")
        
        for x in self.dist_points:
            f.write(f"{x}\n")
        
        f.close()
        
        print("Your .txt file is in the interface folder")
#%%            
    def initUI(self):
        pg.setConfigOption('background', 'w')       
        self.app_name("EKG") #added
        ##################################################################
        ### Barra de Herramientas 
        ##################################################################
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        
        barra_herr = QToolBar("Toolbar")
        self.addToolBar(barra_herr)
        
        barra_menu = QMenuBar()
        self.setMenuBar(barra_menu)
        
        abrir_action = QAction(QIcon('Icons/open.png'), 'Load Signal', self)
        abrir_action.setToolTip('Load Signal')
        abrir_action.setStatusTip('Load signal to segment')
        abrir_action.triggered.connect(self.cargarSenial)
        barra_herr.addAction(abrir_action)
        barra_herr.addSeparator()
        
        #################################################################
        ##     Definición de variables globales
        #################################################################
        self.nombreSenial = ''
        self.y = []
        self.aux = 0
        self.aux2 = False
        #################################################################
        ##     Definición de elementos contenedores
        #################################################################
        contain = QSplitter(Qt.Horizontal)
        graficos = QVBoxLayout()
        botones  = QVBoxLayout()
        results  = QFormLayout()
        dato_frec= QFormLayout()
        exportar_txt= QFormLayout()
        nombre = QVBoxLayout()
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        #Region for segment in signal
        self.lr = pg.LinearRegionItem([0,6000])
        
        btnLoadSig = QPushButton('Load signal')
        btnLoadSig.clicked.connect(self.cargarSenial)
        btnLoadSig.setStyleSheet("font-size: 18px")
        
        self.btnIniciar = QPushButton('Start segmentation')
        self.btnIniciar.clicked.connect(self.enabledButtons)
        self.btnIniciar.setEnabled(False)
        self.btnIniciar.setStyleSheet("font-size: 18px")

        self.btnAdd = QPushButton('Add segment')
        self.btnAdd.clicked.connect(self.addInterval)
        self.btnAdd.setEnabled(False)
        self.btnAdd.setStyleSheet("font-size: 18px")
        
        txtnumseg  = QLabel("Segment num:")
        txtnumseg.setStyleSheet("font-size: 18px")
                
        validator = QIntValidator()
        validator.setRange(100,999)  
        
        self.txtns = QLineEdit()
        self.txtns.setValidator(validator)
        self.txtns.setEnabled(False)
        
        lbl_umbral = QLabel('Upper threshold:')
        lbl_umbral.setStyleSheet("font-size: 18px")
        self.txt_umbral = QLineEdit()
        
        lbl_basal = QLabel('Lower threshold')
        lbl_basal.setStyleSheet("font-size: 18px")
        self.txt_basal = QLineEdit()
        
        lbl_ancho = QLabel('Segment width ')
        lbl_ancho.setStyleSheet("font-size: 18px")
        self.txt_ancho = QLineEdit()
        
        lbl_separacion = QLabel('Distance:')
        lbl_separacion.setStyleSheet("font-size: 18px")
        self.txt_separacion = QLineEdit()
        
        self.btnauto = QPushButton('Start auto-segmentation')
        self.btnauto.clicked.connect(self.autoseg)
        self.btnauto.setStyleSheet("font-size: 18px")
        self.btnauto.setEnabled(False)
        
# =============================================================================
        lbl_total = QLabel('# of segments:')
        lbl_total.setStyleSheet('font-size: 18px')
# =============================================================================
        
        self.txt_total = QLabel()
        self.txt_total.setStyleSheet('font-size: 18px')
        
        lbl_file = QLabel('Segment: ')
        lbl_file.setStyleSheet("font-size: 18px")
        self.seg_pos = QComboBox()
        self.seg_pos.currentIndexChanged.connect(self.localizacion)
        
        self.lbl_inicio = QLabel()
        self.lbl_inicio.setStyleSheet("font-size: 18px")
        self.lbl_final = QLabel()
        self.lbl_final.setStyleSheet("font-size: 18px")
        
        self.btn_loc = QPushButton('Find segment')
        self.btn_loc.setStyleSheet("font-size: 18px")
        self.btn_loc.clicked.connect(self.colocar)
        self.btn_loc.setEnabled(False)
        
        lbl_autoseg = QLabel("Auto-Segmentation")
        lbl_autoseg.setStyleSheet("font-size: 20px")
        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom',color='k', **{'font-size':'16pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        self.plot1.setLabel('left',color='k', **{'font-size':'16pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        graficos.addWidget(self.plot1)
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        botones.addWidget(btnLoadSig)
        botones.addWidget(self.btnIniciar)
        results.addRow(txtnumseg, self.txtns)
        results.addRow(self.btnAdd)
        botones.addLayout(results)     
        
        
#NEW---------------------------------------------------------------------------------------------      
        
        txtRR  = QLabel("R-R Intervals") #Texto intervalos R-R
        txtRR.setStyleSheet("font-size: 18px")
        txtRR.setAlignment(QtCore.Qt.AlignCenter) #centra el texto
       
        #Boton que inicia la seleccion de puntos
        self.btnPuntos = QPushButton('Start points selection') #boton para seleccion de elementos        
        self.btnPuntos.setStyleSheet("font-size: 18px")
        self.btnPuntos.clicked.connect(self.points_selection) #conecta el boton

        txt_umbral_puntos  = QLabel("Threshold for points selection:") #Texto seleccion de puntos
        txt_umbral_puntos.setStyleSheet("font-size: 18px")
        self.form_umbral_puntos = QLineEdit()#linea para poner umbral de puntos       

        txtfreq  = QLabel("Frequency:") #Texto frecuencia
        txtfreq.setStyleSheet("font-size: 18px")
        self.form_freq = QLineEdit()#linea para poner frecuencia
        
        self.btnConfirm = QPushButton('Confirm points selected') #boton para seleccion de elementos        
        self.btnConfirm.setStyleSheet("font-size: 18px")
        self.btnConfirm.clicked.connect(self.distance) #conecta el boton

        self.btnReiniciar = QPushButton('Restart') #boton para seleccion de elementos        
        self.btnReiniciar.setStyleSheet("font-size: 18px")
        self.btnReiniciar.clicked.connect(self.Reiniciar) #conecta el boton
         
        self.btnOndaR = QPushButton('HRV Plot') #boton para seleccion de elementos        
        self.btnOndaR.setStyleSheet("font-size: 18px")
        self.btnOndaR.clicked.connect(self.HRV_plot) #conecta el boton

        self.btnExport = QPushButton('Export HRV') #boton para seleccion de elementos        
        self.btnExport.setStyleSheet("font-size: 18px")
        self.btnExport.clicked.connect(self.export_hrv) #conecta el boton
        
        txtexport  = QLabel("Name for HRV.txt:") #Texto frecuencia
        txtexport.setStyleSheet("font-size: 18px")
        self.form_export = QLineEdit()#linea para poner frecuencia
        
        
        
        nombre.addWidget(txtRR)
        
        botones.addLayout(nombre)
        
        dato_frec.addRow(txt_umbral_puntos, self.form_umbral_puntos)
        dato_frec.addRow(txtfreq, self.form_freq)
        
        
        botones.addLayout(dato_frec) #Añade a nuevos_botenes el layout de datos 
        
        botones.addWidget(self.btnPuntos)        #Añade el widget de boton frecuencia
        botones.addWidget(self.btnConfirm)        #Añade el widget de boton frecuencia
        botones.addWidget(self.btnReiniciar)
        botones.addWidget(self.btnOndaR)
        botones.addWidget(self.btnExport)
        
        exportar_txt.addRow(txtexport, self.form_export)

        botones.addLayout(exportar_txt) #Añade a nuevos_botenes al layout 
#------------------------------------------------------------------------
        
        #################################################################
        ##     Colocar elementos en la ventana
        #################################################################        
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)
        contain.addWidget(gra)
        contain.addWidget(bot)
        
        
        self.setCentralWidget(contain)
        self.show() 
        
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MiInterfaz()
    sys.exit(app.exec_())
         
