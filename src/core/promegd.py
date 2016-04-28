#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
import os
import csv
from excelmatriz import *
from wcsv import *

def lista(matriz, colID):
	listid = []
	
	for y in range(1, matriz.shape[0]):
		ID = matriz[y][colID]
		if ID not in listid: 
			listid.append(ID)
	
	return listid		

def promd(archivo, noun):
	
	matriz = convertCSVMatriz(archivo)
	index = 0
	head = matriz[0,:]

	for value in head:
		if value == 'FID_LINK' or value == 'FID_Link': #La columna de (ID)
			colFID = index
		if value == 'FID_Grilla':
			colFIDG = index
		if value == 'COL':
			colCol = index
		if value == 'ROW':
			colRow = index
		if value == 'LON' or value == 'LON_1':
			colLon = index
		if value == 'LAT' or value == 'LAT_1':
			colLat = index
		if value == 'IDEstacion':
			colIDEst = index
		if value == 'IDNodo':
			colIDNodo = index 
		if value == 'EHPM25':
			colEHPM25 = index
		if value == 'EHPM10':
			colEHPM10 = index
		if value == 'ENHPM25':
			colENHPM25 = index
		if value == 'ENHPM10':
			colENHPM10 = index
		index+=1

	listid = lista(matriz, colFID)
	data ={}
	if 'IDW' in noun or 'Homogeneous' in noun or 'Heterogeneous' in noun:
		emisions =  [ 'EHPM25', 'EHPM10',  'ENHPM25', 'ENHPM10']
	elif 'CKDH' in noun:
		emisions =  [ 'EHPM25', 'EHPM10']
	elif 'CKDNH' in noun:
		emisions =  ['ENHPM25', 'ENHPM10']

	for key in listid: 
		if data.get(key) is None: 
			data[key] = {}
		
		data[key]['GENERAL'] = {'COL':[], 'ROW': [], 'LON': [], 'LAT': [], 'FID_Grilla': [],'IDEstation': [], 'IDNodo': []}
		data[key]['EMISION'] = {}
		
		entryemision = data[key]['EMISION']
		
		for emision in emisions: 
			if entryemision.get(emision) is None:
				entryemision[emision] = []

	for y in range(1, matriz.shape[0]):
		FID = matriz[y][colFID]
		
		if data[FID]['GENERAL']['COL'] == []: 
			data[FID]['GENERAL']['COL'].append(int(float(matriz[y][colCol])))
			data[FID]['GENERAL']['ROW'].append(int(float(matriz[y][colRow])))
			data[FID]['GENERAL']['LON'].append(matriz[y][colLon])
			data[FID]['GENERAL']['LAT'].append(matriz[y][colLat])
			data[FID]['GENERAL']['FID_Grilla'].append(int(float(matriz[y][colFIDG])))
			data[FID]['GENERAL']['IDEstation'].append(int(float(matriz[y][colIDEst])))
			data[FID]['GENERAL']['IDNodo'].append(int(float(matriz[y][colIDNodo])))

		if 'IDW' in noun or 'Homogeneous' in noun or 'Heterogeneous' in noun:	
			data[FID]['EMISION']['EHPM25'].append(matriz[y][colEHPM25])
			data[FID]['EMISION']['EHPM10'].append(matriz[y][colEHPM10])
			data[FID]['EMISION']['ENHPM25'].append(matriz[y][colENHPM25])
			data[FID]['EMISION']['ENHPM10'].append(matriz[y][colENHPM10])
		elif 'CKDH' in noun:
			data[FID]['EMISION']['EHPM25'].append(matriz[y][colEHPM25])
			data[FID]['EMISION']['EHPM10'].append(matriz[y][colEHPM10])
		elif 'CKDNH' in noun:
			data[FID]['EMISION']['ENHPM25'].append(matriz[y][colENHPM25])
			data[FID]['EMISION']['ENHPM10'].append(matriz[y][colENHPM10])


	FID = data.keys()
	for ID in FID: 
		if 'IDW' in noun or 'Homogeneous' in noun or 'Heterogeneous' in noun:	
			data[ID]['EMISION']['EHPM25'][0] = float(eval('+'.join(data[ID]['EMISION']['EHPM25'])))
			data[ID]['EMISION']['EHPM10'][0] = float(eval('+'.join(data[ID]['EMISION']['EHPM10'])))
			data[ID]['EMISION']['ENHPM25'][0] = float(eval('+'.join(data[ID]['EMISION']['ENHPM25'])))
			data[ID]['EMISION']['ENHPM10'][0] = float(eval('+'.join(data[ID]['EMISION']['ENHPM10'])))
		elif 'CKDH' in noun:
			data[ID]['EMISION']['EHPM25'][0] = float(eval('+'.join(data[ID]['EMISION']['EHPM25'])))
			data[ID]['EMISION']['EHPM10'][0] = float(eval('+'.join(data[ID]['EMISION']['EHPM10'])))
		elif 'CKDNH' in noun:
			data[ID]['EMISION']['ENHPM25'][0] = float(eval('+'.join(data[ID]['EMISION']['ENHPM25'])))
			data[ID]['EMISION']['ENHPM10'][0] = float(eval('+'.join(data[ID]['EMISION']['ENHPM10'])))
	
	writeemsions(data, noun, 1)

