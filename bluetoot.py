import winreg
import itertools
import binascii
import array

def hexlify(_bytes, swap=True):
    a = array.array('b', _bytes)
    a.byteswap()
    return binascii.hexlify(a.tobytes()).decode('utf-8')

MAC = '442a60ef7939'
reg_keys = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                          'SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys')
mac_addr = None
for i in itertools.count():
    try:
        device_addr = winreg.EnumKey(reg_keys, i)
        sub_key = winreg.OpenKey(reg_keys, device_addr)
        for i in itertools.count():
            try:
                mac_addr, key, kind = winreg.EnumValue(sub_key, i)
                if mac_addr == MAC:
                    print('Key Found: %s, on device: %s' %
                          (hexlify(key), device_addr))
            except OSError:
                break
    except OSError:
        break

if not mac_addr:
    print('No bluetooth device with given mac address found. Is it paired?')

