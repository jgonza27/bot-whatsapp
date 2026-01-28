import streamlit as st
import google_sheets as db
import pandas as pd
import unicodedata
import time

if "confirmar_guardado" not in st.session_state:
    st.session_state.confirmar_guardado = False

if "id_tabla" not in st.session_state:
    st.session_state.id_tabla = 0

def normalizar_texto(texto):
    if not isinstance(texto, str):
        texto = str(texto)
    texto_limpio = ''.join(c for c in unicodedata.normalize('NFD', texto) 
                           if unicodedata.category(c) != 'Mn')
    return texto_limpio.lower()

st.set_page_config(page_title="Panel de Leads", layout="wide")
st.title("Panel de Control")

if st.button('Actualizar Datos'):
    st.session_state.confirmar_guardado = False
    st.cache_data.clear()
    st.session_state.id_tabla += 1
    st.session_state["buscador"] = "" 
    st.rerun()

try:
    df = db.obtener_todos_registros()

    col1, col2 = st.columns(2)
    col1.metric("Total de Registros", len(df))
    if not df.empty and 'Fecha' in df.columns:
        col2.metric("Último Registro", df.iloc[-1]['Fecha'])
    else:
        col2.metric("Último Registro", "Esperando datos...")

    st.markdown("---")

    filtro = st.text_input("Buscar", key="buscador")

    if filtro:
        filtro_limpio = normalizar_texto(filtro)
        def fila_coincide(row):
            texto_fila = normalizar_texto(str(row.values))
            return filtro_limpio in texto_fila
        
        mask = df.apply(fila_coincide, axis=1)
        df_a_mostrar = df[mask]
        df_oculto = df[~mask]
        
        cantidad = len(df_a_mostrar)
        if cantidad == 1:
            st.info(f"1 registro encontrado")
        else:
            st.info(f"{cantidad} registros encontrados")
    else:
        df_a_mostrar = df
        df_oculto = pd.DataFrame()

    edited_df = st.data_editor(
        df_a_mostrar,
        num_rows="dynamic",
        use_container_width=True,
        key=f"editor_datos_{st.session_state.id_tabla}"
    )

    st.markdown("---")

    filas_originales_visibles = len(df_a_mostrar)
    filas_nuevas_visibles = len(edited_df)
    diferencia = filas_originales_visibles - filas_nuevas_visibles

    if not st.session_state.confirmar_guardado:
        if st.button("Guardar Cambios", type="primary"):
            if diferencia > 0:
                st.session_state.confirmar_guardado = True
                st.rerun()
            else:
                df_final = pd.concat([df_oculto, edited_df], ignore_index=True)
                db.actualizar_todo(df_final)
                st.success("Cambios guardados correctamente")
                time.sleep(1.5)
                st.session_state.id_tabla += 1
                st.rerun()
    else:
        if diferencia == 1:
            st.warning("¿Desea eliminar 1 registro? Confirme la operación.")
        else:
            st.warning(f"¿Desea eliminar {diferencia} registros? Confirme la operación.")
            
        col_si, col_no, vacio = st.columns([1, 1, 5])
        
        with col_si:
            if st.button("Confirmar"):
                df_final = pd.concat([df_oculto, edited_df], ignore_index=True)
                db.actualizar_todo(df_final)
                
                if diferencia == 1:
                    st.success("Se ha eliminado 1 registro correctamente")
                else:
                    st.success(f"Se han eliminado {diferencia} registros correctamente")
                
                st.session_state.confirmar_guardado = False
                st.session_state.id_tabla += 1
                time.sleep(2)
                st.rerun()
        
        with col_no:
            if st.button("Cancelar"):
                st.session_state.confirmar_guardado = False
                st.rerun()

except Exception as e:
    st.error(f"Error: {e}")