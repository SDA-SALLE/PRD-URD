#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python


import sys
sys.path.append("core")
import os
from VNP import *
from excelmatriz import *
from PMC import *



archivepublic = os.path.join("..","data","VNP",'Publico',"PUBLICO.xlsx");
archiveindustrial = os.path.join("..","data","VNP",'Industrial',"INDUSTRIAL.xlsx");


#---------------------Vias No Pavimentadas Publicas-------------------------------------#
print "Convirtiendo Excel a Matriz, para poder tratar los datos del Excel VNP_PUBLICO.xlsx"
matrizpublic = convertXLSCSV(archivepublic)
public(matrizpublic, archivepublic)


#---------------------Vias No Pavimentadas Industriales-------------------------------------#
print "Convirtiendo Excel a Matriz, para poder tratar los datos del Excel VNP_Industrial.xlsx"
matrizindustrial = convertXLSCSV(archiveindustrial)
industrial(matrizindustrial, archiveindustrial)

brindingvnp()

archivesPM251 = os.path.join('..','data','out', 'EmissionGrid', 'VNP','PM25_VNPIndustrial.csv')
archivesPM252 = os.path.join('..','data','out', 'EmissionGrid', 'VNP','PM25_VNPPublic.csv')
brindingfinal(archivesPM251, archivesPM252)

archivesPM101 = os.path.join('..','data','out', 'EmissionGrid', 'VNP','PM10_VNPIndustrial.csv')
archivesPM102 = os.path.join('..','data','out', 'EmissionGrid', 'VNP','PM10_VNPPublic.csv')
brindingfinal(archivesPM101, archivesPM102)

print 'Start PMC'

folderGrid = os.path.join('..','data','out', 'EmissionGrid', 'VNP', '')
pmc(folderGrid)
folderout = os.path.join('..','data','out', 'EmissionGrid', 'VNP', 'PMC', '')
testingpmc (folderout)
print '-------------'
print 'PMC OK'

print  'Finalizado el Proceso'