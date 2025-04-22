import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="NutriApp Avanzada",
    page_icon="💪",
    layout="wide"
)

# --- CONSTANTES Y DATOS ---
COMIDAS = {
    "desayunos": [
        {"nombre": "Chilaquiles rojos con pollo", "calorias": 450, "proteinas": 35, "hidratacion": 0.3},
        {"nombre": "Molletes integrales", "calorias": 380, "proteinas": 18, "hidratacion": 0.2},
        {"nombre": "Avena con proteína", "calorias": 320, "proteinas": 25, "hidratacion": 0.4},
    ],
    "comidas": [
        {"nombre": "Pollo en mole con arroz", "calorias": 600, "proteinas": 45, "hidratacion": 0.2},
        {"nombre": "Enchiladas verdes de pollo", "calorias": 550, "proteinas": 40, "hidratacion": 0.3},
        {"nombre": "Pozole rojo con pollo", "calorias": 500, "proteinas": 38, "hidratacion": 0.5},
    ],
    "cenas": [
        {"nombre": "Sopa de tortilla light", "calorias": 350, "proteinas": 22, "hidratacion": 0.6},
        {"nombre": "Quesadillas de hongos", "calorias": 400, "proteinas": 20, "hidratacion": 0.3},
    ]
}

EJERCICIOS = {
    "Cardio": [
        {"nombre": "HIIT 20 min", "calorias_quemadas": 250, "intensidad": "Alta", "hidratacion": 0.5},
        {"nombre": "Caminata en pendiente", "calorias_quemadas": 200, "intensidad": "Moderada", "hidratacion": 0.3},
    ],
    "Fuerza": [
        {"nombre": "Full body con peso", "calorias_quemadas": 220, "intensidad": "Moderada-Alta", "hidratacion": 0.4},
    ],
    "Flexibilidad": [
        {"nombre": "Yoga para pérdida de grasa", "calorias_quemadas": 150, "intensidad": "Moderada", "hidratacion": 0.2},
    ]
}

class PlanNutricionalCompleto:
    def __init__(self, datos_usuario):
        self.datos = datos_usuario
        self.tmb = self.calcular_tmb()
        self.gea = self.calcular_gea()
        self.deficit = self.calcular_deficit_recomendado()
        self.calorias_objetivo = max(self.gea - self.deficit, self.tmb * 0.8)
        self.agua = self.calcular_agua()
        self.menu_semanal = {}
        self.checklist_diario = {
            "Desayuno": False,
            "Comida": False,
            "Cena": False,
            "Ejercicio": False,
            "Agua": False,
            "Suplementos": False
        }
        self.generar_plan_semanal()
    
    def calcular_tmb(self):
        if self.datos.get("grasa") and 5 < self.datos["grasa"] < 60:
            masa_magra = self.datos["peso"] * (100 - self.datos["grasa"]) / 100
            return 370 + (21.6 * masa_magra)
        else:
            if self.datos["sexo"] == "Hombre":
                return 88.362 + (13.397 * self.datos["peso"]) + (4.799 * self.datos["altura"]) - (5.677 * self.datos["edad"])
            else:
                return 447.593 + (9.247 * self.datos["peso"]) + (3.098 * self.datos["altura"]) - (4.330 * self.datos["edad"])
    
    def calcular_gea(self):
        factores = {
            "Sedentario": 1.2,
            "Ligero (1-3 días/semana)": 1.375,
            "Moderado (3-5 días/semana)": 1.55,
            "Activo (6-7 días/semana)": 1.725,
            "Muy activo": 1.9
        }
        return self.tmb * factores.get(self.datos["actividad"], 1.2)
    
    def calcular_deficit_recomendado(self):
        grasa = self.datos.get("grasa", 25)
        if grasa > 25:
            return min(1000, self.gea * 0.25)
        elif grasa > 20:
            return min(750, self.gea * 0.20)
        else:
            return min(500, self.gea * 0.15)
    
    def calcular_agua(self):
        base = self.datos["peso"] * 0.033
        if self.datos["actividad"] == "Moderado (3-5 días/semana)":
            base += 0.3
        elif self.datos["actividad"] == "Activo (6-7 días/semana)":
            base += 0.5
        elif self.datos["actividad"] == "Muy activo":
            base += 0.7
        return max(1.5, base)
    
    def _seleccionar_ejercicio(self):
        if self.datos["grasa"] > 25:
            tipo = "Cardio" if random.random() > 0.3 else "Fuerza"
        else:
            tipo = "Fuerza" if random.random() > 0.5 else "Cardio"
        return random.choice(EJERCICIOS[tipo])
    
    def generar_plan_semanal(self):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for i, dia in enumerate(dias):
            ejercicio_hoy = i not in [5, 6]  # Ejercicio de lunes a viernes
            
            self.menu_semanal[dia] = {
                "fecha": (datetime.now() + timedelta(days=i)).strftime("%d/%m/%Y"),
                "desayuno": random.choice(COMIDAS["desayunos"]),
                "comida": random.choice(COMIDAS["comidas"]),
                "cena": random.choice(COMIDAS["cenas"]),
                "ejercicio": self._seleccionar_ejercicio() if ejercicio_hoy else None,
                "agua_recomendada": self.calcular_agua(),
                "checklist": self.checklist_diario.copy()
            }

