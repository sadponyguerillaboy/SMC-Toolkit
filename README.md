# SMC-Toolkit
Toolkit written in Python for working with Apple SMC Payloads. It generates complete firmware files from payload components. Intended for 2013+ systems that use smc updates divided into four files (flasher_base, flasher_update, epm, Mac-BoardID). It can also generate payloads, patch the MACA call and dump patched SMC's via MACR.

__Requirements:__
```
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

`reconstruct.py` will strip payload chunks by address block and store them individually in a folder entitled `extracted` in the same location as `reconstruct.py`. It will then take those chunks and build the firmware file and save it in `extracted/firmware`. Works with both older style payloads using 20 byte headers and newer 32 byte headers with 256 RSA signature. Additionally, `reconstruct.py` can also be used on olderstyle single file payloads (example 2012) to generate chunks. The terminal will state checksum errors, but this can be ignored as pre-mid 2013 systems do not have embedded adler32 checksums.


__Createpayload.py Usage:__
```
createpayload.py <complete firmware file> <firmware version>
```

__Createpayload.py Example:__
```
createpayload.py firmware.bin 2.36f7
```

`createpayload.py` generates 3 of the 4 older style payload components from a complete firmware file. It will create `flasher_base.smc, flasher_update.smc and Mac-BoardID.smc` and store them in a folder entitled `payload`. Currently epm files are on the TODO list. For now just use the original epm file. `createpayload.py` is only currently able to generate the older style payloads that use the 20 byte checksum header and security bytes. Deciphering the 256 RSA signature on newer payloads is also on the TODO list.


__Macapatcher.py Usage:__
```
macapatcher.py -p <path to chunks>
macapatcher.py -f <path to file>
```

__Macapatcher.py Example:__
```
macapatcher.py -p extracted/2012MBP13_smc
macapatcher.py -f extracted/firmware/firmware.bin
```
`macapatcher.py` searches either a folder containing the chunks created by `reconstruct.py` or a single binary for the MACA patch location and then patches the chunk or file. Recommended usage is to patch a chunk using the `p` flag, then rebuild your payload with `custompayload.py`. All credit for the patch goes to [@microwave89-hv](https://github.com/microwave89-hv). SMCUtil is required to flash the patched payload (not provided here and don't ask). This patch has been tested on 2012 - 2017 systems using the LM4F smc chips. Note: Be aware that attempting to flash your patched payload may result in irrevocable damage to your system and is not recommened for inexperienced users.


__dumpMACR.py Example:__
```
dumpMACR.py
```
`dumpMACR.py` will dump a patched SMC's complete firmware using `smc-fuzzer`. You must download [smc-fuzzer](https://github.com/theopolis/smc-fuzzer) and compile the binary. Make sure the binary is named `smc` and placed into the same location as `dumpMACR.py`. Note that the resulting SMC firmware will be your patched version, not an original. You will need to revert the patched area and if applicable, the final adler32 checksum present in newer firmwares back to their original state to obtain a complete original rom. Patch info in `macapatcher.py`


__Extra Tools:__
```
adler32.py <path to file>
```
`adler32.py` is a simple script to calculate the adler32 checksum of a file.

```
build.py <path>
```
`build.py` builds / assembles the file chunks created by `reconstruct.py` in the specified path. Example, if you specificy the `<path>` of `extraxcted/Mac-63001698E7A34814_smc`, it will only assemble those files into a binary.

```
custompayload.py <path> <version>
```
`custompayload.py` builds a payload out of file chunks created by `reconstruct.py` in the specified path. This allows for targeted payloads after custom patching of chunks etc. Make sure you include a vectors table file (`00_00000000.bin`) created by `reconstruct.py` in the folder you intend to build. Currently, `custompayload.py` does not perform adler32 checksum recalculations for newer styled payloads, They will need to be manually recalculated.


__TODO:__
- decipher epm file generation
- decipher RSA 256 signature on newer payloads
- custompayload.py needs to have adler32 checksum recalculation functions implemented for newer firmwares
