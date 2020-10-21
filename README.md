# SMC-Toolkit
Toolkit written in Python for working with Apple SMC Payloads. It generates complete firmware files from payload components. Intended for 2013+ systems that use smc updates divided into four files (flasher_base, flasher_update, epm, Mac-BoardID). It can also generate update payloads from a complete firmware file.

__Requirements:__
```
itertools
numpy
termcolor
```

__Reconstruct.py Usage:__
```
reconstruct.py <base path to firmware payloads>
```

__Reconstruct.py Example:__
```
reconstruct.py SMCPayloads/10.15.6/Mac-B4831CEBD52A0C4C
```

`reconstruct.py` will strip payload chunks by address block and store them individually in a folder entitled `extracted` in the same location as `reconstruct.py`. It will then take those chunks and build the firmware file and save it in `extracted/firmware`. Works with both older style payloads using 20 byte headers and newer 32 byte headers with 256 RSA signature.


__Createpayload.py Usage:__
```
createpayload.py <complete firmware file> <firmware version>
```

__Createpayload.py Example:__
```
createpayload.py firmware.bin 2.36f7
```

`createpayload.py` generates 3 of the 4 older style payload components from a complete firmware file. It will create `flasher_base.smc, flasher_update.smc and Mac-BoardID.smc` and store them in a folder entitled `payload`. Currently epm files are on the TODO list. For now just use the original epm file. `createpayload.py` is only currently able to generate the older style payloads that use the 20 byte checksum header and security bytes. Deciphering the 256 RSA signature on newer payloads is also on the TODO list.

__TODO:__
- decipher epm file generation
- decipher RSA 256 signature on newer payloads
