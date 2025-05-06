import platform
import subprocess
import tkinter as tk
from tkinter import messagebox
import wmi

def get_serial_number():
    """Obtiene el número de serie de la computadora."""
    try:
        if platform.system() == "Windows":
            c = wmi.WMI()
            for bios in c.Win32_BIOS():
                return bios.SerialNumber
        elif platform.system() == "Linux":
            print(f"Linux")
            result = subprocess.run(["sudo", "dmidecode", "-s", "system-serial-number"], capture_output=True, text=True)
            serial_number = result.stdout.strip()
        elif platform.system() == "Darwin":
            print(f"Darwin")
            result = subprocess.run(["system_profiler", "SPHardwareDataType"], capture_output=True, text=True)
            serial_number = [line.split(":")[1].strip() for line in result.stdout.split("\n") if "Serial Number" in line][0]
        else:
            print(f"Otro")
            serial_number = "Sistema no compatible"
        print(f"serial_number: {serial_number}")
        return serial_number
    except Exception as e:
        return f"Error: {e}"

def mostrar_serial():
    """Muestra el número de serie en el cuadro de texto."""
    serial = get_serial_number()
    if serial.startswith("Error"):
        messagebox.showerror("Error", serial)
    else:
        entry_serial.config(state="normal")  # Habilitar edición temporalmente
        entry_serial.delete(0, tk.END)  # Limpiar el campo
        entry_serial.insert(0, serial)  # Insertar número de serie
        entry_serial.config(state="readonly")  # Volver a poner solo lectura

# Crear ventana principal
root = tk.Tk()
root.title("Número de Serie")
root.geometry("400x150")
root.resizable(False, False)  # Evita que se pueda modificar el tamaño

# Etiqueta
label = tk.Label(root, text="Presiona el botón para obtener el número de serie:", font=("Arial", 10))
label.pack(pady=5)

# Entrada de texto (solo lectura)
entry_serial = tk.Entry(root, font=("Arial", 12), width=40, state="readonly", justify="center")
entry_serial.pack(pady=5)

# Botón para ejecutar
btn = tk.Button(root, text="Ejecutar", font=("Arial", 12), command=mostrar_serial)
btn.pack(pady=5)

# Ejecutar ventana
root.mainloop()
