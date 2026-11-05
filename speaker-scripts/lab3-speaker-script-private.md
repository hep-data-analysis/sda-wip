# Lab 3 — Speaker Script

*Companion of lab3.md (24 slides).*

## Notes for today

*How to use the scripts, survival phrases and pronunciation help: see `how-to-use-and-pronunciation-private.md`.*

- Oggi è il lab più concettuale: tre idee (vincoli, RooStats, correlazioni). Rallenta nelle formule, accelera negli esercizi.
- Il caso OPERA è reale ma la correlazione tra canali è un'ipotesi nostra: dillo chiaramente, non attribuirla alla collaborazione.

## New phrases for today

| Situation | Say | IT |
| --- | --- | --- |
| Concept check | Who can explain this in one sentence? | Chi lo spiega in una frase? |
| Disagree | I see it differently. Let me explain why. | Io la vedo diversamente |
| Link | This is the same idea as in Lab 2. | Stessa idea del Lab 2 |
| Numbers | Please compare your number with the one in the check cell. | Confrontate col numero della cella check |
| Assumption | This is our assumption, not the paper's. | Ipotesi nostra, non del paper |
| Warn | This step takes a minute. Please be patient. | Ci vuole un minuto |

---

## 0:00 — Recap and solutions of Lab 2 (slides 1–4, 20 min)

**SAY (slide 1):** Good morning, and welcome back. This is Lab 3: systematics and inference. In Lab 2 we saw the profile likelihood and the on/off problem. Today we ask the real question of every analysis: how do we treat what we do not know? \[PAUSE\] We have three parts. First, how to write a systematic uncertainty. Second, how to make statistical statements with RooStats. Third, a real problem, with correlated uncertainties.

*IT: oggi: come scrivere una sistematica, RooStats, caso reale con correlazioni.*

**\[DO\] slide 2 — Recap**

**SAY:** First a short recap. Please discuss in pairs for two minutes. Question one: slice and profile likelihood. Which is wider, and why? Question two: in the on/off problem, where does the uncertainty on the background come from? Question three: your pull has an RMS of one point three. What does it tell you? Question four: which two notebooks of Lab 2 did you submit? Did the toy loop converge for you?

**Expected answers:**

1. Profile is wider: nuisance parameters are re-fitted, so their uncertainty adds.
2. From the control region: it is the Poisson uncertainty of n off, divided by tau.
3. The errors are underestimated by thirty percent: the fit errors are too small.
4. Collect two or three answers. Note which notebook of Lab 2 was the hardest, and what students found unclear: those are the first cells to open in the solutions.

**\[DO\] slide 3 — Solutions of Lab 2 (15 min)**

**SAY:** Now the solutions of Lab 2. I show the cells that were the hardest for you, the ones you named in the recap. \[PAUSE\] Open the solution notebooks, run them from the top, and go to the key cells. One minute of explanation and one question for each.

*IT: 15 minuti: soluzioni del Lab 2, solo le celle più difficili. Una domanda per ciascuno.*

- **Exercise A (5 min).** A1: NLL, MIGRAD, HESSE. A2: MINOS. A5: the contour. **Ask:** HESSE and MINOS differ: which one do you trust? **Expected:** MINOS: the likelihood is not a parabola.
- **Exercise B (5 min).** B1: the on/off model, b hat close to 3.8 and s hat close to 13.2. B2: the profile interval against MINOS. B3: slice against profile, with a poorer control region. **Ask:** why is the profile wider than the slice? **Expected:** the nuisance parameter is re-fitted, so its uncertainty adds.
- **Exercise C (5 min).** C1: the toy loop and the pulls. C2: low statistics, failed fits and boundaries. **Ask:** what does a pull RMS of 1.3 tell you? **Expected:** the errors are underestimated by about thirty percent.
- If a student asks for another cell, show it. The solutions are in the repository from today.

**\[DO\] slide 4 — Schedule**

