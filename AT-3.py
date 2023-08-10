import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('at-2-389315-876ffd02d429.json', scope)
client = gspread.authorize(creds)

spreadsheet_id = '1l_vFOwU0EUksNJftA_6dbYqsDQb0LYq7bV5HKKAKKuw'  # replace with your spreadsheet ID
sheet = client.open_by_key(spreadsheet_id).sheet1
def write_to_sheet(data, sheet):
    # 'data' es una lista de los valores que quieres escribir en la hoja
    # 'sheet' es la hoja de cálculo donde quieres escribir los valores
    # 'append_row' agrega los valores al final de la hoja
    sheet.append_row(data)


st.set_page_config(
    page_title="AutoComplete",
    page_icon="🦓",
)
st.title("AutoComplete")

tab = st.sidebar.selectbox("Elige una opción", ["Inalámbricos", "Cableados"])

departamentos_y_ciudades = {
    "Artigas": ["Artigas", "Bella Unión", "Tomás Gomensoro"],
    "Canelones": ["Canelones","Ciudad de la Costa", "Las Piedras", "Pando", "La Paz", "Santa Lucía"],
    "Cerro Largo": ["Melo", "Río Branco"],
    "Colonia": ["Colonia Del Sacramento", "Juan Lacaze", "Nueva Helvecia"],
    "Durazno": ["Durazno", "Villa del Carmen", "Sarandí del Yí"],
    "Flores": ["Trinidad"],
    "Florida": ["Florida", "Sarandí Grande"],
    "Lavalleja": ["Minas"],
    "Maldonado": ["Maldonado", "Punta del Este", "San Carlos"],
    "Montevideo": ["Montevideo"],
    "Paysandú": ["Paysandú"],
    "Río Negro": ["Fray Bentos", "Young"],
    "Rivera": ["Rivera"],
    "Rocha": ["Rocha", "Chuy", "Lascano"],
    "Salto": ["Salto", "Daymán", "Arapey"],
    "San José": ["San José de Mayo"],
    "Soriano": ["Mercedes", "Dolores"],
    "Tacuarembó": ["Tacuarembó", "Paso de los Toros"],
    "Treinta y Tres": ["Treinta y Tres"]
}

with st.expander("Datos Cliente"):
    hab, rut_col, btn_col, new_comp = st.columns([1, 1, 1, 1])
    empresa_nueva = hab.checkbox("Empresa nueva")
    if not empresa_nueva:
        rows = sheet.get_all_records()
        empresas = []
        for row in rows:
            empresas.append(row["Empresa"])    
        empresa = rut_col.selectbox("Empresa:", list(empresas))
        for row in rows:
            if row['Empresa'] == empresa:
                # Actualiza los campos de entrada (no se puede hacer directamente en Streamlit)
                # Necesitarías usar una biblioteca de terceros o implementar tu propio servidor de estado para hacer esto
                dRut = row['Rut']
                dcontacto = row['contacto']
                dtelefono = row['telefono']
                dcorreo_electronico = row['correo_electronico']
                break
        x, tel = st.columns([1,1])
        rut = btn_col.text_input("rut", value=dRut)
        habilitacion = new_comp.checkbox("Requiere habilitacion")
        contacto = x.text_input("Contacto:", value=dcontacto)
        telefono = tel.text_input("Telefono:", value=dtelefono)
        correo_electronico = st.text_input("Correo electrónico:", value=dcorreo_electronico) 
    else:
        empresa = rut_col.text_input("Empresa:")
        rut = btn_col.text_input("rut")
        habilitacion = new_comp.checkbox("Requiere habilitacion")
        x, tel = st.columns([1,1])
        contacto = x.text_input("Contacto:")
        telefono = tel.text_input("Telefono:")
        correo_electronico = st.text_input("Correo electrónico:") 

with st.expander("Direccion"):
    cols4 = st.columns(2)
    direccion = st.text_input("Calle, número, Barrio*, horario*:")
    departamento = cols4[0].selectbox("Departamento:", list(departamentos_y_ciudades.keys()))
    ciudad = cols4[1].selectbox("Ciudad:", departamentos_y_ciudades[departamento])

