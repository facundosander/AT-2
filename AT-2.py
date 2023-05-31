import streamlit as st
import clipboard
import re

# Función para validar el RUT
def validate_rut(rut):
    return True if re.match(r'^\d{12}$', rut) else False

def get_all_clients():
    # Aquí debes obtener todos los datos de tus clientes desde tu base de datos.
    # Por ahora, esto solo retorna una lista de clientes ficticios.
    return [{'RUT': '123456789012', 'Contacto': 'Juan Perez', 'Telefono': '123456789', 'Correo electrónico': 'juan.perez@ejemplo.com', 'Habilitacion': True, 'Direccion': 'Calle 123', 'Ciudad': 'Ciudad', 'Departamento': 'Departamento'},
            {'RUT': '987654321098', 'Contacto': 'Maria Rodriguez', 'Telefono': '987654321', 'Correo electrónico': 'maria.rodriguez@ejemplo.com', 'Habilitacion': False, 'Direccion': 'Avenida 456', 'Ciudad': 'Otra Ciudad', 'Departamento': 'Otro Departamento'}]

def search_client(rut):
    # Aquí debes buscar el cliente en tu base de datos según su RUT.
    # Por ahora, esto solo retorna un cliente ficticio.
    return {'RUT': rut, 'Contacto': 'Juan Perez', 'Telefono': '123456789', 'Correo electrónico': 'juan.perez@ejemplo.com', 'Habilitacion': True, 'Direccion': 'Calle 123', 'Ciudad': 'Ciudad', 'Departamento': 'Departamento'} if rut == '123456789012' else None

def add_new_client(client_data):
    # Aquí debes agregar un nuevo cliente a tu base de datos.
    # Por ahora, esto solo imprime los datos del cliente.
    print(client_data)

st.title("AutoCompleteTransAct")

tab = st.sidebar.selectbox("Elige una opción", ["Inalámbricos", "Cableados"])

departamentos_y_ciudades = {
    "Artigas": ["Artigas", "Bella Unión", "Tomás Gomensoro"],
    "Canelones": ["Canelones", "Las Piedras", "Pando", "La Paz", "Santa Lucía"],
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
    cols1 = st.columns(2)
    habilitacion = cols1[0].checkbox("Requiere habilitacion")
    rut_col, btn_col = cols1[1].columns([3, 1])
    empresa = rut_col.text_input("Empresa / RUT:")
    btn_buscar = btn_col.button("Buscar")
    cols1[0].markdown("&#32;") 
    cols1[0].markdown("&#32;")
    cols1[0].markdown("&#32;")
    contacto = cols1[0].text_input("Contacto:")
    telefono = cols1[1].text_input("Telefono:")
    correo_electronico = st.text_input("Correo electrónico:") 

with st.expander("Direccion"):
    cols4 = st.columns(2)
    direccion = st.text_input("Calle, número, Barrio:")
    departamento = cols4[0].selectbox("Departamento:", list(departamentos_y_ciudades.keys()))
    ciudad = cols4[1].selectbox("Ciudad:", departamentos_y_ciudades[departamento])

# Cambiar 'Serie:' para aceptar formato xxx-xxx-xxx
if tab == "Inalámbricos":
    with st.expander("Datos POS (Inalámbrico)"):
        cols2 = st.columns(3)
        modelo = cols2[0].selectbox("Modelo:", ["V240M-3G", "V240M-WIFI", "VX680-3G", "VX680-WIFI", "V400m-3G", "V400m-WIFI"])
        serie = cols2[1].text_input("Serie:")
        terminal = cols2[2].text_input("Terminal:")
        cols2[0].divider()
        cols2[1].divider()
        cols2[2].divider()
        modelo_enviar = cols2[0].selectbox("Modelo a enviar:", ["V240M-3G", "V240M-WIFI", "V400m-3G", "V400m-WIFI", "V200T Eth", "VX820 USB", "P400 USB", "VX820 Eth", "P400 Eth"])
        portador = cols2[1].selectbox("Portador:", ["Express", "Combustible"])
        if '3G' in modelo_enviar:
            compania_chip = cols2[2].selectbox("Compañía de chip:", ["ANTEL", "CLARO", "MOVISTAR"]) 
        else:
            compania_chip = cols2[2].selectbox("Compañía de chip:", [])
        remplazar = cols2[0].checkbox("Remplazar")
        con_fuente = cols2[1].checkbox("Con fuente")
        detalle_problema = st.text_area("Detalle del problema:")
    if st.button("Cargar Información Inalámbrico"):
        output = f"""#Datos Cliente \r\nRut: {empresa}  \r\nContacto: {contacto}, {telefono}, {correo_electronico}  \r\nRequiere habilitacion: {"SI" if habilitacion is True else "NO"} \r\n \r\n#Datos Envio: \r\nDirrecion: {direccion}, {departamento}, {ciudad} \r\n \r\n#Datos pos (caso inalambrico): \r\nPos: {modelo}, {serie}, {terminal} \r\nModelo a enviar: {modelo_enviar}, {portador}, {"" if compania_chip is None else f", Operadora: {compania_chip}"} \r\nRemplazar: {"SI" if remplazar is True else "NO"}, Remplazar Fuente: {"SI" if con_fuente is True else "NO"} \r\nDetalle del problema: {detalle_problema} \r\n
"""
        clipboard.copy(output)
        st.text_area("Información cargada", value=output, height=250)
        st.success("Información copiada al portapapeles.")
        st.balloons()

elif tab == "Cableados":
    with st.expander("Datos POS (Cableado)"):
        cols3 = st.columns(3)
        modelo = cols3[0].selectbox("Modelo:", ["VX820", "P400"])
        serie = cols3[1].text_input("Serie:")
        terminal = cols3[2].text_input("Terminal:")
        cols3[0].divider()
        cols3[1].divider()
        cols3[2].divider()
        modelo_enviar = cols3[0].selectbox("Modelo a enviar:", [ "VX820 USB", "P400 USB", "VX820 Eth", "P400 Eth", "V240M-3G", "V240M-WIFI", "V400m-3G", "V400m-WIFI", "V200T Eth"])
        cols3[1].markdown("&#32;")
        cols3[1].markdown("&#32;")
        cols3[1].markdown("&#32;")
        remplazar = cols3[1].checkbox("Remplazar")
        detalle_problema = st.text_area("Detalle del problema:")

    if st.button("Cargar Información Cableado"):
        output = f"""#Datos Cliente \r\nRut: {empresa} \r\nContacto: {contacto}, {telefono}, {correo_electronico} \r\nRequiere habilitacion: {"SI" if habilitacion is True else "NO"} \r\n \r\n#Datos Envio: \r\nDirrecion: {direccion}, {departamento}, {ciudad} \r\n \r\n#Datos pos (caso cableado): \r\nPos: {modelo}, {serie}, {terminal} \r\nModelo a enviar: {modelo_enviar} \r\nRemplazar: {"SI" if remplazar is True else "NO"} \r\nDetalle del problema: {detalle_problema}
"""
        clipboard.copy(output)
        st.text_area("Información cargada", value=output, height=250)
        st.success("Información copiada al portapapeles.")