**SAY:** Here is today's plan. Three talks, three hands-on parts, two breaks. **Before each hands-on, we write the first step together, live, for five minutes.** The last fifteen minutes are an open lab: you finish a notebook, and I help you. Every systematic you will write today has a name, a source and a size. Please listen with these three words in mind.

---

## 0:20 — Talk A: Constraints vs auxiliary measurements (slides 5–8, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold line of each slide and come back to the rest at the end of the hands-on.*

**\[DO\] slide 6 — Two ways to model a systematic**

**SAY:** A nuisance parameter is a quantity that we need in the model, but we know it only with an uncertainty. Where does our knowledge come from? \[PAUSE\] There are two ways to write it. The first: an auxiliary measurement. We write the likelihood of the control data. For example, a Poisson for n off. The second: a constraint term. We write a probability distribution for the result of that measurement. For example, a Gaussian centred on the background estimate, with the quoted uncertainty. \[PAUSE\] Look at the table. With the auxiliary measurement, you need the control data. With the constraint, you need only the summary, for example a paper that says: background three point eight, plus or minus zero point six. **Both enter the likelihood as a factor. The second one is an approximation of the first.**

*IT: misura ausiliaria (likelihood dei dati di controllo) vs vincolo (pdf del risultato). Il vincolo è un'approssimazione.*

**\[DO\] slide 7 — From on/off to a Gaussian constraint**

**SAY:** Let us see when the approximation is good. The control measurement gives b hat equal to n off divided by tau. And the uncertainty is the square root of n off, divided by tau. For a large n off, the Poisson is almost Gaussian. This works for about thirty to fifty counts, or more. \[PAUSE\] For few counts, it fails. The Gaussian is symmetric. It allows negative background. And it makes the significance too high. \[PAUSE\] Two alternatives. If the uncertainty is multiplicative and the quantity is positive, for example an efficiency, use a log-normal. If you know the number of control events, the exact partner of the Poisson is the Gamma distribution. **Rule: use the measurement when you have it. Use a constraint when you have only its result.**

*IT: Gauss ok per n\_off grande; per pochi conteggi sovrastima la significatività; log-normale per efficienze, Gamma come coniugata esatta.*

**Ask the class:** A paper says: background zero point five plus or minus zero point four. Can you use a Gaussian? **Answer:** No: the Gaussian gives weight to negative values. Use a log-normal or a Gamma.

**\[DO\] slide 8 — The full model, and global observables**

**SAY:** Now the full model. It is the one from Lab 1: the extended marked Poisson. A Poisson for the number of events, times the product of the densities. And now, a new factor: the product of all the constraint terms. \[PAUSE\] In a constraint term, a j is the result of the auxiliary measurement. We call it a global observable. Remember this rule. **In the fit, the global observables are constants. In toy experiments, they are thrown again, together with the data.** In RooFit, you tell this to createNLL with the option GlobalObservables. In RooStats, with ModelConfig.

*IT: modello completo = marked Poisson × vincoli. Global observables: costanti nel fit, rigenerate nei toy.*

---

## 0:35 — Live coding A1: the Gaussian constraint (5 min)

**\[DO\]** Open the notebook ex A, cell A1. `build_gauss` is already there, with four TODO lines. We fill them on the screen, one at a time.

**SAY:** Now we write step one together. \[PAUSE\] Look at the top of the function: s and b are the parameters, n on is the observable, and **b zero is a global observable**: the result of the auxiliary measurement. It is a number, it is constant, and it is not in the dataset. \[PAUSE\] First line: the expected count in the signal region, mu on, a RooFormulaVar, at zero plus at one, with s and b. Second line: the Poisson for n on. Third line: **the constraint term**, a RooGaussian of b zero, with mean b and width sigma b. \[PAUSE\] Fourth line: the model is the product of the Poisson and the constraint, a RooProdPdf. \[PAUSE\] And look at the last line, which is already written: createNLL with GlobalObservables. **That is how the fit knows that b zero is not a free variable.**

