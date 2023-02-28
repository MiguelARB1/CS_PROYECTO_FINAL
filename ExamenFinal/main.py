import tkinter as tk
from tkinter import ttk
import sqlite3
from calculos.operaciones import calcular_bonificaciones_descuentos


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora de sueldo")
        self.master.geometry("400x400")

        # Crear los widgets del formulario
        self.nombre_label = tk.Label(self.master, text="Nombre:")
        self.nombre_label.pack()
        self.nombre_entry = tk.Entry(self.master)
        self.nombre_entry.pack()

        self.sueldo_label = tk.Label(self.master, text="Sueldo base:")
        self.sueldo_label.pack()
        self.sueldo_entry = tk.Entry(self.master)
        self.sueldo_entry.pack()

        self.faltas_label = tk.Label(self.master, text="Días de falta:")
        self.faltas_label.pack()
        self.faltas_entry = tk.Entry(self.master)
        self.faltas_entry.pack()

        self.minutos_label = tk.Label(self.master, text="Minutos de falta:")
        self.minutos_label.pack()
        self.minutos_entry = tk.Entry(self.master)
        self.minutos_entry.pack()

        self.horas_label = tk.Label(self.master, text="Horas extras:")
        self.horas_label.pack()
        self.horas_entry = tk.Entry(self.master)
        self.horas_entry.pack()

        # Agregar los botones de Calcular y Salir
        self.calcular_button = tk.Button(self.master, text="Calcular", command=self.calcular)
        self.calcular_button.pack()
        # Agregar un botón para ver los registros de la base de datos

        self.ver_registros_button = tk.Button(self.master, text="Ver registros", command=self.ver_registros)
        self.ver_registros_button.pack()

        self.salir_button = tk.Button(self.master, text="Salir", command=self.master.quit)
        self.salir_button.pack()



    def calcular(self):
        # Obtener los valores de los campos del formulario
        nombre = self.nombre_entry.get()
        sueldo_base = float(self.sueldo_entry.get())
        dias_falta = int(self.faltas_entry.get())
        minutos_falta = int(self.minutos_entry.get())
        horas_extra = int(self.horas_entry.get())

        # Calcular el sueldo neto, bonificaciones y descuentos
        bonificaciones, descuentos = calcular_bonificaciones_descuentos(sueldo_base,horas_extra,dias_falta,minutos_falta)
        sueldo_neto = round(sueldo_base + bonificaciones - descuentos,2)



        # Crear una ventana para mostrar los resultados
        self.resultados_window = tk.Toplevel(self.master)
        self.resultados_window.title("Resultados")
        self.resultados_window.geometry("200x200")

        # Mostrar los resultados en la ventana

        bonificaciones_label = tk.Label(self.resultados_window, text="Bonificaciones: " + str(bonificaciones))
        bonificaciones_label.pack()

        descuentos_label = tk.Label(self.resultados_window, text="Descuentos: " + str(descuentos))
        descuentos_label.pack()
        sueldo_neto_label = tk.Label(self.resultados_window, text="Sueldo neto: " + str(sueldo_neto))
        sueldo_neto_label.pack()



        # Agregar botones para registrar o volver
        registrar_button = tk.Button(self.resultados_window, text="Registrar",
                                     command=lambda: self.registrar(nombre, sueldo_neto, bonificaciones, descuentos))
        registrar_button.pack()

        volver_button = tk.Button(self.resultados_window, text="Volver", command=self.resultados_window
        .destroy)
        volver_button.pack()

    def registrar(self, nombre, sueldo_neto, bonificaciones, descuentos):
        # Crear una conexión con la base de datos
        conn = sqlite3.connect("trabajadores.db")

        # Crear un cursor para ejecutar las consultas
        cursor = conn.cursor()

        # Insertar los datos del trabajador en la tabla
        cursor.execute("INSERT INTO trabajadores(nombre, sueldo_neto, bonificaciones, descuentos) VALUES (?, ?, ?, ?)", (nombre, sueldo_neto, bonificaciones, descuentos))

        # Guardar los cambios en la base de datos
        conn.commit()

        # Cerrar la conexión con la base de datos
        conn.close()

        # Limpiar los campos del formulario
        self.nombre_entry.delete(0, tk.END)
        self.sueldo_entry.delete(0, tk.END)
        self.faltas_entry.delete(0, tk.END)
        self.minutos_entry.delete(0, tk.END)
        self.horas_entry.delete(0, tk.END)

        # Cerrar la ventana de resultados
        self.resultados_window.destroy()

    def ver_registros(self):
        # Crear una conexión con la base de datos
        conn = sqlite3.connect("trabajadores.db")

        # Crear un cursor para ejecutar las consultas
        cursor = conn.cursor()

        # Obtener los datos de los trabajadores de la tabla
        cursor.execute("SELECT * FROM trabajadores")
        trabajadores = cursor.fetchall()

        # Crear una ventana para mostrar los registros
        registros_window = tk.Toplevel(self.master)
        registros_window.title("Registros")
        registros_window.geometry("1000x500")

        # Crear un treeview para mostrar los datos de los trabajadores
        treeview = ttk.Treeview(registros_window, columns=("sueldo_neto", "bonificaciones", "descuentos"))
        treeview.heading("#0", text="Nombre")
        treeview.heading("sueldo_neto", text="Sueldo neto")
        treeview.heading("bonificaciones", text="Bonificaciones")
        treeview.heading("descuentos", text="Descuentos")

        treeview.pack()

        # Agregar los datos de los trabajadores al treeview
        for trabajador in trabajadores:
            nombre = trabajador[1]
            sueldo_neto = trabajador[2]
            bonificaciones = trabajador[3]
            descuentos = trabajador[4]

            treeview.insert("", "end", text=nombre, values=(sueldo_neto, bonificaciones, descuentos))

        # Cerrar la conexión con la base de datos
        conn.close()

# Crear una conexión con la base de datos y crear la tabla si no existe
conn = sqlite3.connect("trabajadores.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS trabajadores(id INTEGER PRIMARY KEY, nombre TEXT, sueldo_neto REAL, bonificaciones REAL, descuentos REAL)")
conn.close()

# Iniciar la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()
