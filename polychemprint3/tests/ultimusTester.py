import serial
import time
from polychemprint3.tools.ultimusExtruder import ultimusExtruder


Branch1 = False

if Branch1:
    ### INSTANTIATION TEST
    ext = ultimusExtruder()

    ### Display Instantiated Attributes
    print("01 ATTRIBUTES AT INSTANTIATION ####")
    print(ext.__dict__)
    print("")
    ### Serial Start Test
    print("02 Activation Test ####")
    ext.activate()
    print("")

    print("03 Set Value Test ####")
    ext.setValue("0500")
    print("")

    ### Serial Close Test
    print("00 Deactivation Test ####")
    ext.deactivate()

else:
    ### INSTANTIATION TEST
    ext = ultimusExtruder()

    ### Display Instantiated Attributes
    print("01 ATTRIBUTES AT INSTANTIATION ####")
    print(ext.__dict__)
    print("")
    ### Serial Start Test
    print("02 Activation Test ####")
    ext.activate()
    print("")
    ### Attempt to Write Data
    print("02 Activation Test ####")
    ext.__writeSerial__(chr(0x05))
    print(ext.readTime(0.1))
    ext.__writeSerial__(ext.pack("DI"))
    print(ext.readTime(0.1))
    ext.__writeSerial__(chr(0x06))
    print(ext.readTime(0.1))

    print("")