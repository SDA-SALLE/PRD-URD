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
from uncertain import *
import csv
import numpy as np
import json


#Pesos Vehiculos
PesosV = {'L':[1.6], 'C':[2.4], 'BT':[8.2], 'B':[14.5], 'AL':[14.5],  'ESP':[8.2], 'INT':[14.5], 'C2P':[4.6], 'C2G':[8.5], 'C3-C4':[28], 'C5':[35.0], '>C5':[40], 'M':[0.2]}
PesosVArt = {'AT': [30.0], 'BA': [42.0]}
NameVehicles = ['L', 'C', 'BT', 'B', 'AL',  'ESP', 'INT', 'C2P', 'C2G', 'C3-C4', 'C5', '>C5', 'M', 'TOTAL', 'NH_>C5', 'NH_AL', 'NH_B', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_INT', 'NH_M', 'NH_ESP', 'NH_L', 'NH_TOTAL']
Art = ['AT', 'BA', 'NH_AT', 'NH_BA', 'TOTAL', 'NH_TOTAL']


#Dias Habiles y No Habiles 2012
DH = 245
DNH = 120

#Constantes.
PMDIEZK = 0.62
PMDOSK = 0.15
PMDIEZSL = 0.677
PMDIEZW =  0.85
PMDOSSL = 0.91
PMDOSW = 1.02


def idw(matrizidw, directorio, noun):

	name = []
	mat = []
	Position = []
	index = 0
	head = matrizidw[0,:]

	for value in head:
		if value == "IDW_Cs": #La columna de (CS...)
			colCs = index
		if value == "Largo_via" or value == "Largo_Via": #La columna de (Long_Grid...)
			colLongGrid = index
		if value == "hora":
			colIH = index+1
		if value == "TOTAL":
			colFH = index
		if value == "NH_TOTAL":
			colFNH = index
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

	headNamesVehicles = matrizidw[0,colIH:colFH]
	NamesVehicles = []

	if noun == 'Principal':
		for vehicle in headNamesVehicles:
			if vehicle in Art:
				pass
			else:
				NamesVehicles.append(vehicle)

		for x in range(0, matrizidw.shape[1]):
			if x in posArt:
				pass
			else:
		  		name.append(matrizidw[0][x])

		for i in range (1, matrizidw.shape[0]):
		 	data = []
		  	for x in range(0, matrizidw.shape[1]):	
			  	if x in posArt:
			  		pass
				else:	
			  		data.append(matrizidw[i][x])

			FlujosVehicularesH = list() #Inicializa los flujos vehiculares
			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

		 	CS = float(matrizidw[i][colCs])
		 	longGri = float(matrizidw[i][colLongGrid])


			#Dias Habiles
		 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
			 	if fh in posArt:
			 		pass
				else:
			 		FlujosVehicularesH.append(float(matrizidw[i][fh]))
		 	flujosH = round(Flujos(FlujosVehicularesH), 1)
		 	
			#Operaciones para dias Habiles
	 	 	PPH = round(PP(FlujosVehicularesH, PesosV, flujosH, NamesVehicles), 2) #Saca PP para dias Habiles
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
			  		FlujosVehicularesNH.append(round(float(matrizidw[i][fnh]), 2))

		  	flujosNH = Flujos(FlujosVehicularesNH)
			
		  	#Operaciones para dias NO Habiles
		  	PPNH = round(PP(FlujosVehicularesNH, PesosV, flujosNH,  NamesVehicles), 2)
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
		  	 	mat.append(np.array(name))

		  	mat.append(np.array(data))
		directorio =  directorio[:22]
		directorio = os.path.join(directorio, '')

	if noun == 'TM':
		
		for vehicle in headNamesVehicles:
			if vehicle in NameVehicles:
				pass
			else:
				NamesVehicles.append(vehicle)

		for x in range(0, matrizidw.shape[1]):
			n = matrizidw[0][x]
			if n in NameVehicles:
				pass
			else:
		  		name.append(matrizidw[0][x])
		  		Position.append(x)

		for i in range (1, matrizidw.shape[0]):
		 	data = []
		  	for x in Position:	
		  		data.append(matrizidw[i][x])

			FlujosVehicularesH = list() #Inicializa los flujos vehiculares
			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

		 	CS = float(matrizidw[i][colCs])
		 	longGri = float(matrizidw[i][colLongGrid])


			#Dias Habiles
		 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
		 		n = matrizidw[0][fh]
		 		if n in NameVehicles:
		 			pass
				else:
			 		FlujosVehicularesH.append(float(matrizidw[i][fh]))

		 	flujosH = round(Flujos(FlujosVehicularesH), 1)
		 	if flujosH == 0.0 or flujosH == 0:
		 		PPH = 0.0
		 	else:
		 		PPH = round(PP(FlujosVehicularesH, PesosVArt, flujosH, NamesVehicles), 2) #Saca PP para dias Habiles
			
			#Operaciones para dias Habiles
		  	FEHPM10 = FEPM(PMDIEZK, CS, PPH, PMDIEZSL, PMDIEZW)
		 	FEHPM25 = FEPM(PMDOSK, CS, PPH, PMDOSSL, PMDOSW)
		  	FAH = FactorActividad(longGri, flujosH)

			#Emision Hour
		  	EHPM10 = Emission(FEHPM10, FAH)
		 	EHPM25 = Emission(FEHPM25, FAH)


			#Dias No Habiles
		 	for fnh in range(colFH+1, colFNH): #Recorre por cada y todas las x que contienen los flujos dia No Habil
		 		n = matrizidw[0][fnh]
		 		if n in NameVehicles:
		 			pass
				else:
			  		FlujosVehicularesNH.append(round(float(matrizidw[i][fnh]), 2))
		  	flujosNH = Flujos(FlujosVehicularesNH)

		  	if flujosNH == 0.0:
		  		PPNH = 0.0
		  	else:
		  		PPNH = round(PP(FlujosVehicularesNH, PesosVArt, flujosNH, NamesVehicles), 2)
			
		  	#Operaciones para dias NO Habiles
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
		  	 	mat.append(np.array(name))


		  	mat.append(np.array(data))
		
		directorio =  directorio[:14]
		directorio = os.path.join(directorio, '')

	arch = directorio + noun + "_(IDW)" + "EmisionHour.csv"
	#print arch
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(mat)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	promd(arch, "EmissionDayIDW" + noun)
	promtyear(DH, DNH, "EmissionDayIDW" + noun ,  "EmissionYearIDW" + noun)
	emissionGrid(arch, 'IDW_' + noun)
	uncertainidw(arch, 'IDW_' + noun)

#Cambiar para que solo haga Habil
def ckdh(matrizckdh, directorio, noun):

	name = []
	mat = []
	Position = []
	index = 0
	head = matrizckdh[0,:]

	for value in head:
		if value == "CK_DH_Cs": #La columna de (CS...)
			colCs = index
		if value == "Largo_via" or value == "Largo_Via": #La columna de (Long_Grid...)
			colLongGrid = index
		if value == "hora":
			colIH = index+1
		if value == "TOTAL":
			colFH = index
		if value == "NH_TOTAL":
			colFNH = index
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

	headNamesVehicles = matrizckdh[0, colIH:colFH]
	NamesVehicles = []

	if noun == 'Principal':
		for vehicle in headNamesVehicles:
			if vehicle in Art:
				pass
			else:
				NamesVehicles.append(vehicle)

		for x in range(0, matrizckdh.shape[1]):
			if x in posArt:
				pass
			else:
		  		name.append(matrizckdh[0][x])

		for i in range (1, matrizckdh.shape[0]):
		 	data = []
		  	for x in range(0, matrizckdh.shape[1]):	
			  	if x in posArt:
			  		pass
				else:	
			  		data.append(matrizckdh[i][x])

			FlujosVehicularesH = list() #Inicializa los flujos vehiculares
			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

		 	CS = float(matrizckdh[i][colCs])
		 	longGri = float(matrizckdh[i][colLongGrid])


			#Dias Habiles
		 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
			 	if fh in posArt:
			 		pass
				else:
			 		FlujosVehicularesH.append(float(matrizckdh[i][fh]))
		 	flujosH = round(Flujos(FlujosVehicularesH), 1)
		 	
			#Operaciones para dias Habiles
	 	 	PPH = round(PP(FlujosVehicularesH, PesosV, flujosH, NamesVehicles), 2) #Saca PP para dias Habiles
		  	FEHPM10 = FEPM(PMDIEZK, CS, PPH, PMDIEZSL, PMDIEZW)
		 	FEHPM25 = FEPM(PMDOSK, CS, PPH, PMDOSSL, PMDOSW)
		  	FAH = FactorActividad(longGri, flujosH)

			#Emision Hour
		  	EHPM10 = Emission (FEHPM10, FAH)
		 	EHPM25 = Emission (FEHPM25, FAH)

		  	res = [float(PPH),  float(FEHPM10), float(FEHPM25), float(FAH), float(EHPM10), float(EHPM25)]
		  	nameres = ["PPH",  "FEHPM10", "FEHPM25",  "FAH",  "EHPM10", "EHPM25"]

		  	for dat in res:
		  		data.append(round(dat, 3))

		   	if i == 1:
		  	 	for nam in nameres:
		  	 		name.append(nam)
		  	 	mat.append(np.array(name))

		  	mat.append(np.array(data))
		directorio =  directorio[:22]
		directorio = os.path.join(directorio, '')
	
	if noun == 'TM':
		
		for vehicle in headNamesVehicles:
			if vehicle in NameVehicles:
				pass
			else:
				NamesVehicles.append(vehicle)

		for x in range(0, matrizckdh.shape[1]):
			n = matrizckdh[0][x]
			if n in NameVehicles:
				pass
			else:
		  		name.append(matrizckdh[0][x])
		  		Position.append(x)

		for i in range (1, matrizckdh.shape[0]):
		 	data = []
		  	for x in Position:	
		  		data.append(matrizckdh[i][x])

			FlujosVehicularesH = list() #Inicializa los flujos vehiculares
			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

		 	CS = float(matrizckdh[i][colCs])
		 	longGri = float(matrizckdh[i][colLongGrid])


			#Dias Habiles
		 	for fh in range(colIH, colFH): #Recorre por cada y todas las x que contienen los flujos dia Habil
		 		n = matrizckdh[0][fh]
		 		if n in NameVehicles:
		 			pass
				else:
			 		FlujosVehicularesH.append(float(matrizckdh[i][fh]))

		 	flujosH = round(Flujos(FlujosVehicularesH), 1)
		 	
		 	if flujosH == 0.0 or flujosH == 0:
		 		PPH = 0
		 	else:
		 		PPH = round(PP(FlujosVehicularesH, PesosVArt, flujosH, NamesVehicles), 2) #Saca PP para dias Habiles
			
			#Operaciones para dias Habiles
		  	FEHPM10 = FEPM(PMDIEZK, CS, PPH, PMDIEZSL, PMDIEZW)
		 	FEHPM25 = FEPM(PMDOSK, CS, PPH, PMDOSSL, PMDOSW)
		  	FAH = FactorActividad(longGri, flujosH)

			#Emision Hour
		  	EHPM10 = Emission(FEHPM10, FAH)
		 	EHPM25 = Emission(FEHPM25, FAH)

		  	res = [float(PPH),  float(FEHPM10), float(FEHPM25), float(FAH), float(EHPM10), float(EHPM25)]
		  	nameres = ["PPH",  "FEHPM10", "FEHPM25",  "FAH",  "EHPM10", "EHPM25"]

		  	for dat in res:
		  		data.append(round(dat, 3))

		   	if i == 1:
		  	 	for nam in nameres:
		  	 		name.append(nam)
		  	 	mat.append(np.array(name))


		  	mat.append(np.array(data))

		directorio =  directorio[:14]
		directorio = os.path.join(directorio, '')

	#directorio =  directorio[:22]
	arch = directorio + noun +"_(CKDH)"+"EmisionHour.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(mat)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	promd(arch, "EmissionDayCKDH" + noun)
	promtyear(DH, DNH, "EmissionDayCKDH" + noun ,  "EmissionYearCKDH" + noun)
	emissionGrid(arch, 'CKDH_' + noun)

#Cambiar para que solo haga No Habil
def ckdnh(matrizckdnh, directorio, noun):

	name = []
	mat = []
	Position = []
	index = 0
	head = matrizckdnh[0,:]

	for value in head:
		if value == "CK_DNH_Cs": #La columna de (CS...)
			colCs = index
		if value == "Largo_via" or value == "Largo_Via": #La columna de (Long_Grid...)
			colLongGrid = index
		if value == "hora":
			colIH = index+1
		if value == "TOTAL":
			colFH = index
		if value == "NH_TOTAL":
			colFNH = index
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

	headNamesVehicles = matrizckdnh[0, colIH:colFH]
	NamesVehicles = []

	if noun == 'Principal':
		for vehicle in headNamesVehicles:
			if vehicle in Art:
				pass
			else:
				NamesVehicles.append(vehicle)

		for x in range(0, matrizckdnh.shape[1]):
			if x in posArt:
				pass
			else:
		  		name.append(matrizckdnh[0][x])

		for i in range (1, matrizckdnh.shape[0]):
		 	data = []
		  	for x in range(0, matrizckdnh.shape[1]):	
			  	if x in posArt:
			  		pass
				else:	
			  		data.append(matrizckdnh[i][x])

			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares
			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

		 	CS = float(matrizckdnh[i][colCs])
		 	longGri = float(matrizckdnh[i][colLongGrid])


			#Dias No Habiles
		 	for fh in range(colFH+1, colFNH): #Recorre por cada y todas las x que contienen los flujos dia Habil
			 	if fh in posArt:
			 		pass
				else:
			 		FlujosVehicularesNH.append(float(matrizckdnh[i][fh]))
		 	flujosNH = round(Flujos(FlujosVehicularesNH), 1)
		 	
			#Operaciones para dias No Habiles
	 	 	PPNH = round(PP(FlujosVehicularesNH, PesosV, flujosNH, NamesVehicles), 2) #Saca PP para dias Habiles
		  	FENHPM10 = FEPM(PMDIEZK, CS, PPNH, PMDIEZSL, PMDIEZW)
		 	FENHPM25 = FEPM(PMDOSK, CS, PPNH, PMDOSSL, PMDOSW)
		  	FANH = FactorActividad(longGri, flujosNH)

			#Emision Hour
		  	ENHPM10 = Emission (FENHPM10, FANH)
		 	ENHPM25 = Emission (FENHPM25, FANH)

		  	res = [float(PPNH),  float(FENHPM10), float(FENHPM25), float(FANH), float(ENHPM10), float(ENHPM25)]
		  	nameres = ["PPNH",  "FENHPM10", "FENHPM25",  "FANH",  "ENHPM10", "ENHPM25"]

		  	for dat in res:
		  		data.append(round(dat, 3))

		   	if i == 1:
		  	 	for nam in nameres:
		  	 		name.append(nam)
		  	 	mat.append(np.array(name))

		  	mat.append(np.array(data))
		directorio =  directorio[:22]
		directorio = os.path.join(directorio, '')
	
	if noun == 'TM':

		for vehicle in headNamesVehicles:
			if vehicle in NameVehicles:
				pass
			else:
				NamesVehicles.append(vehicle)

		for x in range(0, matrizckdnh.shape[1]):
			n = matrizckdnh[0][x]
			if n in NameVehicles:
				pass
			else:
		  		name.append(matrizckdnh[0][x])
		  		Position.append(x)

		for i in range (1, matrizckdnh.shape[0]):
		 	data = []
		  	for x in Position:	
		  		data.append(matrizckdnh[i][x])

			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares
			FlujosVehicularesNH = list() #Inicializa los flujos vehiculares

		 	CS = float(matrizckdnh[i][colCs])
		 	longGri = float(matrizckdnh[i][colLongGrid])


			#Dias No Habiles
		 	for fh in range(colFH+1, colFNH): #Recorre por cada y todas las x que contienen los flujos dia Habil
		 		
		 		n = matrizckdnh[0][fh]

		 		if n in NameVehicles:
		 			pass
				else:
			 		FlujosVehicularesNH.append(float(matrizckdnh[i][fh]))

		 	flujosNH = round(Flujos(FlujosVehicularesNH), 1)
		 	
		 	if flujosNH == 0.0 or flujosNH == 0:
		 		PPNH = 0
		 	else:
		 		PPNH = round(PP(FlujosVehicularesNH, PesosVArt, flujosNH, NamesVehicles), 2) #Saca PP para dias Habiles
			
			#Operaciones para dias Habiles
		  	FENHPM10 = FEPM(PMDIEZK, CS, PPNH, PMDIEZSL, PMDIEZW)
		 	FENHPM25 = FEPM(PMDOSK, CS, PPNH, PMDOSSL, PMDOSW)
		  	FANH = FactorActividad(longGri, flujosNH)

			#Emision Hour
		  	ENHPM10 = Emission(FENHPM10, FANH)
		 	ENHPM25 = Emission(FENHPM25, FANH)

		  	res = [float(PPNH),  float(FENHPM10), float(FENHPM25), float(FANH), float(ENHPM10), float(ENHPM25)]
		  	nameres = ["PPNH",  "FENHPM10", "FENHPM25",  "FANH",  "ENHPM10", "ENHPM25"]

		  	for dat in res:
		  		data.append(round(dat, 3))

		   	if i == 1:
		  	 	for nam in nameres:
		  	 		name.append(nam)
		  	 	mat.append(np.array(name))


		  	mat.append(np.array(data))

		directorio =  directorio[:14]
		directorio = os.path.join(directorio, '')

	#directorio =  directorio[:22]
	arch = directorio + noun +"_(CKDNH)"+"EmisionHour.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(mat)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	promd(arch, "EmissionDayCKDNH" + noun)
	promtyear(DH, DNH, "EmissionDayCKDNH" + noun,  "EmissionYearCKDNH" + noun)
	emissionGrid(arch, 'CKDNH_' + noun)