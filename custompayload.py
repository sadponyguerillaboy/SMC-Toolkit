import os
import sys
from itertools import islice

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def rs232_checksum(the_bytes):
	return b'%02X' % (sum(the_bytes) & 0xFF)

def chunked(iterable, n):
	it = iter(iterable)
	values = bytes(islice(it, n))
	while values:
		yield values
		values = bytes(islice(it, n))

def getfiles(path):
	absolute_path = os.path.join(THIS_FOLDER, path)
	file_list = sorted(os.listdir(absolute_path),  key=str.casefold)
	cleansed  = []
	for file in file_list:
		if file != '.DS_Store':
			cleansed.append(file)
	return cleansed

def create_header_payload(checksum, prefix):
	final_header_array = []

	# calculate header padding size
	difference = 20 - int(len(checksum)/2) - 1 #need to subtract extra because byte is 2 characters
	header_padding_array = []
	while difference >= 0:
		header_padding_array.append('00')
		difference -= 1

	final_padding = ''.join(header_padding_array)
	final_header_hash = str(checksum).replace("b'","").replace("'","") + final_padding
	final_header_array.append(prefix + ':' + str(int(len(final_header_hash)/2)) + ':' + final_header_hash + ':' + str(checksum).replace("b'","").replace("'",""))
	return final_header_array

def create_payload(chunk, address):#, start):
	# Initialize Variables
	header_array = []
	line_counter = 0	
	chunk_array = []

	for block_bytes in chunked(chunk, n=64):
		if line_counter == 0:
			chunk_array.append('D:' + address.upper() + ':' + str(len(block_bytes)) + ':' + block_bytes.hex().upper() + ':' + str(rs232_checksum(block_bytes)).replace("b'","").replace("'",""))
			header_array.append(str(rs232_checksum(block_bytes)).replace("b'","").replace("'",""))
			line_counter += 1

		elif line_counter != 0:
			chunk_array.append('+         :' + str(len(block_bytes)) + ':' + block_bytes.hex().upper() + ':' + str(rs232_checksum(block_bytes)).replace("b'","").replace("'",""))
			header_array.append(str(rs232_checksum(block_bytes)).replace("b'","").replace("'",""))
			line_counter += 1
	
	return header_array, chunk_array

def create_joined(to_join):
		final_array = []
		for array in to_join:
			for item in array:
				final_array.append(item)

		final_array = '\n'.join(final_array)
		return final_array

def main(path, version):

	absolute_path = os.path.join(THIS_FOLDER, path)
	files = getfiles(absolute_path)

	header_array = []
	security_array = bytearray()
	payload_array = []

	for file in files:
		address = file[3:11]
		with open(absolute_path + '/' + file, 'rb') as f:
			data = f.read()
			header_data, payload_data = create_payload(data, address)
			payload_array.append(payload_data)
			header_data_bytes = bytearray.fromhex(''.join(header_data))
			checksum = rs232_checksum(header_data_bytes)
			header_array.append(create_header_payload(checksum, 'H'))
			security_array.extend(checksum)

	security_payload = rs232_checksum(security_array)
	header_array.append(create_header_payload(security_payload, 'S'))
	payload_joined = create_joined(payload_array)
	header_joined = create_joined(header_array)
	
	final_payload = '# Version: ' + version + '\n' + header_joined + '\n' + payload_joined
	
	with open('custom_payload.smc', 'w') as w:
		w.write(final_payload)

path = sys.argv[1]
version = sys.argv[2]
main(path, version)
print('finished')