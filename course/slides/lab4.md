---
marp: true
theme: default
paginate: true
math: katex
header: "Statistical Data Analysis — Lab 4"
style: |
  section { font-size: 26px; }
  section.lead h1 { font-size: 46px; }
  code { font-size: 0.85em; }
  table { font-size: 0.8em; }
---

<!-- _class: lead -->
<!-- _paginate: false -->
# Lab 4 — HistFactory and your analysis
**Statistical Data Analysis for Nuclear and Subnuclear Physics — Module 3**
G. Sirri · Hands-on sessions, 9:00–13:00

---

# Recap (5 minutes)

1. Constraint term or auxiliary measurement: which one do you use, and when?
2. A source of systematic uncertainty moves three channels. How many nuisance parameters do you need?
3. Which tool for a discovery, which for an upper limit?

---

# Recap: answers

1. **Auxiliary measurement**: you have the control data, use it. **Constraint term**: you only have its result ($b_0\pm\sigma_b$)
2. **One** nuisance parameter if the source is fully correlated across the channels. In general, the number of nuisance parameters is the **rank** of the covariance matrix
3. **Discovery**: the $p$-value of the background-only hypothesis. **Upper limit**: $\text{CL}_s$, with `HypoTestInverter`

Today closes the chain: **binned models**, and a first look at **event selection** with TMVA.

---

# Solutions of Lab 3 (15 minutes)

The solutions are in the `solutions` branch: [`solutions/lab3/`](../solutions/lab3), from today.

- **[A](../solutions/lab3/ex_A_solution.ipynb)**: on/off with a Gaussian constraint, and the significance (A1, A2)
- **[B](../solutions/lab3/ex_B_solution.ipynb)**: `ModelConfig`, intervals, and the significance of the background-only hypothesis (B1–B3)
- **[C](../solutions/lab3/ex_C_solution.ipynb)**: OPERA: covariance and diagonalisation (C1–C3)

---

# Today's schedule

| Time | |
|---|---|
| 9:00 | Recap and Lab 3 questions |
| 9:20 | Talk A: from histograms to a likelihood (HistFactory) |
| 9:40 | Hands-on A: one toy, three ways ([ROOT Team course](../../third_party/root-cpp-course-roofit)) |
| 10:20 | **Break (10 min)** |
| 10:30 | Talk B: RDataFrame `Vary` and modern C++ |
| 10:45 | Hands-on B: HistFactory on CMS $H\to4\ell$ |
| 11:20 | **Break (10 min)** |
| 11:30 | Talk C: selecting events with TMVA (slides [`lab4_tmva.md`](./lab4_tmva.md)) |
| 11:50 | Guided demo C: BDT, efficiency, Asimov significance |
| 12:25 | Open lab: finish A and B, ask questions |
| 12:45 | Wrap-up and feedback |

---

<!-- _class: lead -->
# Talk A
## From histograms to a likelihood

---

# The binned model

Bins $b$, expected counts $\nu_b(\vec\phi,\vec\alpha)$, observed $n_b$:

$$L(\vec\phi,\vec\alpha)=\prod_{b\in\text{bins}}\text{Pois}\big(n_b\,|\,\nu_b(\vec\phi,\vec\alpha)\big)\;\times\;\prod_j c_j(a_j\,|\,\alpha_j)$$

$$\nu_b=\sum_{\text{samples}}\;\underbrace{\nu^{0}_{sb}}_{\text{template}}\;\times\;\underbrace{\prod_\kappa \kappa_{sb}(\vec\phi,\vec\alpha)}_{\text{modifiers}}$$

It is the **extended marked Poisson model** of Lab 1, with a histogram as the shape and modifiers as nuisance parameters. **HistFactory** is the recipe that builds this likelihood from histograms.

---

# HistFactory building blocks

| Level | Meaning | In the ROOT API |
|---|---|---|
| **Measurement** | the whole analysis, POI, luminosity | `Measurement` |
| **Channel** | a subset of the data defined by a selection, with its own data (signal region, control region) | `Channel` |
| **Sample** | one **physics process**: a template histogram. The **component** of Lab 1 | `Sample` |
| **Modifier** | how a parameter changes a sample | see next slide |

Output: a **workspace** with a `ModelConfig`: the same objects you used in Lab 3.

---

# Modifiers

| Modifier | Effect | Constraint | Typical use |
|---|---|---|---|
| `NormFactor` | free scale factor | none | signal strength $\mu$; **a background normalised by a control region** |
| `OverallSys` | scale by $1\pm\epsilon$ | Gaussian | luminosity, cross section |
| `HistoSys` | morph the shape (up/down templates) | Gaussian | energy scale, tune parameter |
| `StatError` | per-bin MC statistics | Poisson / Gaussian | finite simulation |

A **shared** `NormFactor` between two channels is a **control-region measurement**: the same idea as the on/off problem, with histograms.

---

# Same likelihood, different file format

- ROOT: `hist2workspace` or the C++/Python API → RooFit workspace
- `pyhf`: the same model in JSON, pure Python
- Both implement the same likelihood, cross-checked by the LHC experiments

What you learn today is what ATLAS and CMS use to publish their statistical models.

---

<!-- _class: lead -->
# Hands-on A
## One toy, three ways

---

# Exercise A (≈ 40 min)

ROOT Team course `02-roofit`, in [`third_party/root-cpp-course-roofit/`](../../third_party/root-cpp-course-roofit/):

