#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
from excelmatriz import *
from wcsv import *
import os
import json 


def flowsdays(archive):
	
	#definition of variables local
	data = {}
	index = 0

	MFlows = convertCSVMatriz(archive)
	head = MFlows[0,:]
	print head


	for name in head:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'Estacion':
			colEstation = index
		if name == 'IDNodo':
			colIDNodo = index
		if name == 'Tipo': 
			colTipe = index
		if name == 'hora': 
			colhour = index
		if name == 'L': 
			colL = index
		if name == '>C5': 
			colXC5 = index
		if name == 'AL': 
			colAL = index
		if name == 'AT': 
			colAT = index
		if name == 'B': 
			colB = index
		if name == 'BA': 
			colBA = index
		if name == 'BT': 
			colBT = index
		if name == 'C': 
			colC = index
		if name == 'C2G': 
			colC2G = index
		if name == 'C2P': 
			colC2P = index
		if name == 'C3-C4': 
			colC3C4 = index
		if name == 'C5': 
			colC5 = index
		if name == 'ESP': 
			colESP = index
		if name == 'INT': 
			colINT = index
		if name == 'M': 
			colM = index
		if name == 'TOTAL':
			colTOTAL = index
		index += 1

	headVehicle = MFlows[0,colhour+1:]

	for y in range(1, MFlows.shape[0]):
		
		IDEstation = MFlows[y][colIDEstation]
		Tipe = MFlows[y][colTipe]


		if data.get(IDEstation) is None:
			data[IDEstation] = {}
			data[IDEstation]['GENERAL'] = []

		entryType = data[IDEstation]

		if entryType.get(Tipe) is None:
			entryType[Tipe] = {}
		
		entryvehicle = entryType[Tipe]
		
		for x in range(0, len(headVehicle)):
			kind = headVehicle[x]
			
			if entryvehicle.get(kind) is None:
				entryvehicle[kind] = []

		if MFlows[y][colEstation] not in data[IDEstation]['GENERAL']:
			data[IDEstation]['GENERAL'].append(MFlows[y][colEstation])
		if MFlows[y][colIDEstation] not in data[IDEstation]['GENERAL']:
			data[IDEstation]['GENERAL'].append(MFlows[y][colIDEstation])
		if MFlows[y][colIDNodo] not in data[IDEstation]['GENERAL']:
			data[IDEstation]['GENERAL'].append(MFlows[y][colIDNodo])

		data[IDEstation][Tipe]['L'].append(MFlows[y][colL])
		data[IDEstation][Tipe]['>C5'].append(MFlows[y][colXC5])
		data[IDEstation][Tipe]['AL'].append(MFlows[y][colAL])
		data[IDEstation][Tipe]['AT'].append(MFlows[y][colAT])
		data[IDEstation][Tipe]['B'].append(MFlows[y][colB])
		data[IDEstation][Tipe]['BA'].append(MFlows[y][colBA])
		data[IDEstation][Tipe]['BT'].append(MFlows[y][colBT])
		data[IDEstation][Tipe]['C'].append(MFlows[y][colC])
		data[IDEstation][Tipe]['C2G'].append(MFlows[y][colC2G])
		data[IDEstation][Tipe]['C2P'].append(MFlows[y][colC2P])
		data[IDEstation][Tipe]['C3-C4'].append(MFlows[y][colC3C4])
		data[IDEstation][Tipe]['C5'].append(MFlows[y][colC5])
		data[IDEstation][Tipe]['ESP'].append(MFlows[y][colESP])
		data[IDEstation][Tipe]['INT'].append(MFlows[y][colINT])
		data[IDEstation][Tipe]['M'].append(MFlows[y][colM])
		data[IDEstation][Tipe]['TOTAL'].append(MFlows[y][colTOTAL])


	Type = ['HABIL', 'NOHAB']	
	IDEstation = data.keys()
	for ID in IDEstation:
		for typ in Type:
			vehicles = data[ID][typ].keys()
			for veh in vehicles:
				data[ID][typ][veh] = eval('+'.join(data[ID][typ][veh]))

	writesum(data)

def full(archive, noun):
	matriz = convertCSVMatriz(archive)
	head = matriz[0,:]
	index = 0
	fullPM25 = 0
	fullPM10 = 0

	for value in head:
		if value == 'ETPM10': 
			colTPM10 = index
		if value == 'ETPM25': 
			colTPM25 = index
		index += 1 

	for i in range(1, matriz.shape[0]):
		fullPM25 += float(matriz[i][colTPM25])
		fullPM10 += float(matriz[i][colTPM10])


	writefull(str(fullPM25), str(fullPM10), noun)

def listaCSV(direccion):
   	#Variable para la ruta al directorio
	path = os.path.join(direccion,'')
	#print direccion

	#Lista vacia para incluir los ficheros
	lstFilesEmissions = []

	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
	datos = {}

	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == '.csv'):
	        	lstFilesEmissions.append(nombreFichero+extension)

	return lstFilesEmissions

