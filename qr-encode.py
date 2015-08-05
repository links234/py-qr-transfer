#!/usr/bin/python

import sys, getopt
import qrcode
import six

import numpy as np

from PIL import Image

def MakeQR(inputfile, outputfile):
	with open(inputfile, 'rb') as ifile:
		data = ifile.read()

		qrData = qrcode.util.QRData(data, qrcode.util.MODE_8BIT_BYTE, False)

		qr = qrcode.QRCode(
			error_correction=qrcode.constants.ERROR_CORRECT_H
		)
		qr.add_data(qrData)
		qr.make(fit=True)

		array=[]

		#with open(outputfile, 'w') as out:
		modcount = qr.modules_count

		def get_module(x, y):
			if min(x, y) < 0 or max(x, y) >= modcount:
				return 0
			return qr.modules[x][y]

		w = modcount+2*qr.border
		h = modcount+2*qr.border
		imgData = np.zeros( (w,h,3), dtype=np.uint8)

		color = []
		color.append( [255, 255, 255] )
		color.append( [  0,   0,   0] )

		for r in range(-qr.border, modcount+qr.border):
			for c in range(-qr.border, modcount+qr.border):
				imgData[r+qr.border, c+qr.border] = color[get_module(r, c)]

		img = Image.fromarray(imgData, 'RGB')
		img.save(outputfile)

def main(argv):
	inputfile = ''
	outputfile = ''

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('qr-encode.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('qr-encode.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	MakeQR(inputfile, outputfile)

if __name__ == "__main__":
	main(sys.argv[1:])