*IT: riempi dal vivo i 4 TODO di build_gauss (circa 5 min): RooFormulaVar s+b; RooPoisson; RooGaussian(b0, b, sb) = termine di vincolo; RooProdPdf. b0 è un osservabile globale: costante, non nel dataset; createNLL con GlobalObservables lo dice al fit.*

**Ask:** Why is b zero not in the dataset? **Expected:** it is the result of the auxiliary measurement: a number that we treat as fixed (a global observable), not a measured event.

---

## 0:40 — Hands-on A: On/off with a Gaussian constraint (slides 9–10, 40 min)

**\[DO\] slide 10 — Exercise A**

**SAY:** Exercise A. We use the top-quark numbers: seventeen events, background three point eight plus or minus zero point six. \[PAUSE\] Step one: build the model with a Gaussian constraint. The function build Poisson aux is given, as a reference. You write build Gauss. Step two: compute the significance for both models. You write the function z zero: a free fit, a fit with s equal to zero, and the square root of two delta NLL. The two models should agree. Step three: repeat with a poor control region, four events. Which model is too optimistic? \[PAUSE\] Open ex A in the lab 3 folder. Forty minutes.

*IT: A1 build\_gauss, A2 z0, A3 controllo povero (4 eventi). Attesi: Z≈4.6 per entrambi; con 4 eventi Poisson 3.06 vs Gauss 3.54.*

**While walking around:**

- What is b zero? Is it in the dataset?
- Is s constant when you fit with s equal to zero?
- Do you get the same significance as the check cell?
- Why do we return a dictionary from the function? (To keep the objects alive.)

**At the end (SAY):** Let's compare. With forty control events, both models give four point six. \[PAUSE\] With four control events, the Poisson gives three, the Gaussian gives three and a half. **The Gaussian is too optimistic. It does not know that four events are a very poor measurement.**

---

## 1:20 — BREAK (15 min)

**SAY:** Let's take a break. We restart at 10:25.

---

## 1:35 — Talk B: RooStats (slides 11–14, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold line of each slide and come back to the rest at the end of the hands-on.*

**\[DO\] slide 12 — Roles in RooStats**

**SAY:** Welcome back. Now RooStats. RooStats needs to know the role of every element of the model. \[PAUSE\] Look at the table. The model: SetPdf. The parameters of interest: for us, the signal strength. The nuisance parameters. The observables, the data. And the global observables. All of these live in an object called ModelConfig. Then the calculators work on a pair: the data, and the ModelConfig. **If you give the right roles, RooStats does the rest.** The calculators we see: the profile likelihood calculator, the asymptotic calculator, the frequentist calculator with toys, and the hypothesis test inverter for limits.

*IT: ModelConfig = ruoli degli elementi. I calcolatori lavorano su (dati, ModelConfig).*

**\[DO\] slide 13 — Hypothesis test and significance**

**SAY:** The hypothesis test. The null hypothesis is: no signal, mu equal to zero. The test statistic, q zero, is minus two times the log of the profile likelihood ratio. The significance Z is the square root of q zero. And the p-value is one minus the Gaussian cumulative of Z. \[PAUSE\] Two numbers to remember. Three sigma, one in about eight hundred: evidence. Five sigma, about three in ten million: discovery. \[PAUSE\] And a useful formula, from the paper of Cowan, Cranmer, Gross and Vitells. When the background is known, the Asimov significance is: square root of two times s plus b, times the log of one plus s over b, minus s. For s much smaller than b it becomes s over square root of b. **But s over root b overestimates the significance when s is not small. Do not use it for a result.**

*IT: q0, Z=sqrt(q0), p; 3σ=1.3e-3, 5σ=2.9e-7; formula di Asimov; s/√b sovrastima.*

**\[DO\] slide 14 — Intervals and limits**

