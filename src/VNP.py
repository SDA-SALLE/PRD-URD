#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python

#List Library Import
import sys
sys.path.append("core")
from operaciones import *
import numpy as np
import csv
from promegd import *
from excelmatriz import *
from wcsv import *
import os
import json
import xlrd

Constants = os.path.join('..', 'data', 'constants', 'Resuspendido.xlsx')
workbook = xlrd.open_workbook(Constants)
year = workbook.sheet_by_index(0)

def industrial(matriz, directorio):
	
	dh = workbook.sheet_by_index(5)
	#constants
	prompeso = {}
	for pos in range(13, dh.nrows):
		#print dh.cell_value(pos, 0)
		estation = int(dh.cell_value(pos, 0))
		peso = dh.cell_value(pos, 17)
		if prompeso.get(estation) is None:
			prompeso[estation] = []

		prompeso[estation].append(peso)

	#print prompeso

	#C, Emission Factor for Exhaust, Brake Wear and Tire Wear
	pm25g = dh.cell_value(0, 1)
	pm10g = dh.cell_value(1, 1)
	
	#Public Roads (Equation 1b)
	#PM25
	pm25kgvkt = dh.cell_value(2, 1)
	
	#PM10
	pm10kgvkt = dh.cell_value(5, 1)
	

	#Shared
	apm25 = dh.cell_value(3, 1)
	bpm25 = dh.cell_value(4, 1)

	apm10 = dh.cell_value(6, 1)
	bpm10 = dh.cell_value(7, 1)
	
	#Dias Habiles
	DH = int(year.cell_value(1, 0))
	#print DH
	name = []
	mat = []
	m = []
	index = 0
	head = matriz[0,:]

	for value in head:
		if value == "Flujo": #Flujo Vehicular
			colFlujo = index
		if value == "Shape_Leng": #Long Grilla
			colLong = index
		if value == "Vel_km_hr":
			colVel = index
		if value == "IDW_S":
			colS = index
		if value == 'Estacion':
			colEstation = index
		index+=1

	for x in range(0, matriz.shape[1]):
	 	name.append(matriz[0][x])

	#print matriz.shape
	for y in range (1, matriz.shape[0]):
		
		data = []

	 	for x in range(0, matriz.shape[1]):		
	 		data.append(matriz[y][x])
		
		#print data
		FA = FAVKT(float(matriz[y][colLong]), float(matriz[y][colFlujo]))
		#print FA

		#EmisionsPM25
	 	FEPM25 = FEVKTI(pm25kgvkt, float(matriz[y][colS]), apm25, prompeso[int(float(matriz[y][colEstation]))][0], bpm25, pm25g) 
	 	EPM25 = Emission(FEPM25, FA)
		ETYPM25 = ETY(EPM25, DH)

		#EmisionsPM10
	 	FEPM10 = FEVKTI(pm10kgvkt, float(matriz[y][colS]), apm10, prompeso[int(float(matriz[y][colEstation]))][0], bpm10, pm10g) 
	 	EPM10 = Emission(FEPM10, FA)
	 	ETYPM10 = ETY(EPM10, DH)
	
		
		res = [float(FA), float(FEPM10), float(FEPM25), float(EPM10), float(EPM25), float(ETYPM10), float(ETYPM25)]
	 	nameres = ["FA", "FEPM10", "FEPM25", "EGDPM10", "EGDPM25", "ETYPM10", "ETYPM25"]

	 	for dat in res:
	 		data.append(round(dat, 3))

		if y == 1:
	 	 	for nam in nameres: 
	 	 		name.append(nam) #Adjunt new name in array names
	 	 	mat.append(np.array(name))
	 	mat.append(np.array(data))

	  	
 	arch = directorio + "_VNPIndustrial.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(matriz)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	promdnp(arch, "VNPIndustrial")
	distribution(arch, "VNPIndustrial")

