# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import os
from excelmatriz import *
from wcsv import *
import json


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

def pmc(folder): 
	listEmitions = listaCSV(folder)	
	#print listEmitions

	listEmitionsPM25 = []
	listEmitionsPM10 = []



	for name in listEmitions:
		if 'PM25' in name: 
			listEmitionsPM25.append(name)
		if 'PM10' in name: 
			listEmitionsPM10.append(name)

	
	for i in range (0, len(listEmitionsPM25)):
		archivePM25 = folder + listEmitionsPM25[i]
		archivePM10 = folder + listEmitionsPM10[i]

		MPM25 = convertCSVMatriz(archivePM25)
		MPM10 = convertCSVMatriz(archivePM10)

		data = {}

		head = MPM25[0,:]

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
			if value == 'POLNAME': 
				colPOL = index
			index += 1 

		for y in range(1, MPM25.shape[0]):
			key = MPM25[y][colROW] + MPM25[y][colCOL]
			

			if data.get(key) is None: 
				data[key] = {}
				data[key]['GENERAL'] = {'COL': [], 'ROW': [], 'LAT': [], 'LON': [], 'POLNAME': []}
				data[key]['hours'] = {}


			if data[key]['GENERAL']['COL'] == []:
				data[key]['GENERAL']['COL'].append(MPM10[y][colCOL])
				data[key]['GENERAL']['ROW'].append(MPM10[y][colROW])
				data[key]['GENERAL']['LAT'].append(MPM10[y][colLAT])
				data[key]['GENERAL']['LON'].append(MPM10[y][colLON])
				data[key]['GENERAL']['POLNAME'].append(MPM10[y][colPOL])

			entryhours = data[key]['hours']
			for hour in range(0, 25):
				if entryhours.get(hour) is None: 
					entryhours[hour] = []

			hour = 0
			for x in range(6, MPM25.shape[1]): 
				data[key]['hours'][hour].append((float(MPM10[y][x])/3600) - (float(MPM25[y][x])/3600))
				hour += 1

		noun = listEmitionsPM25[i]
		if 'EHPM25' in noun: 
			if 'TM' in noun:
				noun = noun.strip('EHPM25.csv')	
			else: 
				noun = noun.strip('_EHPM25.csv')
		if 'ENHPM25' in noun: 
			if 'TM' in noun: 
				noun = noun.strip('ENHPM25.csv')
			else:
				noun = noun.strip('_ENHPM25.csv')

		if 'PM25' in noun: 
			noun = noun.strip('PM25_')
			noun = noun.strip('.csv')

		noun = 'PMC_' + noun 
		PMC(data, noun, folder)

def testingpmc(folder):
	List = listaCSV(folder)
	listPMC = []
	for archive in List:
		if 'PMC' in archive:
			listPMC.append(archive)

	for name in listPMC: 
		MPMC = convertCSVMatriz(folder + name)

		for  i in range(1, MPMC.shape[0]):
			for x in range(6, MPMC.shape[1]):
				if 0 > MPMC[i][x] is True: 
					print 'Review process number <0'
				else: 
					print 'OK'