def promdnp(archivo, noun):
	
	matriz = convertCSVMatriz(archivo)
	index = 0
	head = matriz[0,:]

	for value in head:

		if value == 'FID_Grilla':
			colFID = index
		if value == 'COL':
			colCol = index
		if value == 'ROW':
			colRow = index
		if value == 'LON' or value == 'LON_1':
			colLon = index
		if value == 'LAT' or value == 'LAT_1':
			colLat = index
		if value == 'IDEstacion':
			colIDEst = index
		if value == 'ETYPM25':
			colEPM25 = index
		if value == 'ETYPM10':
			colEPM10 = index
		index+=1

	listid = lista(matriz, colFID)
	data ={}
	emisions = ['EPM25', 'EPM10']

	for key in listid: 
		if data.get(key) is None: 
			data[key] = {}
		
		data[key]['GENERAL'] = {'COL':[], 'ROW': [], 'LON': [], 'LAT': [], 'IDEstation': []}
		data[key]['EMISION'] = {}
		
		entryemision = data[key]['EMISION']
		
		for emision in emisions: 
			if entryemision.get(emision) is None:
				entryemision[emision] = []

	for y in range(1, matriz.shape[0]):
		FID = matriz[y][colFID]
		
		if data[FID]['GENERAL']['COL'] == []: 
			data[FID]['GENERAL']['COL'].append(int(float(matriz[y][colCol])))
			data[FID]['GENERAL']['ROW'].append(int(float(matriz[y][colRow])))
			data[FID]['GENERAL']['LON'].append(matriz[y][colLon])
			data[FID]['GENERAL']['LAT'].append(matriz[y][colLat])
			data[FID]['GENERAL']['IDEstation'].append(int(float(matriz[y][colIDEst])))

		data[FID]['EMISION']['EPM25'].append(matriz[y][colEPM25])
		data[FID]['EMISION']['EPM10'].append(matriz[y][colEPM10])

	FID = data.keys()
	for ID in FID: 

		suma = float(eval('+'.join(data[ID]['EMISION']['EPM25'])))
		data[ID]['EMISION']['EPM25'] = []
		data[ID]['EMISION']['EPM25'].append(suma)

		suma = float(eval('+'.join(data[ID]['EMISION']['EPM10'])))
		data[ID]['EMISION']['EPM10'] = []
		data[ID]['EMISION']['EPM10'].append(suma)
	
	fullPM25 = 0
	fullPM10 = 0
	for ID in FID:
		fullPM25 += data[ID]['EMISION']['EPM25'][0]
		fullPM10 += data[ID]['EMISION']['EPM10'][0]

	writefull(fullPM25, fullPM10, noun)

