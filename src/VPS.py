#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python

import sys
sys.path.append("core")
from operaciones import *
from wcsv import *
from promegd import *
from flowsdays import *
import csv
import json
import numpy as np

PesosV = {'L':[1.6], 'C':[2.4], 'BT':[8.2], 'B':[14.5], 'AL':[14.5],  'ESP':[8.2], 'INT':[14.5], 'C2P':[4.6], 'C2G':[8.5], 'C3-C4':[28], 'C5':[35.0], '>C5':[40], 'M':[0.2]}
Art = ['AT', 'BA', 'NH_AT', 'NH_BA', 'TOTAL', 'NH_TOTAL']

PMDIEZK = 0.62
PMDOSK = 0.15
PMDIEZSL = 0.677
PMDIEZW =  0.85
PMDOSSL = 0.91
PMDOSW = 1.02

#Dias Habiles y No Habiles 2012
DH = 245
DNH = 120

def secundaryHomogeneous(matriz, archive, noun):

	name = []
	mat = []
	m = []
	NamesVehicles = []
	index = 0
	headsecundary = matriz[0,:]

	for value in headsecundary:

		if value == 'Cs_Homog': #La columna de (CS...)
			colCs = index
		if value == 'Largo_Via' or value == 'Largo_via': #La columna de (Long_Grid...)
			colLongGrid = index
		if value == 'hora':
			colIH = index+1
		if value == 'TOTAL':
			colFH = index
		if value == 'NH_TOTAL':
			colFNH = index
		if value == 'FID_Grilla':
			colID = index #La coluna de (TTOAL Suma Flujos vehiculares dia no habil)
		if value == 'BA':
			colBA = index
		if value == 'AT':
			colAT = index
		if value == 'NH_BA':
			colNHBA = index
		if value == 'NH_AT':
			colNHAT = index
		index+=1

	posArt = [colAT, colBA, colNHBA, colNHAT]
	
	headNamesVehicles = matriz[0, colIH:colFH]
	for vehicle in headNamesVehicles:
		if vehicle in Art:
			pass
		else:
			NamesVehicles.append(vehicle)

	for x in range(0, matriz.shape[1]):
			if x in posArt:
				pass
			else:
		  		name.append(matriz[0][x])

		  	

	for i in range (1, matriz.shape[0]):
		data = []

	 	for x in range(0, matriz.shape[1]):	
		  	if x in posArt:
		  		pass
			else:	
		  		data.append(matriz[i][x])

		
	 	FlujosVehicularesH = list() #Inicializa los flujos vehiculares
		FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

	 	CS = float(matriz[i][colCs])
	 	longGri = float(matriz[i][colLongGrid])


	#Dias Habiles
	 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
		 	if fh in posArt:
		 		pass
			else:
		 		FlujosVehicularesH.append(float(matriz[i][fh]))
	 	flujosH = Flujos(FlujosVehicularesH)

		#Operaciones para dias Habiles
		PPH = PP(FlujosVehicularesH, PesosV, flujosH, NamesVehicles) #Saca PP para dias Habiles
		
	 	FEHPM10 = FEPM(PMDIEZK, CS, PPH, PMDIEZSL, PMDIEZW) 
		FEHPM25 = FEPM(PMDOSK, CS, PPH, PMDOSSL, PMDOSW) 
		

	 	FAH = FactorActividad(longGri, flujosH)
		
	  	#Emision Hour
	  	EHPM10 = Emission(FEHPM10, FAH)
	  	EHPM25 = Emission(FEHPM25, FAH)

	 	#Dias No Habiles
	 	for fnh in range(colFH+1, colFNH): #Recorre por cada y todas las x que contienen los flujos dia No Habil
			 	if fnh in posArt:
			 		pass
				else:
			  		FlujosVehicularesNH.append(round(float(matriz[i][fnh]), 2))
	 	flujosNH = Flujos(FlujosVehicularesNH)
		
	 	#Operaciones para dias NO Habiles
	 	PPNH = PP(FlujosVehicularesNH, PesosV, flujosNH, NamesVehicles)
	 	FENHPM10 = FEPM(PMDIEZK, CS, PPNH, PMDIEZSL, PMDIEZW)
	 	FENHPM25 = FEPM(PMDOSK, CS, PPNH, PMDOSSL, PMDOSW)
	 	FANH = FactorActividad(longGri, flujosNH)
	 	
	 	#Emision Hour
	  	ENHPM10 = Emission(FENHPM10, FANH)
	  	ENHPM25 = Emission(FENHPM25, FANH)

	 	res = [float(PPH), float(PPNH), float(FEHPM10), float(FEHPM25), float(FENHPM10), float(FENHPM25), float(FAH), float(FANH), float(EHPM10), float(EHPM25), float(ENHPM10), float(ENHPM25)]
		nameres = ["PPH", "PPNH", "FEHPM10", "FEHPM25", "FENHPM10", "FENHPM25", "FAH", "FANH", "EHPM10", "EHPM25", "ENHPM10", "ENHPM25"]

	 	for dat in res:
	 		data.append(round(dat, 3))

	  	if i == 1:
	 	 	for nam in nameres: 
	 	 		name.append(nam)
	 	 	m.append(name)
	 	 	mat.append(np.array(name))

	 	mat.append(np.array(data))


	archive = archive[:22]
	archive = os.path.join(archive, '')
	arch = archive + noun + "_(Homogeneous)_" + "EmisionHour.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(mat)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	promd(arch, "EmissionDayHomogeneous")
	promtyear(DH, DNH, "EmissionDayHomogeneous",  "EmissionYearHomogeneous")
	emissionGrid(arch, 'Homogeneous_' + noun)

