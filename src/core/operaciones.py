#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python

#Realiza la suma de los flujos vehiculares.
def Flujos (FlujosVehiculares):
	flujos = 0
	tamano = len(FlujosVehiculares)
	for i in range(tamano):
		flujos += FlujosVehiculares[i]

	return flujos

#Realiza el Promedio ponderado de los Vehiculos por su peso.
def PP (FV, PesoVehicle, Total, namesvehicles):
	tamano = len(FV)
	mul = 0
	for i in range(tamano):
		name = namesvehicles[i]
		pvehicle = PesoVehicle[name][0]
		mul += FV[i] * pvehicle
 	PP = mul/Total
 	
	return PP

def FEPM (K, CS, PP, SL, W):
	cs_pow = pow (CS, SL)
	pp_pow = pow (PP, W)
	FE = K * (cs_pow) * (pp_pow)
	return FE

	
def FactorActividad (TamGri, FV):
	FA = TamGri * FV
	FA = FA/1000
	return FA

def Emission (FE, FA):
	E = FE * FA
	return E

def EmisionGrDia (FE, FA):
	EGrD = FE * FA
	return EGrD

def EmisionGrH (EGrD):
	EGrH = EGrD/24
	return EGrH

def FAVKT(lg, flujo):
	FA = (lg/1000)*flujo
	return FA

def FEVKTP(kgpm, s, a, v, d, pmg):
	FE1 = kgpm*(pow((s/12), a))
	FE2 = pow((v/30), d)
	FE = (FE1 * FE2) - pmg
	return FE

def FEVKTI(kgpm, s, a, v, d, pmg):
	FE1 = kgpm*(pow((s/12), a))
	FE2 = pow((v/3), d)
	FE = (FE1 * FE2)
	return FE

def ETY(FE, dh):
	E = (FE*dh)/1000000
	return E
