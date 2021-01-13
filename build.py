import os
import sys

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def getfiles(path):
	absolute_path = os.path.join(THIS_FOLDER, path)
	file_list = sorted(os.listdir(absolute_path),  key=str.casefold)
	cleansed  = []
	for file in file_list:
		if file != '.DS_Store':
			cleansed.append(file)
	return cleansed

def main(path):

	absolute_path = os.path.join(THIS_FOLDER, path)
	files = getfiles(absolute_path)

	final = bytearray()

	for file in files:
		with open(absolute_path + '/' + file, 'rb') as f:
			data = f.read()
			final.extend(data)
	
	with open('built.bin', 'wb') as w:
		w.write(final)

path = sys.argv[1]
main(path)
print('finished')