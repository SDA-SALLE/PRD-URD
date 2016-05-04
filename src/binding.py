#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python

import sys
sys.path.append('core')
from excelmatriz import *
from wcsv import *
import json
import os


def binding(flows, links, folder):
	
	data = {}
	Mdata = convertXLSCSV(links)
	MFlows = convertCSVMatriz(flows)

	headData = Mdata[0,:] 
	headFlows = MFlows[0,:]
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK' or name == 'FID_Link': 
			colLinkID = index
		index += 1

	index = 0

	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, Mdata.shape[0]):

		FID = int(float(Mdata[y][colLinkID]))

		if data.get(FID) is None: 
			data[FID] = {}

		entrygrid =  data[FID]

		if entrygrid.get('link') is None:
			entrygrid['link'] = {}
		
		if entrygrid.get('flows') is None:
			entrygrid['flows'] = {}

		entryname = entrygrid['link']

		for x in range(1, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = int(MFlows[y][colhour])

		FID = data.keys()

		for ID in FID:
			
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))
			if IDdataEstation == IDflowsEstation:
				typ = MFlows[y][colType]
				
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]


				for x in range(colhour+1, MFlows.shape[1]):
				 	headFlows = MFlows[0][x]
				 	if entryVehicle.get(headFlows) is None:
				 		entryVehicle[headFlows] = []
				
				 	entryVehicle[headFlows].append(MFlows[y][x])

	writebinding(folder, data)

def bindingsecondary(flows, links):

	data = {}
	Mdata = convertXLSCSV(links)
	MFlows = convertCSVMatriz(flows)
	
	Intermedia = 0.37
	Local = 0.22
	Activity = ['L', 'C', 'ESP', 'M']
	ResidencialAct = 0.22
	NotActivity = [ 'B', 'C2P', 'BT', 'AL', 'AT', 'BA', 'INT', 'C2G', 'C3-C4', 'C5', '>C5']
	ResidencialNotAct = 0


	headData = Mdata[0,:] 
	headFlows = MFlows[0,:]
	#print headData
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK' or name == 'FID_Link': 
			colLinkID = index
		index += 1

	index = 0

	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, Mdata.shape[0]):

		FID = int(float(Mdata[y][colLinkID]))

		if data.get(FID) is None: 
			data[FID] = {}

		entrygrid =  data[FID]

		if entrygrid.get('link') is None:
			entrygrid['link'] = {}
		
		if entrygrid.get('flows') is None:
			entrygrid['flows'] = {}

		entryname = entrygrid['link']

		for x in range(1, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = int(MFlows[y][colhour])

		FID = data.keys()

		for ID in FID:
			
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))

			if IDdataEstation == IDflowsEstation:
				typ = MFlows[y][colType]
				
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]


				for x in range(colhour+1, MFlows.shape[1]):
				 	headFlows = MFlows[0][x]
				 	if entryVehicle.get(headFlows) is None:
				 		entryVehicle[headFlows] = []
				
				 	entryVehicle[headFlows].append(MFlows[y][x])

	FID = data.keys()
	
	for ID in FID:
		clasifi = data[ID]['link']['CLASIFI_SU'][0]
		#print clasifi
		types = data[ID]['flows'].keys()
		for typ in types:
			hour = data[ID]['flows'][typ].keys()
			for hr in hour:
				namevehicle = sorted(data[ID]['flows'][typ][hr].keys())
				
				if clasifi == 'Local':
					for Vehicle in namevehicle: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * Local

				if clasifi == 'Intermedia':
					for Vehicle in namevehicle: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * Intermedia 

				if clasifi == 'Residencial':

					for Vehicle in Activity: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * ResidencialAct

					for Vehicle in NotActivity:
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * ResidencialNotAct


	folder = os.path.join('..', 'data', 'VP', 'Secundarias', '')
	writebinding(folder, data)