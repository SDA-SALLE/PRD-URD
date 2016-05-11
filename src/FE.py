# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import os
import sys
sys.path.append("core")
from excelmatriz import *


#archiveidwsecundarias = os.path.join('..', 'data', 'VP', 'Secundarias','Secundary_(IDW)_EmisionHour.csv')
#archivesidwprincipales = os.path.join('..', 'data', 'VP', 'Principales', 'Principal_(IDW)EmisionHour.csv')
archivesidwtm = os.path.join('..', 'data', 'VP', 'TM', 'TM_(IDW)EmisionHour.csv')

Archives = [archiveidwsecundarias, archivesidwprincipales, archivesidwtm]

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
		if value == 'EHPM10':
			colEHPM10 = index
		if value == 'EHPM25':
			colEHPM25 = index
		if value == 'ENHPM10':
			colENHPM10 = index
		if value == 'ENHPM25':
			colENHPM25 = index
		index += 1

	promFEHPM10 = 0
	promFEHPM25 = 0
	promFENHPM10 = 0
	promFENHPM25 = 0
	
	promFAH = 0
	promFANH = 0
	
	promPPH = 0
	promPPNH = 0

	promEHPM10 = 0
	promEHPM25 = 0
	promENHPM10 = 0
	promENHPM25 = 0

	for i in range(1, matriz.shape[0]):
		
		dataFEHPM10 = matriz[i][colFEHPM10]
		dataFEHPM25 = matriz[i][colFEHPM25]
		dataFENHPM10 = matriz[i][colFENHPM10]
		dataFENHPM25 = matriz[i][colFENHPM25]
		
		dataFAH = matriz[i][colFAH]
		dataFANH = matriz[i][colFANH]
		
		dataPPH = matriz[i][colPPH]
		dataPPNH = matriz[i][colPPNH]

		dataEHPM10 = matriz[i][colEHPM10]
		dataEHPM25 = matriz[i][colEHPM25]
		dataENHPM10 = matriz[i][colENHPM10]
		dataENHPM25 = matriz[i][colENHPM25]

		promFEHPM25 += float(dataFEHPM25)
		promFEHPM10 += float(dataFEHPM10)
		promFENHPM25 += float(dataFENHPM25)
		promFENHPM10 += float(dataFENHPM10)
		
		promFAH += float(dataFAH)
		promFANH += float(dataFANH)
		
		promPPH += float(dataPPH)
		promPPNH += float(dataPPNH)

		promEHPM25 += float(dataEHPM25)
		promEHPM10 += float(dataEHPM10)
		promENHPM25 += float(dataENHPM25)
		promENHPM10 += float(dataENHPM10)

	promFEHPM25 = promFEHPM25/(matriz.shape[0]-1)
	promFEHPM10 = promFEHPM10/(matriz.shape[0]-1)
	promFENHPM25 = promFENHPM25/(matriz.shape[0]-1)
	promFENHPM10 = promFENHPM10/(matriz.shape[0]-1)
	
	promFAH = promFAH/(matriz.shape[0]-1)
	promFANH = promFANH/(matriz.shape[0]-1)
	
	promPPH = promPPH/(matriz.shape[0]-1)
	promPPNH = promPPNH/(matriz.shape[0]-1)

	promEHPM25 = promEHPM25
	promEHPM10 = promEHPM10
	promENHPM25 = promENHPM25
	promENHPM10 = promENHPM10

	print "Archivo: ",  archive
	print "promedioFEHPM10: ", promFEHPM10
	print "promedioFEHPM25: ", promFEHPM25
	print "promedioFENHPM10: ", promFENHPM10
	print "promedioFENHPM25: ", promFENHPM25
	print '---------------------------------'
	print "promedioFAH: ", promFAH
	print "promedioFANH: ", promFANH
	print '---------------------------------'
	print "promedioPPH: ", promPPH
	print "promedioPPNH: ", promPPNH
	print '---------------------------------'
	print "promedioEHPM10: ", promEHPM10
	print "promedioEHPM25: ", promEHPM25
	print "promedioENHPM10: ", promENHPM10
	print "promedioENHPM25: ", promENHPM25


