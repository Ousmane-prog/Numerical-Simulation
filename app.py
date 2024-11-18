import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import plotly.graph_objects as go

# Define the ODE system
def model(t, y, rho, K, m, alpha, C, beta):
    s, r = y
    ds_dt = rho * (1 - (s + m * r) / K) * s - alpha * C * s
    dr_dt = rho * (1 - (s + m * r) / K) * r - beta * s / K * r
    return [ds_dt, dr_dt]


# App title
st.title("Numerical Simulation of an ODE System:")

st.write("This app simulates the dynamics of a system of ordinary differential equations (ODEs) that models the population of sensitive and resistant cells in the presence of a drug.")
st.write("The system is given by:")
st.latex(r'''
\begin{cases}
s'(t) = \rho \left(1 - \frac{s(t) + m r(t)}{K}\right) s(t) - \alpha C s(t) \\
r'(t) = \rho \left(1 - \frac{s(t) + m r(t)}{K}\right) r(t) - \beta \frac{s(t)}{K} r(t) \\
s(0) = s_0, r(0) = r_0 \\
\end{cases}
''')
st.write("where:")
st.write(r"$s(t)$ and $r(t)$ respectively represent the number of sensitive and resistant cells at time $t$.")
st.write(r"and:")
st.latex(r'''
\begin{array}{llll}
\hline \text { Symbol } & \text { Meaning } & \text { Value } & \text { Unit } \\
\hline s_0 & \text { sensitive cells number } & \text { initial:5000 } & \text { cells } \\
r_0 & \text { resistant cells number } & \text { initial:5000 } & \text { cells } \\
K & \text { Petry dish carrying capacity } & 4800000 & \text { cells } \\
m & \text { size ratio between } s \text { and } r & 30 & \text { adimensional } \\
\rho_s & \text { sensitive cells growth rate } & 0.031 & \text { cells/hour } \\
\rho_r & \text { resistant cells growth rate } & 0.026 & \text { cells/hour } \\
C & \text { drug concentration } & \text { maximum:5 } & \mathrm{nM} / \text { hour } \\
\alpha & \text { drug effect } & 0.06 & \mathrm{nM}^{-1} \\
\beta & \text { action of sensitive on resistant } & 6.25 \cdot 10^{-7} & \mathrm{cells}^{-1} \\
T & \text { experiments duration } & 720 & \mathrm{~h} \\
\hline
\end{array}
''')
# User inputs
rho_s = 0.031
rho_r = 0.026
k = 4800000
m = 30
alpha = 0.06
beta = beta = k*6.25*10**(-7)
# C = st.slider("Drug concentration  (C)", 0.0, 5.0, 1.0, 0.1)
C = st.number_input("Drug concentration  (C)", min_value=0.0, max_value=5.0, value=0.90, step=0.1)
s0 = st.number_input("Initial sensitive (s0)", min_value=5000.0, value=1000000.00, step=1.0)
r0 = st.number_input("Initial resistant (r0)", min_value=5000.0, value=5000.0, step=1.0)

# Solve the ODE
t_span = (0, 700)  # Simulation time
y0 = [s0, r0]
t_eval = np.linspace(t_span[0], t_span[1], 500)  # Time points for evaluation
solution = solve_ivp(model, t_span, y0, t_eval=t_eval, args=(rho_s, k, m, alpha, C, beta))

# Extract results
t = solution.t
s, r = solution.y
# Plot with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=s, mode='lines', name='S', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=t, y=r, mode='lines', name='R', line=dict(color='red')))
fig.update_layout(
    title="Cells Population Dynamics",
    xaxis_title="Duration (hours)",
    yaxis_title="Cells Population",
    legend=dict(x=0.8, y=0.9),
    template="plotly_white"
)

# Define initial conditions for phase plane analysis
default_init_cond = [
    [10**6, 10**5], 
    [0.1*10**6, 1.4*10**5], 
    [4*10**4, k/m-100], 
    [11*10**5, 5*10**4], 
    [17*10**5, 2*10**4]
]
init_cond = st.multiselect("Initial conditions for phase plane analysis", default_init_cond, default=[default_init_cond[0]])
st.write("The following plots show the evolution of the sensitive and resistant cells populations over time, as well as the phase plane analysis of the system. The phase plane analysis shows the trajectories of the system for different initial conditions. The study of the system has shown that it has three equilibrium points: (0, k/m), (k, 0), and (0, 0). The phase plane analysis intend to unserstand the behavior of the system around these equilibrium points.")
# Phase plane plot
def format_number(num):
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(num)

fig_phase_plane = go.Figure()

# Annotate equilibrium points
equilibrium_points = [(0, k/m), (k, 0), (0, 0)]
for point in equilibrium_points:
    fig_phase_plane.add_annotation(x=point[0], y=point[1], text=f"({format_number(point[0])},{format_number(point[1])})", showarrow=True, arrowhead=2)

# Add trajectories for each initial condition
for elt in init_cond:
    S0, R0 = elt
    solution = solve_ivp(model, t_span, [S0, R0], t_eval=t_eval, args=(rho_s, k, m, alpha, C, beta))
    s, r = solution.y
    fig_phase_plane.add_trace(go.Scatter(x=s, y=r, mode='lines', name=f"S0={format_number(S0)}, R0={format_number(R0)}"))

fig_phase_plane.update_layout(
    title=f"Phase Plane Analysis (C = {C})",
    xaxis_title="Sensitive Cells (s)",
    yaxis_title="Resistant Cells (r)",
    template="plotly_white"
)

# Display Plotly figures in Streamlit side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
with col2:
    st.plotly_chart(fig_phase_plane)
