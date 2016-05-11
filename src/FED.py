# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons
import os
import sys
import json
sys.path.append("core")
from excelmatriz import *


#archiveidwsecundarias = os.path.join('..', 'data', 'VP', 'Secundarias','Secundary_(IDW)_EmisionHour.csv')
#archivesidwprincipales = os.path.join('..', 'data', 'VP', 'Principales', 'Principal_(IDW)EmisionHour.csv')
archivesidwtm = os.path.join('..', 'data', 'VP', 'TM', 'TM_(IDW)EmisionHour.csv')

Archives = [archivesidwtm] #archiveidwsecundarias, archivesidwprincipales

for archive in Archives:

	matriz = convertCSVMatriz(archive)
	head = matriz[0,:]
	index = 0
	for value in head:
		if value == 'FEHPM10':
			colFEHPM10 = index
		if value == 'FEHPM25':
			colFEHPM25 = index
		if value == 'FENHPM10':
			colFENHPM10 = index
		if value == 'FENHPM25':
			colFENHPM25 = index
		if value == 'FAH':
			colFAH = index
		if value == 'FANH':
			colFANH = index
		if value == 'PPH':
			colPPH = index
		if value == 'PPNH':
			colPPNH = index
		if value == 'EHPM25':
			colEHPM25 = index
		if value == 'EHPM10':
			colEHPM10 = index
		if value == 'ENHPM25':
			colENHPM25 = index
		if value == 'ENHPM10':
			colENHPM10 = index
		if value == 'FID_LINK':
			colFIDLink = index
		index += 1

	data = {}

	for i in range(1, matriz.shape[0]):
		key = int(float(matriz[i][colFIDLink]))
		if data.get(key) is None:
			data[key] = {'FE': {'Habil': {'PM25': [], 'PM10': []}, 'NHabil': {'PM25': [], 'PM10': []}}, 'FA': {'Habil': [], 'NHabil': []}, 'PP': {'Habil': [], 'NHabil': []}, 'PP2': {'Habil': [], 'NHabil': []}, 'E':{'Habil': {'PM25':[], 'PM10':[]}, 'NHabil':{'PM25':[], 'PM10':[]}}}

		data[key]['FE']['Habil']['PM25'].append(matriz[i][colFEHPM25])
		data[key]['FE']['Habil']['PM10'].append(matriz[i][colFEHPM10])

		data[key]['FE']['NHabil']['PM25'].append(matriz[i][colFENHPM25])
		data[key]['FE']['NHabil']['PM10'].append(matriz[i][colFENHPM10])

		data[key]['FA']['Habil'].append(matriz[i][colFAH])
		data[key]['FA']['NHabil'].append(matriz[i][colFANH])

		data[key]['PP']['Habil'].append(matriz[i][colPPH])
		data[key]['PP']['NHabil'].append(matriz[i][colPPNH])

		data[key]['PP2']['Habil'].append(matriz[i][colPPH])
		data[key]['PP2']['NHabil'].append(matriz[i][colPPNH])

		data[key]['E']['Habil']['PM25'].append(matriz[i][colEHPM25])
		data[key]['E']['Habil']['PM10'].append(matriz[i][colEHPM10])

		data[key]['E']['NHabil']['PM25'].append(matriz[i][colENHPM25])
		data[key]['E']['NHabil']['PM10'].append(matriz[i][colENHPM10])

		

	keys = data.keys()
	promFE = 0
	for key in keys:
		factors = data[key].keys()
		for factor in factors:
			Types = data[key][factor].keys()
			for Type in Types:
				if factor == 'FE' or factor == 'E':
					PMs = data[key][factor][Type].keys()
					for PM in PMs:
						suma = eval('+'.join(data[key][factor][Type][PM]))
						data[key][factor][Type][PM] = []
						data[key][factor][Type][PM].append(float(suma))
				
				elif factor == 'PP':
					#print data[key][factor][Type]
					suma = eval('+'.join(data[key][factor][Type]))
					#suma2 = suma
					suma = suma/24
					data[key][factor][Type] = []
					data[key][factor][Type].append(float(suma))
				else:
				    suma = eval('+'.join(data[key][factor][Type]))
				    data[key][factor][Type] = []
				    data[key][factor][Type].append(float(suma))
	
	prom = len(keys)
	promFEHPM25 = 0
	promFEHPM10 = 0
	promFENHPM25 = 0
	promFENHPM10 = 0

	promFAH = 0
	promFANH = 0

	promPPH2 = 0
	promPPNH2 = 0

	promPPH = 0
	promPPNH = 0

	promEHPM25 = 0
	promEHPM10 = 0
	promENHPM25 = 0
	promENHPM10 = 0

	for key in keys:
		promFEHPM25 += data[key]['FE']['Habil']['PM25'][0]
		promFEHPM10 += data[key]['FE']['Habil']['PM10'][0]

		promFENHPM25 += data[key]['FE']['NHabil']['PM25'][0]
		promFENHPM10 += data[key]['FE']['NHabil']['PM10'][0]

		promFAH += data[key]['FA']['Habil'][0]
		promFANH += data[key]['FA']['NHabil'][0]

		promPPH += data[key]['PP']['Habil'][0]
		promPPNH += data[key]['PP']['NHabil'][0]

		promPPH2 += data[key]['PP2']['Habil'][0]
		promPPNH2 += data[key]['PP2']['NHabil'][0]

		promEHPM25 += data[key]['E']['Habil']['PM25'][0]
		promEHPM10 += data[key]['E']['Habil']['PM10'][0]

		promENHPM25 += data[key]['E']['NHabil']['PM25'][0]
		promENHPM10 += data[key]['E']['NHabil']['PM10'][0]

	promFEHPM25 = promFEHPM25/prom
	promFEHPM10 = promFEHPM10/prom
	promFENHPM25 = promFENHPM25/prom
	promFENHPM10 = promFENHPM10/prom

	promFAH = promFAH/prom
	promFANH = promFANH/prom

	promPPH = promPPH/prom
	promPPNH = promPPNH/prom

	promPPH2 = promPPH2/prom
	promPPNH2 = promPPNH2/prom


	print archive
	print 'promFEHPM25', promFEHPM25
	print 'promFEHPM10', promFEHPM10
	print 'promFENHPM25', promFENHPM25
	print 'promFENHPM10', promFENHPM10
	print '----------------------------------'
	print 'promFAH', promFAH
	print 'promFANH', promFANH
	print '----------------------------------'
	print 'Dividido en 24'
	print 'promPPH', promPPH
	print 'promPPNH', promPPNH
	print '----------------------------------'
	print 'Sin dividir en 24'
	print 'promPPH2', promPPH2
	print 'promPPNH2', promPPNH2

	print '----------------------------------'
	print 'promEHPM25', promEHPM25
	print 'promEHPM10', promEHPM10
	print 'promENHPM25', promENHPM25
	print 'promENHPM10', promENHPM10