def secundaryHeterogeneous(matriz, archive, noun):

	name = []
	mat = []
	m = []
	NamesVehicles = []
	index = 0
	headsecundary = matriz[0,:]

	for value in headsecundary:

		if value == 'Cs_Hetero': #La columna de (CS...)
			colCs = index
		if value == 'Largo_Via' or value == 'Largo_via': #La columna de (Long_Grid...)
			colLongGrid = index
		if value == 'hora':
			colIH = index+1
		if value == 'TOTAL':
			colFH = index
		if value == 'NH_TOTAL':
			colFNH = index
		if value == 'FID_Grilla':
			colID = index #La coluna de (TTOAL Suma Flujos vehiculares dia no habil)
		if value == 'BA':
			colBA = index
		if value == 'AT':
			colAT = index
		if value == 'NH_BA':
			colNHBA = index
		if value == 'NH_AT':
			colNHAT = index
		index+=1

	posArt = [colAT, colBA, colNHBA, colNHAT]
	
	headNamesVehicles = matriz[0, colIH:colFH]

	for vehicle in headNamesVehicles:
		if vehicle in Art:
			pass
		else:
			NamesVehicles.append(vehicle)

	for x in range(0, matriz.shape[1]):
			if x in posArt:
				pass
			else:
		  		name.append(matriz[0][x])

		  	

	for i in range (1, matriz.shape[0]):
		data = []

	 	for x in range(0, matriz.shape[1]):	
		  	if x in posArt:
		  		pass
			else:	
		  		data.append(matriz[i][x])

		
	 	FlujosVehicularesH = list() #Inicializa los flujos vehiculares
		FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

	 	CS = float(matriz[i][colCs])
	 	longGri = float(matriz[i][colLongGrid])


	#Dias Habiles
	 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
		 	if fh in posArt:
		 		pass
			else:
		 		FlujosVehicularesH.append(float(matriz[i][fh]))
	 	flujosH = Flujos(FlujosVehicularesH)

		#Operaciones para dias Habiles
		PPH = PP(FlujosVehicularesH, PesosV, flujosH, NamesVehicles) #Saca PP para dias Habiles
		
	 	FEHPM10 = FEPM(PMDIEZK, CS, PPH, PMDIEZSL, PMDIEZW) 
		FEHPM25 = FEPM(PMDOSK, CS, PPH, PMDOSSL, PMDOSW) 
		

	 	FAH = FactorActividad(longGri, flujosH)
	 	#print "Longitud Grilla", longGri, "flujosH", flujosH, "==", FAH
		
	  	#Emision Hour
	  	EHPM10 = Emission(FEHPM10, FAH)
	  	EHPM25 = Emission(FEHPM25, FAH)


	 	#Dias No Habiles
	 	for fnh in range(colFH+1, colFNH): #Recorre por cada y todas las x que contienen los flujos dia No Habil
			 	if fnh in posArt:
			 		pass
				else:
			  		FlujosVehicularesNH.append(round(float(matriz[i][fnh]), 2))
	 	flujosNH = Flujos(FlujosVehicularesNH)
		
	 	#Operaciones para dias NO Habiles
	 	PPNH = PP(FlujosVehicularesNH, PesosV, flujosNH, NamesVehicles)
	 	FENHPM10 = FEPM(PMDIEZK, CS, PPNH, PMDIEZSL, PMDIEZW)
	 	FENHPM25 = FEPM(PMDOSK, CS, PPNH, PMDOSSL, PMDOSW)
	 	FANH = FactorActividad(longGri, flujosNH)
	 	
	 	#Emision Hour
	  	ENHPM10 = Emission(FENHPM10, FANH)
	  	ENHPM25 = Emission(FENHPM25, FANH)

	 	res = [float(PPH), float(PPNH), float(FEHPM10), float(FEHPM25), float(FENHPM10), float(FENHPM25), float(FAH), float(FANH), float(EHPM10), float(EHPM25), float(ENHPM10), float(ENHPM25)]
		nameres = ["PPH", "PPNH", "FEHPM10", "FEHPM25", "FENHPM10", "FENHPM25", "FAH", "FANH", "EHPM10", "EHPM25", "ENHPM10", "ENHPM25"]

	 	for dat in res:
	 		data.append(round(dat, 3))

	  	if i == 1:
	 	 	for nam in nameres: 
	 	 		name.append(nam)
	 	 	m.append(name)
	 	 	mat.append(np.array(name))

	 	mat.append(np.array(data))


	archive = archive[:22]
	archive = os.path.join(archive, '')
	arch = archive + noun + "_(Heterogeneous)_" + "EmisionHour.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(mat)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	
	promd(arch, "EmissionDayHeterogeneous")
	promtyear(DH, DNH, "EmissionDayHeterogeneous" ,  "EmissionYearHeterogeneous")
	emissionGrid(arch, 'Heterogeneous_' + noun)

