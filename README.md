# 📈 ODE Simulation: Drug Impact on Cell Populations

This interactive [Streamlit](https://streamlit.io/) web app simulates a system of ordinary differential equations (ODEs) describing the dynamics of two cell populations — **sensitive** and **resistant** — under the effect of a drug. Users can explore both time evolution and phase plane trajectories for various initial conditions and drug concentrations.

> 🧑‍🔬 *This system was originally studied during my M1 internship at Institut de Mathématique de Marseille(I2M). The idea to develop this interactive web application came to me as a way to deepen my understanding and make the simulations more accessible and visually intuitive.*

---

## 🧪 Model Overview

The biological system is governed by the following ODEs:

```math
\begin{cases}
s'(t) = \rho \left(1 - \frac{s(t) + m r(t)}{K}\right) s(t) - \alpha C s(t) \\
r'(t) = \rho \left(1 - \frac{s(t) + m r(t)}{K}\right) r(t) - \beta \frac{s(t)}{K} r(t)
\end{cases}
```
- s(t): Number of sensitive cells at time t

- r(t): Number of resistant cells at time t

The model incorporates logistic growth and drug-induced effects.

If you'd like to experiment with the model yourself, feel free to try the interactive app here: [Launch the App](https://ousmane-prog-numerical-simulation-app-ibv1zd.streamlit.app/)
