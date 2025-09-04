
"""
El objetivo de este archivo es:
  - Explicar línea a línea qué hace cada sección del código.
  - Señalar para qué sirve cada bloque en términos de diseño de interfaz.
  - Indicar puntos de integración / arquitectura si se quisiera conectar la UI
    con un sistema de robótica, visión o backend (por ejemplo ROS, servicios REST, etc.)
  - Mantener el mismo comportamiento funcional que la app original.

Notas de diseño (inspiración Tekniker):
  - Tekniker ha desarrollado plataformas móviles y soluciones de inspección para
    detección y tratamiento de plagas en invernaderos (GreenPatrol, robots con visión).
    Estas soluciones requieren separar la interfaz de usuario (UI) de la lógica de
    control y del procesamiento de visión/ML. (Ver documentación pública de Tekniker).
  - En este archivo se añaden secciones comentadas que muestran cómo pensar esa separación:
    * Frontend (Tkinter) -> solo interacción, validación y presentación de resultados.
    * Backend (módulo aparte) -> cálculos estequiométricos, balanceo, integración con sensores.
    * Integración con robot -> hooks/colas/servicios que la UI puede llamar (ej.: enviar payload JSON).

Ejecutar:
  python3 app_estequiometria_tk_documentado_tekniker.py

Autor: (tu nombre)
Fecha: 2025-09-03
"""

# ================================
# IMPORTACIONES
# ================================
# Aquí importamos las bibliotecas para construir la interfaz gráfica.
# Separación clara: todas las importaciones relacionadas con la UI están en este archivo.
import tkinter as tk                # Módulo base Tkinter: ventanas, eventos, widgets básicos
from tkinter import ttk, messagebox # ttk: widgets estilizados; messagebox: diálogos (alertas, info, error)

# ================================
# CONSTANTES DE CONFIGURACIÓN DE LA VENTANA
# ================================
# Estas constantes definen el aspecto inicial de la ventana.
# Diseño: mantener constantes al inicio facilita cambiar el layout global.
APP_TITLE = "Estequiometría - Interfaz (Tkinter) - Documentado"
APP_WIDTH = 740
APP_HEIGHT = 520

# ================================
# FUNCIÓN DE PROCESAMIENTO (BACKEND PROVISIONAL)
# ================================
def intentar_procesamiento(comp1: str, masa1: float, comp2: str, masa2: float) -> str:
    """
    Propósito:
      - Ejemplo de 'backend' sencillo que intenta calcular masas molares y moles.
      - En una arquitectura inspirada en Tekniker, esta función representaría
        una capa de cálculo que podría vivir en otro proceso/máquina.
    Diseño:
      - La UI NO debe implementar cálculos complejos; solo invoca funciones
        o servicios que encapsulan la lógica. Esto facilita pruebas y reemplazo
        por motores más avanzados (balanceo, reactivo limitante, visión química).
    Flujo:
      1. Intentar importar la librería `periodictable` (si está disponible).
      2. Si no está, devolver un mensaje claro que indique que el cálculo
         real se hará cuando el backend esté disponible.
      3. Si está disponible, calcular masa molar y moles (n = m / M).
    Parámetros:
      - comp1, comp2: fórmulas químicas como cadenas ("H2", "O2", "NaCl").
      - masa1, masa2: masas en gramos (float).
    Retorna:
      - Texto formateado con el resultado o un mensaje de error/amplio.
    """
    try:
        # IMPORTACIÓN LOCAL: se hace aquí para que la aplicación pueda arrancar
        # incluso si la librería no está instalada. Esto mantiene la UI aislada.
        from periodictable import formula
    except Exception:
        # Mensaje destilado y amigable para el usuario.
        return (
            "⚠️ Procesamiento en revisión:\n"
            "- La librería 'periodictable' no está disponible o el backend está pendiente.\n"
            "- La interfaz funciona, pero los cálculos finales se integrarán más adelante."
        )

    try:
        # Obtener masa molar (g/mol) a partir de la fórmula química
        mm1 = formula(comp1).mass
        mm2 = formula(comp2).mass

        # Validaciones sencillas: si alguna masa molar es inválida, se informa.
        if mm1 <= 0 or mm2 <= 0:
            raise ValueError("Masas molares no válidas.")

        # Cálculo de moles: n = m (g) / M (g/mol)
        moles1 = masa1 / mm1
        moles2 = masa2 / mm2

        # Preparar una salida de texto clara para la UI.
        return (
            "=== RESULTADO (provisional) ===\n"
            f"Reactivo 1: {comp1}\n"
            f" - Masa ingresada: {masa1:.6g} g\n"
            f" - Masa molar:     {mm1:.6g} g/mol\n"
            f" - Moles:          {moles1:.6g} mol\n\n"
            f"Reactivo 2: {comp2}\n"
            f" - Masa ingresada: {masa2:.6g} g\n"
            f" - Masa molar:     {mm2:.6g} g/mol\n"
            f" - Moles:          {moles2:.6g} mol\n\n"
            "Nota: Este cálculo es de referencia. El motor completo de procesamiento\n"
            "puede incorporar balanceo de ecuaciones, reactivo limitante, rendimientos, etc."
        )
    except Exception as e:
        # Mensaje de error útil para el usuario y para depuración.
        return f"Ocurrió un problema durante el cálculo provisional: {e}"

