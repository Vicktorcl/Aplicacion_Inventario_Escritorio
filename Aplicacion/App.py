
from cProfile import label 
from tkinter import ttk
from tkinter import *

import sqlite3


class Product:
    
    db_name = "database.db"
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('Aplicación de productos')
    
        #Creando un frame contenedor
        frame = LabelFrame(self.wind, text= "Registra un nuevo producto")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        #Input de nombre
        Label(frame, text= "Nombre: ").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column= 1)
        
        #Input de precio
        Label(frame, text = "Precio: ").grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        
        # Botón para añadir un producto
        ttk.Button(frame, text = "Guardar Producto", command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)
        # Output de mensajes
        self.message = Label(text = "", fg = "red")
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        # Tabla 
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading("#0", text = "Nombre", anchor = CENTER)
        self.tree.heading("#1", text = "Precio", anchor = CENTER)
        
        # Botones
        ttk.Button(text = "Quitar", command = self.delete_product).grid(row = 5, column = 0, sticky= W + E)
        ttk.Button(text = "Editar", command = self.edit_product).grid(row = 5, column = 1, sticky= W + E)
        # Llenando las filas de las tablas
        self.get_products()
        
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_products(self):
        # Limpiando la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Consultando tabla 
        query = "SELECT * FROM product ORDER BY name DESC"
        db_rows = self.run_query(query)
        # Llenando datos
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
        
    def add_product(self):
        if self.validation():
            query = "INSERT INTO product VALUES(NULL, ?, ?)"
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message["text"] = "Producto {} se ha añadido exitosamente ".format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message["text"] = "Nombre y Precio requerido"
        self.get_products() 
        
    def delete_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona un registro"
            return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM product WHERE name = ?"
        self.run_query(query, (name, ))
        self.message["text"] = "Registro eliminado satisfactoriamente".format(name)
        self.get_products()
        
    def edit_product(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"] = "Por favor selecciona un registro"
            return
        name = self.tree.item(self.tree.selection())["text"]
        old_price = self.tree.item(self.tree.selection())["values"][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Editar Producto"
        
        # Nombre antiguo
        Label(self.edit_wind, text = "Nombre Antiguo: ").grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = "readonly").grid(row = 0, column = 2) 
        # Nombre nuevo
        Label(self.edit_wind, text = "Nombre Nuevo: ").grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2 )
        # Precio antiguo
        Label(self.edit_wind, text = "Precio Antiguo: ").grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = "readonly").grid(row = 2, column = 2)
        # Precio nuevo
        Label(self.edit_wind, text = "Precio Nuevo: ").grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)
        
        Button(self.edit_wind, text = "Actualizar", command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        
    def edit_records(self, new_name, name, new_price, old_price):
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?"
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message["text"] = "Registro {} actualizado correctamente".format(name)
        self.get_products()
        
        
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()