# Topics

For each statistical **problem**: the **concept** that solves it, the **tool** (RooFit, RooStats, HistFactory, TMVA, ROOT) and **where** to find it. The slides are in [`slides/`](slides/), the exercises in the folder of each lab.

## Lab 1: the model and the fit

| Problem | Concept | Tool | Where |
|---|---|---|---|
| How do I write the probability of my data? | marked Poisson model: rate (Poisson) and shape (product of pdfs) | `RooAddPdf`, `RooDataSet` | [slides](slides/lab1.md) (Talk A) |
| What is a channel, a component, a physics process? | channel = selected data, component = one physics process | `RooAddPdf` (components), HistFactory (channel, sample) | [slides](slides/lab1.md) (Talk A) |
| What is the range of a variable? | an observable's range defines the model, a parameter's limits steer the fit | `RooRealVar`, `setRange` | [Exercise A](lab1/ex_A.ipynb) |
| Fit every event, or a histogram? | unbinned and binned (Poisson per bin) likelihood | `RooDataSet`, `RooDataHist`, `fitTo` | [Exercise A](lab1/ex_A.ipynb), [backup](slides/lab1_backup.md) |
| A resonance with a detector resolution | Breit–Wigner convolved with a Gaussian | `RooBreitWigner`, `RooVoigtian` | [Exercise B](lab1/ex_B.ipynb), [list of pdfs](../docs/roofit_pdfs.md) |
| Do I measure the rate, or only the shape? | extended fit, or fractions (one parameter fewer) | `RooAddPdf` with N or N−1 coefficients | [Exercise C](lab1/ex_C.ipynb) |
| Which pdf do I need? | list of the standard shapes | classes derived from `RooAbsPdf` | [list of pdfs](../docs/roofit_pdfs.md) |

## Lab 2: errors and validation

| Problem | Concept | Tool | Where |
|---|---|---|---|
| What happens inside a fit? | NLL, minimisation, covariance | `createNLL`, `RooMinimizer`, MINUIT | [slides](slides/lab2.md) (Talk A), [Exercise A](lab2/ex_A.ipynb), [why MINUIT](slides/lab2_backup.md) |
| Is the error symmetric? | HESSE (parabola) against MINOS (the real curve) | `minimizer.hesse()`, `minimizer.minos()` | [slides](slides/lab2.md), [Exercise A](lab2/ex_A.ipynb) |
| My fit fails or looks strange | checklist: convergence, correlation, limits, low statistics | start values, ranges, reparametrisation | [slides](slides/lab2.md) (Talk A) |
| How do I see the likelihood? | scan: slice (fixed) or profile (re-fitted) | `createProfile` | [Exercise A](lab2/ex_A.ipynb), [Exercise B](lab2/ex_B.ipynb) |
| The background is measured in a control region | on/off problem, nuisance parameter | `RooPoisson`, `RooProdPdf` | [slides](slides/lab2.md) (Talk B), [Exercise B](lab2/ex_B.ipynb) |
| Can I trust my errors? | toy Monte Carlo and pulls: bias, RMS, coverage | `RooMCStudy`, `plotPull` | [slides](slides/lab2.md) (Talk C), [Exercise C](lab2/ex_C.ipynb) |
| Many toys on a cluster | one process, one seed per job | `RooRandom.randomGenerator().SetSeed` | [backup](slides/lab2_backup.md) |

## Lab 3: systematics and inference

| Problem | Concept | Tool | Where |
|---|---|---|---|
| A systematic is known only up to an uncertainty | auxiliary measurement or constraint term, global observables | `RooGaussian`, `createNLL(GlobalObservables)` | [slides](slides/lab3.md) (Talk A), [Exercise A](lab3/ex_A.ipynb) |
| Poisson or Gaussian constraint? | the Gaussian is good for many counts only | log-normal, Gamma | [slides](slides/lab3.md) (Talk A) |
| How do I tell RooStats the role of each variable? | `ModelConfig`: pdf, POI, nuisance, observables, global observables | `RooWorkspace`, `ModelConfig` | [slides](slides/lab3.md) (Talk B), [Exercise B](lab3/ex_B.ipynb) |
| Is the excess significant? | background-only hypothesis, $q_0$, $p$-value, $Z$ | `ProfileLikelihoodCalculator` | [Exercise B](lab3/ex_B.ipynb) |
| How big can the signal be? | interval, $\text{CL}_s$ upper limit | `HypoTestInverter` | [slides](slides/lab3.md) (Talk B), [optional notebook](optional/) |
| Correlated systematics | covariance matrix, diagonalisation, rank | `numpy.linalg.eigh`, `RooFormulaVar` | [slides](slides/lab3.md) (Talk C), [Exercise C](lab3/ex_C.ipynb) |

## Lab 4: binned models and event selection

| Problem | Concept | Tool | Where |
|---|---|---|---|
| A model from simulated histograms | HistFactory: measurement, channel, sample | `Measurement`, `Channel`, `Sample` | [slides](slides/lab4.md) (Talk A), [Exercise A](lab4/ex_A.ipynb) |
| A background normalisation shared by two regions | shared `NormFactor` | `AddNormFactor` | [Exercise B](lab4/ex_B.ipynb) |
| Systematic variations of a selection | variations of the columns of a dataframe | `RDataFrame`, `Vary` | [slides](slides/lab4.md) (Talk B) |
| Select signal events among many background events | classifier, ROC, working point, Asimov significance | TMVA | [slides](slides/lab4_tmva.md), [demo](lab4/demo_C_tmva.ipynb) |

## Where is a topic that is not here?

The [gallery](../gallery/) show the same tools on real measurements. If a topic is missing, [write to the lecturer](../README.md).
