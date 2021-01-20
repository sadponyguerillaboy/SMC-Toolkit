import os
import sys

search = b'\x4B\x1B\x78\x01\x2B\x14\xD1\xA1\xF1\x00\x51\xB1\xF5\x00\x4F\x0F\xD2\x00\x21'
patch = b'\x4B\x1B\x78\x01\x2B\x14\xD1\xA1\xF1\x00\x51\xB1\xF5\x00\x4F\x00\xBF\x00\x21'

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def getfiles(path):
	absolute_path = os.path.join(THIS_FOLDER, path)
	file_list = sorted(os.listdir(absolute_path),  key=str.casefold)
	cleansed  = []
	for file in file_list:
		if file != '.DS_Store':
			cleansed.append(file)
	return cleansed

def main(path, option):

    absolute_path = os.path.join(THIS_FOLDER, path)

    if option == '-p':
        files = getfiles(absolute_path)
        for file in files:
            with open(absolute_path + '/' + file, 'rb') as f:
                data = f.read()
            found = data.find(search)
            if found != -1:
                print('Found in Chunk:', file, 'at offset:', found)
                with open(absolute_path + '/' + file + '_patched.bin', 'wb') as w:
                    w.write(data)
                    w.close()
                with open(absolute_path + '/' + file + '_patched.bin', 'rb+') as w:
                    w.seek(found)
                    w.write(patch)
    
    if option == '-f':
        with open(path, 'rb') as f:
            data = f.read()
        found = data.find(search)
        if found != -1:
            print('Found in File:', absolute_path, 'at offset:', found)
            with open(absolute_path + '_patched.bin', 'wb') as w:
                w.write(data)
                w.close()
            with open(absolute_path + '_patched.bin', 'rb+') as w:
                w.seek(found)
                w.write(patch)

option = sys.argv[1]
path = sys.argv[2]
main(path, option)
print('finished')


#Notes:
###########################################
#Original MACA:
#4B1B7801 2B14D1A1 F10051B1 F5004F0F D20021
#Patch: 00BF
#4B1B7801 2B14D1A1 F10051B1 F5004F00 BF0021
