# -*- coding: utf-8 -*-
"""
ENGLISH EXPLORERS — UTB EDITION 🏆 (Versión Streamlit Web)
===============================================================================
Aplicación Educativa Interactiva Gamificada desplegable en la Web.
===============================================================================
"""

import streamlit as st
import random
import os

import db_manager as db
import questions_db as qdb

# Configuración de página
st.set_page_config(
    page_title="English Explorers — UTB",
    page_icon="🏆",
    layout="wide"
)

LOGO_PATH = "utb_logotipo.png"

# Inicializar Base de Datos y Sesión
db.init_db()

if "user" not in st.session_state:
    st.session_state.user = None

if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = None


# =============================================================================
# CABECERA Y NAVBAR INSTITUCIONAL
# =============================================================================
def render_header(title_sub="PLATAFORMA INSTITUCIONAL"):
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=100)
        else:
            st.title("🏆")
    with col2:
        st.title("ENGLISH EXPLORERS")
        st.caption(f"UTB • {title_sub}")
    
    if st.session_state.user:
        u = st.session_state.user
        role_str = "👨‍🏫 Docente" if u[3] == "docente" else f"🎓 Grado {u[4]}°"
        st.sidebar.markdown(f"### Usuario: **{u[2]}**")
        st.sidebar.write(f"Rol: {role_str}")
        if st.sidebar.button("Cerrar Sesión 🚪"):
            st.session_state.user = None
            st.session_state.quiz_state = None
            st.rerun()

    st.markdown("---")


# =============================================================================
# VISTAS DE LA APLICACIÓN
# =============================================================================

