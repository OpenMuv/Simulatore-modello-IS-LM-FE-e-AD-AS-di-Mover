import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("Simulatore IS-LM-FE")

# Slider per le variabili
G = st.slider("Spesa Pubblica (G)", 0, 100, 30)
M = st.slider("Offerta Moneta (M)", 100, 600, 350)

# Calcoli semplificati per le curve
Y = np.linspace(0, 500, 100)
r_is = 15 - 0.05 * Y + (G * 0.1)
r_lm = -5 + 0.02 * Y + (350/M * 2)

# Creazione grafico
fig = go.Figure()
fig.add_trace(go.Scatter(x=Y, y=r_is, name="IS"))
fig.add_trace(go.Scatter(x=Y, y=r_lm, name="LM"))
fig.add_vline(x=250, line_dash="dash", line_color="green", name="FE")

st.plotly_chart(fig)
st.write("Muovi gli slider per vedere le curve spostarsi!")