def emissiontotal():

	folderEmsionYear = os.path.join('..','data','out', 'EmissionYear', '')
	listEmsionYear = listaCSV(folderEmsionYear)

	for name in listEmsionYear:
		archive = os.path.join(folderEmsionYear, name)
		if 'Principal' in name: 
			full(archive, 'PrincipalIDW')
		if 'Secundary' in name:
			full(archive, 'SecundaryIDW')
		if 'TM' in name: 
			full(archive, 'TMIDW')


	#------ not process 2014---- #
	#ckdhprincipal = os.path.join('..','data','out','EmissionYear', 'EmissionYearCKDHPrincipal.csv')
	#ckdhtm = os.path.join('..','data','out','EmissionYear', 'EmissionYearCKDHTM.csv')
	#full(ckdhprincipal, 'CKDH_Principal')
	#full(ckdhtm, 'CKDH_TM')

	#ckdnhprincipal = os.path.join('..','data','out','EmissionYear', 'EmissionYearCKDNHPrincipal.csv')
	#ckdnhtm = os.path.join('..','data','out','EmissionYear', 'EmissionYearCKDNHTM.csv')
	#full(ckdnhprincipal, 'CKDNH_Principal')
	#full(ckdnhtm, 'CKDNH_TM')
	
	#secundaryhomogeneous = os.path.join('..','data','out','EmissionYear', 'EmissionYearHomogeneous.csv')
	#full(secundaryhomogeneous,'SecundaryHomogeneous')

	#secundaryhetereogeneous = os.path.join('..','data','out', 'EmissionYear', 'EmissionYearHeterogeneous.csv')
	#full(secundaryhetereogeneous,'SecundaryHetereogeneous')

def emissionGrid(archive, noun):
	
	matriz = convertCSVMatriz(archive)
	data = {}

	head = matriz[0,:]
	index = 0

	for value in head:
		if value == 'FID_Grilla':
			colIDGrill = index
		if value == 'hora':
			colhour = index
		if value == 'LON' or value == 'LON_1':
			colLON = index 
		if value == 'LAT' or value == 'LAT_1':
			colLAT = index
		if value == 'ROW':
			colROW = index
		if value == 'COL':
			colCOL = index
		if value == 'EHPM10':
			colEHPM10 = index
		if value == 'EHPM25':
			colEHPM25 = index
		if value == 'ENHPM10':
			colENHPM10 = index
		if value == 'ENHPM25':
			colENHPM25 = index
		index += 1

	for i in range(1, matriz.shape[0]):
		ID_Grid = matriz[i][colIDGrill]
		hour = int(matriz[i][colhour])

		if data.get(ID_Grid) is None:
			data[ID_Grid] = {}
			data[ID_Grid]['GENERAL'] = {'COL':[], 'ROW': [], 'LON': [], 'LAT': []}
			data[ID_Grid]['Emissions'] = {}
			if 'IDW' in noun or 'Homogeneous' in noun or 'Heterogeneous' in noun:
				data[ID_Grid]['Emissions']['EHPM25'] = {}
				data[ID_Grid]['Emissions']['EHPM10'] = {}
				data[ID_Grid]['Emissions']['ENHPM25'] = {}
				data[ID_Grid]['Emissions']['ENHPM10'] = {}
			elif 'CKDH' in noun:
				data[ID_Grid]['Emissions']['EHPM25'] = {}
				data[ID_Grid]['Emissions']['EHPM10'] = {}
			elif 'CKDNH' in noun:
				data[ID_Grid]['Emissions']['ENHPM25'] = {}
				data[ID_Grid]['Emissions']['ENHPM10'] = {}

		if data[ID_Grid]['GENERAL']['COL'] == []:
			data[ID_Grid]['GENERAL']['COL'].append(int(float(matriz[i][colCOL])))
			data[ID_Grid]['GENERAL']['ROW'].append(int(float(matriz[i][colROW])))
			data[ID_Grid]['GENERAL']['LON'].append(matriz[i][colLON])
			data[ID_Grid]['GENERAL']['LAT'].append(matriz[i][colLAT])

		Types = data[ID_Grid]['Emissions'].keys()

		for Type in Types:
			entryhour = data[ID_Grid]['Emissions'][Type]
			
			if entryhour.get(hour) is None: 
				entryhour[hour] = []
			if 'IDW' in noun or 'Homogeneous' in noun or 'Heterogeneous' in noun:
				if Type == 'EHPM25':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colEHPM25])
				elif Type == 'EHPM10':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colEHPM10])
				elif Type == 'ENHPM25':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colENHPM25])
				elif Type == 'ENHPM10':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colENHPM10])
			elif 'CKDH' in noun:
				if Type == 'EHPM25':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colEHPM25])
				elif Type == 'EHPM10':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colEHPM10])
			elif 'CKDNH' in noun:
				if Type == 'ENHPM25':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colENHPM25])
				elif Type == 'ENHPM10':
					data[ID_Grid]['Emissions'][Type][hour].append(matriz[i][colENHPM10])
	

	#Error
	keys = data.keys()
	
	for key in keys:
		Types = data[key]['Emissions'].keys()
	 	for Type in Types:
	 		hours = data[key]['Emissions'][Type].keys()
	 		suma = 0
	 		for hour in hours:
	 			suma = eval('+'.join(data[key]['Emissions'][Type][hour]))
	 			data[key]['Emissions'][Type][hour] = []
	 			data[key]['Emissions'][Type][hour].append(suma)

	#print data
	wcsv(data, noun)
	