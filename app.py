import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(page_title="Generador de Gráficas QA", page_icon="📊")

st.title("📊 Generador de Gráficas de Desempeño")
st.markdown("""
Edita los valores en la tabla de abajo. La gráfica se actualizará automáticamente.
""")

# 2. Datos Iniciales (Default)
default_data = {
    "Categoría": [
        "Intro & Closing Professionalism", "Call Branding & Offer to Assist",
        "Rapport, Tone & Communication", "Issue Diagnosis & Discovery",
        "Policy & Procedure Knowledge", "Empathy & Soft Skills",
        "Direct Resolution of Queries", "Environment & Background Noise",
        "Call Categorization Accuracy", "Agent Documentation (Notes)",
        "Brand Ambassadorship & Value Add", "Communication of Next Steps",
        "Escalation Protocol & Structure", "Overall Score"
    ],
    "Score": [94, 98, 86, 96, 92, 88, 96, 100, 96, 100, 78, 94, 96, 93.6]
}

# 3. Editor de Datos Interactivo
df = pd.DataFrame(default_data)
edited_df = st.data_editor(df, num_rows="dynamic", hide_index=True)

# 4. Lógica de la Gráfica
if not edited_df.empty:
    # Preparar datos
    categories = edited_df['Categoría'].tolist()[::-1]
    scores = edited_df['Score'].tolist()[::-1]

    # Asignar Colores (Lógica de negocio)
    colors = []
    for cat in categories:
        if "Overall Score" in cat:
            colors.append("#1F618D") # Azul Oscuro
        elif "Rapport" in cat or "Brand Ambassadorship" in cat:
            colors.append("#F15656") # Rojo (Atención)
        else:
            colors.append("#5DADE2") # Azul Claro

    # Crear Figura
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(categories, scores, color=colors, height=0.65)

    # Formato Limpio
    ax.set_xlim(0, 115)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    # Etiquetas de datos
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{score}%', ha='left', va='center', fontsize=9)

    # Línea de Promedio
    avg_score = sum(scores) / len(scores)
    ax.axvline(x=avg_score, color='gray', linestyle='--', alpha=0.5)
    ax.text(avg_score + 1, -0.8, f'Promedio: {avg_score:.1f}%', color='gray', fontsize=9)

    ax.set_xlabel("Puntaje de Desempeño (%)")
    plt.tight_layout()

    # 5. Mostrar Gráfica en la Web
    st.pyplot(fig)

else:
    st.warning("Por favor ingresa datos en la tabla.")
