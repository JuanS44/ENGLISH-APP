# -*- coding: utf-8 -*-
"""
ENGLISH EXPLORERS — UTB EDITION 🏆
===============================================================================
Aplicación Educativa Interactiva Gamificada de Alto Impacto Visual.
Soporte para Imagen Oficial: utb_logotipo.png
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from PIL import Image, ImageTk  # Carga y escalado de imágenes

import db_manager as db
import questions_db as qdb

# =============================================================================
# PALETA DE COLORES Y SISTEMA DE DISEÑO (DARK GAMING & UTB BRANDING)
# =============================================================================
COLOR_BG_MAIN = "#0B0F19"         # Fondo general Azul Abismo
COLOR_BG_CARD = "#151C2C"         # Superficie de tarjeta
COLOR_BG_CARD_HOVER = "#1E293B"   # Tarjeta iluminada
COLOR_BORDER = "#2A364F"          # Bordes neutros

COLOR_UTB_BLUE = "#0284C7"        # Azul Institucional UTB
COLOR_UTB_CYAN = "#38BDF8"        # Cían Neón
COLOR_UTB_GOLD = "#F59E0B"        # Dorado UTB
COLOR_UTB_AMBER = "#FBBF24"       # Ámbar de Acierto / XP

COLOR_SUCCESS = "#10B981"         # Verde Esmeralda Acierto
COLOR_ERROR = "#EF4444"           # Rojo Coral Error
COLOR_TEXT_WHITE = "#F8FAFC"      # Texto Principal
COLOR_TEXT_MUTED = "#94A3B8"      # Texto Secundario

# =============================================================================
# GESTOR DE IMAGEN / LOGO UTB
# =============================================================================
LOGO_PATH = "utb_logotipo.png"

def load_utb_logo(size=(50, 50)):
    """Carga y escala la imagen utb_logotipo.png de forma segura."""
    if os.path.exists(LOGO_PATH):
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return None
    return None


# =============================================================================
# MOTOR DE RENDERIZADO VISUAL (CUSTOM CANVAS)
# =============================================================================

class CustomRoundedCard(tk.Canvas):
    """Tarjeta contenedora con soporte para bordes suaves y sombras."""
    def __init__(self, parent, width=400, height=200, radius=20, bg_color=COLOR_BG_CARD,
                 border_color=COLOR_BORDER, border_width=2, cursor="", command=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"),
                         highlightthickness=0, cursor=cursor, **kwargs)
        self.w = width
        self.h = height
        self.radius = radius
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.command = command
        self.is_hovered = False

        self.bind("<Configure>", self._on_resize)
        if self.command:
            self.bind("<Button-1>", lambda e: self.command())
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)

        self.draw()

    def _on_resize(self, event):
        self.w = event.width
        self.h = event.height
        self.draw()

    def _on_enter(self, e):
        self.is_hovered = True
        self.draw()

    def _on_leave(self, e):
        self.is_hovered = False
        self.draw()

    def draw(self):
        self.delete("all")
        r = self.radius
        w, h = self.w, self.h
        
        current_bg = COLOR_BG_CARD_HOVER if (self.is_hovered and self.command) else self.bg_color
        current_border = COLOR_UTB_CYAN if self.is_hovered else self.border_color

        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=current_bg, outline="")
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=current_bg, outline="")
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=current_bg, outline="")
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=current_bg, outline="")

        self.create_rectangle((r, 0, w-r, h), fill=current_bg, outline="")
        self.create_rectangle((0, r, w, h-r), fill=current_bg, outline="")

        bw = self.border_width
        if bw > 0:
            self.create_arc((bw, bw, 2*r, 2*r), start=90, extent=90, style="arc", outline=current_border, width=bw)
            self.create_arc((w-2*r, bw, w-bw, 2*r), start=0, extent=90, style="arc", outline=current_border, width=bw)
            self.create_arc((bw, h-2*r, 2*r, h-bw), start=180, extent=90, style="arc", outline=current_border, width=bw)
            self.create_arc((w-2*r, h-2*r, w-bw, h-bw), start=270, extent=90, style="arc", outline=current_border, width=bw)

            self.create_line((r, bw, w-r, bw), fill=current_border, width=bw)
            self.create_line((r, h-bw, w-r, h-bw), fill=current_border, width=bw)
            self.create_line((bw, r, bw, h-r), fill=current_border, width=bw)
            self.create_line((w-bw, r, w-bw, h-r), fill=current_border, width=bw)


class ModernProgressBar(tk.Canvas):
    """Barra de progreso animada de alto impacto visual."""
    def __init__(self, parent, width=300, height=16, bg_color="#1E293B", fill_color=COLOR_UTB_CYAN):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0)
        self.w = width
        self.h = height
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.progress = 0.0
        self.draw()

    def set_progress(self, value):
        self.progress = max(0.0, min(1.0, value))
        self.draw()

    def draw(self):
        self.delete("all")
        w, h = self.w, self.h

        self.create_rectangle(0, 0, w, h, fill=self.bg_color, outline="")
        fill_w = w * self.progress
        if fill_w > 0:
            self.create_rectangle(0, 0, fill_w, h, fill=self.fill_color, outline="")
            self.create_line(0, 2, fill_w, 2, fill="#7DD3FC", width=1)


class InteractiveOptionWidget(tk.Canvas):
    """Tarjeta de Respuesta Gamificada."""
    def __init__(self, parent, text, index, callback, width=650, height=65):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0, cursor="hand2")
        self.w = width
        self.h = height
        self.text = text
        self.index = index
        self.callback = callback
        self.state = "normal"
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.draw()

    def set_state(self, state):
        self.state = state
        self.draw()

    def _on_enter(self, e):
        if self.state == "normal":
            self.state = "hover"
            self.draw()

    def _on_leave(self, e):
        if self.state == "hover":
            self.state = "normal"
            self.draw()

    def _on_click(self, e):
        self.callback(self.index)

    def draw(self):
        self.delete("all")
        w, h = self.w, self.h
        
        bg = COLOR_BG_CARD
        border = COLOR_BORDER
        badge_bg = COLOR_UTB_BLUE
        badge_fg = COLOR_TEXT_WHITE
        txt_fg = COLOR_TEXT_WHITE

        if self.state == "hover":
            bg = COLOR_BG_CARD_HOVER
            border = COLOR_UTB_CYAN
            badge_bg = COLOR_UTB_CYAN
            badge_fg = COLOR_BG_MAIN
        elif self.state == "selected":
            bg = "#0C4A6E"
            border = COLOR_UTB_GOLD
            badge_bg = COLOR_UTB_GOLD
            badge_fg = COLOR_BG_MAIN
        elif self.state == "correct":
            bg = "#064E3B"
            border = COLOR_SUCCESS
            badge_bg = COLOR_SUCCESS
            badge_fg = COLOR_TEXT_WHITE
        elif self.state == "wrong":
            bg = "#7F1D1D"
            border = COLOR_ERROR
            badge_bg = COLOR_ERROR
            badge_fg = COLOR_TEXT_WHITE

        r = 12
        self.create_rectangle(r, 0, w-r, h, fill=bg, outline="")
        self.create_rectangle(0, r, w, h-r, fill=bg, outline="")
        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=bg, outline="")
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=bg, outline="")
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=bg, outline="")
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=bg, outline="")

        self.create_line(r, 1, w-r, 1, fill=border, width=2)
        self.create_line(r, h-1, w-r, h-1, fill=border, width=2)
        self.create_line(1, r, 1, h-r, fill=border, width=2)
        self.create_line(w-1, r, w-1, h-r, fill=border, width=2)

        letter = chr(65 + self.index)
        bx, by, bw_size = 20, (h // 2) - 16, 32
        self.create_rectangle(bx, by, bx + bw_size, by + bw_size, fill=badge_bg, outline="")
        self.create_text(bx + bw_size/2, by + bw_size/2, text=letter, font=("Segoe UI", 11, "bold"), fill=badge_fg)

        self.create_text(70, h // 2, text=self.text, font=("Segoe UI", 11, "bold"), fill=txt_fg, anchor="w")


# =============================================================================
# APLICACIÓN PRINCIPAL (ENGLISH EXPLORERS UTB)
# =============================================================================

class EnglishExplorersApp(tk.Tk):
    """Controlador principal de la ventana y rutas de la app."""
    
    def __init__(self):
        super().__init__()
        self.title("ENGLISH EXPLORERS — Universidad Tecnológica de Bolívar 🏆")
        self.geometry("1180x820")
        self.minsize(1024, 720)
        self.configure(bg=COLOR_BG_MAIN)

        db.init_db()
        self.current_user = None

        # Caché de imágenes
        self.img_navbar = load_utb_logo((50, 50))
        self.img_large = load_utb_logo((90, 90))

        # Contenedor dinámico de vistas
        self.main_container = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.main_container.pack(fill="both", expand=True)

        self.show_login()

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # -------------------------------------------------------------------------
    # NAVBAR INSTITUCIONAL CON LOGO REAL
    # -------------------------------------------------------------------------
    def draw_navbar(self, title_sub="PLATAFORMA INSTITUCIONAL"):
        nav = tk.Frame(self.main_container, bg="#030712", height=75)
        nav.pack(fill="x", side="top")

        brand_box = tk.Frame(nav, bg="#030712")
        brand_box.pack(side="left", padx=25, pady=10)

        # Muestra el Logo en la barra si está disponible
        if self.img_navbar:
            lbl_logo = tk.Label(brand_box, image=self.img_navbar, bg="#030712")
            lbl_logo.pack(side="left", padx=(0, 15))

        title_box = tk.Frame(brand_box, bg="#030712")
        title_box.pack(side="left")

        tk.Label(title_box, text="ENGLISH EXPLORERS", font=("Segoe UI", 13, "bold"), fg=COLOR_TEXT_WHITE, bg="#030712").pack(anchor="w")
        tk.Label(title_box, text=f"UTB • {title_sub}", font=("Segoe UI", 8, "bold"), fg=COLOR_UTB_GOLD, bg="#030712").pack(anchor="w")

        if self.current_user:
            user_box = tk.Frame(nav, bg="#030712")
            user_box.pack(side="right", padx=25)

            role_str = "👨‍🏫 Docente" if self.current_user[3] == "docente" else f"🎓 Grado {self.current_user[4]}°"
            
            info_frame = tk.Frame(user_box, bg="#030712")
            info_frame.pack(side="left", padx=(0, 15))
            
            tk.Label(info_frame, text=self.current_user[2], font=("Segoe UI", 10, "bold"), fg=COLOR_TEXT_WHITE, bg="#030712", anchor="e").pack(anchor="e")
            tk.Label(info_frame, text=role_str, font=("Segoe UI", 8), fg=COLOR_UTB_CYAN, bg="#030712", anchor="e").pack(anchor="e")

            btn_logout = tk.Button(
                user_box, text="Salir 🚪", font=("Segoe UI", 9, "bold"), bg="#1F2937", fg=COLOR_ERROR,
                activebackground=COLOR_ERROR, activeforeground="white", relief="flat", cursor="hand2",
                command=self.show_login
            )
            btn_logout.pack(side="right", ipady=4, ipadx=10)

    # -------------------------------------------------------------------------
    # VISTA: INICIO DE SESIÓN
    # -------------------------------------------------------------------------
    def show_login(self):
        self.current_user = None
        self.clear_container()
        self.draw_navbar("ACCESO DE USUARIOS")

        body = tk.Frame(self.main_container, bg=COLOR_BG_MAIN)
        body.pack(fill="both", expand=True)

        card_w, card_h = 440, 510
        card_frame = tk.Frame(body, bg=COLOR_BG_MAIN)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        card_bg = CustomRoundedCard(card_frame, width=card_w, height=card_h, radius=24, bg_color=COLOR_BG_CARD, border_color=COLOR_UTB_BLUE, border_width=2)
        card_bg.pack()

        content = tk.Frame(card_bg, bg=COLOR_BG_CARD, padx=30, pady=25)
        content.place(x=0, y=0, width=card_w, height=card_h)

        # Muestra el Logo grande de la UTB
        if self.img_large:
            lbl_large_logo = tk.Label(content, image=self.img_large, bg=COLOR_BG_CARD)
            lbl_large_logo.pack(pady=(0, 10))

        tk.Label(content, text="¡Bienvenido Explorer!", font=("Segoe UI", 16, "bold"), fg=COLOR_TEXT_WHITE, bg=COLOR_BG_CARD).pack()
        tk.Label(content, text="Ingresa tus credenciales para continuar", font=("Segoe UI", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_CARD).pack(pady=(0, 15))

        tk.Label(content, text="Usuario", font=("Segoe UI", 9, "bold"), fg=COLOR_UTB_CYAN, bg=COLOR_BG_CARD).pack(anchor="w")
        ent_user = tk.Entry(content, font=("Segoe UI", 11), bg="#0B0F19", fg="white", insertbackground="white", relief="flat")
        ent_user.pack(fill="x", pady=(4, 12), ipady=8)

        tk.Label(content, text="Contraseña", font=("Segoe UI", 9, "bold"), fg=COLOR_UTB_CYAN, bg=COLOR_BG_CARD).pack(anchor="w")
        ent_pass = tk.Entry(content, font=("Segoe UI", 11), show="*", bg="#0B0F19", fg="white", insertbackground="white", relief="flat")
        ent_pass.pack(fill="x", pady=(4, 20), ipady=8)

        def do_login():
            u = db.authenticate_user(ent_user.get().strip(), ent_pass.get().strip())
            if u:
                self.current_user = u
                if u[3] == "docente":
                    self.show_teacher_dashboard()
                else:
                    self.show_student_home()
            else:
                messagebox.showerror("Error de Acceso", "Usuario o contraseña incorrectos.")

        btn_login = tk.Button(content, text="INICIAR SESIÓN 🚀", font=("Segoe UI", 10, "bold"), bg=COLOR_UTB_BLUE, fg="white", activebackground=COLOR_UTB_CYAN, relief="flat", cursor="hand2", command=do_login)
        btn_login.pack(fill="x", pady=(5, 8), ipady=8)

        btn_reg = tk.Button(content, text="¿No tienes cuenta? Regístrate aquí", font=("Segoe UI", 9, "bold"), bg="#1E293B", fg=COLOR_TEXT_WHITE, activebackground="#334155", relief="flat", cursor="hand2", command=self.show_register)
        btn_reg.pack(fill="x", ipady=6)

    # -------------------------------------------------------------------------
    # VISTA: REGISTRO DE ESTUDIANTES
    # -------------------------------------------------------------------------
    def show_register(self):
        self.clear_container()
        self.draw_navbar("REGISTRO DE ESTUDIANTES")

        body = tk.Frame(self.main_container, bg=COLOR_BG_MAIN)
        body.pack(fill="both", expand=True)

        card_w, card_h = 480, 540
        card_frame = tk.Frame(body, bg=COLOR_BG_MAIN)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        card_bg = CustomRoundedCard(card_frame, width=card_w, height=card_h, radius=24, bg_color=COLOR_BG_CARD, border_color=COLOR_UTB_GOLD, border_width=2)
        card_bg.pack()

        content = tk.Frame(card_bg, bg=COLOR_BG_CARD, padx=35, pady=25)
        content.place(x=0, y=0, width=card_w, height=card_h)

        tk.Label(content, text="📝 Registro de Nuevo Estudiante", font=("Segoe UI", 15, "bold"), fg=COLOR_UTB_GOLD, bg=COLOR_BG_CARD).pack(pady=(0, 15))

        fields = [("Nombre Completo:", "ent_name"), ("Usuario Único:", "ent_user"), ("Contraseña:", "ent_pass")]
        entries = {}

        for label_text, var_name in fields:
            tk.Label(content, text=label_text, font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_WHITE, bg=COLOR_BG_CARD).pack(anchor="w")
            show_char = "*" if var_name == "ent_pass" else ""
            ent = tk.Entry(content, font=("Segoe UI", 10), bg="#0B0F19", fg="white", insertbackground="white", relief="flat", show=show_char)
            ent.pack(fill="x", pady=(2, 10), ipady=6)
            entries[var_name] = ent

        tk.Label(content, text="Grado Escolar (Mineducación):", font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_WHITE, bg=COLOR_BG_CARD).pack(anchor="w")
        combo_grade = ttk.Combobox(content, values=[f"Grado {i}°" for i in range(1, 12)], state="readonly", font=("Segoe UI", 10))
        combo_grade.current(0)
        combo_grade.pack(fill="x", pady=(2, 20))

        def do_register():
            name = entries["ent_name"].get().strip()
            user = entries["ent_user"].get().strip()
            pwd = entries["ent_pass"].get().strip()
            grade = combo_grade.current() + 1

            if not name or not user or not pwd:
                messagebox.showwarning("Campos Incompletos", "Por favor completa todos los datos.")
                return

            ok, msg = db.register_user(user, pwd, name, 'estudiante', grade)
            if ok:
                messagebox.showinfo("¡Registro Exitoso! 🏆", f"¡Bienvenido/a {name}!\nTu cuenta ha sido creada exitosamente.")
                self.current_user = db.authenticate_user(user, pwd)
                self.show_student_home()
            else:
                messagebox.showerror("Error", msg)

        btn_reg = tk.Button(content, text="CREAR CUENTA Y EMPEZAR ⚡", font=("Segoe UI", 10, "bold"), bg=COLOR_SUCCESS, fg="white", activebackground="#059669", relief="flat", cursor="hand2", command=do_register)
        btn_reg.pack(fill="x", pady=(5, 6), ipady=8)

        btn_back = tk.Button(content, text="⬅ Volver al Login", font=("Segoe UI", 9), bg="#1E293B", fg=COLOR_TEXT_WHITE, relief="flat", cursor="hand2", command=self.show_login)
        btn_back.pack(fill="x", ipady=6)

    # -------------------------------------------------------------------------
    # VISTA: PANEL DEL ESTUDIANTE
    # -------------------------------------------------------------------------
    def show_student_home(self):
        self.clear_container()
        self.draw_navbar("RUTA DE APRENDIZAJE")

        body = tk.Frame(self.main_container, bg=COLOR_BG_MAIN, padx=40, pady=20)
        body.pack(fill="both", expand=True)

        grade = self.current_user[4]
        data = qdb.CURRICULUM.get(grade, qdb.CURRICULUM[1])

        header_card = CustomRoundedCard(body, width=1100, height=100, radius=18, bg_color=COLOR_BG_CARD, border_color=COLOR_UTB_GOLD, border_width=2)
        header_card.pack(fill="x", pady=(0, 20))

        header_content = tk.Frame(header_card, bg=COLOR_BG_CARD, padx=25, pady=15)
        header_content.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(header_content, text=f"{data['emoji']} {data['title']}", font=("Segoe UI", 16, "bold"), fg=COLOR_UTB_GOLD, bg=COLOR_BG_CARD).pack(anchor="w")
        tk.Label(header_content, text=f"Estándar Curricular MEN: {qdb.GRADE_REFERENCE.get(grade, 'A1-A2')}", font=("Segoe UI", 10), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_CARD).pack(anchor="w")

        tk.Label(body, text="SELECCIONA TU DESAFÍO DE HOY", font=("Segoe UI", 11, "bold"), fg=COLOR_UTB_CYAN, bg=COLOR_BG_MAIN).pack(anchor="w", pady=(0, 10))

        units_frame = tk.Frame(body, bg=COLOR_BG_MAIN)
        units_frame.pack(fill="both", expand=True)

        for idx, (unit_name, desc) in enumerate(data["units"], start=1):
            unit_card = CustomRoundedCard(
                units_frame, width=1050, height=90, radius=16, bg_color=COLOR_BG_CARD,
                border_color=COLOR_BORDER, border_width=1, cursor="hand2",
                command=lambda u=idx: self.start_quiz(grade, u)
            )
            unit_card.pack(fill="x", pady=8)

            uc_frame = tk.Frame(unit_card, bg=COLOR_BG_CARD, padx=20, pady=15)
            uc_frame.place(x=0, y=0, relwidth=1, relheight=1)

            num_box = tk.Frame(uc_frame, bg=COLOR_UTB_BLUE, width=40, height=40)
            num_box.pack(side="left", padx=(0, 15))
            num_box.pack_propagate(False)
            tk.Label(num_box, text=str(idx), font=("Segoe UI", 12, "bold"), fg="white", bg=COLOR_UTB_BLUE).pack(expand=True)

            info_box = tk.Frame(uc_frame, bg=COLOR_BG_CARD)
            info_box.pack(side="left", fill="both", expand=True)
            tk.Label(info_box, text=f"UNIDAD {idx}: {unit_name}", font=("Segoe UI", 12, "bold"), fg=COLOR_TEXT_WHITE, bg=COLOR_BG_CARD).pack(anchor="w")
            tk.Label(info_box, text=desc, font=("Segoe UI", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_CARD).pack(anchor="w")

            btn_play = tk.Button(uc_frame, text="¡JUGAR AHORA! ⚡", font=("Segoe UI", 10, "bold"), bg=COLOR_SUCCESS, fg="white", activebackground="#059669", relief="flat", cursor="hand2", command=lambda u=idx: self.start_quiz(grade, u))
            btn_play.pack(side="right", ipadx=15, ipady=6)

    # -------------------------------------------------------------------------
    # VISTA: INTERFAZ INTERACTIVA DEL QUIZ
    # -------------------------------------------------------------------------
    def start_quiz(self, grade, unit):
        questions = qdb.QUESTION_BANK.get(grade, qdb.QUESTION_BANK[1])
        selected_q = random.sample(questions, min(2, len(questions)))
        
        q_idx = 0
        score = 0

        def render_question():
            nonlocal q_idx, score
            self.clear_container()
            self.draw_navbar("DESAFÍO EN LÍNEA")

            if q_idx >= len(selected_q):
                xp_gained = score * 25
                db.save_score(self.current_user[0], grade, unit, score, len(selected_q), xp_gained)

                res_body = tk.Frame(self.main_container, bg=COLOR_BG_MAIN)
                res_body.pack(fill="both", expand=True)

                card_w, card_h = 520, 480
                c_frame = tk.Frame(res_body, bg=COLOR_BG_MAIN)
                c_frame.place(relx=0.5, rely=0.5, anchor="center")

                c_card = CustomRoundedCard(c_frame, width=card_w, height=card_h, radius=24, bg_color=COLOR_BG_CARD, border_color=COLOR_UTB_GOLD, border_width=3)
                c_card.pack()

                c_content = tk.Frame(c_card, bg=COLOR_BG_CARD, padx=35, pady=25)
                c_content.place(x=0, y=0, width=card_w, height=card_h)

                if self.img_large:
                    lbl_logo = tk.Label(c_content, image=self.img_large, bg=COLOR_BG_CARD)
                    lbl_logo.pack(pady=(0, 10))

                tk.Label(c_content, text="🏆 ¡DESAFÍO COMPLETADO!", font=("Segoe UI", 16, "bold"), fg=COLOR_UTB_GOLD, bg=COLOR_BG_CARD).pack(pady=5)
                tk.Label(c_content, text=f"Puntuación Obtenida: {score} de {len(selected_q)} correctas", font=("Segoe UI", 12), fg=COLOR_TEXT_WHITE, bg=COLOR_BG_CARD).pack(pady=5)
                
                xp_box = tk.Frame(c_content, bg="#1E293B", padx=15, pady=8)
                xp_box.pack(pady=15)
                tk.Label(xp_box, text=f" +{xp_gained} PUNTOS DE EXPERIENCIA (XP) ", font=("Segoe UI", 12, "bold"), fg=COLOR_UTB_CYAN, bg="#1E293B").pack()

                btn_finish = tk.Button(c_content, text="Volver al Menú Principal ➔", font=("Segoe UI", 11, "bold"), bg=COLOR_UTB_BLUE, fg="white", activebackground=COLOR_UTB_CYAN, relief="flat", cursor="hand2", command=self.show_student_home)
                btn_finish.pack(fill="x", pady=10, ipady=10)
                return

            q_text, opts, correct_idx, exp = selected_q[q_idx]
            selected_option = [-1]

            quiz_body = tk.Frame(self.main_container, bg=COLOR_BG_MAIN, padx=40, pady=20)
            quiz_body.pack(fill="both", expand=True)

            quiz_card = CustomRoundedCard(quiz_body, width=1050, height=620, radius=24, bg_color=COLOR_BG_CARD, border_color=COLOR_UTB_BLUE, border_width=2)
            quiz_card.pack(fill="both", expand=True)

            q_content = tk.Frame(quiz_card, bg=COLOR_BG_CARD, padx=40, pady=25)
            q_content.place(x=0, y=0, relwidth=1, relheight=1)

            status_bar = tk.Frame(q_content, bg=COLOR_BG_CARD)
            status_bar.pack(fill="x", pady=(0, 15))

            tk.Label(status_bar, text=f"Grado {grade}° • Unidad {unit}", font=("Segoe UI", 10, "bold"), fg=COLOR_UTB_GOLD, bg=COLOR_BG_CARD).pack(side="left")
            tk.Label(status_bar, text=f"Pregunta {q_idx + 1} de {len(selected_q)}", font=("Segoe UI", 10, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_CARD).pack(side="right")

            progress_bar = ModernProgressBar(q_content, width=970, height=12, bg_color="#0B0F19", fill_color=COLOR_UTB_CYAN)
            progress_bar.pack(fill="x", pady=(0, 20))
            progress_bar.set_progress((q_idx) / len(selected_q))

            q_title_box = tk.Frame(q_content, bg="#0B0F19", padx=20, pady=15)
            q_title_box.pack(fill="x", pady=(0, 25))
            tk.Label(q_title_box, text=q_text, font=("Segoe UI", 13, "bold"), fg=COLOR_TEXT_WHITE, bg="#0B0F19", wraplength=900, justify="center").pack()

            option_widgets = []

            def on_option_click(index):
                selected_option[0] = index
                for i, w in enumerate(option_widgets):
                    w.set_state("selected" if i == index else "normal")

            opts_frame = tk.Frame(q_content, bg=COLOR_BG_CARD)
            opts_frame.pack(fill="x")

            for i, opt in enumerate(opts):
                w = InteractiveOptionWidget(opts_frame, opt, i, on_option_click, width=970, height=60)
                w.pack(fill="x", pady=6)
                option_widgets.append(w)

            def check_answer():
                nonlocal q_idx, score
                sel = selected_option[0]
                if sel == -1:
                    messagebox.showwarning("Atención", "Por favor selecciona una opción de respuesta.")
                    return

                if sel == correct_idx:
                    score += 1
                    option_widgets[sel].set_state("correct")
                    messagebox.showinfo("¡Excelentemente Correcto! 🎉", exp)
                else:
                    option_widgets[sel].set_state("wrong")
                    option_widgets[correct_idx].set_state("correct")
                    messagebox.showerror("Respuesta Incorrecta ❌", f"La opción correcta era: {opts[correct_idx]}\n\nExplicación: {exp}")

                q_idx += 1
                render_question()

            btn_check = tk.Button(q_content, text="COMPROBAR Y CONTINUAR ➔", font=("Segoe UI", 11, "bold"), bg=COLOR_UTB_GOLD, fg=COLOR_BG_MAIN, activebackground=COLOR_UTB_AMBER, relief="flat", cursor="hand2", command=check_answer)
            btn_check.pack(fill="x", pady=(20, 0), ipady=10)

        render_question()

    # -------------------------------------------------------------------------
    # VISTA: DASHBOARD DOCENTE COMPLETO
    # -------------------------------------------------------------------------
    def show_teacher_dashboard(self):
        self.clear_container()
        self.draw_navbar("PANEL DE MONITOREO Y ANALÍTICA DOCENTE")

        body = tk.Frame(self.main_container, bg=COLOR_BG_MAIN, padx=35, pady=20)
        body.pack(fill="both", expand=True)

        metrics_frame = tk.Frame(body, bg=COLOR_BG_MAIN)
        metrics_frame.pack(fill="x", pady=(0, 20))

        records = db.get_all_students_progress()
        total_students = len(records)
        total_xp_all = sum(r[4] for r in records)

        cards_data = [
            ("👥 Estudiantes Registrados", str(total_students), COLOR_UTB_BLUE),
            ("⚡ Puntos XP Totales", f"{total_xp_all} XP", COLOR_UTB_GOLD),
            ("📊 Estándar Activo", "MEN Colombia (A1-B1)", COLOR_SUCCESS)
        ]

        for title, val, col in cards_data:
            c = CustomRoundedCard(metrics_frame, width=330, height=80, radius=16, bg_color=COLOR_BG_CARD, border_color=col, border_width=1.5)
            c.pack(side="left", padx=10, fill="x", expand=True)

            cf = tk.Frame(c, bg=COLOR_BG_CARD, padx=15, pady=12)
            cf.place(x=0, y=0, relwidth=1, relheight=1)

            tk.Label(cf, text=title, font=("Segoe UI", 9, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_BG_CARD).pack(anchor="w")
            tk.Label(cf, text=val, font=("Segoe UI", 14, "bold"), fg=col, bg=COLOR_BG_CARD).pack(anchor="w")

        table_card = CustomRoundedCard(body, width=1100, height=480, radius=20, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER, border_width=1)
        table_card.pack(fill="both", expand=True)

        tc_frame = tk.Frame(table_card, bg=COLOR_BG_CARD, padx=20, pady=20)
        tc_frame.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(tc_frame, text="📋 Progreso Detallado de Estudiantes", font=("Segoe UI", 13, "bold"), fg=COLOR_TEXT_WHITE, bg=COLOR_BG_CARD).pack(anchor="w", pady=(0, 15))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0B0F19", foreground="white", fieldbackground="#0B0F19", rowheight=32, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=COLOR_UTB_BLUE, foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", COLOR_UTB_CYAN)], foreground=[("selected", "black")])

        cols = ("Estudiante", "Grado", "Aciertos", "Efectividad %", "XP Acumulado", "Unidades")
        tree = ttk.Treeview(tc_frame, columns=cols, show="headings", height=12)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=140)
        tree.column("Estudiante", anchor="w", width=220)

        tree.pack(fill="both", expand=True)

        for rec in records:
            name, grade, correct, total, xp, units = rec
            pct = f"{(correct/total*100):.1f}%" if total > 0 else "0%"
            tree.insert("", "end", values=(name, f"Grado {grade}°", f"{correct} / {total}", pct, f"{xp} XP", units))


if __name__ == "__main__":
    app = EnglishExplorersApp()
    app.mainloop()