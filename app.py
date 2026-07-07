import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurazione pagina
st.set_page_config(layout="wide", page_title="Simulatore Macro")

# Stato per i parametri (usiamo session_state per mantenere i valori)
if 'G' not in st.session_state: st.session_state.G = 30
if 'T' not in st.session_state: st.session_state.T = 30
if 'M' not in st.session_state: st.session_state.M = 350
if 'A' not in st.session_state: st.session_state.A = 1.0

# Sidebar
st.sidebar.header("Controlli")
st.session_state.G = st.sidebar.slider("Spesa Pubblica (G)", 0, 100, st.session_state.G)
st.session_state.T = st.sidebar.slider("Tasse (T)", 0, 100, st.session_state.T)
st.session_state.M = st.sidebar.slider("Moneta (M)", 100, 600, st.session_state.M)
st.session_state.A = st.sidebar.slider("Produttività (A)", 0.5, 2.0, st.session_state.A)

# Scenari
if st.sidebar.button("Simula Espansione Fiscale"):
    st.session_state.G = 60
if st.sidebar.button("Simula Espansione Monetaria"):
    st.session_state.M = 500

# Calcoli Macro
Y_fe = 200 * st.session_state.A
q_is = (110 + st.session_state.G - 0.5 * st.session_state.T) / 10
m_is = -0.05
Y_range = np.linspace(50, 500, 100)

# Curve IS-LM
r_is = q_is + m_is * Y_range
r_lm = -(st.session_state.M / 1.0) / 20 + 0.1 * Y_range # P=1 per brevità

# Grafico IS-LM-FE
fig = go.Figure()
fig.add_trace(go.Scatter(x=Y_range, y=r_is, name="IS", line=dict(color='red')))
fig.add_trace(go.Scatter(x=Y_range, y=r_lm, name="LM", line=dict(color='blue')))
fig.add_vline(x=Y_fe, line_dash="dash", line_color="green", name="FE")
fig.update_layout(title="Modello IS-LM-FE", xaxis_title="Output (Y)", yaxis_title="Tasso (r)")

st.plotly_chart(fig, use_container_width=True)

# Scomposizione (Dietro le quinte)
with st.expander("🔎 Dietro le quinte: Scomposizione dei Mercati"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("Mercato del Lavoro")
        # Logica semplificata mercato lavoro
        fig_l = go.Figure()
        fig_l.add_trace(go.Scatter(x=[0,200], y=[0,200], name="Offerta"))
        fig_l.add_trace(go.Scatter(x=[0,200], y=[200,0], name="Domanda"))
        st.plotly_chart(fig_l, use_container_width=True)
        
    with col2:
        st.write("Mercato della Moneta")
        fig_m = go.Figure()
        fig_m.add_vline(x=st.session_state.M/1, line_color="black")
        st.plotly_chart(fig_m, use_container_width=True)

    with col3:
        st.write("Risparmio-Investimento")
        fig_si = go.Figure()
        fig_si.add_trace(go.Scatter(x=[0,100], y=[10,0], name="Investimento"))
        st.plotly_chart(fig_si, use_container_width=True)