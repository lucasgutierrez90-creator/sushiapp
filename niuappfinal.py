import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Niu Sushi Finder", page_icon="🍣")

st.title("Niu Sushi Finder 🍣")
st.caption("Buscador offline de ingredientes y categorías")

# Cargar Excel
@st.cache_data
def load_data():
    df = pd.read_excel("Base_Datos_NiuSushi_Limpia.xlsx")
    df['Nombre Roll'] = df['Nombre Roll'].astype(str).str.upper().str.strip()
    return df

try:
    df = load_data()
except:
    st.error("No se encontró el archivo Excel.")
    st.stop()

# Entrada de usuario
busqueda = st.text_input("Ingresa los rolls (ej: Tori, Almond, Ebi)", placeholder="Separa por comas")

# Botón Limpiar (Streamlit limpia al borrar el texto, pero podemos forzar el estado)
if st.button("Limpiar Búsqueda"):
    st.rerun()

if busqueda:
    terminos = [t.strip().upper() for t in busqueda.split(",") if t.strip()]
    
    for termino in terminos:
        # Buscamos coincidencias
        resultados = df[df['Nombre Roll'].str.contains(termino, na=False)]
        
        if not resultados.empty:
            for _, row in resultados.iterrows():
                with st.expander(f"✅ {row['Nombre Roll']}", expanded=True):
                    st.write(f"**Categoría:** {row['Categoría']}")
                    st.write(f"**Ingredientes:** {row['Ingredientes']}")
        else:
            st.warning(f"No se encontró: '{termino}'")