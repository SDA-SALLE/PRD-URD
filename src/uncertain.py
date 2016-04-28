#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python

import json
import os
import sys
import math
sys.path.append('core')
from excelmatriz import *
from wcsv import *

multpesos = 0.1
FAVKT = 0.26**2
PM10K = 0.62
PM25K = 0.15
PesosV = {'L':[1.6], 'C':[2.4], 'BT':[8.2], 'B':[14.5], 'AL':[14.5],  'ESP':[8.2], 'INT':[14.5], 'C2P':[4.6], 'C2G':[8.5], 'C3-C4':[28], 'C5':[35.0], '>C5':[40], 'M':[0.2]}
PesosVArt = {'AT': [30.0], 'BA': [42.0]}
NameVehicles = ['L', 'C', 'BT', 'B', 'AL',  'ESP', 'INT', 'C2P', 'C2G', 'C3-C4', 'C5', '>C5', 'M', 'NH_>C5', 'NH_AL', 'NH_B', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_INT', 'NH_M', 'NH_ESP', 'NH_L']
Art = ['AT', 'BA', 'NH_AT', 'NH_BA']
DH = 245
DNH = 120

names = PesosV.keys()
for name in names:
	PesosV[name][0] = round((PesosV[name][0] * multpesos), 3)

names = PesosVArt.keys()
for name in names:
	PesosVArt[name][0] = PesosVArt[name][0] * multpesos

def uncertainidw(archive, noun):

	contantEmssion = os.path.join('..', 'data', 'constants', 'IncetidumbreEstacion.xlsx')
	matrizEmissionE = convertXLSCSV(contantEmssion)
	Emissions = {}

	for i in range(2, matrizEmissionE.shape[0]):
		estation = int(float(matrizEmissionE[i][0]))
		ICS = float(matrizEmissionE[i][2])

		if Emissions.get(estation) is None:
			Emissions[estation] = []

		Emissions[estation].append(ICS)

	matrizEmissionE = None

	data = {}
	matriz = convertCSVMatriz(archive)

	head = matriz[0,:]

	index = 0
	for value in head:
		if value == 'FID_LINK' or value == 'FID_Link':
			colFID = index
		if value == 'IDEstacion':
			colEstation = index
		if value == 'FID_Grilla':
			colIDGrid = index
		if value == 'IDW_Cs': 
			colIDW = index
		if value == 'hora':
			colIH = index + 1
		if value == 'TOTAL':
			colFH = index
		if value == 'NH_TOTAL':
			colFNH = index
		if value == 'PPH':
			colPPH = index
		if value == 'PPNH':
			colPPNH = index
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
		FID_Link = int(float(matriz[i][colFID]))
		hour = int(matriz[i][colIH-1])

		if data.get(FID_Link) is None: 
			data[FID_Link] = {}
			data[FID_Link]['General'] = {'IDW': [], 'Estation': [], 'FID_Grilla': []}
			data[FID_Link]['hours'] = {}

		if data[FID_Link]['General']['IDW'] == []:
			data[FID_Link]['General']['IDW'] = float(matriz[i][colIDW])
			data[FID_Link]['General']['Estation'] = int(float(matriz[i][colEstation]))
			data[FID_Link]['General']['FID_Grilla'] = int(float(matriz[i][colIDGrid]))
		

		entryhour = data[FID_Link]['hours']
		
		if entryhour.get(hour) is None:
			entryhour[hour] = {}
			entryhour[hour]['flows'] = {}
			entryhour[hour]['TOTAL'] = {}
			entryhour[hour]['Result'] = {'PP': {'H': [], 'NH': []}, 'FA': {'H': [], 'NH': []}, 'FE': {'H': {'PM10': [] ,'PM25': []}, 'NH': {'PM10': [] ,'PM25': []} }, 'E': {'H': {'PM10': [], 'PM25': []}, 'NH': {'PM10': [], 'PM25': []}}}
			entryhour[hour]['TOTAL']['Habil'] = []
			entryhour[hour]['TOTAL']['NHabil'] = []

		entryvehicles = entryhour[hour]['flows']
		if noun == 'Principal':
			for name in NameVehicles: 
				if entryvehicles.get(name) is None: 
					entryvehicles[name] = []
			
			suma = 0
			for x in range(colIH, colFH):
				name = matriz[0][x]
				entryvehicles[name].append(float(matriz[i][x]))
				suma += float(matriz[i][x])

			entryhour[hour]['TOTAL']['Habil'].append(suma)			

			suma = 0
			for x in range(colFH+1, colFNH):
				name = matriz[0][x]
				entryvehicles[name].append(float(matriz[i][x]))
				suma += float(matriz[i][x])

			entryhour[hour]['TOTAL']['NHabil'].append(suma)

		if noun == 'TM':
			for name in Art: 
				if entryvehicles.get(name) is None: 
					entryvehicles[name] = []
				
			suma = 0
			for x in range(colIH, colIH+2):
				name = matriz[0][x]
				entryvehicles[name].append(float(matriz[i][x]))
				suma += float(matriz[i][x])
			entryhour[hour]['TOTAL']['Habil'].append(suma)

			suma = 0
			for x in range(colIH+2, colIH+4):
				name = matriz[0][x]
				entryvehicles[name].append(float(matriz[i][x]))
				suma += float(matriz[i][x])
			entryhour[hour]['TOTAL']['NHabil'].append(suma)

		data[FID_Link]['hours'][hour]['Result']['PP']['H'].append(float(matriz[i][colPPH]))
		data[FID_Link]['hours'][hour]['Result']['PP']['NH'].append(float(matriz[i][colPPNH]))

		data[FID_Link]['hours'][hour]['Result']['FA']['H'].append(float(matriz[i][colFAH]))
		data[FID_Link]['hours'][hour]['Result']['FA']['NH'].append(float(matriz[i][colFANH]))

		data[FID_Link]['hours'][hour]['Result']['FE']['H']['PM10'].append(float(matriz[i][colFEHPM10]))
		data[FID_Link]['hours'][hour]['Result']['FE']['H']['PM25'].append(float(matriz[i][colFEHPM25]))

		data[FID_Link]['hours'][hour]['Result']['FE']['NH']['PM10'].append(float(matriz[i][colFENHPM10]))
		data[FID_Link]['hours'][hour]['Result']['FE']['NH']['PM25'].append(float(matriz[i][colFENHPM25]))

		data[FID_Link]['hours'][hour]['Result']['E']['H']['PM10'].append(float(matriz[i][colEHPM10]))
		data[FID_Link]['hours'][hour]['Result']['E']['H']['PM25'].append(float(matriz[i][colEHPM25]))

		data[FID_Link]['hours'][hour]['Result']['E']['NH']['PM10'].append(float(matriz[i][colENHPM10]))
		data[FID_Link]['hours'][hour]['Result']['E']['NH']['PM25'].append(float(matriz[i][colENHPM25]))
	
	#print data
	FID_Link = data.keys()
	for ID in FID_Link: 
		hours = data[ID]['hours'].keys()
		EtonTAnoPM25 = 0
		EtonTAnoPM10 = 0
		for hour in hours:
			cars = data[ID]['hours'][hour]['flows'].keys()
			for car in cars:
				if noun == 'Principal':
					if 'NH_' in car: 
						data[ID]['hours'][hour]['flows'][car][0] = ((data[ID]['hours'][hour]['flows'][car][0]/data[ID]['hours'][hour]['TOTAL']['NHabil'][0])**2) * (PesosV[car[3:]][0]**2)
					else: 				
						data[ID]['hours'][hour]['flows'][car][0] = ((data[ID]['hours'][hour]['flows'][car][0]/data[ID]['hours'][hour]['TOTAL']['Habil'][0])**2) * (PesosV[car][0]**2)


				if noun == 'TM':
					if data[ID]['hours'][hour]['TOTAL']['NHabil'][0] == 0 or data[ID]['hours'][hour]['TOTAL']['Habil'][0] == 0:
						data[ID]['hours'][hour]['flows'][car][0] = 0
					else: 
						if 'NH_' in car: 	
							data[ID]['hours'][hour]['flows'][car][0] = ((data[ID]['hours'][hour]['flows'][car][0]/data[ID]['hours'][hour]['TOTAL']['NHabil'][0])**2) * (PesosVArt[car[3:]][0]**2)
						else: 
							data[ID]['hours'][hour]['flows'][car][0] = ((data[ID]['hours'][hour]['flows'][car][0]/data[ID]['hours'][hour]['TOTAL']['Habil'][0]**2)) * (PesosVArt[car][0]**2)

			
			sumaHabil = sumaNHabil = 0
			for car in cars:
				if 'NH_' in car: 
					sumaNHabil += data[ID]['hours'][hour]['flows'][car][0]
				else: 
					sumaHabil += data[ID]['hours'][hour]['flows'][car][0]
							
			
			#PP
			PPH = data[ID]['hours'][hour]['Result']['PP']['H'][0]
			data[ID]['hours'][hour]['Result']['PP']['H'][0] = math.sqrt(sumaHabil)
			PPNH = data[ID]['hours'][hour]['Result']['PP']['NH'][0]
			data[ID]['hours'][hour]['Result']['PP']['NH'][0] = math.sqrt(sumaNHabil)

			#FAVKT
			FAH = data[ID]['hours'][hour]['Result']['FA']['H'][0]
			data[ID]['hours'][hour]['Result']['FA']['H'][0] = math.sqrt(data[ID]['hours'][hour]['Result']['FA']['H'][0] * FAVKT)
			FANH = data[ID]['hours'][hour]['Result']['FA']['NH'][0]
			data[ID]['hours'][hour]['Result']['FA']['NH'][0] = math.sqrt(data[ID]['hours'][hour]['Result']['FA']['NH'][0] * FAVKT)

			#FE
			#HABIL PM10
			FEHPM10 = data[ID]['hours'][hour]['Result']['FE']['H']['PM10'][0]
			ICS_2 = Emissions[data[ID]['General']['Estation']][0]**2
			OP1 = ((0.91*(PM10K/1000000)*(data[ID]['General']['IDW']**(-0.09))*(PPH**1.02))**2)
			OP2 =  ((data[ID]['hours'][hour]['Result']['PP']['H'][0])**2)*(1.02*(PM10K/1000000)*(PPH**0.02)*(data[ID]['General']['IDW']**0.91))**2
			OP = ICS_2 * OP1 + OP2
			data[ID]['hours'][hour]['Result']['FE']['H']['PM10'][0] = math.sqrt(OP)
			
			#HABIL PM25
			FEHPM25 = data[ID]['hours'][hour]['Result']['FE']['H']['PM25'][0]			
			ICS_2 = Emissions[data[ID]['General']['Estation']][0]**2
			OP1 = ((0.91*(PM25K/1000000)*(data[ID]['General']['IDW']**(-0.09))*(PPH**1.02))**2)
			OP2 =  ((data[ID]['hours'][hour]['Result']['PP']['H'][0])**2)*(1.02*(PM25K/1000000)*(PPH**0.02)*(data[ID]['General']['IDW']**0.91))**2
			OP = ICS_2 * OP1 + OP2
			data[ID]['hours'][hour]['Result']['FE']['H']['PM25'][0] = math.sqrt(OP)
			
			#NO HABIL PM10
			FENHPM10 = data[ID]['hours'][hour]['Result']['FE']['NH']['PM10'][0]
			ICS_2 = Emissions[data[ID]['General']['Estation']][0]**2
			OP1 = ((0.91*(PM10K/1000000)*(data[ID]['General']['IDW']**(-0.09))*(PPNH**1.02))**2)
			OP2 =  ((data[ID]['hours'][hour]['Result']['PP']['NH'][0])**2)*(1.02*(PM10K/1000000)*(PPNH**0.02)*(data[ID]['General']['IDW']**0.91))**2
			OP = ICS_2 * OP1 + OP2
			data[ID]['hours'][hour]['Result']['FE']['NH']['PM10'][0] = math.sqrt(OP)

			#NO HABIL PM25	
			FENHPM25 = data[ID]['hours'][hour]['Result']['FE']['NH']['PM25'][0]		
			ICS_2 = Emissions[data[ID]['General']['Estation']][0]**2
			OP1 = ((0.91*(PM25K/1000000)*(data[ID]['General']['IDW']**(-0.09))*(PPNH**1.02))**2)
			OP2 =  ((data[ID]['hours'][hour]['Result']['PP']['NH'][0])**2)*(1.02*(PM25K/1000000)*(PPNH**0.02)*(data[ID]['General']['IDW']**0.91))**2
			OP = ICS_2 * OP1 + OP2
			data[ID]['hours'][hour]['Result']['FE']['NH']['PM25'][0] = math.sqrt(OP)

			#E
			#Habil EPM10
			OP1 =(data[ID]['hours'][hour]['Result']['E']['H']['PM10'][0]/1000000)**2
			if FEHPM10 == 0:
				OP2 = 0
			else:
				OP2 = (data[ID]['hours'][hour]['Result']['FE']['H']['PM10'][0]**2)/((FEHPM10/1000000)**2)
			if FAH == 0:
				OP3 = 0
			else:
				OP3 = (data[ID]['hours'][hour]['Result']['FA']['H'][0]**2)/(FAH**2)
			OP = OP1 * OP2 + OP3
			data[ID]['hours'][hour]['Result']['E']['H']['PM10'][0] = OP

			#Habil EPM25
			OP1 =(data[ID]['hours'][hour]['Result']['E']['H']['PM25'][0]/1000000)**2
			if FEHPM25 == 0:
				OP2 = 0
			else:
				OP2 = (data[ID]['hours'][hour]['Result']['FE']['H']['PM25'][0]**2)/((FEHPM25/1000000)**2)
			if FAH == 0:
				OP3 = 0
			else:
				OP3 = (data[ID]['hours'][hour]['Result']['FA']['H'][0]**2)/(FAH**2)
			OP = OP1 * OP2 + OP3
			data[ID]['hours'][hour]['Result']['E']['H']['PM25'][0] = OP

			#No Habil EPM10
			OP1 =(data[ID]['hours'][hour]['Result']['E']['NH']['PM10'][0]/1000000)**2
			if FENHPM10 == 0:
				OP2 = 0
			else:
				OP2 = (data[ID]['hours'][hour]['Result']['FE']['NH']['PM10'][0]**2)/((FENHPM10/1000000)**2)
			if FANH == 0:
				OP3 = 0
			else:
				OP3 = (data[ID]['hours'][hour]['Result']['FA']['NH'][0]**2)/(FANH**2)
			OP = OP1 * OP2 + OP3
			data[ID]['hours'][hour]['Result']['E']['NH']['PM10'][0] = OP

			#No Habil EPM25
			OP1 =(data[ID]['hours'][hour]['Result']['E']['NH']['PM25'][0]/1000000)**2
			if FENHPM25 == 0:
				OP2 = 0
			else:
				OP2 = (data[ID]['hours'][hour]['Result']['FE']['NH']['PM25'][0]**2)/((FENHPM25/1000000)**2)
			if FANH == 0:
				OP3 = 0
			else:
				OP3 = (data[ID]['hours'][hour]['Result']['FA']['NH'][0]**2)/(FANH**2)
			OP = OP1 * OP2 + OP3
			data[ID]['hours'][hour]['Result']['E']['NH']['PM25'][0] = OP

	UEHPM25 = 0
	UEHPM10 = 0
	UENHPM25 = 0
	UENHPM10 = 0
	FID_Link = data.keys()
	for ID in FID_Link:
		#print ID
		hours = data[ID]['hours'].keys()
		for hour in hours:
			#print hour
			#print  data[ID]['hours'][hour]['Result']['E']['NH']['PM25'][0]
			UENHPM25 += data[ID]['hours'][hour]['Result']['E']['NH']['PM25'][0]
			UENHPM10 += data[ID]['hours'][hour]['Result']['E']['NH']['PM10'][0]
			UEHPM25 += data[ID]['hours'][hour]['Result']['E']['H']['PM25'][0]
			UEHPM10 += data[ID]['hours'][hour]['Result']['E']['H']['PM10'][0]


	UENHPM25 = math.sqrt(UENHPM25)*DNH
	UENHPM10 = math.sqrt(UENHPM10)*DNH
	UEHPM25 = math.sqrt(UEHPM25)*DH
	UEHPM10 = math.sqrt(UEHPM10)*DH

	#print 'UENHPM25', UENHPM25
	#print 'UENHPM10', UENHPM10
	#print 'UEHPM25', UEHPM25
	#print 'UEHPM10', UEHPM10
	EPM25 = math.sqrt((UEHPM25**2) + (UENHPM25**2))
	EPM10 = math.sqrt((UEHPM10**2) + (UENHPM10**2))
	#print 'EPM25', round(EPM25, 3)
	#print 'EPM10', round(EPM10, 3)

	writefull(EPM25, EPM10, noun + '_Uncertain')	