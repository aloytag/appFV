import streamlit as st

st.title('Esta es la página 1')
x = st.session_state['N']
st.write(f'La cantidad de paneles es {x}')
with st.sidebar:
    st.write('### Sidebar Pág. 1')