def mostrar_checklist(dia_info):
    st.subheader("✅ Checklist Diario")
    
    checklist = dia_info["checklist"]
    
    cols = st.columns(2)
    with cols[0]:
        checklist["Desayuno"] = st.checkbox("Desayuno completado", value=checklist["Desayuno"])
        checklist["Comida"] = st.checkbox("Comida completada", value=checklist["Comida"])
        checklist["Cena"] = st.checkbox("Cena completada", value=checklist["Cena"])
    
    with cols[1]:
        checklist["Ejercicio"] = st.checkbox("Ejercicio completado", value=checklist["Ejercicio"])
        checklist["Agua"] = st.checkbox(f"Agua ({dia_info['agua_recomendada']:.1f}L)", value=checklist["Agua"])
        checklist["Suplementos"] = st.checkbox("Suplementos tomados", value=checklist["Suplementos"])
    
    # Calcular progreso diario
    progreso = sum(checklist.values()) / len(checklist) * 100
    st.progress(int(progreso), text=f"Progreso diario: {progreso:.0f}%")
    
    if progreso == 100:
        st.success("¡Día completado! 🎉")
    elif progreso > 70:
        st.info("¡Buen trabajo! Sigue así 💪")
    else:
        st.warning("Aún puedes mejorar, ¡no te rindas!")

def main():
    st.title("💪 NutriApp Avanzada con Checklist")
    
    # Inicialización de sesión
    if 'plan' not in st.session_state:
        with st.form("user_data"):
            st.header("📋 Datos Personales")
            
            col1, col2 = st.columns(2)
            with col1:
                datos = {
                    "sexo": st.selectbox("Sexo biológico", ["Hombre", "Mujer"]),
                    "edad": st.number_input("Edad", 18, 80, 30),
                    "peso": st.number_input("Peso actual (kg)", 40.0, 200.0, 70.0, 0.5),
                    "grasa": st.slider("% Grasa corporal estimada", 5.0, 50.0, 25.0, 0.5)
                }
            
            with col2:
                datos.update({
                    "altura": st.number_input("Altura (cm)", 140, 220, 165),
                    "actividad": st.selectbox("Nivel de actividad", [
                        "Sedentario", 
                        "Ligero (1-3 días/semana)", 
                        "Moderado (3-5 días/semana)", 
                        "Activo (6-7 días/semana)", 
                        "Muy activo"
                    ]),
                    "clima": st.selectbox("Clima predominante", ["Templado", "Cálido", "Muy cálido"])
                })
            
            if st.form_submit_button("Generar Plan"):
                st.session_state.plan = PlanNutricionalCompleto(datos)
                st.rerun()
    
    if 'plan' in st.session_state:
        plan = st.session_state.plan
        
        # Selector de día
        dia_seleccionado = st.selectbox("Selecciona un día", list(plan.menu_semanal.keys()))
        dia_info = plan.menu_semanal[dia_seleccionado]
        
        # Mostrar plan del día
        st.header(f"📅 Plan para {dia_seleccionado} - {dia_info['fecha']}")
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("🍽️ Nutrición")
            st.markdown(f"**Desayuno:** {dia_info['desayuno']['nombre']} ({dia_info['desayuno']['calorias']} kcal)")
            st.markdown(f"**Comida:** {dia_info['comida']['nombre']} ({dia_info['comida']['calorias']} kcal)")
            st.markdown(f"**Cena:** {dia_info['cena']['nombre']} ({dia_info['cena']['calorias']} kcal)")
        
        with cols[1]:
            st.subheader("🏋️‍♀️ Ejercicio")
            if dia_info['ejercicio']:
                st.markdown(f"**{dia_info['ejercicio']['nombre']}**")
                st.markdown(f"Quema calórica: {dia_info['ejercicio']['calorias_quemadas']} kcal")
                st.markdown(f"Intensidad: {dia_info['ejercicio']['intensidad']}")
            else:
                st.info("Día de descanso - Recomendado: caminata ligera o estiramientos")
        
        # Mostrar checklist
        mostrar_checklist(dia_info)
        
        # Estadísticas
        st.subheader("📊 Estadísticas Diarias")
        calorias_totales = dia_info['desayuno']['calorias'] + dia_info['comida']['calorias'] + dia_info['cena']['calorias']
        proteinas_totales = dia_info['desayuno']['proteinas'] + dia_info['comida']['proteinas'] + dia_info['cena']['proteinas']
        
        cols_stats = st.columns(3)
        cols_stats[0].metric("Calorías totales", f"{calorias_totales} kcal")
        cols_stats[1].metric("Proteínas totales", f"{proteinas_totales} g")
        cols_stats[2].metric("Agua recomendada", f"{dia_info['agua_recomendada']:.1f} L")

if __name__ == "__main__":
    main()