def promtyear(dh, dnh, name, nametwo):
	
	folder = os.path.join('..', 'data', 'out', 'EmissionDay', '')
	archive = folder + name + '.csv'
	matriz  = convertCSVMatriz(archive)

	head = matriz[0,:]
	index = 0
	data = {}
	
	if 'IDW' in name or 'Homogeneous' in name or 'Heterogeneous' in name:
		emisions =  [ 'EHPM25', 'EHPM10',  'ENHPM25', 'ENHPM10', 'ETPM25', 'ETPM10']
	elif 'CKDH' in name:
		emisions =  [ 'EHPM25', 'EHPM10', 'ETPM25', 'ETPM10']
	elif 'CKDNH' in name:
		emisions =  ['ENHPM25', 'ENHPM10', 'ETPM25', 'ETPM10']
	
	for value in head: 
		if value == 'FID_Grilla': 
			colFIDG = index
		if value == 'IDEstacion':
			colIDEst = index
		if value == 'IDNodo':
			colIDNodo = index 
		if value == 'COL':
			colCol = index
		if value == 'ROW':
			colRow = index
		if value == 'LON':
			colLon = index
		if value == 'LAT':
			colLat = index
		if value == 'EHPM10':
			colEHPM10 = index
		if value == 'EHPM25':
			colEHPM25 = index
		if value == 'ENHPM10': 
			colENHPM10 = index
		if value == 'ENHPM25': 
			colENHPM25 = index
		index += 1

	for y in range(1, matriz.shape[0]):

		key = matriz[y][colFIDG]
		if data.get(key) is None:
			data[key] = {}

		data[key]['GENERAL'] = {'COL':[], 'ROW': [], 'LON': [], 'LAT': [], 'FID_Grilla': [],'IDEstation': [], 'IDNodo': []}
		data[key]['EMISION'] = {}

		entryemision = data[key]['EMISION']
		
		for emision in emisions: 
			if entryemision.get(emision) is None:
				entryemision[emision] = []


	for y in range(1, matriz.shape[0]):
		key = matriz[y][colFIDG]
		
		if data[key]['GENERAL']['COL'] == []: 
			data[key]['GENERAL']['COL'].append(int(float(matriz[y][colCol])))
			data[key]['GENERAL']['ROW'].append(int(float(matriz[y][colRow])))
			data[key]['GENERAL']['LON'].append(matriz[y][colLon])
			data[key]['GENERAL']['LAT'].append(matriz[y][colLat])
			data[key]['GENERAL']['FID_Grilla'].append(int(float(matriz[y][colFIDG])))
			data[key]['GENERAL']['IDEstation'].append(int(float(matriz[y][colIDEst])))
			data[key]['GENERAL']['IDNodo'].append(int(float(matriz[y][colIDNodo])))

		if 'IDW' in name or 'Homogeneous' in name or 'Heterogeneous' in name:
			data[key]['EMISION']['EHPM25'].append(matriz[y][colEHPM25])
			data[key]['EMISION']['EHPM10'].append(matriz[y][colEHPM10])
			data[key]['EMISION']['ENHPM25'].append(matriz[y][colENHPM25])
			data[key]['EMISION']['ENHPM10'].append(matriz[y][colENHPM10])
		elif 'CKDH' in name:
			data[key]['EMISION']['EHPM25'].append(matriz[y][colEHPM25])
			data[key]['EMISION']['EHPM10'].append(matriz[y][colEHPM10])
		elif 'CKDNH' in name:
			data[key]['EMISION']['ENHPM25'].append(matriz[y][colENHPM25])
			data[key]['EMISION']['ENHPM10'].append(matriz[y][colENHPM10])


	FID = data.keys()

	for ID in FID: 
		if 'IDW' in name or 'Homogeneous' in name or 'Heterogeneous' in name:
			#print data[ID]['EMISION']['EHPM25']
			suma = float(eval('+'.join(data[ID]['EMISION']['EHPM25'])))
			data[ID]['EMISION']['EHPM25'] = []
			data[ID]['EMISION']['EHPM25'].append(suma)
			data[ID]['EMISION']['EHPM25'][0] = (float(data[ID]['EMISION']['EHPM25'][0] * dh))/1000000

			suma = float(eval('+'.join(data[ID]['EMISION']['ENHPM25']))) 
			data[ID]['EMISION']['ENHPM25'] = []
			data[ID]['EMISION']['ENHPM25'].append(suma)
			data[ID]['EMISION']['ENHPM25'][0] = (float(data[ID]['EMISION']['ENHPM25'][0] * dnh))/1000000
			
			suma = float(eval('+'.join(data[ID]['EMISION']['EHPM10']))) 
			data[ID]['EMISION']['EHPM10'] = []
			data[ID]['EMISION']['EHPM10'].append(suma)
			data[ID]['EMISION']['EHPM10'][0] = (float(data[ID]['EMISION']['EHPM10'][0] * dh))/1000000

			suma = float(eval('+'.join(data[ID]['EMISION']['ENHPM10']))) 
			data[ID]['EMISION']['ENHPM10'] = []
			data[ID]['EMISION']['ENHPM10'].append(suma)
			data[ID]['EMISION']['ENHPM10'][0] = (float(data[ID]['EMISION']['ENHPM10'][0] * dnh))/1000000

		elif 'CKDH' in name:
			suma = float(eval('+'.join(data[ID]['EMISION']['EHPM25'])))
			data[ID]['EMISION']['EHPM25'] = []
			data[ID]['EMISION']['EHPM25'].append(suma)
			data[ID]['EMISION']['EHPM25'][0] = (float(data[ID]['EMISION']['EHPM25'][0] * dh))/1000000

			suma = float(eval('+'.join(data[ID]['EMISION']['EHPM10']))) 
			data[ID]['EMISION']['EHPM10'] = []
			data[ID]['EMISION']['EHPM10'].append(suma)
			data[ID]['EMISION']['EHPM10'][0] = (float(data[ID]['EMISION']['EHPM10'][0] * dh))/1000000			
		
		elif 'CKDNH' in name:
			suma = float(eval('+'.join(data[ID]['EMISION']['ENHPM25']))) 
			data[ID]['EMISION']['ENHPM25'] = []
			data[ID]['EMISION']['ENHPM25'].append(suma)
			data[ID]['EMISION']['ENHPM25'][0] = (float(data[ID]['EMISION']['ENHPM25'][0] * dnh))/1000000

			suma = float(eval('+'.join(data[ID]['EMISION']['ENHPM10']))) 
			data[ID]['EMISION']['ENHPM10'] = []
			data[ID]['EMISION']['ENHPM10'].append(suma)
			data[ID]['EMISION']['ENHPM10'][0] = (float(data[ID]['EMISION']['ENHPM10'][0] * dnh))/1000000

	
	for ID in FID:
		if 'IDW' in name or 'Homogeneous' in name or 'Heterogeneous' in name:
			data[ID]['EMISION']['ETPM25'].append(str(data[ID]['EMISION']['EHPM25'][0] + data[ID]['EMISION']['ENHPM25'][0]))
			data[ID]['EMISION']['ETPM10'].append(str(data[ID]['EMISION']['EHPM10'][0] + data[ID]['EMISION']['ENHPM10'][0]))
		
		elif 'CKDH' in name:
			data[ID]['EMISION']['ETPM25'].append(str(data[ID]['EMISION']['EHPM25'][0]))
			data[ID]['EMISION']['ETPM10'].append(str(data[ID]['EMISION']['EHPM10'][0]))

		elif 'CKDNH' in name:
			data[ID]['EMISION']['ETPM25'].append(str(data[ID]['EMISION']['ENHPM25'][0]))
			data[ID]['EMISION']['ETPM10'].append(str(data[ID]['EMISION']['ENHPM10'][0]))


	writeemsions(data, nametwo, 2)