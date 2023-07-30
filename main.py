import csv
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

class TiendaRopa:
    def __init__(self):
        self.inventario = {}

    def agregar_producto(self, codigo, nombre, precio, cantidad):
        producto = Producto(codigo, nombre, precio, cantidad)
        self.inventario[codigo] = producto
        print(Fore.GREEN + "Producto agregado exitosamente.")

    def producto_existe(self, codigo):
        return codigo in self.inventario

    def producto_existe(self, codigo):
        return codigo in self.inventario

    def vender_producto(self, codigo, cantidad):
        if codigo in self.inventario:
            producto = self.inventario[codigo]
            if producto.cantidad >= cantidad:
                producto.cantidad -= cantidad
                return producto.precio * cantidad
            else:
                print(Fore.RED + "No hay suficiente stock para completar la venta.")
        else:
            print(Fore.RED + "El producto no se encuentra en el inventario.")

    def verificar_inventario(self):
        print(Fore.CYAN + "\nInventario actual:")
        for producto in self.inventario.values():
            print(f"Código: {producto.codigo}, Nombre: {producto.nombre}, Precio: {producto.precio}, Cantidad: {producto.cantidad}")

    def guardar_venta_en_csv(self, codigo, cantidad, total_venta):
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("./data/ventas.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([fecha_hora, codigo, cantidad, total_venta])

    def guardar_inventario_en_csv(self):
        with open("./data/inventario.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Código", "Nombre", "Precio", "Cantidad"])
            for producto in self.inventario.values():
                writer.writerow([producto.codigo, producto.nombre, producto.precio, producto.cantidad])

    def cargar_inventario_desde_csv(self):
        try:
            with open("./data/inventario.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la primera fila que contiene las cabeceras
                for row in reader:
                    codigo, nombre, precio, cantidad = row
                    precio = float(precio)
                    cantidad = int(cantidad)
                    self.agregar_producto(codigo, nombre, precio, cantidad)
            print(Fore.GREEN + "Inventario cargado desde el archivo CSV.")
        except FileNotFoundError:
            print(Fore.RED + "No se encontró el archivo CSV de inventario.")

def main():
    tienda = TiendaRopa()
    tienda.cargar_inventario_desde_csv()

    while True:
        print(Fore.YELLOW + "\n" + "*" * 20)
        print(Fore.YELLOW + "Mar de Cores - Tienda de Ropa")
        print(Fore.YELLOW + "*" * 20)
        print("1. Agregar Producto")
        print("2. Registrar Venta")
        print("3. Verificar Inventario")
        print("4. Revisar Ventas Registradas")
        print("5. Editar Producto en Stock")
        print("6. Guardar Inventario en CSV")
        print("7. Salir")  # Salir ahora es la última opción

        opcion = input(Fore.WHITE + "Seleccione una opción (1/2/3/4/5/6/7): ")

        if opcion == "1":
            codigo = input("Ingrese el código del producto: ")
            if tienda.producto_existe(codigo):
                print(Fore.RED + "El producto ya existe en el inventario. No se puede agregar.")
            else:
                nombre = input("Ingrese el nombre del producto: ")
                precio = float(input("Ingrese el precio del producto: "))
                cantidad = int(input("Ingrese la cantidad del producto: "))
                tienda.agregar_producto(codigo, nombre, precio, cantidad)



        elif opcion == "2":
            codigo = input("Ingrese el código del producto a vender: ")
            cantidad = int(input("Ingrese la cantidad a vender: "))
            total_venta = tienda.vender_producto(codigo, cantidad)
            if total_venta:
                tienda.guardar_venta_en_csv(codigo, cantidad, total_venta)
                print(Fore.GREEN + f"Venta realizada. Total: {total_venta}")

        elif opcion == "3":
            tienda.verificar_inventario()

        elif opcion == "4":
            try:
                with open("./data/ventas.csv", mode="r") as file:
                    reader = csv.reader(file)
                    print(Fore.CYAN + "Ventas realizadas:")
                    for row in reader:
                        print(f"Fecha y Hora: {row[0]}, Código: {row[1]}, Cantidad: {row[2]}, Total Venta: {row[3]}")
            except FileNotFoundError:
                print("No se encontraron archivos CSV de ventas.")

        elif opcion == "5":
            codigo = input("Ingrese el código del producto a editar: ")
            if codigo in tienda.inventario:
                print(Fore.YELLOW + f"Información actual del producto (Código: {codigo}):")
                print(f"Nombre: {tienda.inventario[codigo].nombre}, Precio: {tienda.inventario[codigo].precio}, Cantidad: {tienda.inventario[codigo].cantidad}")
                nombre = input("Ingrese el nuevo nombre del producto: ")
                precio = float(input("Ingrese el nuevo precio del producto: "))
                cantidad = int(input("Ingrese la nueva cantidad del producto: "))
                tienda.agregar_producto(codigo, nombre, precio, cantidad)
            else:
                print(Fore.RED + "El producto no se encuentra en el inventario.")

        elif opcion == "6":
            tienda.guardar_inventario_en_csv()
            print(Fore.GREEN + "Inventario guardado en el archivo CSV.")

        elif opcion == "7":
            tienda.guardar_inventario_en_csv()  # Guardar el inventario antes de salir
            print(Fore.MAGENTA + "Gracias por utilizar la aplicación, Aldanita. ¡Nos Vemos en Brasil!")
            break

        else:
            print(Fore.RED + "Opción inválida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()