# Cambiar 'Serie:' para aceptar formato xxx-xxx-xxx
if tab == "Inalámbricos":
    with st.expander("Datos POS (Inalámbrico)"):
        mod, ser, ter = st.columns([1,1,1])
        modelo = mod.selectbox("Modelo:", ["V240M-3G", "V240M-WIFI", "VX680-3G", "VX680-WIFI", "V400m-3G", "V400m-WIFI"])
        serie = ser.text_input("Serie:")
        terminal = ter.text_input("Terminal:")
        x, y, z = st.columns([1,1,1])
        x.divider()
        y.divider()
        z.divider()
        env, por, comp = st.columns([1,1,1])
        modelo_enviar = env.selectbox("Modelo a enviar:", ["V240M-3G", "V240M-WIFI", "V400m-3G", "V400m-WIFI", "V200T Eth", "VX820 USB", "P400 USB", "VX820 Eth", "P400 Eth"])
        portador = por.selectbox("Tipo de perfil:", ["Común", "Combustible"])
        if '3G' in modelo_enviar:
            compania_chip = comp.selectbox("Compañía de chip:", ["ANTEL", "CLARO", "MOVISTAR"]) 
        else:
            compania_chip = comp.selectbox("Compañía de chip:", [])
        remp , con , empty = st.columns([1,1,1])
        remplazar = remp.checkbox("Remplazar")
        con_fuente = con.checkbox("Con fuente")
        detalle_problema = st.text_area("Detalle del problema:")
    if st.button("Cargar Información Inalámbrico"):
        output = f"""#Datos Cliente \r\nEmpresa: {empresa} \r\nRut: {rut} \r\nContacto: {contacto}, {telefono}, {correo_electronico}  \r\nRequiere habilitacion: {"SI" if habilitacion is True else "NO"} \r\n \r\n#Datos Envio: \r\nDirección: {direccion}, {departamento}, {ciudad} \r\n \r\n#Datos pos (caso inalambrico): \r\nPos: {modelo}, S/N: {serie}, {terminal} \r\nModelo a enviar: {modelo_enviar}, {portador}, {"" if compania_chip is None else f"Operadora: {compania_chip}"} \r\nRemplazar: {"SI" if remplazar is True else "NO"}, Fuente: {"SI" if con_fuente is True else "NO"} \r\nDetalle del problema: {detalle_problema} \r\n
"""

        st.text_area("Información cargada", value=output, height=250)
        #st.success("Información copiada al portapapeles.")
        st.balloons()
        if empresa_nueva:
        # Reúne la información en una lista
            data = [empresa, rut, contacto, "/" + telefono, correo_electronico]
            # Llama a la función para escribir los datos en la hoja
            write_to_sheet(data, sheet)
elif tab == "Cableados":
    with st.expander("Datos POS (Cableado)"):
        mod, ser, ter = st.columns([1,1,1])
        modelo = mod.selectbox("Modelo:", [ "P400 USB", "VX820 USB", "P400 Eth", "VX820 Eth"])
        serie = ser.text_input("Serie:")
        terminal = ter.text_input("Terminal:")
        d1, d2, d3 = st.columns([1,1,1])
        d1.divider()
        d2.divider()
        d3.divider()
        env, remp, x = st.columns([1,1,1])
        modelo_enviar = env.selectbox("Modelo a enviar:", [ "P400 USB", "VX820 USB", "P400 Eth", "VX820 Eth", "V240M-3G", "V240M-WIFI", "V400m-3G", "V400m-WIFI", "V200T Eth"])
        remp.markdown("&#32;")
        remp.markdown("&#32;")
        remp.markdown("&#32;")
        remplazar = remp.checkbox("Remplazar")
        detalle_problema = st.text_area("Detalle del problema:")

    if st.button("Cargar Información Cableado"):
        output = f"""#Datos Cliente \r\nEmpresa: {empresa} \r\nRut: {rut} \r\nContacto: {contacto}, {telefono}, {correo_electronico} \r\nRequiere habilitacion: {"SI" if habilitacion is True else "NO"} \r\n \r\n#Datos Envio: \r\nDirrcción: {direccion}, {departamento}, {ciudad} \r\n \r\n#Datos pos (caso cableado): \r\nPos: {modelo}, S/N: {serie}, {terminal} \r\nModelo a enviar: {modelo_enviar} \r\nRemplazar: {"SI" if remplazar is True else "NO"} \r\nDetalle del problema: {detalle_problema}
"""
        st.text_area("Información cargada", value=output, height=250)
        #st.success("Información copiada al portapapeles.")
        st.balloons()
        # Reúne la información en una lista
        if empresa_nueva:
            data = [empresa, rut, contacto, telefono, correo_electronico]
            # Llama a la función para escribir los datos en la hoja
            write_to_sheet(data, sheet)