def show_login():
    render_header("ACCESO DE USUARIOS")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("¡Bienvenido Explorer!")
        st.write("Ingresa tus credenciales para continuar")
        
        user_input = st.text_input("Usuario")
        pass_input = st.text_input("Contraseña", type="password")
        
        if st.button("INICIAR SESIÓN 🚀", use_container_width=True, type="primary"):
            u = db.authenticate_user(user_input.strip(), pass_input.strip())
            if u:
                st.session_state.user = u
                st.success("¡Bienvenido!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
        
        st.write("")
        if st.button("¿No tienes cuenta? Regístrate aquí", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()


def show_register():
    render_header("REGISTRO DE ESTUDIANTES")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("📝 Registro de Nuevo Estudiante")
        
        name = st.text_input("Nombre Completo:")
        user = st.text_input("Usuario Único:")
        pwd = st.text_input("Contraseña:", type="password")
        
        grade_str = st.selectbox(
            "Grado Escolar (Mineducación):",
            [f"Grado {i}°" for i in range(1, 12)]
        )
        grade = int(grade_str.split()[1].replace("°", ""))
        
        if st.button("CREAR CUENTA Y EMPEZAR ⚡", use_container_width=True, type="primary"):
            if not name or not user or not pwd:
                st.warning("Por favor completa todos los datos.")
            else:
                ok, msg = db.register_user(user, pwd, name, 'estudiante', grade)
                if ok:
                    st.success(f"¡Bienvenido/a {name}! Tu cuenta ha sido creada.")
                    st.session_state.user = db.authenticate_user(user, pwd)
                    st.rerun()
                else:
                    st.error(msg)
                    
        if st.button("⬅ Volver al Login", use_container_width=True):
            st.session_state.view = "login"
            st.rerun()


def show_student_home():
    render_header("RUTA DE APRENDIZAJE")
    user = st.session_state.user
    grade = user[4]
    
    data = qdb.CURRICULUM.get(grade, qdb.CURRICULUM[1])
    
    st.info(f"### {data['emoji']} {data['title']}\n**Estándar Curricular MEN:** {qdb.GRADE_REFERENCE.get(grade, 'A1-A2')}")
    st.subheader("SELECCIONA TU DESAFÍO DE HOY")
    
    for idx, (unit_name, desc) in enumerate(data["units"], start=1):
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"#### UNIDAD {idx}: {unit_name}")
                st.write(desc)
            with col2:
                if st.button(f"¡JUGAR UNIDAD {idx}! ⚡", key=f"unit_{idx}", type="primary"):
                    questions = qdb.QUESTION_BANK.get(grade, qdb.QUESTION_BANK[1])
                    selected_q = random.sample(questions, min(2, len(questions)))
                    st.session_state.quiz_state = {
                        "unit": idx,
                        "questions": selected_q,
                        "q_idx": 0,
                        "score": 0
                    }
                    st.rerun()
            st.divider()


def show_quiz():
    render_header("DESAFÍO EN LÍNEA")
    qstate = st.session_state.quiz_state
    user = st.session_state.user
    grade = user[4]
    
    q_idx = qstate["q_idx"]
    questions = qstate["questions"]
    
    if q_idx >= len(questions):
        # Fin del juego
        score = qstate["score"]
        total = len(questions)
        xp_gained = score * 25
        
        db.save_score(user[0], grade, qstate["unit"], score, total, xp_gained)
        
        st.balloons()
        st.success("🏆 ¡DESAFÍO COMPLETADO!")
        st.metric(label="Puntuación Obtenida", value=f"{score} de {total}")
        st.info(f"⚡ **+{xp_gained} PUNTOS DE EXPERIENCIA (XP)**")
        
        if st.button("Volver al Menú Principal ➔", type="primary"):
            st.session_state.quiz_state = None
            st.rerun()
        return

    # Pregunta actual
    q_text, opts, correct_idx, exp = questions[q_idx]
    
    st.progress((q_idx) / len(questions))
    st.caption(f"Pregunta {q_idx + 1} de {len(questions)} • Grado {grade}° • Unidad {qstate['unit']}")
    
    st.markdown(f"### {q_text}")
    
    selected = st.radio("Selecciona tu respuesta:", opts, key=f"q_{q_idx}")
    
    if st.button("COMPROBAR Y CONTINUAR ➔", type="primary"):
        sel_idx = opts.index(selected)
        if sel_idx == correct_idx:
            st.session_state.quiz_state["score"] += 1
            st.success(f"¡Excelentemente Correcto! 🎉\n\n{exp}")
        else:
            st.error(f"Respuesta Incorrecta ❌\n\nLa opción correcta era: **{opts[correct_idx]}**\n\n{exp}")
            
        st.session_state.quiz_state["q_idx"] += 1
        st.button("Siguiente Pregunta ➔")


def show_teacher_dashboard():
    render_header("PANEL DE MONITOREO Y ANALÍTICA DOCENTE")
    
    records = db.get_all_students_progress()
    total_students = len(records)
    total_xp_all = sum(r[4] for r in records)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Estudiantes Registrados", total_students)
    c2.metric("⚡ Puntos XP Totales", f"{total_xp_all} XP")
    c3.metric("📊 Estándar Activo", "MEN Colombia (A1-B1)")
    
    st.write("---")
    st.subheader("📋 Progreso Detallado de Estudiantes")
    
    table_data = []
    for rec in records:
        name, grade, correct, total, xp, units = rec
        pct = f"{(correct/total*100):.1f}%" if total > 0 else "0%"
        table_data.append({
            "Estudiante": name,
            "Grado": f"Grado {grade}°",
            "Aciertos": f"{correct} / {total}",
            "Efectividad": pct,
            "XP Acumulado": f"{xp} XP",
            "Unidades": units
        })
        
    st.dataframe(table_data, use_container_width=True)


# =============================================================================
# ENRUTADOR PRINCIPAL DE VISTAS
# =============================================================================
if not st.session_state.user:
    if st.session_state.get("view") == "register":
        show_register()
    else:
        show_login()
else:
    user_role = st.session_state.user[3]
    if user_role == "docente":
        show_teacher_dashboard()
    else:
        if st.session_state.quiz_state is not None:
            show_quiz()
        else:
            show_student_home()
