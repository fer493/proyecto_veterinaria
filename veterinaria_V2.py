# -*- coding: utf-8 -*-
"""


@author: Fernando Marquez Arres
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import sqlite3
from datetime import datetime, date
import hashlib  # Para el hash de contraseñas
import re  # Para validación de email

# ====================== CLASES DEL DOMINIO ======================

class Animal:
    def __init__(self, id=None, nombre=None, especie=None, raza=None, fecha_nacimiento=None):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = fecha_nacimiento
    
    def calcular_edad(self):
        if self.fecha_nacimiento:
            try:
                nacimiento = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d").date()
                return (date.today() - nacimiento).days // 365
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD")
                return None
        return None

class Propietario:
    def __init__(self, id=None, nombre=None, telefono=None, email=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
    
    def asociar_animal(self, animal_id, db):
        try:
            animal_id = int(animal_id)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return False
        
        try:
             cursor = db.conn.cursor()
             # Verificar que la relación no existe ya
             cursor.execute(
                 "SELECT * FROM Propietario_Animal WHERE propietario_id = ? AND animal_id = ?",
                 (self.id, animal_id)
             )
             if cursor.fetchone():
                 messagebox.showerror("Error", "Esta asociación ya existe")
                 return False
            
             cursor.execute(
                 "INSERT INTO Propietario_Animal (propietario_id, animal_id) VALUES (?, ?)",
                 (self.id, animal_id)
             )
             db.conn.commit()
             return True
        except sqlite3.Error as e:
             db.conn.rollback()
             messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
             return False
            

class Administrador:
    def __init__(self, id=None, nombre=None, email=None, password=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = self._hash_password(password) if password else None
    
    def _hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def configurar_servicios(self, servicios, db):
        pass
    
    def establecer_precios(self, precios, db):
        pass
    
    def generar_reportes(self, tipo, db):
        pass

class Recepcionista:
    def __init__(self, id=None, nombre=None, email=None, password=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = self._hash_password(password) if password else None
    
    def _hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def registrar_animal(self, animal, db):
        if not animal or not isinstance(animal, Animal):
            messagebox.showerror("Error", "Datos del animal inválidos")
            return False
            
        if not animal.nombre or not isinstance(animal.nombre, str):
            messagebox.showerror("Error", "Nombre del animal es requerido")
            return False
            
        try:
            cursor = db.conn.cursor()
            cursor.execute(
                "INSERT INTO Animal (nombre, especie, raza, fecha_nacimiento) VALUES (?, ?, ?, ?)",
                (animal.nombre, animal.especie, animal.raza, animal.fecha_nacimiento)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False
    
    def actualizar_datos_animal(self, animal, db):
        if not animal or not isinstance(animal, Animal):
            messagebox.showerror("Error", "Datos del animal inválidos")
            return False
        
        if not animal.id or not isinstance(animal.id, int):
            messagebox.showerror("Error", "ID de animal inválido")
            return False
        
        try:
            cursor = db.conn.cursor()
            # Verificar que el animal existe
            cursor.execute("SELECT id FROM Animal WHERE id = ?", (animal.id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", f"No existe un animal con ID {animal.id}")
                return False
            
            cursor.execute(
                """UPDATE Animal 
                SET nombre = ?, especie = ?, raza = ?, fecha_nacimiento = ?
                WHERE id = ?""",
                (animal.nombre, animal.especie, animal.raza, animal.fecha_nacimiento, animal.id)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False
    
    def administrar_cita(self, cita_id, accion, db):
        pass
    
    def enviar_recordatorio(self, cita_id, medio, db):
        pass
    
    def registrar_pago(self, cita_id, monto, estado, db):
        if not cita_id or not isinstance(cita_id, int):
            messagebox.showerror("Error", "ID de cita inválido")
            return False
            
        if not monto or not isinstance(monto, (int, float)) or monto <= 0:
            messagebox.showerror("Error", "Monto inválido")
            return False
            
        try:
            cursor = db.conn.cursor()
            cursor.execute(
                "INSERT INTO Pago (monto, fecha, estado, cita_id) VALUES (?, date('now'), ?, ?)",
                (monto, estado, cita_id)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False

class Veterinario:
    def __init__(self, id=None, nombre=None, email=None, password=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = self._hash_password(password) if password else None
    
    def _hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def buscar_historial(self, animal_id, db):
        try:
            animal_id = int(animal_id)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return None
        
        try:
            cursor = db.conn.cursor()
            # Primero verificar que el animal existe
            cursor.execute("SELECT id FROM Animal WHERE id = ?", (animal_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", f"No existe un animal con ID {animal_id}")
                return None
            
            cursor.execute(
                "SELECT fecha, tipo, descripcion, tratamiento FROM HistorialMedico WHERE animal_id = ? ORDER BY fecha DESC",
                (animal_id,)
            )
            historial_medico=cursor.fetchall()
        
            cursor.execute(
                """SELECT c.fecha, s.nombre, c.motivo, v.nombre 
                FROM Cita c
                JOIN Servicio s ON c.servicio_id = s.id
                JOIN Veterinario v ON c.veterinario_id = v.id
                WHERE c.animal_id = ?
                ORDER BY c.fecha DESC""",
                (animal_id,)
            )
            citas = cursor.fetchall()
            
            return {
                'historial_medico': historial_medico,
                'citas': citas
            }
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return None
    
    def registrar_tratamiento(self, animal_id, tipo, descripcion, tratamiento, db):
        try:
            animal_id = int(animal_id)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return False
        
        if not tipo or not isinstance(tipo, str):
            messagebox.showerror("Error", "Tipo de tratamiento inválido")
            return False
        
        try:
            cursor = db.conn.cursor()
            cursor.execute("SELECT id FROM Animal WHERE id = ?", (animal_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", f"No existe un animal con ID {animal_id}")
                return False
            
            cursor.execute(
                """INSERT INTO HistorialMedico 
                (fecha, tipo, descripcion, tratamiento, animal_id, veterinario_id)
                VALUES (date('now'), ?, ?, ?, ?, ?)""",
                (tipo, descripcion, tratamiento, animal_id, self.id)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False
    
    def registrar_vacuna(self, animal_id, vacuna, proxima_aplicacion, db):
        if not animal_id or not isinstance(animal_id, int):
            messagebox.showerror("Error", "ID de animal inválido")
            return False
            
        if not vacuna or not isinstance(vacuna, str):
            messagebox.showerror("Error", "Tipo de vacuna inválido")
            return False
            
        try:
            descripcion = f"Vacuna: {vacuna}\nPróxima aplicación: {proxima_aplicacion}"
            cursor = db.conn.cursor()
            cursor.execute(
                """INSERT INTO HistorialMedico 
                (fecha, tipo, descripcion, animal_id, veterinario_id)
                VALUES (date('now'), 'Vacunación', ?, ?, ?)""",
                (descripcion, animal_id, self.id)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False
    
    def generar_alerta_vacuna(self, animal_id, db):
        if not animal_id or not isinstance(animal_id, int):
            messagebox.showerror("Error", "ID de animal inválido")
            return []
            
        try:
            cursor = db.conn.cursor()
            cursor.execute(
                """SELECT a.id, a.nombre, hm.descripcion 
                FROM Animal a
                JOIN HistorialMedico hm ON a.id = hm.animal_id
                WHERE hm.tipo = 'Vacunación' 
                AND hm.descripcion LIKE '%Próxima aplicación%'
                AND date(substr(hm.descripcion, instr(hm.descripcion, 'Próxima aplicación: ') + 19, 10)) <= date('now', '+7 day')
                AND a.id = ?""",
                (animal_id,)
            )
            return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return []

class Cita:
    def __init__(self, id=None, fecha=None, motivo=None, estado_pago=None, animal_id=None, veterinario_id=None, servicio_id=None):
        self.id = id
        self.fecha = fecha
        self.motivo = motivo
        self.estado_pago = estado_pago
        self.animal_id = animal_id
        self.veterinario_id = veterinario_id
        self.servicio_id = servicio_id
    
    def programar_cita(self, db):
        if not self.fecha or not self.motivo or not self.animal_id or not self.veterinario_id or not self.servicio_id:
            messagebox.showerror("Error", "Todos los campos de la cita son requeridos")
            return False
            
        try:
            cursor = db.conn.cursor()
            cursor.execute(
                """INSERT INTO Cita 
                (fecha, motivo, animal_id, veterinario_id, servicio_id)
                VALUES (?, ?, ?, ?, ?)""",
                (self.fecha, self.motivo, self.animal_id, self.veterinario_id, self.servicio_id)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False
    
    def cancelar_cita(self, db):
        if not self.id or not isinstance(self.id, int):
            messagebox.showerror("Error", "ID de cita inválido")
            return False
            
        try:
            cursor = db.conn.cursor()
            cursor.execute("DELETE FROM Cita WHERE id = ?", (self.id,))
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False

class HistorialMedico:
    def __init__(self, id=None, fecha=None, tipo=None, descripcion=None, tratamiento=None, animal_id=None, veterinario_id=None):
        self.id = id
        self.fecha = fecha
        self.tipo = tipo
        self.descripcion = descripcion
        self.tratamiento = tratamiento
        self.animal_id = animal_id
        self.veterinario_id = veterinario_id
    
    def registrar_pago(self, cita_id, monto, db):
        if not cita_id or not isinstance(cita_id, int):
            messagebox.showerror("Error", "ID de cita inválido")
            return False
            
        if not monto or not isinstance(monto, (int, float)) or monto <= 0:
            messagebox.showerror("Error", "Monto inválido")
            return False
            
        try:
            cursor = db.conn.cursor()
            cursor.execute(
                "INSERT INTO Pago (monto, fecha, cita_id) VALUES (?, date('now'), ?)",
                (monto, cita_id)
            )
            db.conn.commit()
            return True
        except sqlite3.Error as e:
            db.conn.rollback()
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")
            return False

# ====================== BASE DE DATOS ======================

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("veterinaria.db")
            self.crear_tablas()
            self.insertar_datos_prueba()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {str(e)}")
            raise
    
    def crear_tablas(self):
        try:
            cursor = self.conn.cursor()
            tablas = [
                """CREATE TABLE IF NOT EXISTS Administrador (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password TEXT NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Propietario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT UNIQUE
                )""",
                """CREATE TABLE IF NOT EXISTS Animal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    especie TEXT,
                    raza TEXT,
                    fecha_nacimiento DATE
                )""",
                """CREATE TABLE IF NOT EXISTS Propietario_Animal (
                    propietario_id INTEGER,
                    animal_id INTEGER,
                    FOREIGN KEY (propietario_id) REFERENCES Propietario(id),
                    FOREIGN KEY (animal_id) REFERENCES Animal(id),
                    PRIMARY KEY (propietario_id, animal_id)
                )""",
                """CREATE TABLE IF NOT EXISTS Recepcionista (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password TEXT NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Veterinario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password TEXT NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Servicio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    precio REAL NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS Cita (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATETIME NOT NULL,
                    motivo TEXT NOT NULL,
                    estado TEXT DEFAULT 'pendiente',
                    animal_id INTEGER NOT NULL,
                    veterinario_id INTEGER NOT NULL,
                    servicio_id INTEGER NOT NULL,
                    FOREIGN KEY (animal_id) REFERENCES Animal(id),
                    FOREIGN KEY (veterinario_id) REFERENCES Veterinario(id),
                    FOREIGN KEY (servicio_id) REFERENCES Servicio(id)
                )""",
                """CREATE TABLE IF NOT EXISTS Pago (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    monto REAL NOT NULL,
                    fecha DATE NOT NULL,
                    estado TEXT DEFAULT 'pendiente',
                    cita_id INTEGER NOT NULL,
                    FOREIGN KEY (cita_id) REFERENCES Cita(id)
                )""",
                """CREATE TABLE IF NOT EXISTS HistorialMedico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE NOT NULL,
                    tipo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    tratamiento TEXT,
                    animal_id INTEGER NOT NULL,
                    veterinario_id INTEGER NOT NULL,
                    FOREIGN KEY (animal_id) REFERENCES Animal(id),
                    FOREIGN KEY (veterinario_id) REFERENCES Veterinario(id)
                )"""
            ]
            for tabla in tablas:
                cursor.execute(tabla)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al crear tablas: {str(e)}")
            raise

    def insertar_datos_prueba(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Propietario")
            if cursor.fetchone()[0] == 0:
                # Hasheamos las contraseñas de prueba
                admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
                recep_pass = hashlib.sha256("recepcion123".encode()).hexdigest()
                vet_pass = hashlib.sha256("vet123".encode()).hexdigest()
                
                datos_prueba = [
                    ("INSERT INTO Administrador (nombre, email, password) VALUES (?, ?, ?)", 
                     ("Admin Principal", "admin@vet.com", admin_pass)),
                    ("INSERT INTO Recepcionista (nombre, email, password) VALUES (?, ?, ?)", 
                     ("Ana Recepcion", "recepcion@vet.com", recep_pass)),
                    ("INSERT INTO Veterinario (nombre, email, password) VALUES (?, ?, ?)", 
                     ("Dr. Perez", "vet@vet.com", vet_pass)),
                    ("INSERT INTO Propietario (nombre, telefono, email) VALUES (?, ?, ?)", 
                     ("Juan Perez", "5551234567", "juan@email.com")),
                    ("INSERT INTO Animal (nombre, especie, raza, fecha_nacimiento) VALUES (?, ?, ?, ?)", 
                     ("Firulais", "Perro", "Labrador", "2020-05-15")),
                    ("INSERT INTO Servicio (nombre, precio) VALUES (?, ?)", 
                     ("Consulta General", 300.0))
                ]
                for consulta, parametros in datos_prueba:
                    cursor.execute(consulta, parametros)
                self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al insertar datos de prueba: {str(e)}")
            
         
            
            

# ====================== INTERFAZ DE USUARIO ======================

class PantallaLogin:
    def __init__(self, root, db, mostrar_panel_callback):
        self.root = root
        self.db = db
        self.mostrar_panel_callback = mostrar_panel_callback
        self.marco = tk.Frame(root, bg="#f0f0f0")
        self.marco.pack(expand=True)
        
        tk.Label(self.marco, text="Inicio de Sesión", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)
        
        tk.Label(self.marco, text="Rol:", bg="#f0f0f0").pack()
        self.rol_var = tk.StringVar()
        roles = ["Administrador", "Recepcionista", "Veterinario", "Propietario"]
        combobox_rol = ttk.Combobox(self.marco, textvariable=self.rol_var, values=roles, state="readonly")
        combobox_rol.pack()
        
        self.marco_email = tk.Frame(self.marco, bg="#f0f0f0")
        self.marco_email.pack()
        tk.Label(self.marco_email, text="Email:", bg="#f0f0f0").pack()
        self.entrada_email = tk.Entry(self.marco_email)
        self.entrada_email.pack()
        
        self.marco_password = tk.Frame(self.marco, bg="#f0f0f0")
        self.marco_password.pack()
        tk.Label(self.marco_password, text="Contraseña:", bg="#f0f0f0").pack()
        self.entrada_password = tk.Entry(self.marco_password, show="*")
        self.entrada_password.pack()
        
        tk.Button(self.marco, text="Ingresar", command=self.verificar_login).pack(pady=20)
        
        self.rol_var.trace_add("write", self.actualizar_campos_login)

    def actualizar_campos_login(self, *args):
        if self.rol_var.get() == "Propietario":
            self.marco_email.pack_forget()
            self.marco_password.pack_forget()
        else:
            self.marco_email.pack()
            self.marco_password.pack()

    def verificar_login(self):
        rol = self.rol_var.get()
        
        if rol == "Propietario":
            id_usuario = 1
            nombre_usuario = "Propietario"
            self.mostrar_panel_callback(rol, id_usuario, nombre_usuario)
        else:
            email = self.entrada_email.get()
            password = self.entrada_password.get()
            
            # Validación básica de email
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Formato de email inválido")
                return
                
            if not password:
                messagebox.showerror("Error", "La contraseña es requerida")
                return
            
            try:
                cursor = self.db.conn.cursor()
                # Hasheamos la contraseña ingresada para comparar con la almacenada
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute(f"SELECT id, nombre FROM {rol} WHERE email = ? AND password = ?", 
                             (email, hashed_password))
                usuario = cursor.fetchone()
                
                if usuario:
                    self.mostrar_panel_callback(rol, usuario[0], usuario[1])
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error de base de datos: {str(e)}")

# [El resto del código permanece exactamente igual, solo se han modificado las clases anteriores]


class PanelPrincipal:
    def __init__(self, root, db, rol, id_usuario, nombre_usuario):
        self.root = root
        self.db = db
        self.rol = rol
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.cuaderno = ttk.Notebook(root)
        self.cuaderno.pack(expand=True, fill="both")
        self.texto_historial = None  # Lo inicializaremos después
        self.style = ttk.Style()
        self.style.configure('Titulo.TLabel', font=('Arial', 10, 'bold'))
        
        self.crear_menu()
        self.crear_pestanas()

    def crear_menu(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

    def cerrar_sesion(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        PantallaLogin(self.root, self.db, self.mostrar_panel_callback)

    def mostrar_panel_callback(self, rol, id_usuario, nombre_usuario):
        for widget in self.root.winfo_children():
            widget.destroy()
        PanelPrincipal(self.root, self.db, rol, id_usuario, nombre_usuario)

    def crear_pestanas(self):
        if self.rol == "Propietario":
            self.pestanas_propietario()
        elif self.rol == "Recepcionista":
            self.pestanas_recepcionista()
        elif self.rol == "Veterinario":
            self.pestanas_veterinario()
        elif self.rol == "Administrador":
            self.pestanas_administrador()

    def pestanas_propietario(self):
        pestana1 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(pestana1, text="Asociar Animal")
    
        # Mostrar ID del animal seleccionado
        tk.Label(pestana1, text="ID del Animal:").pack()
        self.id_animal_asociar = tk.Label(pestana1, text="")
        self.id_animal_asociar.pack()
    
        # Combobox para seleccionar animal
        tk.Label(pestana1, text="Seleccionar Animal:").pack()
        cursor = self.db.conn.cursor()
        cursor.execute("""
        SELECT a.id, a.nombre, a.especie 
        FROM Animal a
        LEFT JOIN Propietario_Animal pa ON a.id = pa.animal_id
        WHERE pa.animal_id IS NULL
         """)
        animales = [f"{id} - {nombre} ({especie})" for id, nombre, especie in cursor.fetchall()]
    
        combobox_animal = ttk.Combobox(pestana1, values=animales, state="readonly")
        combobox_animal.pack(pady=5)
        combobox_animal.bind("<<ComboboxSelected>>", lambda e: self.id_animal_asociar.config(
            text=combobox_animal.get().split(" - ")[0]))
    
        # Botón para asociar
        tk.Button(pestana1, text="Asociar a mi cuenta", 
                 command=lambda: self.asociar_animal_propietario(
                     combobox_animal.get().split(" - ")[0]
                 )).pack(pady=10)
    
        # Lista de animales disponibles
        tk.Label(pestana1, text="Animales disponibles para asociar:").pack(pady=10)
        for animal in animales:
            tk.Label(pestana1, text=animal).pack()
    
        pestana2 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(pestana2, text="Mis Animales")
        self.mostrar_animales_propietario(pestana2)

    def asociar_animal_propietario(self, id_animal):
        try:
            id_animal = int(id_animal)
        except (ValueError, TypeError):
             messagebox.showerror("Error", "ID de animal inválido")
             return
        
        # Verificar que el animal existe y no está ya asociado
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM Animal WHERE id = ?", (id_animal,))
        if not cursor.fetchone():
            messagebox.showerror("Error", f"No existe un animal con ID {id_animal}")
            return
    
        cursor.execute("""
        SELECT animal_id FROM Propietario_Animal 
        WHERE animal_id = ? AND propietario_id = ?
        """, (id_animal, self.id_usuario))
        if cursor.fetchone():
            messagebox.showerror("Error", "Este animal ya está asociado a tu cuenta")
            return
    
        propietario = Propietario(id=self.id_usuario)
        if propietario.asociar_animal(id_animal, self.db):
            messagebox.showinfo("Éxito", "Animal asociado correctamente")
             # Actualizar la lista de animales
            for widget in self.cuaderno.winfo_children():
                if isinstance(widget, ttk.Notebook):
                    for tab_id in widget.tabs():
                        if "Mis Animales" in widget.tab(tab_id, "text"):
                            widget.forget(tab_id)
                            new_tab = ttk.Frame(widget)
                            widget.add(new_tab, text="Mis Animales")
                            self.mostrar_animales_propietario(new_tab)
                            break

    def mostrar_animales_propietario(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("""
        SELECT a.id, a.nombre, a.especie, a.raza, a.fecha_nacimiento 
        FROM Animal a
        JOIN Propietario_Animal pa ON a.id = pa.animal_id
        WHERE pa.propietario_id = ?
        """, (self.id_usuario,))
        
        for datos_animal in cursor.fetchall():
            animal = Animal(*datos_animal)
            marco = tk.Frame(pestana, borderwidth=2, relief="groove", padx=10, pady=10)
            marco.pack(fill="x", padx=5, pady=5)
            
            edad = animal.calcular_edad()
            
            tk.Label(marco, text=f"Nombre: {animal.nombre}", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
            tk.Label(marco, text=f"Especie: {animal.especie}").grid(row=1, column=0, sticky="w")
            tk.Label(marco, text=f"Raza: {animal.raza}").grid(row=2, column=0, sticky="w")
            tk.Label(marco, text=f"Edad: {edad} años" if edad else "Edad: Desconocida").grid(row=3, column=0, sticky="w")

    def pestanas_recepcionista(self):
        pestanas = [
            ("Registrar Animal", self.pestana_registrar_animal),
            ("Modificar Animal", self.pestana_modificar_animal),
            ("Programar Cita", self.pestana_programar_cita),
            ("Registrar Pago", self.pestana_registrar_pago),
            ("Enviar Recordatorios", self.pestana_enviar_recordatorios)
        ]
        
        for texto, comando in pestanas:
            pestana = ttk.Frame(self.cuaderno)
            self.cuaderno.add(pestana, text=texto)
            comando(pestana)

    def pestana_registrar_animal(self, pestana):
        campos = [
            ("Nombre:", tk.Entry(pestana)),
            ("Especie:", tk.Entry(pestana)),
            ("Raza:", tk.Entry(pestana)),
            ("Fecha Nacimiento (YYYY-MM-DD):", tk.Entry(pestana))
        ]
        
        for i, (etiqueta, entrada) in enumerate(campos):
            tk.Label(pestana, text=etiqueta).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entrada.grid(row=i, column=1, padx=5, pady=5)
        
        tk.Button(pestana, text="Registrar", 
                 command=lambda: self.registrar_animal(
                     campos[0][1].get(),
                     campos[1][1].get(),
                     campos[2][1].get(),
                     campos[3][1].get()
                 )).grid(row=len(campos), columnspan=2, pady=10)

    def registrar_animal(self, nombre, especie, raza, fecha_nacimiento):
        animal = Animal(nombre=nombre, especie=especie, raza=raza, fecha_nacimiento=fecha_nacimiento)
        recepcionista = Recepcionista(id=self.id_usuario)
        if recepcionista.registrar_animal(animal, self.db):
            messagebox.showinfo("Éxito", "Animal registrado")

    def pestana_modificar_animal(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre FROM Animal")
        animales = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
    
        tk.Label(pestana, text="ID del Animal:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_animal_label = tk.Label(pestana, text="")
        self.id_animal_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
        tk.Label(pestana, text="Seleccionar Animal:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        combobox_animal = ttk.Combobox(pestana, values=animales, state="readonly")
        combobox_animal.grid(row=1, column=1, padx=5, pady=5)
        
        campos = [
            ("Nombre:", tk.Entry(pestana)),
            ("Especie:", tk.Entry(pestana)),
            ("Raza:", tk.Entry(pestana)),
            ("Fecha Nacimiento (YYYY-MM-DD):", tk.Entry(pestana))
        ]
        
        for i, (etiqueta, entrada) in enumerate(campos):
            tk.Label(pestana, text=etiqueta).grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
            entrada.grid(row=i+1, column=1, padx=5, pady=5)
        
        tk.Button(pestana, text="Cargar Datos", 
                 command=lambda: self.cargar_datos_animal(
                     combobox_animal.get().split(" - ")[0], campos
                 )).grid(row=len(campos)+1, columnspan=2, pady=5)
        
        tk.Button(pestana, text="Actualizar", 
                 command=lambda: self.actualizar_animal(
                     combobox_animal.get().split(" - ")[0],
                     campos[0][1].get(),
                     campos[1][1].get(),
                     campos[2][1].get(),
                     campos[3][1].get()
                 )).grid(row=len(campos)+2, columnspan=2, pady=10)

    def cargar_datos_animal(self, id_animal, campos):
        try:
            id_animal = int(id_animal)
            self.id_animal_label.config(text=str(id_animal))  # Actualizar el label del ID
        
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT nombre, especie, raza, fecha_nacimiento FROM Animal WHERE id = ?", (id_animal,))
            datos_animal = cursor.fetchone()
        
            if datos_animal:
                # Limpiar todos los campos primero
                for campo in campos:
                    campo[1].delete(0, tk.END)
            
                # Llenar los campos en el orden correcto
                campos[0][1].insert(0, datos_animal[0])  # Nombre
                campos[1][1].insert(0, datos_animal[1])  # Especie
                campos[2][1].insert(0, datos_animal[2])  # Raza
                campos[3][1].insert(0, datos_animal[3] if datos_animal[3] else "")  # Fecha nacimiento
            
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {str(e)}")

    def actualizar_animal(self, id_animal, nombre, especie, raza, fecha_nacimiento):
        try:
            
            id_animal = int(id_animal)  # Convertir a entero
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return
       
        animal = Animal(id=id_animal, nombre=nombre, especie=especie, raza=raza, fecha_nacimiento=fecha_nacimiento)
        recepcionista = Recepcionista(id=self.id_usuario)
        if recepcionista.actualizar_datos_animal(animal, self.db):
            messagebox.showinfo("Éxito", "Datos del animal actualizados")

    def pestana_programar_cita(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre FROM Animal")
        animales = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
        
        cursor.execute("SELECT id, nombre FROM Veterinario")
        veterinarios = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
        
        cursor.execute("SELECT id, nombre FROM Servicio")
        servicios = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
        
        campos = [
            ("Animal:", ttk.Combobox(pestana, values=animales, state="readonly")),
            ("Veterinario:", ttk.Combobox(pestana, values=veterinarios, state="readonly")),
            ("Servicio:", ttk.Combobox(pestana, values=servicios, state="readonly")),
            ("Fecha y Hora (YYYY-MM-DD HH:MM):", tk.Entry(pestana)),
            ("Motivo:", tk.Entry(pestana))
        ]
        
        for i, (etiqueta, widget) in enumerate(campos):
            tk.Label(pestana, text=etiqueta).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=5, pady=5)
        
        tk.Button(pestana, text="Programar", 
                 command=lambda: self.programar_cita(
                     campos[0][1].get().split(" - ")[0],
                     campos[1][1].get().split(" - ")[0],
                     campos[2][1].get().split(" - ")[0],
                     campos[3][1].get(),
                     campos[4][1].get()
                 )).grid(row=len(campos), columnspan=2, pady=10)

    def programar_cita(self, id_animal, id_veterinario, id_servicio, fecha_hora, motivo):
        cita = Cita(fecha=fecha_hora, motivo=motivo, animal_id=id_animal, 
                   veterinario_id=id_veterinario, servicio_id=id_servicio)
        if cita.programar_cita(self.db):
            messagebox.showinfo("Éxito", "Cita programada")

    def pestana_registrar_pago(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("""
        SELECT c.id, a.nombre, c.fecha, s.nombre, s.precio 
        FROM Cita c
        JOIN Animal a ON c.animal_id = a.id
        JOIN Servicio s ON c.servicio_id = s.id
        WHERE c.id NOT IN (SELECT cita_id FROM Pago)
        """)
        citas = [f"{id} - {animal} ({fecha}) - {servicio} - ${precio}" 
                for id, animal, fecha, servicio, precio in cursor.fetchall()]
        
        tk.Label(pestana, text="Cita:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        combobox_cita = ttk.Combobox(pestana, values=citas, state="readonly", width=50)
        combobox_cita.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(pestana, text="Monto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entrada_monto = tk.Entry(pestana)
        entrada_monto.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(pestana, text="Registrar Pago", 
                 command=lambda: self.registrar_pago(
                     combobox_cita.get().split(" - ")[0],
                     entrada_monto.get()
                 )).grid(row=2, columnspan=2, pady=10)

    def registrar_pago(self, id_cita, monto):
        recepcionista = Recepcionista(id=self.id_usuario)
        if recepcionista.registrar_pago(id_cita, monto, "completado", self.db):
            messagebox.showinfo("Éxito", "Pago registrado")

    def pestana_enviar_recordatorios(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("""
        SELECT c.id, a.nombre, p.telefono, c.fecha 
        FROM Cita c
        JOIN Animal a ON c.animal_id = a.id
        JOIN Propietario_Animal pa ON a.id = pa.animal_id
        JOIN Propietario p ON pa.propietario_id = p.id
        WHERE date(c.fecha) = date('now', '+1 day')
        """)
        
        citas = cursor.fetchall()
        
        if not citas:
            tk.Label(pestana, text="No hay citas para recordar mañana").pack(pady=20)
            return
        
        tk.Label(pestana, text="Citas para mañana:").pack(pady=10)
        
        for cita in citas:
            marco = tk.Frame(pestana, borderwidth=1, relief="groove", padx=10, pady=5)
            marco.pack(fill="x", padx=5, pady=2)
            
            tk.Label(marco, text=f"ID: {cita[0]} - {cita[1]} a las {cita[3]}").pack(side="left")
            tk.Button(marco, text="Enviar SMS", 
                     command=lambda tel=cita[2], cid=cita[0]: self.enviar_sms(tel, cid)).pack(side="right", padx=5)

    def enviar_sms(self, telefono, id_cita):
        messagebox.showinfo("Recordatorio enviado", 
                          f"Se envió recordatorio al teléfono {telefono} para la cita {id_cita}")

    def pestanas_veterinario(self):
        pestanas = [
            ("Buscar Historial", self.pestana_buscar_historial),
            ("Registrar Tratamiento", self.pestana_registrar_tratamiento),
            ("Registrar Vacuna", self.pestana_registrar_vacuna),
            ("Alertas de Vacunas", self.pestana_alertas_vacunas)
        ]
        
        for texto, comando in pestanas:
            pestana = ttk.Frame(self.cuaderno)
            self.cuaderno.add(pestana, text=texto)
            comando(pestana)

    def pestana_buscar_historial(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre FROM Animal")
        animales = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
    
        tk.Label(pestana, text="ID del Animal:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_animal_historial = tk.Label(pestana, text="")
        self.id_animal_historial.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
        tk.Label(pestana, text="Seleccionar Animal:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        combobox_animal = ttk.Combobox(pestana, values=animales, state="readonly")
        combobox_animal.grid(row=1, column=1, padx=5, pady=5)
        combobox_animal.bind("<<ComboboxSelected>>", lambda e: self.id_animal_historial.config(
             text=combobox_animal.get().split(" - ")[0]))
    
        tk.Button(pestana, text="Buscar Historial", 
                 command=lambda: self.mostrar_historial(
                     pestana, 
                     combobox_animal.get().split(" - ")[0]
                 )).grid(row=2, columnspan=2, pady=10)
    
        self.texto_historial = scrolledtext.ScrolledText(pestana, wrap=tk.WORD, width=60, height=15)
        self.texto_historial.grid(row=3, columnspan=2, padx=5, pady=5, sticky="nsew")

    def mostrar_historial(self, pestana, id_animal):
        self.texto_historial.delete(1.0, tk.END)
    
        try:
            id_animal = int(id_animal)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return
    
        veterinario = Veterinario(id=self.id_usuario)
        historial_completo = veterinario.buscar_historial(id_animal, self.db)
    
        if not historial_completo:
            self.texto_historial.insert(tk.END, "No hay registros para este animal")
            return
    
        # Mostrar citas primero
        self.texto_historial.insert(tk.END, "=== CITAS ===\n\n", 'titulo')
        if historial_completo['citas']:
            for cita in historial_completo['citas']:
                fecha, servicio, motivo, veterinario = cita
                self.texto_historial.insert(tk.END, f"Fecha: {fecha}\n")
                self.texto_historial.insert(tk.END, f"Servicio: {servicio}\n")
                self.texto_historial.insert(tk.END, f"Motivo: {motivo}\n")
                self.texto_historial.insert(tk.END, f"Veterinario: {veterinario}\n")
                self.texto_historial.insert(tk.END, "-"*50 + "\n\n")
        else:
            self.texto_historial.insert(tk.END, "No hay citas registradas\n\n")
    
        # Mostrar historial médico
        self.texto_historial.insert(tk.END, "\n=== HISTORIAL MÉDICO ===\n\n", 'titulo')
        if historial_completo['historial_medico']:
            for registro in historial_completo['historial_medico']:
                fecha, tipo, descripcion, tratamiento = registro
                self.texto_historial.insert(tk.END, f"Fecha: {fecha}\n")
                self.texto_historial.insert(tk.END, f"Tipo: {tipo}\n")
                self.texto_historial.insert(tk.END, f"Descripción:\n{descripcion}\n")
                if tratamiento:
                    self.texto_historial.insert(tk.END, f"Tratamiento:\n{tratamiento}\n")
                self.texto_historial.insert(tk.END, "-"*50 + "\n\n")
        else:
            self.texto_historial.insert(tk.END, "No hay registros médicos\n")
    
        # Configurar estilo para los títulos
        self.texto_historial.tag_config('titulo', font=('Arial', 10, 'bold'))

    def pestana_registrar_tratamiento(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre FROM Animal")
        animales = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
    
        tk.Label(pestana, text="ID del Animal:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_animal_tratamiento = tk.Label(pestana, text="")
        self.id_animal_tratamiento.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
        tk.Label(pestana, text="Animal:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        combobox_animal = ttk.Combobox(pestana, values=animales, state="readonly")
        combobox_animal.grid(row=1, column=1, padx=5, pady=5)
        combobox_animal.bind("<<ComboboxSelected>>", lambda e: self.id_animal_tratamiento.config(
        text=combobox_animal.get().split(" - ")[0]))
    
        campos = [
            ("Tipo:", ttk.Combobox(pestana, values=["Consulta", "Cirugía", "Control"], state="readonly")),
            ("Descripción:", tk.Entry(pestana)),
            ("Tratamiento:", tk.Entry(pestana))
        ]
    
        for i, (etiqueta, widget) in enumerate(campos):
            tk.Label(pestana, text=etiqueta).grid(row=i+2, column=0, padx=5, pady=5, sticky="e")
            widget.grid(row=i+2, column=1, padx=5, pady=5)
    
        tk.Button(pestana, text="Registrar", 
                 command=lambda: self.registrar_tratamiento(
                     combobox_animal.get().split(" - ")[0],
                     campos[0][1].get(),
                     campos[1][1].get(),
                     campos[2][1].get(),
                     self.db
                 )).grid(row=len(campos)+2, columnspan=2, pady=10)

    def registrar_tratamiento(self, id_animal, tipo, descripcion, tratamiento, db):
        try:
           id_animal = int(id_animal)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return
        
        veterinario = Veterinario(id=self.id_usuario)
        if veterinario.registrar_tratamiento(id_animal, tipo, descripcion, tratamiento, db):
            messagebox.showinfo("Éxito", "Tratamiento registrado")

    def pestana_registrar_vacuna(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre FROM Animal")
        animales = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
    
        tk.Label(pestana, text="ID del Animal:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.id_animal_vacuna = tk.Label(pestana, text="")
        self.id_animal_vacuna.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
        tk.Label(pestana, text="Animal:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        combobox_animal = ttk.Combobox(pestana, values=animales, state="readonly")
        combobox_animal.grid(row=1, column=1, padx=5, pady=5)
        combobox_animal.bind("<<ComboboxSelected>>", lambda e: self.id_animal_vacuna.config(
        text=combobox_animal.get().split(" - ")[0]))
        
        campos = [
            ("Animal:", ttk.Combobox(pestana, values=animales, state="readonly")),
            ("Tipo de Vacuna:", tk.Entry(pestana)),
            ("Próxima Aplicación (YYYY-MM-DD):", tk.Entry(pestana))
        ]
        
        for i, (etiqueta, widget) in enumerate(campos):
            tk.Label(pestana, text=etiqueta).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            widget.grid(row=i, column=1, padx=5, pady=5)
        
        tk.Button(pestana, text="Registrar", 
                 command=lambda: self.registrar_vacuna(
                     campos[0][1].get().split(" - ")[0],
                     campos[1][1].get(),
                     campos[2][1].get()
                 )).grid(row=len(campos), columnspan=2, pady=10)

    def registrar_vacuna(self, id_animal, vacuna, proxima_aplicacion):
        try:
            
            id_animal = int(id_animal)  # Convertir a entero
        except (ValueError, TypeError):
            messagebox.showerror("Error", "ID de animal inválido")
            return
       
        veterinario = Veterinario(id=self.id_usuario)
        if veterinario.registrar_vacuna(id_animal, vacuna, proxima_aplicacion, self.db):
            messagebox.showinfo("Éxito", "Vacuna registrada")

    def pestana_alertas_vacunas(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM Animal")
        animales = [id for (id,) in cursor.fetchall()]
        
        alertas = []
        veterinario = Veterinario(id=self.id_usuario)
        for id_animal in animales:
            alertas.extend(veterinario.generar_alerta_vacuna(id_animal, self.db))
        
        if not alertas:
            tk.Label(pestana, text="No hay alertas de vacunas próximas").pack(pady=20)
            return
        
        tk.Label(pestana, text="Animales con vacunas próximas a vencer:").pack(pady=10)
        
        for alerta in alertas:
            marco = tk.Frame(pestana, borderwidth=1, relief="groove", padx=10, pady=5)
            marco.pack(fill="x", padx=5, pady=2)
            
            tk.Label(marco, text=f"ID: {alerta[0]} - {alerta[1]}").pack(side="left")
            tk.Label(marco, text=alerta[2].split("\n")[1]).pack(side="right")

    def pestanas_administrador(self):
        pestanas = [
            ("Servicios", self.pestana_servicios),
            ("Reportes", self.pestana_reportes)
        ]
        
        for texto, comando in pestanas:
            pestana = ttk.Frame(self.cuaderno)
            self.cuaderno.add(pestana, text=texto)
            comando(pestana)

    def pestana_servicios(self, pestana):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre, precio FROM Servicio")
        servicios = cursor.fetchall()
        
        self.arbol_servicios = ttk.Treeview(pestana, columns=("ID", "Nombre", "Precio"), show="headings")
        self.arbol_servicios.heading("ID", text="ID")
        self.arbol_servicios.heading("Nombre", text="Nombre")
        self.arbol_servicios.heading("Precio", text="Precio")
        self.arbol_servicios.pack(fill="both", expand=True, padx=5, pady=5)
        
        for servicio in servicios:
            self.arbol_servicios.insert("", "end", values=servicio)
        
        marco_edicion = tk.Frame(pestana)
        marco_edicion.pack(fill="x", padx=5, pady=5)
        
        tk.Label(marco_edicion, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        entrada_nombre = tk.Entry(marco_edicion)
        entrada_nombre.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(marco_edicion, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
        entrada_precio = tk.Entry(marco_edicion)
        entrada_precio.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(marco_edicion, text="Agregar", 
                 command=lambda: self.agregar_servicio(
                     entrada_nombre.get(),
                     entrada_precio.get()
                 )).grid(row=2, column=0, padx=5, pady=5)
        
        tk.Button(marco_edicion, text="Actualizar", 
                 command=lambda: self.actualizar_servicio(
                     entrada_nombre.get(),
                     entrada_precio.get()
                 )).grid(row=2, column=1, padx=5, pady=5)

    def agregar_servicio(self, nombre, precio):
        cursor = self.db.conn.cursor()
        cursor.execute("INSERT INTO Servicio (nombre, precio) VALUES (?, ?)", (nombre, precio))
        self.db.conn.commit()
        self.actualizar_lista_servicios()

    def actualizar_servicio(self, nombre, precio):
        cursor = self.db.conn.cursor()
        cursor.execute("UPDATE Servicio SET precio = ? WHERE nombre = ?", (precio, nombre))
        self.db.conn.commit()
        self.actualizar_lista_servicios()

    def actualizar_lista_servicios(self):
        for item in self.arbol_servicios.get_children():
            self.arbol_servicios.delete(item)
        
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, nombre, precio FROM Servicio")
        for servicio in cursor.fetchall():
            self.arbol_servicios.insert("", "end", values=servicio)

    def pestana_reportes(self, pestana):
        tk.Button(pestana, text="Generar Reporte de Citas", 
                 command=self.generar_reporte_citas).pack(pady=10)
        
        tk.Button(pestana, text="Generar Reporte de Ingresos", 
                 command=self.generar_reporte_ingresos).pack(pady=10)

    def generar_reporte_citas(self):
        cursor = self.db.conn.cursor()
        cursor.execute("""
        SELECT c.id, a.nombre, c.fecha, s.nombre, v.nombre 
        FROM Cita c
        JOIN Animal a ON c.animal_id = a.id
        JOIN Servicio s ON c.servicio_id = s.id
        JOIN Veterinario v ON c.veterinario_id = v.id
        ORDER BY c.fecha DESC
        """)
        
        with open("reporte_citas.txt", "w") as f:
            f.write("=== Reporte de Citas ===\n\n")
            for cita in cursor.fetchall():
                f.write(f"ID: {cita[0]}\n")
                f.write(f"Animal: {cita[1]}\n")
                f.write(f"Fecha: {cita[2]}\n")
                f.write(f"Servicio: {cita[3]}\n")
                f.write(f"Veterinario: {cita[4]}\n")
                f.write("-" * 50 + "\n")
        
        messagebox.showinfo("Éxito", "Reporte de citas generado como 'reporte_citas.txt'")

    def generar_reporte_ingresos(self):
        cursor = self.db.conn.cursor()
        cursor.execute("""
        SELECT strftime('%Y-%m', p.fecha) AS mes, 
               SUM(p.monto) AS ingresos,
               COUNT(*) AS citas
        FROM Pago p
        GROUP BY mes
        ORDER BY mes
        """)
        
        with open("reporte_ingresos.txt", "w") as f:
            f.write("=== Reporte de Ingresos ===\n\n")
            f.write("Mes\t\tIngresos\tCitas\n")
            f.write("=" * 50 + "\n")
            for row in cursor.fetchall():
                f.write(f"{row[0]}\t${row[1]:.2f}\t\t{row[2]}\n")
        
        messagebox.showinfo("Éxito", "Reporte de ingresos generado como 'reporte_ingresos.txt'")

class Veterinaria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Veterinaria")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        
        self.db = Database()
        self.pantalla_login = PantallaLogin(self, self.db, self.mostrar_panel_principal)
    
    def mostrar_panel_principal(self, rol, id_usuario, nombre_usuario):
        for widget in self.winfo_children():
            widget.destroy()
        PanelPrincipal(self, self.db, rol, id_usuario, nombre_usuario)

if __name__ == "__main__":
    
    db = Database()
   
    app = Veterinaria()
    app.mainloop()