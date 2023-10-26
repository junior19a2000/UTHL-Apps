import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from pydeck.types import String

st.set_page_config(page_title = 'Unidad Técnica de Hidrocarburos Líquidos', page_icon = '⚡', layout = "wide", initial_sidebar_state = "expanded")
plt.style.use("dark_background")

@st.cache_data
def read_excel(value):
    data = pd.read_excel(
        pd.ExcelFile(
            f"https://docs.google.com/spreadsheets/d/1UDqS8RcqBb6qsjMseBilKh4WC-cyDsVIDw0tu2ahdbs/export?format=xlsx"
        ),
        sheet_name = "Hoja 1",
    )
    return data
data2 = read_excel('value').fillna(' ')

data1 = {'Regiones': ['PERU', 'AMAZONAS', 'ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO', 'CAJAMARCA', 'CUSCO', 'HUANCAVELICA', 'ICA', 'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LIMA SUR', 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'PASCO', 'PIURA', 'PUNO', 'SAN MARTIN', 'TACNA', 'TUMBES', 'UCAYALI', 'LIMA NORTE'],
        'Latitud': [-10.0482, -5.0692, -9.4424, -13.9814, -15.8583, -14.1174, -6.4038, -13.1015, -12.9636, -14.0880, -11.4667, -7.9153, -6.3473, -12.4938, -4.2350, -12.0060, -16.8856, -10.4277, -5.0920, -15.0278, -7.0932, -17.6542, -3.8748, -9.6856, -11.1066],
        'Longitud': [-75.4150, -78.1372, -77.6563, -73.0001, -72.5821, -74.2405, -78.7729, -72.2125, -75.0095, -76.1658, -75.0168, -78.3590, -79.8315, -76.1103, -74.6214, -70.5679, -70.8773, -75.3734, -80.3432, -70.0588, -76.7218, -70.2955, -80.5715, -73.4782, -76.9343],
        'Expedientes': ['PERU', 'AMAZONAS', 'ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO', 'CAJAMARCA', 'CUSCO', 'HUANCAVELICA', 'ICA', 'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LIMA SUR', 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'PASCO', 'PIURA', 'PUNO', 'SAN MARTIN', 'TACNA', 'TUMBES', 'UCAYALI', 'LIMA NORTE'],}
data1 = pd.DataFrame(data1)

data3 = []
for i in data2['REGION'].unique():
    data3.append([i, data2[(data2['REGION'] == i) & (data2['ESTADO'] == 'PENDIENTE')]['N_EXPDNTE'].shape[0]])
data3 = pd.DataFrame(data3, columns = ['REGION', 'EXP_PEN'])
data3 = pd.concat([data3, pd.DataFrame([['PERU', data3['EXP_PEN'].sum()]], columns = ['REGION', 'EXP_PEN'])])
data3 = data3.sort_values(by = 'EXP_PEN', ascending = False)

for i in data1['Regiones']:
    data1 = data1.replace({'Expedientes': i}, i + '\n[' + str(data3[data3['REGION'] == i]['EXP_PEN'].iat[0]) + ' pendientes]')
data4 = data1.replace({'Latitud': -10.0482}, -13.7851)
data4 = data4.replace({'Longitud': -75.4150}, -79.0624)

with st.sidebar: 
    region = st.selectbox('Region', data3['REGION'])
    empty1 = st.empty()
    # st.image(Image.open('logo.png'), use_column_width = True)

if region == 'PERU':
    empty1.pydeck_chart(pdk.Deck(
        map_style = 'dark_no_labels',
        initial_view_state = pdk.ViewState(
            latitude = data1[data1['Regiones'] == region]['Latitud'].iat[0],
            longitude = data1[data1['Regiones'] == region]['Longitud'].iat[0],
            zoom = 4,
            pitch = 0,
            bearing = 0,
        ),
        layers = [
            pdk.Layer(
                "TextLayer",
                data = data4[data4['Regiones'] == region],
                pickable = True,
                auto_highlight = True,
                get_position = '[Longitud, Latitud]',
                get_text = 'Expedientes',
                get_size = 10,
                get_color = [255, 255, 255],
                get_angle = 0,
                get_text_anchor = String("middle"),
                get_alignment_baseline = String("center"),
            )
        ]
    ), use_container_width = False)
else:
    empty1.pydeck_chart(pdk.Deck(
        map_style = 'dark_no_labels',
        initial_view_state = pdk.ViewState(
            latitude = data1[data1['Regiones'] == region]['Latitud'].iat[0],
            longitude = data1[data1['Regiones'] == region]['Longitud'].iat[0],
            zoom = 6,
            pitch = 0,
            bearing = 0,
        ),
        layers = [
            pdk.Layer(
                "TextLayer",
                data = data1[data1['Regiones'] == region],
                pickable = True,
                auto_highlight = True,
                get_position = '[Longitud, Latitud]',
                get_text = 'Expedientes',
                get_size = 10,
                get_color = [255, 255, 255],
                get_angle = 0,
                get_text_anchor = String("middle"),
                get_alignment_baseline = String("center"),
            )
        ]
    ), use_container_width = False)

st.header(':rainbow[Reporte de informes técnicos favorables pendientes]', divider = 'rainbow')

slider1 = st.slider('Rango de dias habiles transcurridos', data2['TIEMPO T'].min(), data2['TIEMPO T'].max(), (data2['TIEMPO T'].min(), data2['TIEMPO T'].max()), step = 1.0)

data5 = []
for i in data2['REGION'].unique():
    data5.append(data2[(data2['REGION'] == i) & (data2['ESTADO'] == 'PENDIENTE') & (data2['TIEMPO T'] >= data2['TIEMPO T'].min()) & (data2['TIEMPO T'] <= data2['TIEMPO T'].max())]['N_EXPDNTE'].shape[0])
pen_max = max(data5)

data5 = []
for i in data2['REGION'].unique():
    data5.append([i, data2[(data2['REGION'] == i) & (data2['ESTADO'] == 'PENDIENTE') & (data2['TIEMPO T'] >= slider1[0]) & (data2['TIEMPO T'] <= slider1[1])]['N_EXPDNTE'].shape[0]])
data5 = pd.DataFrame(data5, columns = ['REGION', 'PEN_SDH'])
data5 = data5.sort_values(by = 'PEN_SDH', ascending = False)

fig1, axe1 = plt.subplots()
bar1 = axe1.barh(data5['REGION'], data5['PEN_SDH'], color = 'skyblue')
axe1.set_xlabel('Expedientes pendientes de atención con un número de dias habiles transcurridos entre ' + str(int(slider1[0])) + ' y ' + str(int(slider1[1])) + '\n[Total: ' + str(data5['PEN_SDH'].sum()) + ' expedientes pendientes de atención para dicho rango]', fontsize = 7)
axe1.set_title('Resultados por región')
fig1.gca().invert_yaxis()  # Invertir el eje y para que la barra superior sea la más grande
fig1.tight_layout()
plt.xticks([])
for bar, value in zip(bar1, data5['PEN_SDH']):
    axe1.text(bar.get_width() + data5['PEN_SDH'].max() / pen_max, bar.get_y() + bar.get_height() / 2, str(value), ha = 'center', va = 'center', color = 'white')
st.pyplot(fig1)

# st.dataframe(data5, hide_index = True)
