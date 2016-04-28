#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
import csv
import os
from excelmatriz import *

def wcsv(data, noun):

	folder = os.path.join('..','data','out','EmissionGrid', 'VP', '')

	keys = data.keys()

	Types = data[keys[0]]['Emissions'].keys ()
	for Type in Types:
		csvsalida = open(folder + noun + "_" + Type + ".csv", 'w')
		salida = csv.writer(csvsalida, delimiter=',')#, quoting=csv.QUOTE_ALL
		argumentos = ["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"]
		salida.writerow(argumentos)

		for key in keys:
			csvsalida.write(str(data[key]['GENERAL']['ROW'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[key]['GENERAL']['COL'][0]))
			csvsalida.write(',')
			csvsalida.write(data[key]['GENERAL']['LAT'][0])
			csvsalida.write(',')
			csvsalida.write(data[key]['GENERAL']['LON'][0])
			csvsalida.write(',')
			if Type == 'EHPM10' or Type == 'ENHPM10':
				csvsalida.write('PM10')
			elif Type == 'EHPM25' or Type == 'ENHPM25':
				csvsalida.write('PM25')	
			csvsalida.write(',')
			csvsalida.write('g/h')
			csvsalida.write(',')
			hours = data[key]['Emissions'][Type].keys()
			for hour in hours:
				csvsalida.write(str(data[key]['Emissions'][Type][hour][0]))
				csvsalida.write(',')
			csvsalida.write(str(data[key]['Emissions'][Type][hours[0]][0]))


			csvsalida.write('\n')


	csvsalida.close()

def writematriz(matriz, folder):

	csvsalida = open(folder + ".csv", 'w')
	#print csvsalida
	#print matriz.shape[0]
	salida = csv.writer(csvsalida, delimiter=',')#, quoting=csv.QUOTE_ALL

	for x in range(0, matriz.shape[0]):
		salida.writerow(matriz[x])

	csvsalida.close()

def writesum(data):
	folder = os.path.join('..', 'data', 'flows', 'EmissionDay','')
	csvsalida = open(folder + "sumcol.csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['Estacion', 'IDEstacion', 'IDNodo', '>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL', 'NH_>C5', 'NH_AL', 'NH_AT', 'NH_B', 'NH_BA', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_ESP', 'NH_INT', 'NH_L', 'NH_M', 'NH_TOTAL'])

	IDEstation = data.keys()
	
	for ID in IDEstation: 

		flujos = sorted(data[ID]['HABIL'].keys())
		#print flujos

		for veh in range(0, 3):
			csvsalida.write(data[ID]['GENERAL'][veh])
			csvsalida.write(",")
		
		for vehicles in flujos:
				csvsalida.write(str(data[ID]['HABIL'][vehicles]))
				csvsalida.write(",")

		for vehicles in flujos:
				csvsalida.write(str(data[ID]['NOHAB'][vehicles]))
				csvsalida.write(",")
		csvsalida.write('\n')
	
	csvsalida.close()

def writebinding(folder, data):

	csvsalida = open(folder + "brinding.csv", 'w')
	namevehiclefull = ['hora','>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL', 'NH_>C5', 'NH_AL', 'NH_AT', 'NH_B', 'NH_BA', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_ESP', 'NH_INT', 'NH_L', 'NH_M', 'NH_TOTAL']
	
	FID = data.keys()

	cont = 0
	
	for ID in FID:
		nameslinks = data[ID]['link'].keys()
		namevehicle = sorted(data[ID]['flows']['HABIL'][0].keys())
		hours = data[ID]['flows']['HABIL'].keys()

		#print hours

		if cont == 0:
			for name in nameslinks:
				csvsalida.write(name)
				csvsalida.write(',')

			rest = 0
			for name in namevehiclefull:
				if rest == 0:
					csvsalida.write(name)
					rest += 1
				else: 
					csvsalida.write(',')
					csvsalida.write(name)
			csvsalida.write('\n')

			cont += 1
	 	

		for hour in hours:

		 	for name in nameslinks:
		 		csvsalida.write(data[ID]['link'][name][0])
		 		csvsalida.write(',')
		 	csvsalida.write(str(hour))
		 	csvsalida.write(',')

		 	for vehicle in namevehicle:
		 		csvsalida.write (str(data[ID]['flows']['HABIL'][hour][vehicle][0]))
		 		csvsalida.write(',')
		 	cont = 0
		 	for vehicle in namevehicle:
		 		if cont == 0:
		 			csvsalida.write (str(data[ID]['flows']['HABIL'][hour][vehicle][0]))
		 			cont += 1
		 		else:
		 			csvsalida.write(',')
		 			csvsalida.write (str(data[ID]['flows']['NOHAB'][hour][vehicle][0]))


		 	csvsalida.write('\n')

def writeemsions(data, name, identy): 

	if identy == 1:

		folder = os.path.join("..", "data", "out", 'EmissionDay','')
		csvsalida = open(folder + name + ".csv", 'w')
		salida = csv.writer(csvsalida, delimiter=',')
		if 'IDW' in name or 'Heterogeneous' in name or 'Homogeneous' in name: 
			salida.writerow(["FID_Link","FID_Grilla", "IDEstacion", "IDNodo", "COL", "ROW", "LAT", "LON", "EHPM10", "EHPM25", "ENHPM10", "ENHPM25"])
		elif 'CKDH' in name: 
			salida.writerow(["FID_Link","FID_Grilla", "IDEstacion", "IDNodo", "COL", "ROW", "LAT", "LON", "EHPM10", "EHPM25"])
		elif 'CKDNH' in name: 
			salida.writerow(["FID_Link","FID_Grilla", "IDEstacion", "IDNodo", "COL", "ROW", "LAT", "LON", "ENHPM10", "ENHPM25"])


		FID_Link = data.keys()
		
		for FID in FID_Link: 
			identy = int(float(FID))
			csvsalida.write(str(identy))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['FID_Grilla'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['IDEstation'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['IDNodo'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['COL'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['ROW'][0]))
			csvsalida.write(',')
			csvsalida.write(data[FID]['GENERAL']['LAT'][0])
			csvsalida.write(',')
			csvsalida.write(data[FID]['GENERAL']['LON'][0])
			csvsalida.write(',')
			if 'IDW' in name or 'Heterogeneous' in name or 'Homogeneous' in name: 
				csvsalida.write(str(data[FID]['EMISION']["EHPM10"][0]))
				csvsalida.write(',')
				csvsalida.write(str(data[FID]['EMISION']["EHPM25"][0]))
				csvsalida.write(',')
				csvsalida.write(str(data[FID]['EMISION']["ENHPM10"][0]))
				csvsalida.write(',')
				csvsalida.write(str(data[FID]['EMISION']["ENHPM25"][0]))
			elif 'CKDH' in name: 
				csvsalida.write(str(data[FID]['EMISION']["EHPM10"][0]))
				csvsalida.write(',')
				csvsalida.write(str(data[FID]['EMISION']["EHPM25"][0]))
			elif 'CKDNH' in name:
				csvsalida.write(str(data[FID]['EMISION']["ENHPM10"][0]))
				csvsalida.write(',')
				csvsalida.write(str(data[FID]['EMISION']["ENHPM25"][0]))

			csvsalida.write('\n')
		csvsalida.close()	

	elif identy == 2: 

		folder = os.path.join("..", "data", "out", 'EmissionYear','')
		csvsalida = open(folder + name + ".csv", 'w')
		salida = csv.writer(csvsalida, delimiter=',')

		salida.writerow(['FID_Grilla', 'IDEstacion', 'IDNodo', 'COL', 'ROW', 'LAT', 'LON', 'ETPM10', 'ETPM25'])

		FID_Link = data.keys()
		
		for FID in FID_Link: 
			identy = int(float(FID))
			csvsalida.write(str(identy))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['IDEstation'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['IDNodo'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['COL'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['GENERAL']['ROW'][0]))
			csvsalida.write(',')
			csvsalida.write(data[FID]['GENERAL']['LAT'][0])
			csvsalida.write(',')
			csvsalida.write(data[FID]['GENERAL']['LON'][0])
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['EMISION']['ETPM10'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[FID]['EMISION']['ETPM25'][0]))
			csvsalida.write('\n')
		csvsalida.close()	

def writefull(fullPM25, fullPM10, noun): 

	folder = os.path.join('..', 'data', 'out', 'TotalEmissions', '')
	csvsalida = open(folder + noun + "_E(TYear).csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['PM25', 'PM10'])

	csvsalida.write(str(fullPM25))
	csvsalida.write(',')
	csvsalida.write(str(fullPM10))
	csvsalida.close()

def writefullfull(noun):

	folder = os.path.join('..','data', 'out', 'TotalEmissions', '')
	if 'IDW' in noun or 'Homogeneous' in noun or 'Heterogeneous' in noun:
		archive1 = folder + noun + '_Uncertain_E(TYear).csv'
	if 'CKDH' in noun:
		archive1 = folder + noun + '_Uncertain_E(TYear).csv'
	if 'CKDNH' in noun:
		archive1 = folder + noun + '_Uncertain_E(TYear).csv'
	
	archive2 = folder + noun + '_E(TYear).csv'

	foldersave = os.path.join('..','data','out', 'TotalEmissions', 'TotalUncertainEmission','')
	csvsalida = open(foldersave + noun + "_EUncertain(TYear).csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	Emissions = convertCSVMatriz(archive2)
	Uncertain = convertCSVMatriz(archive1)

	salida.writerow(['Tipo','Emision Ton/Year', 'Incertidumbre', 'Porcentaje Incertidumbre'])
	
	csvsalida.write('PM25')
	csvsalida.write(',')
	csvsalida.write(Emissions[1][0])
	csvsalida.write(',')
	csvsalida.write(Uncertain[1][0])
	csvsalida.write(',')
	operation = round(float(Uncertain[1][0])/float(Emissions[1][0])*100, 4)
	csvsalida.write(str(operation))
	csvsalida.write('\n')

	csvsalida.write('PM10')
	csvsalida.write(',')
	csvsalida.write(Emissions[1][1])
	csvsalida.write(',')
	csvsalida.write(Uncertain[1][1])
	csvsalida.write(',')
	operation = round(float(Uncertain[1][1])/float(Emissions[1][1])*100, 4)
	csvsalida.write(str(operation))

	csvsalida.close()

def writevnp(data, noun):

	folder = os.path.join('..', 'data', 'out', 'EmissionGrid', 'VNP', '')
	argumentos = ["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"]
		
	for POLNAME in ['PM25','PM10']:
		csvsalida = open(folder + POLNAME + '_' + noun + '.csv', 'w')
		salida = csv.writer(csvsalida, delimiter=',')
		salida.writerow(argumentos)
		keys = data.keys()
		for key in keys: 
			csvsalida.write(str(data[key]['GENERAL']['ROW'][0]))
			csvsalida.write(',')
			csvsalida.write(str(data[key]['GENERAL']['COL'][0]))
			csvsalida.write(',')
			csvsalida.write(data[key]['GENERAL']['LAT'][0])
			csvsalida.write(',')
			csvsalida.write(data[key]['GENERAL']['LON'][0])
			csvsalida.write(',')
			csvsalida.write(POLNAME)
			csvsalida.write(',')
			csvsalida.write('g/h')
			csvsalida.write(',')
			hours = data[key]['hours'][POLNAME].keys()
			for hour in hours:
				if hour == 24: 
					csvsalida.write(str(data[key]['hours'][POLNAME][hour][0]))
				else:	
					csvsalida.write(str(data[key]['hours'][POLNAME][hour][0]))
					csvsalida.write(',')
			
			csvsalida.write('\n')
		csvsalida.close()

def PMC(data, noun, folder):

	folder = os.path.join(folder, 'PMC', '')
	csvsalida = open(folder + noun + '.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	keys = data.keys()

	salida.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])
	for key in keys: 
		csvsalida.write(str(int(data[key]['GENERAL']['ROW'][0])))
		csvsalida.write(',')
		csvsalida.write(str(int(data[key]['GENERAL']['COL'][0])))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['LAT'][0]))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['LON'][0]))
		csvsalida.write(',')
		csvsalida.write('PMC')
		csvsalida.write(',')
		csvsalida.write('g/s')
		hours = data[key]['hours'].keys()
		for hour in hours:
			csvsalida.write(',')
			csvsalida.write(str(data[key]['hours'][hour][0]))
		csvsalida.write('\n')
			
	csvsalida.close()