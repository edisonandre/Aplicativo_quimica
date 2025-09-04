from periodictable import formula
from tkinter import *


def masa_molar(compuesto):
    """Calcula la masa molar de un compuesto químico."""
    f = formula(compuesto)
    return f.mass

nombre = input("Hola, ¿cómo te llamas? ").capitalize()


def calcular():
    print("\n=== CÁLCULOS ESTEQUIOMÉTRICOS ===")
    print("Aqui podrás resolver tus problemas de químicas de forma rápida y sencilla \n")

    # Entrada de datos
    comp1 = input(f"{nombre} Por favor Ingrese el primer reactivo (ej: H2): ")
    masa1 = float(input(f"{nombre} Por favor ingrese la masa de {comp1} (g): "))
    comp2 = input(f"{nombre} Por favor ingrese el segundo reactivo (ej: O2): ")
    masa2 = float(input(f"{nombre} Por favor ingrese la masa de {comp2} (g): "))

    # Masas molares
    mm1 = masa_molar(comp1)
    mm2 = masa_molar(comp2)

    # Conversión a moles
    moles1 = masa1 / mm1
    moles2 = masa2 / mm2

    # Resultados finales
    print("\n=== RESULTADO FINAL ===")
    print(f"{moles1:.1f} mol de {comp1}")
    print(f"{moles2:.1f} mol de {comp2}")

def menu():
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Realizar un cálculo estequiométrico")
        print("2. Salir")
        
        opcion = input("Por favor Seleccione una opción: ")
        
        if opcion == "1":
            calcular()
        elif opcion == "2":
            print(f"¡Gracias por usar el programa! 😊 Deseo que vuelvas {nombre}")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()