**SAY:** Three questions, three tools. How significant is the excess? The hypothesis test. What is mu, with its uncertainty? The profile likelihood interval, as in Lab 2. Nothing is seen: how large can mu be? The upper limit, with the CLs method. \[PAUSE\] Asymptotic formulae are fast, and good for large samples. With few counts you need toys. **Choose the calculator from the question, not from habit.**

*IT: tre domande, tre strumenti; asintotico vs toy. CLs nel notebook opzionale.*

---

## 1:50 — Live coding B1: the ModelConfig (5 min)

**\[DO\]** Open the notebook ex B, cell B1. The workspace is already built. We fill the ModelConfig lines on the screen.

**SAY:** Now the ModelConfig. \[PAUSE\] RooStats needs to know the **role** of each variable. We say it five times. The pdf: mc dot SetPdf, with the pdf of the workspace. The parameter of interest: SetParametersOfInterest, a RooArgSet with s. The nuisance parameters: SetNuisanceParameters, with b. The observables: SetObservables, with n on. And the global observables: SetGlobalObservables, with b zero. \[PAUSE\] **Five roles: the parameter we want, the parameter we do not care about, the data, and the result of the auxiliary measurement.** Then mc dot Print, to check.

*IT: riempi dal vivo i TODO del ModelConfig (circa 5 min): SetPdf, SetParametersOfInterest(s), SetNuisanceParameters(b), SetObservables(n_on), SetGlobalObservables(b0); poi Print.*

**Ask:** Which variable is the parameter of interest, which one is nuisance, which one is a global observable? **Expected:** s, b, b zero.

---

## 1:55 — Hands-on B: ModelConfig and hypothesis test (slides 15–16, 40 min)

**\[DO\] slide 16 — Exercise B**

**SAY:** Exercise B. The same top-quark model, now in a workspace. \[PAUSE\] Step one: import the model and the data, and define the roles in the ModelConfig. Step two: the sixty-eight and ninety-five percent intervals on s, with the profile likelihood calculator. Step three: the significance and the p-value. Step four: compare with s over root b, and with the Asimov formula. Which is closest to RooStats? And why? \[PAUSE\] Forty minutes.

*IT: B1 ModelConfig, B2 intervalli, B3 significatività, B4 confronto formule. Attesi: \[9.4,17.7\] al 68%; Z≈4.6; Z\_A=4.95; s/√b=6.8.*

**While walking around:**

- Which are the global observables in your model?
- Did you set the null parameters before the hypothesis test?
- What does the check cell say?
- Why is the Asimov number higher than the RooStats number?

**At the end (SAY):** Let's look at the three numbers. S over root b: six point eight. Asimov: four point nine five. RooStats: four point six. \[PAUSE\] **Each step adds realism: first the Poisson fluctuations, then the uncertainty on the background.** And each number is a good lesson: a simple formula can overestimate a significance by fifty percent.

---

## 2:35 — BREAK (10 min)

**SAY:** Let's take a short break. We restart at 11:35.

---

## 2:45 — Talk C: Correlated systematics (slides 17–20, 10 min)

*Time-box: 10 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold line of each slide and come back to the rest at the end of the hands-on.*

**\[DO\] slide 18 — Systematics are correlated**

**SAY:** A systematic uncertainty rarely affects only one number. A source, for example the charm cross section, or the tagging efficiency, or the luminosity, moves several yields together. \[PAUSE\] We write this with a covariance matrix. Sigma i j is the sum, over the sources, of the effect of source k on channel i, times the effect on channel j. If the errors are independent, the matrix is diagonal. If a source is common to two channels, we have off-diagonal terms. **Ignoring them changes the size of the uncertainty on mu. How much? Only a calculation can tell.**

*IT: una sorgente muove più canali; Sigma = somma v v^T; fuori diagonale = correlazioni.*

**\[DO\] slide 19 — Diagonalise**

