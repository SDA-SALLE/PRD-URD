#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
import os
import sys
sys.path.append("core")
from excelmatriz import *


archiveidw = os.path.join('..', 'data', 'VP', 'Secundarias','Secundary_(IDW)_EmisionHour.csv')
archivehetero = os.path.join('..', 'data', 'VP', 'Secundarias','Secundary_(Heterogeneous)_EmisionHour.csv')
archivehomo = os.path.join('..', 'data', 'VP', 'Secundarias', 'Secundary_(Homogeneous)_EmisionHour.csv')

Archives = [archiveidw, archivehetero, archivehomo]

for archive in Archives:
	matriz = convertCSVMatriz(archive)

	head = matriz[0,:]
	#print head
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
		index += 1

	promFEHPM10 = 0
	promFEHPM25 = 0
	promFENHPM10 = 0
	promFENHPM25 = 0
	for i in range(1, matriz.shape[0]):
		dataFEHPM10 = matriz[i][colFEHPM10]
		dataFEHPM25 = matriz[i][colFEHPM25]
		dataFENHPM10 = matriz[i][colFENHPM10]
		dataFENHPM25 = matriz[i][colFENHPM25]


		promFEHPM25 += float(dataFEHPM25)
		promFEHPM10 += float(dataFEHPM10)
		promFENHPM25 += float(dataFENHPM25)
		promFENHPM10 += float(dataFENHPM10)

	promFEHPM25 = promFEHPM25/(matriz.shape[0]-1)
	promFEHPM10 = promFEHPM10/(matriz.shape[0]-1)
	promFENHPM25 = promFENHPM25/(matriz.shape[0]-1)
	promFENHPM10 = promFENHPM10/(matriz.shape[0]-1)

	print "Archivo: ",  archive
	print "promedioFEHPM10: ", promFEHPM10
	print "promedioFEHPM25: ", promFEHPM25
	print "promedioFENHPM10: ", promFENHPM10
	print "promedioFENHPM25: ", promFENHPM25


