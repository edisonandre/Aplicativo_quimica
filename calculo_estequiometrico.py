from periodictable import formula

def masa_molar(compuesto):
    """Calcula la masa molar usando periodictable."""
    try:
        return formula(compuesto).mass
    except Exception:
        print("⚠ Error: compuesto no válido.")
        return None

nombre = input("Hola, ¿cómo te llamas? ").upper()

print(f"BIENVENIDO/A {nombre} AL PROGRAMAS DE CÁLCULOS ESTEQUIOMÉTRICOS\n")
print("Aqui podrás resolver tus problemas de químicas de forma rápida y sencilla ")

def calculo_estequiometrico():
    # Entrada de datos
    compuesto_origen = input("Ingrese el compuesto de origen (ej. H2O): ")
    masa_origen = float(input(f"Ingrese la masa de {compuesto_origen} en gramos: "))
    coef_origen = float(input(f"Ingrese el coeficiente estequiométrico de {compuesto_origen}: "))

    compuesto_objetivo = input("Ingrese el compuesto objetivo (ej. CO2): ")
    coef_objetivo = float(input(f"Ingrese el coeficiente estequiométrico de {compuesto_objetivo}: "))

    # Calcular masas molares
    mm_origen = masa_molar(compuesto_origen)
    mm_objetivo = masa_molar(compuesto_objetivo)

    if mm_origen is None or mm_objetivo is None:
        return

    # Conversión: regla de 3
    moles_origen = masa_origen / mm_origen
    moles_objetivo = moles_origen * (coef_objetivo / coef_origen)
    masa_objetivo = moles_objetivo * mm_objetivo

    # Resultado
    print("\n📊 Resultados:")
    print(f"Masa molar de {compuesto_origen}: {mm_origen:.2f} g/mol")
    print(f"Masa molar de {compuesto_objetivo}: {mm_objetivo:.2f} g/mol")
    print(f"Se producirán {masa_objetivo:.2f} g de {compuesto_objetivo}")

# Ejecutar
calculo_estequiometrico()
