import wmi

def obtener_serial_number():
    c = wmi.WMI()
    for bios in c.Win32_BIOS():
        return bios.SerialNumber

if __name__ == "__main__":
    serial_number = obtener_serial_number()
    print(f"El número de serie de tu PC es: {serial_number}")