# ================================
# CLASE PRINCIPAL DE LA INTERFAZ (Vista)
# ================================
class App(tk.Tk):
    """
    Clase que representa la aplicación GUI completa.
    Diseño y responsabilidades:
      - Construcción de la ventana y widgets (entradas, botones, área de salida).
      - Validación mínima de entradas del usuario.
      - Orquestación: cuando el usuario pide 'Calcular' la UI llama al backend.
      - Mantener elementos de estado (por ejemplo var_status) para mostrar progreso.
    En un diseño más avanzado se recomienda:
      - Extraer los widgets en componentes más pequeños (clases o funciones).
      - Pasar un objeto 'backend' (inyección de dependencias) para permitir mocks
        y pruebas unitarias (por ejemplo: App(backend=my_backend)).
    """
    def __init__(self):
        # Inicializar la ventana principal (constructor de Tk)
        super().__init__()
        # Título de la ventana
        self.title(APP_TITLE)
        # Centrar la ventana y aplicar tamaño
        self._center_window(APP_WIDTH, APP_HEIGHT)
        # Aplicar estilos visuales (ttk themes y ajustes)
        self._apply_style()

        # Construcción del menú y widgets
        self._make_menubar()
        self._make_widgets()

        # Asociar la tecla Enter para activar "Calcular" y mejorar usabilidad
        self.bind("<Return>", lambda _: self.on_calcular())

    # -------------------------
    # UTILIDADES DE INTERFAZ
    # -------------------------
    def _center_window(self, w: int, h: int):
        """
        Calcular la posición para centrar la ventana en la pantalla.
        - update_idletasks(): asegura que las dimensiones y métricas estén actualizadas.
        - self.geometry(): define posición y tamaño.
        - self.minsize(): establece tamaño mínimo para evitar que la UI quede inutilizable.
        """
        self.update_idletasks()
        sw = self.winfo_screenwidth()   # ancho de la pantalla
        sh = self.winfo_screenheight()  # alto de la pantalla
        x = int((sw - w) / 2)
        y = int((sh - h) / 3)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.minsize(620, 440)

    def _apply_style(self):
        """
        Aplicar estilos básicos a widgets ttk:
        - Elegir un tema (si está disponible).
        - Configurar paddings y fuentes para mejorar legibilidad.
        Diseño UX:
        - Tipografía legible.
        - Espaciado consistente.
        - Etiquetas de cabecera y ayudas visuales.
        """
        style = ttk.Style(self)
        try:
            # 'clam' suele verse bien en diferentes sistemas; si falla, se ignora.
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Configuraciones generales de estilo
        style.configure("TButton", padding=8)
        style.configure("TLabel", padding=2)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Hint.TLabel", foreground="#555")
        style.configure("Card.TFrame", relief="groove", borderwidth=2)

    def _make_menubar(self):
        """
        Construir el menú superior:
         - Archivo -> Salir
         - Ayuda -> Acerca de
        Accesibilidad y UX:
         - Asociar atajos de teclado (Ctrl+Q) para cerrar la aplicación.
         - Mantener menús sencillos para no sobrecargar al usuario.
        """
        menubar = tk.Menu(self)

        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.on_salir, accelerator="Ctrl+Q")
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.on_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Configurar menubar en la ventana
        self.config(menu=menubar)
        # Asociar atajo global Ctrl+Q a la acción de salir
        self.bind_all("<Control-q>", lambda _: self.on_salir())

    def _make_widgets(self):
        """
        Crear y posicionar todos los widgets de la interfaz:
         - Contenedor principal con padding.
         - Secciones (labelframes) para: datos del usuario, reactivo 1, reactivo 2, botones y salida.
         - Campos de entrada ligados a variables StringVar (fácil lectura/escritura).
         - Botones con comandos directos (calcular, limpiar, salir).
        Diseño modular:
         - Cada 'tarjeta' (LabelFrame) es una sección lógica. Facilita migrar a
           otra librería (por ejemplo a una app web) porque la estructura está separada.
        """
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        # Permitir que la UI sea redimensionable de forma proporcionada
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # Encabezado y texto de ayuda
        ttk.Label(container, text="Cálculos Estequiométricos", style="Header.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(
            container,
            text="Interfaz de usuario en Tkinter. El procesamiento está en revisión.",
            style="Hint.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # -----------------------
        # Tarjeta: Datos del usuario
        # -----------------------
        card_user = ttk.LabelFrame(container, text="Datos del usuario")
        card_user.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=2, pady=6)
        for i in range(2):
            card_user.columnconfigure(i, weight=1)

        ttk.Label(card_user, text="Nombre:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        # StringVar es un contenedor que sincroniza el valor entre la UI y el código
        self.var_nombre = tk.StringVar()
        ttk.Entry(card_user, textvariable=self.var_nombre).grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        # -----------------------
        # Tarjeta: Reactivo 1
        # -----------------------
        card_r1 = ttk.LabelFrame(container, text="Reactivo 1")
        card_r1.grid(row=3, column=0, sticky="nsew", padx=(0, 4), pady=6)
        card_r1.columnconfigure(1, weight=1)

        ttk.Label(card_r1, text="Fórmula (ej: H2):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.var_comp1 = tk.StringVar()
        ttk.Entry(card_r1, textvariable=self.var_comp1).grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        ttk.Label(card_r1, text="Masa (g):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.var_masa1 = tk.StringVar()
        ttk.Entry(card_r1, textvariable=self.var_masa1).grid(row=1, column=1, sticky="ew", padx=6, pady=6)

        # -----------------------
        # Tarjeta: Reactivo 2
        # -----------------------
        card_r2 = ttk.LabelFrame(container, text="Reactivo 2")
        card_r2.grid(row=3, column=1, sticky="nsew", padx=(4, 0), pady=6)
        card_r2.columnconfigure(1, weight=1)

        ttk.Label(card_r2, text="Fórmula (ej: O2):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.var_comp2 = tk.StringVar()
        ttk.Entry(card_r2, textvariable=self.var_comp2).grid(row=0, column=1, sticky="ew", padx=6, pady=6)

        ttk.Label(card_r2, text="Masa (g):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.var_masa2 = tk.StringVar()
        ttk.Entry(card_r2, textvariable=self.var_masa2).grid(row=1, column=1, sticky="ew", padx=6, pady=6)

        # -----------------------
        # Botones de acción
        # -----------------------
        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2, sticky="ew", pady=6)
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)
        btns.columnconfigure(2, weight=1)

        # Botones enlazados a métodos: separación clara de responsabilidades
        ttk.Button(btns, text="Calcular", command=self.on_calcular).grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(btns, text="Limpiar", command=self.on_limpiar).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(btns, text="Salir", command=self.on_salir).grid(row=0, column=2, padx=6, pady=6, sticky="ew")

        # -----------------------
        # Área de resultados (con scrollbar)
        # -----------------------
        salida_frame = ttk.LabelFrame(container, text="Salida")
        salida_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=6)
        container.rowconfigure(5, weight=1)
        salida_frame.columnconfigure(0, weight=1)
        salida_frame.rowconfigure(0, weight=1)

        # Caja de texto para mostrar resultados. State=disabled evita edición directa.
        self.txt_salida = tk.Text(salida_frame, height=10, wrap="word", state="disabled")
        self.txt_salida.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(salida_frame, command=self.txt_salida.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.txt_salida.configure(yscrollcommand=scrollbar.set)

        # Barra de estado en la parte inferior: muestra mensajes breves de estado
        self.var_status = tk.StringVar(value="Listo.")
        status = ttk.Label(self, textvariable=self.var_status, anchor="w")
        status.grid(row=1, column=0, sticky="ew")

    # =======================
    # MÉTODOS: MENSAJES Y EVENTOS
    # =======================
    def on_acerca_de(self):
        """
        Mostrar un cuadro 'Acerca de' con información de la aplicación.
        En diseño: útil para incluir versión, autor y enlaces al backend/documentación.
        """
        messagebox.showinfo(
            "Acerca de",
            "Interfaz de usuario para cálculos estequiométricos.\n"
            "Versión documentada (inspirada en diseño Tekniker)."
        )

    def on_salir(self):
        """Cerrar la aplicación (liberar recursos)."""
        self.destroy()

    def on_limpiar(self):
        """
        Limpiar campos de entrada y agregar una nota en el área de salida.
        Diseño: mantener una acción clara que restablezca el estado de la UI.
        """
        self.var_comp1.set("")
        self.var_masa1.set("")
        self.var_comp2.set("")
        self.var_masa2.set("")
        self._append_salida("— Campos limpiados —\n")
        self.var_status.set("Campos limpios.")

    def _append_salida(self, text: str):
        """
        Añadir texto al widget de salida de forma segura:
        - Habilitar edición temporalmente.
        - Insertar texto y desplazar al final.
        - Volver a deshabilitar para evitar ediciones accidentales.
        Esto evita que el usuario modifique el histórico de resultados.
        """
        self.txt_salida.configure(state="normal")
        self.txt_salida.insert("end", text + ("\n" if not text.endswith("\n") else ""))
        self.txt_salida.see("end")
        self.txt_salida.configure(state="disabled")

    def _validar_float(self, value: str, nombre_campo: str) -> float:
        """
        Validar que la entrada es convertible a float.
        - Normalizar comas a punto.
        - Lanzar ValueError con mensaje claro si falla.
        Diseño: centralizar validaciones para mantener consistencia.
        """
        try:
            v = float(value)
            return v
        except ValueError:
            raise ValueError(f"El valor de '{nombre_campo}' debe ser numérico.")

    def on_calcular(self):
        """
        Orquestador principal cuando el usuario presiona 'Calcular':
          1. Leer valores desde StringVars.
          2. Validar que las fórmulas estén presentes.
          3. Validar que las masas sean numéricas.
          4. Mostrar un resumen en la salida.
          5. Llamar al backend de cálculo (intentar_procesamiento).
          6. Mostrar resultados y actualizar estado.
        Diseño para integración con sistemas de inspección/robótica:
          - En lugar de llamar directamente al cálculo local, la UI podría:
            a) Enviar los datos a un servicio REST (/compute) y recibir resultados.
            b) Publicar un mensaje en una cola (MQTT, RabbitMQ) para que el backend lo procese.
            c) Publicar un mensaje ROS si se integra con un robot (topic /compute_esteq).
        """
        nombre = self.var_nombre.get().strip()
        comp1 = self.var_comp1.get().strip()
        comp2 = self.var_comp2.get().strip()
        # Reemplazar comas por puntos para manejar decimales en locales que usan coma
        masa1_txt = self.var_masa1.get().strip().replace(",", ".")
        masa2_txt = self.var_masa2.get().strip().replace(",", ".")

        # Verificaciones de presencia mínima
        if not comp1 or not comp2:
            messagebox.showwarning("Datos incompletos", "Ingrese las fórmulas de ambos reactivos.")
            return

        # Validar que las masas sean números
        try:
            masa1 = self._validar_float(masa1_txt, "Masa (Reactivo 1)")
            masa2 = self._validar_float(masa2_txt, "Masa (Reactivo 2)")
        except ValueError as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        # Mostrar saludo opcional y resumen de entrada
        saludo = f"Hola {nombre}.\n" if nombre else ""
        self._append_salida(
            f"{saludo}=== CÁLCULOS ESTEQUIOMÉTRICOS ===\n"
            f"- Reactivo 1: {comp1}, masa: {masa1:.6g} g\n"
            f"- Reactivo 2: {comp2}, masa: {masa2:.6g} g\n"
        )

        # Feedback visual: cambiar estado y procesar
        self.var_status.set("Procesando...")
        self.update_idletasks()

        # Llamada al backend de cálculo (local en este ejemplo)
        resultado = intentar_procesamiento(comp1, masa1, comp2, masa2)
        self._append_salida(resultado + "\n")
        self.var_status.set("Listo.")

# ================================
# PUNTO DE ENTRADA (MAIN)
# ================================
def main():
    """
    Punto de entrada principal de la aplicación.
    Diseño: mantener la creación de la App en una función para facilitar pruebas.
    """
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
