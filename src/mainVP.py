# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import sys
sys.path.append('core')
from binding import *
from PMC import *
from VPP import *
from VPS import *
from excelmatriz import *
from binding import *
from flowsdays import *
from csv import *
from speciation import *
import os


archiveflows = os.path.join('..','data','flows','promFinal_1.csv'); #Archive traffic flow

archiveprincipal = os.path.join('..','data','VP' , 'Principales','PRINCIPALES_1.xlsx');
archivesecondary = os.path.join('..','data','VP','Secundarias','SECUNDARIAS_1.xlsx');
archivetm = os.path.join('..','data','VP','TM','TM_1.xlsx')

#flowsdays(archiveflows)
print 'comienza brinding hora para principales'
print '|==                                     |- 0%'

folder = os.path.join('..','data','VP','Principales','')
binding (archiveflows, archiveprincipal, folder)

print 'Finaliza proceso brinding hora principales' #End of main hour brinding process
print '|=========                              |- 25%'

print '------------------------------------------------------------------------'
print 'comienza brinding hora para secundarias' # Begining of secondary briniding process
print '|===================                    |- 50%'
bindingsecondary (archiveflows, archivesecondary)
print 'finaliza proceso brinding hora secundarias'

print '------------------------------------------------------------------------'
print 'comienza brinding hora para TM'
print '|===============================	       |- 75%'
folder = os.path.join('..','data','VP','TM','')
binding (archiveflows, archivetm, folder)
print 'finaliza proceso brinding hora TM'
print '|=======================================|- 100%'

archiveprincipal = os.path.join('..','data','VP','Principales','brinding.csv');
archivesecondary = os.path.join('..','data','VP','Secundarias','brinding.csv');
archivetm = os.path.join('..','data','VP','TM','brinding.csv');

#---------------------Vias Pavimentadas Principales-------------------------------------#
print 'Convirtiendo Excel a Matriz, para poder tratar los datos del Excel PRINCIPALES.xlsx'
matrizprincipal = convertCSVMatriz(archiveprincipal)

print 'Comienza Proceso para datos IDW Vias Principales Pavimentadas'
idw(matrizprincipal, archiveprincipal, 'Principal')


#---No process in 2014-----#
# print 'Comienza Proceso para datos CoKrigin Dia Habil Vias Principales Pavimentadas'
# ckdh(matrizprincipal, archiveprincipal, 'Principal')

# print 'Comienza Proceso para datos CoKrigin Dia No Habil Vias Principales Pavimentadas'
# ckdnh(matrizprincipal, archiveprincipal, 'Principal')

print ''
print '----------------------------------------------------------------------------------'
print ''

#---------------------Vias Pavimentadas TM-------------------------------------#
print 'Convirtiendo Excel a Matriz, para poder tratar los datos del Excel TM.xlsx'
matriztroncales = convertCSVMatriz(archivetm)

print 'Comienza Proceso para datos IDW Vias TM Pavimentadas'
idw(matriztroncales, archivetm,'TM')


#------No process in 2014-----#
# print 'Comienza Proceso para datos CoKrigin Dia Habil Vias TM Pavimentadas'
# ckdh(matriztroncales, archivetm, 'TM')

# print 'Comienza Proceso para datos CoKrigin Dia No Habil Vias TM Pavimentadas'
# ckdnh(matriztroncales, archivetm, 'TM')

print ''
print '----------------------------------------------------------------------------------'
print ''

#---------------------Vias Pavimentadas Secundarias-------------------------------------#
print 'Convirtiendo Excel a Matriz, para poder tratar los datos del Excel SECUNDARIAS.xlsx'
matrizsecondary = convertCSVMatriz(archivesecondary)

print 'Comienza Proceso para datos IDW Vias Secundarias Pavimentadas'
secundaryIDW(matrizsecondary, archivesecondary, 'Secundary')

#-- No process in 2014---#
# print 'Comienza Proceso para datos Homogeneos Vias Secundarias Pavimentadas'
# secundaryHomogeneous(matrizsecondary, archivesecondary, 'Secundary')

# print 'Comienza Proceso para datos Heterogeneos Vias Secundarias Pavimentadas'
# secundaryHeterogeneous(matrizsecondary, archivesecondary, 'Secundary')

print '----------------------------------------------------------------------------------'

emissiontotal()

print 'Start PMC'
folderGrid = os.path.join('..','data','out', 'EmissionGrid', 'VP', '')
pmc(folderGrid)
folderGrid = os.path.join('..', 'out', 'emissions', 'grid', '')
folderout = os.path.join('..', 'data','out', 'EmissionGrid', 'VP', 'PMC', '')
testingpmc(folderout)
print '-------------------'
print 'PMC OK'

#writefullfull('IDW_Principal')
#writefullfull('IDW_TM')


print "Comienza proceso de especiacion"
print "WARNING! Emissions to speciate are in g/h"
speciationvp()

print 'Process Testing'
testing()
print 'Testing OK'
print 'Finaliza con Exito'

