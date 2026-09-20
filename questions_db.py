# -*- coding: utf-8 -*-
"""
MÓDULO DE PREGUNTAS Y CURRÍCULO (questions_db.py)
Estructura curricular y Banco de Preguntas alineado al MEN Colombia & ICFES Saber 11°
"""

GRADE_REFERENCE = {
    1: "A1.1 — Principiante Básico", 2: "A1.1 — Principiante Básico", 3: "A1.2 — Principiante",
    4: "A2.1 — Básico Funcional", 5: "A2.1 — Básico Funcional", 6: "A2.2 — Pre-intermedio I",
    7: "A2.2 — Pre-intermedio II", 8: "B1.1 — Pre-intermedio Avanzado", 9: "B1.1 — Pre-intermedio Avanzado",
    10: "B1.2 — Intermedio / Saber 11°", 11: "B1.2 — Académico / Saber 11°"
}

CURRICULUM = {
    1: {"title": "First Steps (A1.1)", "emoji": "🌟", "units": [("Greetings & Expressions", "Interacción básica y saludos"), ("Colors & Numbers", "Conteo y colores"), ("My Family", "Miembros de familia")]},
    2: {"title": "My World (A1.1)", "emoji": "🌍", "units": [("Body & Health", "Partes del cuerpo"), ("My House", "Espacios del hogar"), ("Daily Food", "Alimentos cotidianos")]},
    3: {"title": "Daily Routine (A1.2)", "emoji": "☀️", "units": [("Everyday Actions", "Rutinas en presente"), ("Telling the Time", "Lectura de hora"), ("School Subjects", "Materias escolares")]},
    4: {"title": "Our Community (A2.1)", "emoji": "🏙️", "units": [("Places in City", "Ubicación en la ciudad"), ("Giving Directions", "Instrucciones"), ("Healthy Habits", "Estilos de vida")]},
    5: {"title": "Communication (A2.1)", "emoji": "💬", "units": [("Personal Info", "Intercambio de datos"), ("Simple Present", "Hábitos de otros"), ("Describing Objects", "Adjetivos")]},
    6: {"title": "English in Action (A2.2)", "emoji": "🚀", "units": [("Personal Identity", "Experiencias"), ("Present Continuous", "Acciones del momento"), ("Past Memories", "Sucesos pasados")]},
    7: {"title": "Connect & Discover (A2.2)", "emoji": "🧭", "units": [("Life Experiences", "Presente Perfecto"), ("Past Narrative", "Pasado Continuo"), ("Giving Advice", "Modales (Should/Must)")]},
    8: {"title": "World Cultures (B1.1)", "emoji": "🔎", "units": [("Culture & Traditions", "Expresión de opiniones"), ("Eco Solutions", "Medio ambiente"), ("Media & News", "Noticias breves")]},
    9: {"title": "Critical Thinker (B1.1)", "emoji": "🧠", "units": [("Social Connections", "Argumentación"), ("Digital Footprint", "Mundo digital"), ("Complex Narratives", "Conectores de contraste")]},
    10: {"title": "Future Leaders (B1.2)", "emoji": "🎯", "units": [("Saber 11° Prep", "Simulacro e inferencia"), ("Career Objectives", "Metas profesionales"), ("Global Issues", "Desafíos globales")]},
    11: {"title": "Mastery for Life (B1.2)", "emoji": "🏆", "units": [("Academic Reading", "Análisis textual"), ("Professional CV", "Perfil profesional"), ("Saber 11° Grand Challenge", "Comprensión B1")]}
}

QUESTION_BANK = {
    1: [
        ("Look at the sentence: 'The book is ________ the desk.'\n(Elija la preposición adecuada para un objeto sobre una superficie)", 
         ["under", "inside", "on", "behind"], 2, 
         "Explicación MEN (A1): Usamos 'on' para indicar que un objeto está ubicado sobre una superficie plana."),
        ("Read the dialog:\nPerson A: 'How old are you?'\nPerson B: '___________'", 
         ["I am fine, thank you.", "I live in Colombia.", "I am nine years old.", "My name is Lucas."], 2, 
         "Explicación MEN (A1): 'How old are you?' pregunta explícitamente por la edad."),
    ],
    4: [
        ("Complete the sentence about routines:\n'What time ________ your brother usually go to school?'", 
         ["do", "does", "is", "did"], 1, 
         "Explicación MEN (A2): En Presente Simple, la tercera persona del singular (he/brother) requiere el auxiliar 'does'."),
        ("Read the text:\n'Last weekend, my family visited a farm in Nariño. We walked through the green fields and fed the animals.'\nWhat did the family do?", 
         ["They built a house.", "They bought animals.", "They walked in the fields and fed animals.", "They stayed inside."], 2, 
         "Explicación MEN (A2): Extracción directa de información explícita del texto narrativo."),
    ],
    8: [
        ("Select the correct connective for contrast:\n'She studied hard for the test; ________, she didn't get a perfect score.'", 
         ["However", "Therefore", "In addition", "Because"], 0, 
         "Explicación MEN (B1): 'However' es un conector de contraste adecuado para unir dos ideas opuestas."),
    ],
    10: [
        ("Prueba Saber 11° (Parte 4):\n'If cities replace traditional streetlights with LED solar lights, they ________ energy consumption significantly.'", 
         ["will lower", "lowered", "would have lowered", "lowers"], 0, 
         "Explicación MEN (B1 - Saber 11°): Estructura del Primer Condicional (If + Presente Simple, sujeto + WILL + verbo base)."),
        ("Prueba Saber 11° (Parte 7 - Lectura Crítica):\n'Renewable energy projects require not only technical installation but also community engagement. When local inhabitants participate, long-term success increases.'\nWhat is the main idea?", 
         ["Solar panels are too expensive.", "Community involvement is essential for project sustainability.", "Technical training is the only requirement.", "Rural areas do not need energy."], 1, 
         "Explicación MEN (B1 - Saber 11°): La idea principal sintetiza la importancia de la participación comunitaria en el éxito de los proyectos."),
    ],
    11: [
        ("Academic Reading (B1.2):\nSelect the word closest in meaning to 'Plausible' in academic writing:", 
         ["Impossible", "Credible / Reasonable", "Ridiculous", "Short"], 1, 
         "Explicación MEN (B1+): 'Plausible' hace referencia a un argumento o hipótesis creíble y razonable."),
    ]
}