#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
import os
import sys
import json
import csv
sys.path.append('core')
from excelmatriz import * 

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

def writespeciation(data, namearchive, namespecie):

	folder = os.path.join('..', 'data', 'out', 'speciation', 'VP', '')
	csvsalida = open(folder+ namespecie+'_'+namearchive, 'w')
	salida = csv.writer(csvsalida, delimiter=',')#, quoting=csv.QUOTE_ALL

	salida.writerow(['ROW', 'COL', 'LAT', 'LON', 'POLNAME', 'UNIT', 'E00h', 'E01h', 'E02h', 'E03h', 'E04h', 'E05h', 'E06h' ,'E07h', 'E08h', 'E09h', 'E10h', 'E11h', 'E12h', 'E13h', 'E14h', 'E15h', 'E16h', 'E17h', 'E18h', 'E19h', 'E20h', 'E21h', 'E22h', 'E23h', 'E24h'])

	keys = data.keys()
	for key in keys:
		csvsalida.write(str(data[key]['GENERAL']['ROW'][0]))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['COL'][0]))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['LAT'][0]))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['LON'][0]))
		csvsalida.write(',')
		csvsalida.write(namespecie)
		csvsalida.write(',')
		csvsalida.write('g/s')
		csvsalida.write(',')
		hours = data[key]['hours'].keys()
		#print hours
		for hour in hours:
			csvsalida.write(data[key]['hours'][hour][0])
			if hour != 24:
				csvsalida.write(',')
		csvsalida.write('\n')
	csvsalida.close()

def speciationvp():
	print 'PM2.5 speciation taken from gsref*(EI SMOKE 2007 PM) for RPM from paved roads with PROFID = 92053'
	print 'Speciated emissions in g/s per SPCID per ROW,COL,H'

	archivespeciation = os.path.join('..', 'data', 'constants', 'VP_SPC_PROF.xlsx')
	folder = os.path.join('..','data','out', 'EmissionGrid', 'VP', '')
	lstFilesEmissions = listaCSV(folder)
	
	Files25 = []

	for File in lstFilesEmissions: 
		if 'PM25' in File: 
			Files25.append(File)
	
	
	Mspeciation = convertXLSCSV(archivespeciation)

	head = Mspeciation[0,:]
	index = 0
	for value in head: 
		if value == 'SPCID':
			colSPCID = index
		if value == 'MASSFRAC':
			colMASSFRAC = index
		index += 1 

	speciation = {}

	for i in range(1, Mspeciation.shape[0]):
		name = Mspeciation[i][colSPCID]
		val = Mspeciation[i][colMASSFRAC]

		if speciation.get(name) is None: 
			speciation[name] = val

	namesspecies = speciation.keys()
	

	for species in namesspecies:
		for File in Files25:
			data = {}
			archive = folder + File
			matriz = convertCSVMatriz(archive)

			head = matriz[0,:]
			index = 0
			for value in head:
				if value == 'ROW':
					colROW = index
				if value == 'COL':
					colCOL = index
				if value == 'LAT':
					colLAT = index
				if value == 'LON':
					colLON = index

				index += 1 
			
			for i in range(1, matriz.shape[0]):
				keys = int(matriz[i][0] + matriz[i][1])
				if data.get(keys) is None: 
					data[keys] = {}
					data[keys]['GENERAL'] = {'ROW': [] ,'COL': [],'LAT': [],'LON': []} 
					data[keys]['hours'] = {}

					if data[keys]['GENERAL']['ROW'] == []:
						data[keys]['GENERAL']['ROW'].append(int(matriz[i][colROW]))
						data[keys]['GENERAL']['COL'].append(int(matriz[i][colCOL]))
						data[keys]['GENERAL']['LAT'].append(matriz[i][colLAT])
						data[keys]['GENERAL']['LON'].append(matriz[i][colLON])

					entryhour = data[keys]['hours']
					
					for hour in range(0, 25):
						if entryhour.get(hour) is None:
							entryhour[hour] = []

					hour = 0
					for x in range(6, matriz.shape[1]):
						data[keys]['hours'][hour].append(str((float(matriz[i][x]) * float(speciation[species]))/3600))
						hour += 1			
			writespeciation(data, File, species)

def testing():
	folder1 = os.path.join('..','data','out', 'EmissionGrid', 'VP', '')
	folder2 = os.path.join('..','data','out', 'speciation', 'VP', '')


	listEmision = listaCSV(folder1)
	listEspeciation = listaCSV(folder2)
	#print listEspeciation
	data = {}
	listPM25 = []
	for File in listEmision:
		if 'PM25' in File:
			listPM25.append(File)
			if data.get(File) is None: 
				data[File] = []

	Files = data.keys()
	for specie in listEspeciation:
		for File in Files:
			if File in specie:
				data[File].append(specie)

	names = data.keys()

	for key in names:
		#print data[key]
		Factors = data[key]
		sumTotal1 = 0
		sumTotal2 = 0
		for subkey in Factors: 

			archive = folder2 + subkey 
			#print archive
			Marchive = convertCSVMatriz(archive)

			for i in range(1, Marchive.shape[0]):
				for x in range(6, Marchive.shape[1]):
					sumTotal1 += float(Marchive[i][x])

		sumTotal1 = sumTotal1 * 3600

		archive = folder1 + key
		Marchive = convertCSVMatriz(archive)
		for i in range(1, Marchive.shape[0]):
				for x in range(6, Marchive.shape[1]):
					sumTotal2 += float(Marchive[i][x])

		

		sumTotal1 = str(sumTotal1)
		sumTotal2 = str(sumTotal2)
		
		#print sumTotal1, sumTotal2
		#print sumTotal1 == sumTotal2


		if sumTotal1 == sumTotal2:
			print 'OK'
		else: 
			print 'Review process or data' 
			
		






			


