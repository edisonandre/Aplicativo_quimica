from chempy.chemistry import balance_stoichiometry

from periodictable import formula

def masa_molar(compuesto):
    """Calcula la masa molar de un compuesto químico."""
    f = formula(compuesto)
    return f.mass

decicion = input("BIENVENID@S Deceas continuar con el programa (CALCULOS_ESTEQUIOMETRICOS)").lower()

while decicion == "si":
    
    nombre = input("Hola, ¿cómo te llamas? ").upper()

    print(f"BIENVENIDO/A {nombre} AL PROGRAMAS DE CÁLCULOS ESTEQUIOMÉTRICOS\n")
    print("Aqui podrás resolver tus problemas de químicas de forma rápida y sencilla ")
    def calcular():
        # Entrada de datos
        reaccion = input("Ingrese la reacción química (ej: H2 + O2 -> H2O): ")
        compuesto_origen = input("ingrese el Compuesto de origen: ")
        masa_origen = float(input("ingrese la masa del compuesto origen (g): "))
        compuesto_objetivo = input("ingrese el Compuesto objetivo: ")
    
        # Proceso: balanceo
        reac, prod = balance_stoichiometry(
            *[s.split(' + ') for s in reaccion.split(' -> ')]
        )
    
        # Coeficientes estequiométricos
        coef_origen = reac.get(compuesto_origen, prod.get(compuesto_origen))
        coef_objetivo = reac.get(compuesto_objetivo, prod.get(compuesto_objetivo))
    
        # Masas molares
        mm_origen = masa_molar(compuesto_origen)
        mm_objetivo = masa_molar(compuesto_objetivo)
    
        # Conversión: regla de 3
        moles_origen = masa_origen / mm_origen
        moles_objetivo = moles_origen * (coef_objetivo / coef_origen)
        masa_objetivo = moles_objetivo * mm_objetivo
    
        # Resultado
        print(f"\nResultados:")
        print(f"Masa molar {compuesto_origen}: {mm_origen:.2f} g/mol")
        print(f"Masa molar {compuesto_objetivo}: {mm_objetivo:.2f} g/mol")
        print(f"Masa obtenida de {compuesto_objetivo}: {masa_objetivo:.2f} g\n")
    if __name__ == "__main__":
        calcular()
        
    decicion = input("Deseas ingresar otras reacciones quimicas").lower()
    if decicion == "no":
        break


