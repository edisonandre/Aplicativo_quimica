#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App de interfaz (Tkinter) para cálculos estequiométricos.
- Este archivo se centra en la interacción con el usuario.
- El procesamiento está "en revisión". Si la librería `periodictable`
  está instalada, se hará un cálculo básico de moles como ejemplo.
  Si no, la interfaz sigue funcionando y mostrará un aviso.
"""

import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "Estequiometría - Interfaz (Tkinter)"
APP_WIDTH = 740
APP_HEIGHT = 520


def intentar_procesamiento(comp1: str, masa1: float, comp2: str, masa2: float) -> str:
    """
    Intenta realizar un cálculo básico (moles) si periodictable está disponible.
    Enfoque: interacción con el usuario; el backend definitivo puede cambiar.
    """
    try:
        from periodictable import formula  # opcional, sólo si está disponible
    except Exception:
        return (
            "⚠️ Procesamiento en revisión:\n"
            "- La librería 'periodictable' no está disponible o el backend está pendiente.\n"
            "- La interfaz funciona, pero los cálculos finales se integrarán más adelante."
        )

    try:
        mm1 = formula(comp1).mass
        mm2 = formula(comp2).mass
        if mm1 <= 0 or mm2 <= 0:
            raise ValueError("Masas molares no válidas.")

        moles1 = masa1 / mm1
        moles2 = masa2 / mm2

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
            "Nota: Este cálculo es de referencia. El motor completo de "
            "procesamiento puede incorporar balanceo de ecuaciones, reactivo "
            "limitante, rendimientos, etc. cuando esté aprobado."
        )
    except Exception as e:
        return f"Ocurrió un problema durante el cálculo provisional: {e}"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self._center_window(APP_WIDTH, APP_HEIGHT)
        self._apply_style()
        self.iconbitmap()

        self._make_menubar()
        self._make_widgets()
        self.bind("<Return>", lambda _: self.on_calcular())  # Enter -> Calcular

    def _center_window(self, w: int, h: int):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 3)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.minsize(620, 440)

    def _apply_style(self):
        style = ttk.Style(self)
        try:
            # En Windows, 'vista' o 'clam' suelen verse bien
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TButton", padding=8)
        style.configure("TLabel", padding=2)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Hint.TLabel", foreground="#555")
        style.configure("Card.TFrame", relief="groove", borderwidth=2)
        

    def _make_menubar(self):
        menubar = tk.Menu(self)
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.on_salir, accelerator="Ctrl+Q")
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=self.on_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=menubar)
        self.bind_all("<Control-q>", lambda _: self.on_salir())

    def _make_widgets(self):
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # Encabezado
        ttk.Label(container, text="Cálculos Estequiométricos", style="Header.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(
            container,
            text="Interfaz de usuario en Tkinter. El procesamiento está en revisión.",
            style="Hint.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Tarjeta: Datos del usuario
        card_user = ttk.LabelFrame(container, text="Datos del usuario")
        card_user.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=2, pady=6)
        for i in range(2):
            card_user.columnconfigure(i, weight=1)

        ttk.Label(card_user, text="Nombre:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.var_nombre = tk.StringVar()
        
        # Tarjeta: Reactivo 1
        card_r1 = ttk.LabelFrame(container, text="Reactivo 1")
        card_r1.grid(row=3, column=0, sticky="nsew", padx=(0, 4), pady=6)
        card_r1.columnconfigure(1, weight=1)

        ttk.Label(card_r1, text="Fórmula (ej: H2):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.var_comp1 = tk.StringVar()
        
        ttk.Label(card_r1, text="Masa (g):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.var_masa1 = tk.StringVar()
        
        # Tarjeta: Reactivo 2
        card_r2 = ttk.LabelFrame(container, text="Reactivo 2")
        card_r2.grid(row=3, column=1, sticky="nsew", padx=(4, 0), pady=6)
        card_r2.columnconfigure(1, weight=1)

        ttk.Label(card_r2, text="Fórmula (ej: O2):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.var_comp2 = tk.StringVar()
        
        ttk.Label(card_r2, text="Masa (g):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.var_masa2 = tk.StringVar()
        
        # Botones de acción
        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2, sticky="ew", pady=6)
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)
        btns.columnconfigure(2, weight=1)

        
        # Resultado / consola
        salida_frame = ttk.LabelFrame(container, text="Salida")
        salida_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=6)
        container.rowconfigure(5, weight=1)
        salida_frame.columnconfigure(0, weight=1)
        salida_frame.rowconfigure(0, weight=1)

        self.txt_salida = tk.Text(salida_frame, height=10, wrap="word", state="disabled")
        self.txt_salida.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(salida_frame, command=self.txt_salida.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.txt_salida.configure(yscrollcommand=scrollbar.set)

        # Barra de estado
        self.var_status = tk.StringVar(value="Listo.")
        

    # ======================= Eventos / utilidades =======================

    def on_acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Interfaz de usuario para cálculos estequiométricos.\n"
            "Desarrollado con Tkinter (solo interacción)."
        )

    def on_salir(self):
        self.destroy()
#limpia todos los datos ingresados
    def on_limpiar(self):
        self.var_comp1.set("")
        self.var_masa1.set("")
        self.var_comp2.set("")
        self.var_masa2.set("")
        self._append_salida("— Campos limpiados —\n")
        self.var_status.set("Campos limpios.")

    def _append_salida(self, text: str):
        self.txt_salida.configure(state="normal")
        self.txt_salida.insert("end", text + ("\n" if not text.endswith("\n") else ""))
        self.txt_salida.see("end")
        self.txt_salida.configure(state="disabled")

    def _validar_float(self, value: str, nombre_campo: str) -> float:
        try:
            v = float(value)
            return v
        except ValueError:
            raise ValueError(f"El valor de '{nombre_campo}' debe ser numérico.")

    def on_calcular(self):
        nombre = self.var_nombre.get().strip()
        comp1 = self.var_comp1.get().strip()
        comp2 = self.var_comp2.get().strip()
        masa1_txt = self.var_masa1.get().strip().replace(",", ".")
        masa2_txt = self.var_masa2.get().strip().replace(",", ".")

        if not comp1 or not comp2:
            messagebox.showwarning("Datos incompletos", "Ingrese las fórmulas de ambos reactivos.")
            return

        try:
            masa1 = self._validar_float(masa1_txt, "Masa (Reactivo 1)")
            masa2 = self._validar_float(masa2_txt, "Masa (Reactivo 2)")
        except ValueError as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        saludo = f"Hola {nombre}.\n" if nombre else ""
        self._append_salida(
            f"{saludo}=== CÁLCULOS ESTEQUIOMÉTRICOS ===\n"
            f"- Reactivo 1: {comp1}, masa: {masa1:.6g} g\n"
            f"- Reactivo 2: {comp2}, masa: {masa2:.6g} g\n"
        )

        self.var_status.set("Procesando...")
        self.update_idletasks()

        # Intento de procesamiento provisional (opcional)
        resultado = intentar_procesamiento(comp1, masa1, comp2, masa2)
        self._append_salida(resultado + "\n")
        self.var_status.set("Listo.")

def main():
    app = App()
    app.mainloop()



if __name__ == "__main__":
    main()