def public(matriz, directorio):
	
	dh = workbook.sheet_by_index(4)
	
	#constantes
	
	#C, Emission Factor for Exhaust, Brake Wear and Tire Wear
	pm25g = dh.cell_value(0, 1)
	pm10g = dh.cell_value(1, 1)

	#Public Roads (Equation 1b)
	#PM25
	pm25kgvkt = dh.cell_value(2, 1)
	
	#PM10
	pm10kgvkt = dh.cell_value(6, 1)

	#Shared
	apm25 = dh.cell_value(3, 1)
	cpm25 = dh.cell_value(4, 1)
	dpm25 = dh.cell_value(5, 1)

	apm10 = dh.cell_value(7, 1)
	cpm10 = dh.cell_value(8, 1)
	dpm10 = dh.cell_value(9, 1)
	
	DH = int(year.cell_value(1, 0))

	
	name = []
	mat = []
	m = []
	index = 0
	head = matriz[0,:]

	for value in head:
		if value == "Flujo": #Flujo Vehicular
			colFlujo = index
		if value == "Shape_Leng": #Long Grilla
			colLong = index
		if value == "Vel_km_hr":
			colVel = index
		if value == "IDW_S":
			colS = index
		index+=1

	for x in range(0, matriz.shape[1]):
	 	name.append(matriz[0][x])

	for y in range (1, matriz.shape[0]):
		
		data = []

	 	for x in range(0, matriz.shape[1]):		
	 		data.append(matriz[y][x])
		
		FA = FAVKT(float(matriz[y][colLong]), float(matriz[y][colFlujo]))

		#EmisionsPM25
		#print pm25kgvkt, float(matriz[y][colS]), apm25, float(matriz[y][colVel]), dpm25, pm25g
		FEPM25 = FEVKTP(pm25kgvkt, float(matriz[y][colS]), apm25, float(matriz[y][colVel]), dpm25, pm25g)
		#print FA, FEPM25, DH
		EPM25 = Emission(FEPM25, FA)
		ETYPM25 = ETY(EPM25, DH)

		#EmisionsPM10
		FEPM10 = FEVKTP(pm10kgvkt, float(matriz[y][colS]), apm10, float(matriz[y][colVel]), dpm10, pm10g)
		EPM10 = Emission(FEPM10, FA)
		ETYPM10 = ETY(EPM10, DH)
		#print EGHPM10
		

		res = [float(FA), float(FEPM10), float(FEPM25), float(EPM10), float(EPM25), float(ETYPM10), float(ETYPM25)]
	 	nameres = ["FA", "FEPM10", "FEPM25", "EGDPM10", "EGDPM25", "ETYPM10", "ETYPM25"]

	 	for dat in res:
	 		data.append(round(dat, 3))

		if y == 1:
	 	 	for nam in nameres: 
	 	 		name.append(nam) #Adjunt new name in array names
	 	 	mat.append(np.array(name))
	 	mat.append(np.array(data))

	  	
 	arch = directorio + "_VNPPublic.csv"
	csvsalida = open(arch, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	for x in range (0, len(matriz)):
		salida.writerow([e.encode("utf-8") for e in mat[x]])
	csvsalida.close()

	promdnp(arch, "VNPPublic")
	distribution(arch, "VNPPublic")

def brindingvnp():

	Industrial = os.path.join('..', 'data', 'out', 'TotalEmissions', 'VNPIndustrial_E(TYear).csv')
	Public = os.path.join('..', 'data', 'out', 'TotalEmissions', 'VNPPublic_E(TYear).csv')

	MIndustrial = convertCSVMatriz(Industrial)
	MPublic = convertCSVMatriz(Public)

	TotalPM25 = float(MIndustrial[1][0]) + float(MPublic[1][0])
	TotalPM10 = float(MIndustrial[1][1]) + float(MPublic[1][1])

	writefull(TotalPM25, TotalPM10, 'TotalVNP')

def distribution(archive, noun):
	matriz = convertCSVMatriz (archive)	
	dh = workbook.sheet_by_index(6)

	head = matriz[0,:]
	index = 0
	for value in head: 
		if value == 'FID_LINK': 
			colFIDLink = index
		if value == 'FID_Grilla':
			colFIDGrid = index
		if value == 'ROW': 
			colROW = index
		if value == 'COL': 
			colCOL = index
		if value == 'LAT': 
			colLAT = index 
		if value == 'LON':
			colLON = index 
		if value == 'EGDPM10':
			colEGDPM10 = index
		if value == 'EGDPM25':
			colEGDPM25 = index
		index +=1

	data = {}
	for i in range(1, matriz.shape[0]):
		key = matriz[i][colFIDGrid]

		if data.get(key) is None: 
			data[key] = {}
			data[key]['Emissions'] = {'EGDPM10': [], 'EGDPM25': []}
			data[key]['GENERAL'] = {'COL': [], 'ROW': [], 'LAT': [], 'LON': []}
			data[key]['hours'] = {}
			data[key]['hours']['PM25'] = {}
			data[key]['hours']['PM10'] = {}

		if data[key]['GENERAL']['COL'] == []:
			data[key]['GENERAL']['COL'].append(int(float(matriz[i][colCOL])))
			data[key]['GENERAL']['ROW'].append(int(float(matriz[i][colROW])))
			data[key]['GENERAL']['LON'].append(matriz[i][colLON])
			data[key]['GENERAL']['LAT'].append(matriz[i][colLAT])

		data[key]['Emissions']['EGDPM25'].append(matriz[i][colEGDPM25])
		data[key]['Emissions']['EGDPM10'].append(matriz[i][colEGDPM10])

		for hour in range(0, 25):
			entryHourspm25 = data[key]['hours']['PM25']
			entryHourspm10 = data[key]['hours']['PM10']
			if entryHourspm25.get(hour) is None:
				entryHourspm10[hour] = []
				entryHourspm25[hour] = []

	keys = data.keys()
	for key in keys: 
		suma = eval('+'.join(data[key]['Emissions']['EGDPM10']))
		data[key]['Emissions']['EGDPM10'] = []
		data[key]['Emissions']['EGDPM10'].append(suma)

		suma = eval('+'.join(data[key]['Emissions']['EGDPM25']))
		data[key]['Emissions']['EGDPM25'] = []
		data[key]['Emissions']['EGDPM25'].append(suma)
		
		hours = data[key]['hours']['PM25'].keys()
		for hour in hours:
			data[key]['hours']['PM25'][hour].append(dh.cell_value(4, hour) * data[key]['Emissions']['EGDPM25'][0])
			data[key]['hours']['PM10'][hour].append(dh.cell_value(4, hour) * data[key]['Emissions']['EGDPM10'][0])

	writevnp(data, noun)

def brindingfinal(archive1, archive2):
	Marchive1 = convertCSVMatriz(archive1)
	Marchive2 = convertCSVMatriz(archive2) 

	head = Marchive1[0,:]
	index = 0
	data = {}
	
	for value in head: 
		if value == 'COL':
			colCOL = index
		if value == 'ROW': 
			colROW = index
		if value == 'LON':
			colLON = index
		if value == 'LAT': 
			colLAT = index
		if value == 'POLNAME': 
			colPOLL = index
		if value == 'UNIT': 
			colUNIT = index
		index += 1

	for i in range(1, Marchive1.shape[0]):
		key = str(int(Marchive1[i][colROW])) + str(int(Marchive1[i][colCOL]))
		
		if data.get(key) is None:
			data[key] = {}
			data[key]['GENERAL'] = {'ROW': [], 'COL': [], 'LAT': [], 'LON': [], 'POLNAME': [], 'UNIT': []}
			data[key]['hours'] = {}

		entryhour = data[key]['hours']
		for hour in range(0, 25):
			if entryhour.get(hour) is None: 
				entryhour[hour] = []

		if data[key]['GENERAL']['ROW'] == []:
			data[key]['GENERAL']['ROW'].append(Marchive1[i][colROW])
			data[key]['GENERAL']['COL'].append(Marchive1[i][colCOL])
			data[key]['GENERAL']['LAT'].append(Marchive1[i][colLAT])
			data[key]['GENERAL']['LON'].append(Marchive1[i][colLON])
			data[key]['GENERAL']['POLNAME'].append(Marchive1[i][colPOLL])
			data[key]['GENERAL']['UNIT'].append(Marchive1[i][colUNIT])

		hour = 0
		for x in range(colUNIT+1, Marchive1.shape[1]):
			data[key]['hours'][hour].append(Marchive1[i][x])
			hour += 1

	for i in range(1, Marchive2.shape[0]):
		key = str(int(Marchive2[i][colROW])) + str(int(Marchive2[i][colCOL]))

		if data.get(key) is None:
			data[key] = {}
			data[key]['GENERAL'] = {'ROW': [], 'COL': [], 'LAT': [], 'LON': [], 'POLNAME': [], 'UNIT': []}
			data[key]['hours'] = {}

		entryhour = data[key]['hours']
		for hour in range(0, 25):
			if entryhour.get(hour) is None: 
				entryhour[hour] = []

		if data[key]['GENERAL']['ROW'] == []:
			data[key]['GENERAL']['ROW'].append(Marchive2[i][colROW])
			data[key]['GENERAL']['COL'].append(Marchive2[i][colCOL])
			data[key]['GENERAL']['LAT'].append(Marchive2[i][colLAT])
			data[key]['GENERAL']['LON'].append(Marchive2[i][colLON])
			data[key]['GENERAL']['POLNAME'].append(Marchive2[i][colPOLL])
			data[key]['GENERAL']['UNIT'].append(Marchive2[i][colUNIT])

		hour = 0
		for x in range(colUNIT+1, Marchive2.shape[1]):
			data[key]['hours'][hour].append(Marchive2[i][x])
			hour += 1

	keys = data.keys()

	for key in keys:
		hours = data[key]['hours'].keys()
		for hour in hours:
			suma = eval('+'.join(data[key]['hours'][hour]))
			data[key]['hours'][hour] = []
			data[key]['hours'][hour].append(suma)

	#Falta Escitrura del archivo, verificar datos de PM10 PUblic and PM25 Public







