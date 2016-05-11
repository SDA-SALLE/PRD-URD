# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import os

def clear(folder):
	for root, dirs, files in os.walk(folder, topdown=False):
	   for name in files:
	       os.remove(os.path.join(root, name))