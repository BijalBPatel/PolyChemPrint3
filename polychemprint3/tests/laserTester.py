from polychemprint3.tools import *
from polychemprint3.tools.omnicureS2000 import omnicureS2000
import crcmod.predefined

#omni = omnicureS2000()

def crc8Calc(cmdString):


    # Notes for figuring out this part
        # Omnicure manual has example C++ code for manual calculation
        # Instead, pulled two examples "CONN" -> 0x18, "READY" -> 0x0A
        # Use online calculator to figure out which CRC-8 Algorithm they implemented
        # https: // crccalc.com /
        # CRC-8/MAXIM gives correct values
        # Googled "CRC Python Packages" until I found one that implements CRC-8 MAXIM
        # http://crcmod.sourceforge.net/crcmod.predefined.html

    encodedString = cmdString.encode()
    print("Input String: " + cmdString)
    print("Encoded String: ", end='')
    print(encodedString)

    crc8_func = crcmod.predefined.mkCrcFun('crc-8-maxim')
    return hex(crc8_func(encodedString))


print("Test Start")
print(crc8Calc("READY"))

print("Test End")
#print(las.activate())
#print(las.deactivate())