**SAY:** How do we put a covariance matrix in a likelihood? We diagonalise it. A real symmetric matrix can be written as U Lambda U transpose. Lambda is diagonal, with the eigenvalues. Then we define independent nuisance parameters, z k. Each one is a standard Gaussian. And the correlated parameters are: beta zero, plus U, times square root of Lambda, times z. \[PAUSE\] Two practical results. One: we need one nuisance parameter for each non-zero eigenvalue. This is the rank of the matrix. Four channels, three sources: three nuisance parameters, not four. Two: if the errors are fully correlated, there is only one nuisance parameter. **This is what HistFactory, pyhf, and the experiment combinations do under the hood.**

*IT: Σ=UΛU^T; β=β0+U√Λ z; z indipendenti N(0,1); rango = numero di sorgenti.*

**\[DO\] slide 20 — A real problem: OPERA**

**SAY:** Here is our real problem. The OPERA experiment. It looks for tau neutrinos appearing in a muon-neutrino beam. This is the final analysis, from the 2018 paper. Four channels, which are four decay modes of the tau. Ten candidate events. \[PAUSE\] Look at the table: the backgrounds by source, the expected signal, the observed events. Notice something. All the signal errors are about twenty percent. In the 2015 paper, the sources are listed: the model, ten percent. The oscillation parameters, ten percent. The tagging efficiency, fifteen percent. These are common to all channels. \[PAUSE\] **Our assumption: each source is fully correlated across the channels it affects. This is our modelling choice. It is not the published treatment of the collaboration.** Please remember this, and say it in your report.

*IT: OPERA reale (Tab. III, arXiv:1804.04912). L'ipotesi di correlazione piena è NOSTRA, non della collaborazione: ribadiscilo.*

---

## 2:55 — Live coding C1: covariance and diagonalisation (5 min)

**\[DO\]** Open the notebook ex C, cell C1. The function `factor` has a TODO with the hint in a comment. We write the three lines on the screen.

**SAY:** Now the factorisation of the covariance matrix. \[PAUSE\] We want a matrix A such that A times A transposed is Sigma. First line: eigh of Sigma, which gives the eigenvalues, w, and the eigenvectors, U. \[PAUSE\] Second line: **we keep only the non-zero eigenvalues**. Third line: A is U times the square root of the eigenvalues, one column for each non-zero eigenvalue. \[PAUSE\] **The number of columns is the rank of Sigma: the number of independent sources.** Four channels with three sources give three columns, so three nuisance parameters, not four.

*IT: riempi dal vivo factor (circa 5 min): eigh(Sigma) → tieni solo gli autovalori > tol → A = U·sqrt(w). Le colonne = rango = fonti indipendenti: 4 canali e 3 fonti → 3 nuisance.*

**Ask:** Four channels, three independent sources. How many columns does A have? **Expected:** three.

---

## 3:00 — Hands-on C: OPERA with a covariance matrix (slides 21–22, 40 min)

**\[DO\] slide 22 — Exercise C**

**SAY:** Exercise C is the main one today. \[PAUSE\] Step one: build the covariance matrix of the backgrounds from the three sources, and diagonalise it with numpy. What is the rank? Step two: build the RooFit model. Four Poisson terms. The expected background is beta zero plus A times z. And one Gaussian constraint for each z. Step three: fit, compute the significance and the sixty-eight percent interval on mu. Step four: add the signal uncertainty, twenty percent per channel, with correlation rho. Scan rho equal to zero, zero point five, one. Step five: by how much does the interval change? Does the significance change? \[PAUSE\] This will take about forty minutes. Please ask when you are stuck: the model building is the difficult part.

*IT: C1 factor(), C2 build\_opera (formule lin e lam), C3 scansione rho. Attesi: rango 3; Z≈3.9; larghezza intervallo ≈0.96 (ρ=0), ≈1.06 (ρ=1).*

**While walking around:**

- What is the rank of your matrix? Why not four?
- What is the range of z? Is the background positive at the minimum?
- Why do we use max of the expression and a small number in the Poisson mean?
- Does the fit converge?