def secundaryIDW(matriz, archive, noun):

	name = []
	mat = []
	m = []
	NamesVehicles = []
	index = 0
	headsecundary = matriz[0,:]

	for value in headsecundary:

		if value == 'IDW_Cs': #La columna de (CS...)
			colCs = index
		if value == 'Largo_Via' or value == 'Largo_via': #La columna de (Long_Grid...)
			colLongGrid = index
		if value == 'hora':
			colIH = index+1
		if value == 'TOTAL':
			colFH = index
		if value == 'NH_TOTAL':
			colFNH = index
		if value == 'FID_Grilla':
			colID = index #La coluna de (TTOAL Suma Flujos vehiculares dia no habil)
		if value == 'BA':
			colBA = index
		if value == 'AT':
			colAT = index
		if value == 'NH_BA':
			colNHBA = index
		if value == 'NH_AT':
			colNHAT = index
		index+=1

	posArt = [colAT, colBA, colNHBA, colNHAT]
	
	headNamesVehicles = matriz[0, colIH:colFH]

	for vehicle in headNamesVehicles:
		if vehicle in Art:
			pass
		else:
			NamesVehicles.append(vehicle)

	for x in range(0, matriz.shape[1]):
			if x in posArt:
				pass
			else:
		  		name.append(matriz[0][x])

		  	

	for i in range (1, matriz.shape[0]):
		data = []

	 	for x in range(0, matriz.shape[1]):	
		  	if x in posArt:
		  		pass
			else:	
		  		data.append(matriz[i][x])

		
	 	FlujosVehicularesH = list() #Inicializa los flujos vehiculares
		FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

	 	CS = float(matriz[i][colCs])
	 	longGri = float(matriz[i][colLongGrid])


	#Dias Habiles
	 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
		 	if fh in posArt:
		 		pass
			else:
		 		FlujosVehicularesH.append(float(matriz[i][fh]))
	 	flujosH = Flujos(FlujosVehicularesH)

		#Operaciones para dias Habiles
		PPH = PP(FlujosVehicularesH, PesosV, flujosH, NamesVehicles) #Saca PP para dias Habiles
		
	 	FEHPM10 = FEPM(PMDIEZK, CS, PPH, PMDIEZSL, PMDIEZW) 
		FEHPM25 = FEPM(PMDOSK, CS, PPH, PMDOSSL, PMDOSW) 
		

	 	FAH = FactorActividad(longGri, flujosH)
	 	#print "Longitud Grilla", longGri, "flujosH", flujosH, "==", FAH
		
	  	#Emision Hour
	  	EHPM10 = Emission(FEHPM10, FAH)
	  	EHPM25 = Emission(FEHPM25, FAH)


	 	#Dias No Habiles
	 	for fnh in range(colFH+1, colFNH): #Recorre por cada y todas las x que contienen los flujos dia No Habil
			 	if fnh in posArt:
			 		pass
				else:
			  		FlujosVehicularesNH.append(round(float(matriz[i][fnh]), 2))
	 	flujosNH = Flujos(FlujosVehicularesNH)
		
	 	#Operaciones para dias NO Habiles
	 	PPNH = PP(FlujosVehicularesNH, PesosV, flujosNH, NamesVehicles)
	 	FENHPM10 = FEPM(PMDIEZK, CS, PPNH, PMDIEZSL, PMDIEZW)
	 	FENHPM25 = FEPM(PMDOSK, CS, PPNH, PMDOSSL, PMDOSW)
	 	FANH = FactorActividad(longGri, flujosNH)
	 	
	 	#Emision Hour
	  	ENHPM10 = Emission(FENHPM10, FANH)
	  	ENHPM25 = Emission(FENHPM25, FANH)

	 	res = [float(PPH), float(PPNH), float(FEHPM10), float(FEHPM25), float(FENHPM10), float(FENHPM25), float(FAH), float(FANH), float(EHPM10), float(EHPM25), float(ENHPM10), float(ENHPM25)]
		nameres = ["PPH", "PPNH", "FEHPM10", "FEHPM25", "FENHPM10", "FENHPM25", "FAH", "FANH", "EHPM10", "EHPM25", "ENHPM10", "ENHPM25"]

	 	for dat in res:
	 		data.append(round(dat, 3))

	  	if i == 1:
	 	 	for nam in nameres: 
	 	 		name.append(nam)
	 	 	m.append(name)
	 	 	mat.append(np.array(name))

	 	mat.append(np.array(data))


	archive = archive[:22]
	archive = os.path.join(archive, '')
	arch = archive + noun + "_(IDW)_" + "EmisionHour.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(mat)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	
	promd(arch, "EmissionDayIDWSecundary")
	promtyear(DH, DNH, "EmissionDayIDWSecundary" ,  "EmissionYearIDWSecundary")
	emissionGrid(arch, 'IDW_' + noun)
