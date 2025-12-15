# Core Equations of the Semantic Physics Model (SPM)

This document outlines the mathematical foundation of SPM. These equations govern how we measure, predict, and defend against semantic manipulation.

## 1. The Fundamental Law of Semantic Dynamics

Analogous to Newton's Second Law ($F=ma$), the movement of a concept in semantic space is defined by:

$$ \vec{A_s} = \frac{\eta \cdot \vec{F_r}}{M_s} $$

### Variables:
*   $\vec{A_s}$ : **Semantic Acceleration** (Vector)
*   $\vec{F_r}$ : **Rhetorical Force** (Vector)
*   $M_s$ : **Semantic Mass** (Scalar)
*   $\eta$ : **Ethos Coefficient** (Scalar, $0 \le \eta \le 1$)

---

## 2. Definitions & Derivations

### 2.1 Semantic Mass ($M_s$)
A measure of a concept's inertia or resistance to re-definition. A concept with high mass (e.g., "Love", "Sun") requires immense force to move.

**Approximation:**
$$ M_s(c) = \alpha \cdot C(c) + \beta \cdot T_{stability}(c) $$

Where:
*   $c$ is the concept.
*   $C(c)$ is the network centrality of $c$ in the global knowledge graph (e.g., PageRank).
*   $T_{stability}(c)$ is the historical variance of $c$'s embedding vector over time (inverse variance).
*   $\alpha, \beta$ are weighting constants.

### 2.2 Rhetorical Force ($\vec{F_r}$)
The vector quantity of persuasive pressure applied by an input sequence $I$.

**Calculation:**
$$ \vec{F_r}(I) = V(I) \cdot (1 + \lambda_{emotional}) \cdot (1 + \lambda_{repetition}) $$

Where:
*   $V(I)$ is the raw embedding vector of the input $I$.
*   $\lambda_{emotional}$ is the sentiment intensity score.
*   $\lambda_{repetition}$ is the frequency of the concept in the input stream.

### 2.3 Semantic Acceleration ($\vec{A_s}$)
The observed rate of change in a concept's position within the high-dimensional semantic vector space.

$$ \vec{A_s} = \frac{\Delta \vec{P}}{\Delta t^2} $$

Where $\vec{P}$ is the position vector of the concept.

### 2.4 Ethos Coefficient ($\eta$)
A damping scalar representing the credibility of the source.

*   $\eta = 1.0$: Fully trusted source (e.g., peer-reviewed consensus).
*   $\eta \to 0$: Untrusted/Malicious source.

**Formula:**
$$ \eta(s) = \sigma( R_{history}(s) - P_{bias}(s) ) $$

Where:
*   $s$ is the source.
*   $R_{history}$ is the historical reliability score.
*   $P_{bias}$ is the detected bias penalty.
*   $\sigma$ is a sigmoid function normalizing to $[0, 1]$.

---

## 3. Interaction Mechanics

### Elastic vs. Plastic Deformation
*   **Elastic:** If $\vec{F_r}$ is removed, the concept returns to its original position (common in low-mass concepts).
*   **Plastic:** If $\vec{F_r} > \text{Yield Strength of } M_s$, the concept is permanently redefined (Semantic Drift).

**Defense Goal:** Maximize $M_s$ for protected concepts and ensure $\eta$ correctly dampens malicious $\vec{F_r}$.