**At the end (SAY):** Let's see the result. \[PAUSE\] The interval on mu is about ten percent wider when the signal uncertainty is fully correlated. And the significance of mu equal to zero does not change at all. Why? \[PAUSE\] Because at mu equal to zero the signal is multiplied by zero. **The signal uncertainty cannot matter for the discovery. It matters for the measurement.** And the main message: ten events. The Poisson fluctuation dominates. The systematics change the interval by only ten percent. So improving the systematic estimate would help little here.

---

## 3:40 — Open lab (slide 23, 15 min)

**SAY:** Now fifteen minutes of open lab. Finish a notebook, or start the one you have not done. The three notebooks of today are independent. \[PAUSE\] For every systematic you write, ask three questions. Is it an auxiliary measurement, or a constraint term? What is the source, and what size can you justify? And how much does the result change, with and without it? **If the answer is almost nothing, write it in your notebook. That is a result.** I walk around.

*IT: lab aperto; una sistematica = nome, sorgente, taglia; risultato con e senza; "quasi nulla" è un risultato.*

**Questions to ask each student:**

- Which notebook are you on? Which two will you submit?
- Is this systematic an auxiliary measurement or a constraint?
- How big is the change on your result?
- In Exercise C: which are the global observables, and which are the nuisance parameters?

---

## 3:55 — Wrap-up (slide 24, 5 min)

**SAY:** Let's finish. Today you learned three things. First, constraint terms and auxiliary measurements, and the global observables. Second, RooStats: the ModelConfig, the hypothesis test, the profile interval, and the Asimov formula. Third, correlated systematics, covariance, diagonalisation, and rank. \[PAUSE\] For Lab 4: submit two of the three notebooks on Virtuale. At the beginning of Lab 4, we look together at the solutions of all three. And read the HistFactory section in the ROOT manual. \[PAUSE\] **In Lab 4 we build a binned model with HistFactory, we use RDataFrame, and we finish with a demo of TMVA.** Thank you. See you in two weeks.

*IT: 3 cose, compiti (2 notebook su 3 su Virtuale, lettura HistFactory), anteprima Lab 4: HistFactory, RDataFrame, demo TMVA.*

---

## Emergency notes

- **Late?** Skip B4 (the formula comparison) and shorten the CLs remark. Never skip Exercise C: it is the capstone.
- **build\_opera fails or does not converge?** Say: Please widen the range of z, or start from mu equal to one. Use the solution notebook for the formula lines only.
- **RooStats PLC returns strange numbers?** Check the global observables and the null parameters. Say: This is a role problem, not a physics problem.
- **A student asks about the paper's 6.1 sigma?** Say: The paper uses the kinematic information of each candidate. We use only the counts, so we get less.

---

## Setup reminders (ROOT on the student laptops)

**SAY (at the start, after the recap):** A short reminder. If ROOT is not working on your laptop, please use GitHub Codespaces in your browser. Today the notebooks are heavier: the RooStats calculators and the OPERA model need a minute to run. Please be patient, and please do not close the notebook while a cell is running. \[PAUSE\] When you finish, stop your codespace. It uses your free quota while it is running.

*IT: ricorda Codespaces come piano B; le celle RooStats/OPERA richiedono circa un minuto; fermare il codespace a fine lavoro.*

**Notes for you:**

- Exercise C (OPERA) builds a model with many nuisance parameters. On a 2-core codespace it can take a few minutes: tell the students before they start.
- If a student sees a crash in RooStats on their own laptop, ask for the ROOT version. Compare it with the one in the Codespace, and suggest to continue in the Codespace.
- Students working in Codespaces download the notebooks and upload them on Virtuale.

| Situation | Say | IT |
| --- | --- | --- |
| Slow | This step takes a minute. Please be patient. | Ci vuole un minuto |
| Version | Which ROOT version do you have? | Che versione di ROOT? |
| Fallback | Please continue in Codespaces. | Continuate in Codespaces |
