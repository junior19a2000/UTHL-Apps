import io
import numpy as np
import pandas as pd
import streamlit as st

buffer = io.BytesIO()

st.set_page_config(layout = "wide", initial_sidebar_state = 'expanded')

def ex2py(fecha):
    if pd.notnull(fecha):
        fecha = str(fecha)[:10]
    else:
        fecha = None
    return fecha

st.title('Informes Técnicos Favorables')

with st.sidebar: 
    excel  = st.file_uploader('Subir el reporte generado por el sistema:')
    empty1 = st.empty()
        
if excel is not None:
    if st.button('Generar excel arreglado', use_container_width = True):
        data = pd.read_excel(excel, sheet_name = 'ITF-Concluidos')
        date1 = data['FCHA_EXPDNTE'].apply(ex2py)
        date2 = data['FECHA_EMISION_OFI'].apply(ex2py)
        date3 = []
        for i in range(date1.shape[0]):
            if date1.iat[i] != None and date2.iat[i] != None:
                date3.append(np.busday_count(date1.iat[i], date2.iat[i]))
            else:
                date3.append(None)
        date3 = pd.DataFrame(date3, columns = ['DIAS_HABILES'])
        date4 = pd.concat([date1, date2, date3], axis = 1)
        st.write(date4)
        with pd.ExcelWriter(buffer, engine = 'xlsxwriter') as writer:
            date4.to_excel(writer, index = False)
            writer.close()
            st.download_button(label = "Descargar excel arreglado", data = buffer, file_name = 'Arreglado.xlsx', 
            mime = "application/vnd.ms-excel", use_container_width = True)
