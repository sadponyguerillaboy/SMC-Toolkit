import numpy as np
import sys
import zlib

def main(file):
	with open(file, 'rb') as f:
		content = f.read()
		reversed_content = np.flip(np.frombuffer(bytearray(content), dtype=np.uint8, count=-1, offset=0),0).tobytes()
		print('adler32: ', hex(zlib.adler32(content) & 0xffffffff))
		print('adler32 reversed: ', hex(zlib.adler32(reversed_content) & 0xffffffff))
		f.close()

file = sys.argv[1]
main(file)