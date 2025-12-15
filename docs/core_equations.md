# Core Equations of the Semantic Physics Model (SPM v3.0)

This document outlines the mathematical foundation of SPM v3.0. These equations govern how we measure, predict, and defend against semantic manipulation.

## 1. The Fundamental Law of Semantic Dynamics

Analogous to Newton's Second Law ($F=ma$), the movement of a concept in semantic space is defined by:

$$\vec{A_s} = \frac{\eta \cdot \|\vec{F_r}\|}{M_s}$$

### Variables:
* $\vec{A_s}$ : **Semantic Acceleration** (Scalar Magnitude of Shift)
* $\vec{F_r}$ : **Rhetorical Force Vector** (Decomposed Vector)
* $M_s$ : **Semantic Mass** (Scalar)
* $\eta$ : **Ethos Coefficient** (Scalar, $0 \le \eta \le 1$)

---

## 2. Definitions & Derivations

### 2.1 Semantic Mass ($M_s$) — The Hybrid-Proxy Model
A measure of a concept's inertia or resistance to re-definition.

**v3.0 Definition:** $M_s$ represents the **Topological Stability** of a concept's "HyperToken."
**Calculation (Hybrid-Proxy):** To maintain computational efficiency, we approximate the topological shape using graph centrality and variance:

$$M_s(c) \approx \alpha \cdot C_{graph}(c) + \beta \cdot T_{stability}(c)$$

Where:
* $C_{graph}(c)$ is the network centrality (e.g., PageRank).
* $T_{stability}(c)$ is the inverse variance of the embedding vector over time.

### 2.2 Rhetorical Force ($\vec{F_r}$) — The Vector Model
In v3.0, Force is not a single number but a 3-dimensional vector representing the *composition* of the argument.

$$\vec{F_r} = \begin{bmatrix} F_{logos} \\ F_{pathos} \\ F_{ethos} \end{bmatrix}$$

The magnitude used in the acceleration equation is the Euclidean norm:
$$\|\vec{F_r}\| = \sqrt{F_{logos}^2 + F_{pathos}^2 + F_{ethos}^2}$$

### 2.3 The Ethos Coefficient ($\eta$) — The Circuit Breaker
A damping scalar representing the credibility of the source.

**Formula:**
$$\eta_{raw} = \sigma( R_{history} - P_{bias} )$$

**The Circuit Breaker Logic:**
To prevent "leakage" from malicious sources, v3.0 implements a hard threshold ($\tau$):

$$
\eta =
\begin{cases}
0 & \text{if } \eta_{raw} < \tau \\
\eta_{raw} & \text{if } \eta_{raw} \ge \tau
\end{cases}
$$

* Default $\tau = 0.3$.
* If a source falls below this threshold, their effective force becomes **Zero**.

---

## 3. Interaction Mechanics

### Elastic vs. Plastic Deformation
* **Elastic:** If $\vec{F_r}$ is removed, the concept returns to its original position (common in low-mass concepts).
* **Plastic:** If $\vec{F_r} > \text{Yield Strength of } M_s$, the concept is permanently redefined (Semantic Drift).

**Defense Goal:** Maximize $M_s$ for protected concepts and ensure $\eta$ correctly triggers the Circuit Breaker for malicious actors.
