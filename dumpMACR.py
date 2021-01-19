import subprocess

spell = 'SMC The place to be, definitely!'
subprocess.run(['sudo', './smc', '-c', spell])

rounds = 8192
count = 0
full_dump = bytearray()

while count < rounds:
	dump = subprocess.run(['./smc', '-k', 'MACR', '-r'], stdout=subprocess.PIPE, text=True)
	line = dump.stdout.splitlines()
	for item in line:
		snippet = item[23:118].replace(' ', '')
		converted = bytes.fromhex(snippet)
		full_dump.extend(converted)
	count += 1

with open('MACR_dump.bin', 'wb') as w:
	w.write(full_dump)

# Notes:
# 256kb = 262144 bytes
# MACR reads out 32 bytes per read
# 262144 / 32 = 8192
# subprocess smc-fuzzer stdout text ouput splice locations: 23 & 118