import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Simulatore Macroeconomico: IS-LM-FE + AD-AS")

# 1. Gestione Stati
if 'P' not in st.session_state: st.session_state.P = 1.0

# Sidebar
st.sidebar.header("Controlli")
G = st.sidebar.slider("Spesa Pubblica (G)", 0, 100, 30)
T = st.sidebar.slider("Tasse (T)", 0, 100, 30)
M = st.sidebar.slider("Moneta (M)", 100, 600, 350)
A = st.sidebar.slider("Produttività (A)", 0.5, 2.0, 1.0)

# 2. Motore Matematico
Y_fe = 200 * A
q_is = (110 + G - 0.5 * T) / 10
Y_range = np.linspace(50, 500, 100)

# Curve
r_is = q_is - 0.05 * Y_range
r_lm = -(M / st.session_state.P) / 20 + 0.1 * Y_range
# AD: P = M / (20 * (0.15*Y - q_is))
p_ad = M / (20 * (0.15 * Y_range - q_is + 0.0001)) # Piccola costante per evitare divisioni per zero

# 3. Logica Aggiustamento (Pulsante Simulazione)
if st.sidebar.button("Esegui Aggiustamento Prezzi"):
    # Calcolo nuovo equilibrio di lungo periodo
    L_req = 2 * Y_fe - 20 * (q_is - 0.05 * Y_fe)
    st.session_state.P = M / L_req
    st.rerun()

# 4. Grafici
col1, col2 = st.columns(2)

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=Y_range, y=r_is, name="IS", line=dict(color='red')))
    fig1.add_trace(go.Scatter(x=Y_range, y=r_lm, name="LM", line=dict(color='blue')))
    fig1.add_vline(x=Y_fe, line_dash="dash", line_color="green", name="FE")
    fig1.update_layout(title="IS-LM-FE", xaxis_title="Y", yaxis_title="r")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=Y_range, y=p_ad, name="AD", line=dict(color='purple')))
    fig2.add_hline(y=st.session_state.P, line_dash="dot", line_color="orange", name="SRAS (Prezzi)")
    fig2.add_vline(x=Y_fe, line_dash="dash", line_color="green", name="LRAS")
    fig2.update_layout(title="AD-AS (Prezzo P attuale: {:.2f})".format(st.session_state.P), xaxis_title="Y", yaxis_title="P")
    st.plotly_chart(fig2, use_container_width=True)

# 5. Spiegazione
st.write("### Dinamica dei Mercati")
st.write(f"Prezzo corrente: **{st.session_state.P:.2f}**. Il modello mostra come, se l'intersezione AD-SRAS non coincide con la LRAS, il sistema subisce pressioni sui prezzi.")