1. Run the pipeline (`make_toys`, `unbinned`, `analysis`, `histfactory`, `likelihood`)
2. **Where do $\mu$ and $\theta$ act in the simulation?** (look at `physics.h`)
3. Compare the three fits of the same data: numbers of events, $\hat\mu$, uncertainties
4. Read $\hat\theta=\theta_{\rm nom}+\hat\alpha\,\Delta\theta$ and compare with $\theta_{\rm true}=1.3$
5. Compare the slice and the profile of $\mu$ with Lab 2

Notebook: [`course/lab4/ex_A.ipynb`](../lab4/ex_A.ipynb) (guide, C++ macros run from Python)


---

### Key Takeaways from Hands-on A

**Statistics**
- The **unbinned** fit uses the **known shapes**, the **HistFactory** fit uses **templates** from simulation: the templates have their own **statistical uncertainty** (`ActivateStatError`)
- The three fits of the same toy give **compatible** results: they are three ways to write one likelihood

**Tools**
- The macros of the ROOT Team course (`make_toys`, `unbinned`, `analysis`, `histfactory`) run from Python with `subprocess`. The results are in `results/*.root`
---

<!-- _class: lead -->
# Talk B
## RDataFrame `Vary` and modern C++

---

# Systematic variations in one event loop

```python
ROOT.gInterpreter.Declare("double w_theta(double eta, double theta) {...}")   # weight as a function of theta

df = df.Vary("bkg_w", "ROOT::RVec<double>{w_theta(eta, 1.4), w_theta(eta, 0.6)}",
             ["theta_up", "theta_down"], "bkg_shape")
h_nom = df.Histo1D(("h", ";|#eta|;events", 8, 0, 2.2), "aeta", "bkg_w")
variations = ROOT.RDF.Experimental.VariationsFor(h_nom)
h_up, h_down = variations["bkg_shape:theta_up"], variations["bkg_shape:theta_down"]
```

- **One event loop**: nominal and varied histograms together
- The varied histograms are exactly the `HistoSys` inputs
- Cost: close to a single loop, not $1+2N$ loops

Code from the ROOT Team course: [`analysis.cpp`](../../third_party/root-cpp-course-roofit/analysis.cpp).

---

# Why modern C++ in analysis

```python
ROOT.gInterpreter.Declare("""
double mass_scale(double m, double k) { return m * (1 + k); }
""")
df = df.Define("m_up", "mass_scale(m, 0.005)")
```

- The expression is **compiled just in time**: C++ speed from Python
- Lambdas, `auto`, `RVec`: concise, vectorised code
- A Python loop over events does **not** scale; RDataFrame does
- Production code (experiment frameworks) is C++: you can read and write both

See the optional notebook [`course/optional/rdf_cpp_speed.ipynb`](../optional/rdf_cpp_speed.ipynb).

---

<!-- _class: lead -->
# Hands-on B
## HistFactory on CMS $H\to4\ell$

---

# The case

CMS Open Data, $H\to ZZ^*\to4\ell$ ([arXiv:1207.7235](https://arxiv.org/abs/1207.7235)). Real data and simulated templates.

| | Signal region | Control region |
|---|---|---|
| range | $70$–$181$ GeV, 37 bins | $m_{4\ell}>181$ GeV, **1 bin** |
| data | 102 events | 176 events |
| samples | $H\to4\ell$, $ZZ$, DY, $t\bar t$ | the same |

- Signal: $\mu$ (`NormFactor`)
- $ZZ$: `kZZ` (`NormFactor`) **shared** by both channels: the control region measures it
- Other backgrounds: from simulation (Lab 3: they could be constrained)

---

# Exercise B (≈ 35 min)

1. Build the `Measurement`: two channels, four samples, shared `kZZ`
2. Fit: $\hat\mu$, $\hat k_{ZZ}$. Compare with the fit **without** control region ($k_{ZZ}=1$)
3. 68 % interval on $\mu$, significance of $\mu=0$ (RooStats, as in Lab 3)
4. Add a 5 % luminosity uncertainty (`OverallSys`; **illustrative size**). What changes?
5. Slice vs profile of $\mu$: how correlated are $\mu$ and $k_{ZZ}$?

Notebook: [`course/lab4/ex_B.ipynb`](../lab4/ex_B.ipynb)


---

### Key Takeaways from Hands-on B

**Statistics**
- A **control region** constrains a background normalisation that the signal region shares. A **shared `NormFactor`** (same name in two channels) is **one** parameter
- A **luminosity uncertainty** is a global nuisance parameter that scales all the samples

**HistFactory**
- `Measurement`, `Channel`, `Sample`: `AddNormFactor("mu", 1, 0, 5)` on the signal, `AddNormFactor("kZZ", 1, 0.1, 3)` on ZZ, and `SetLumi`, `SetLumiRelErr` for the luminosity
- The workspace goes straight into RooStats
---

# Wrap-up and feedback

**You can now**
- write the full model: marked Poisson, nuisance parameters, constraints, control regions
- fit it, validate it with toys, and make statements with RooStats
- read a HistFactory workspace and a published statistical model

**Submission**
- Lab 4: **both** notebooks (A and B), on **Virtuale**
- In total: 2 of 3 notebooks in each of Labs 1–3, plus A and B of Lab 4
- The solutions of Lab 4 are published after the lab

**Before you leave**
- Optional material: [`course/optional/`](../optional/)
- Short anonymous feedback form (5 questions)

Thank you!
