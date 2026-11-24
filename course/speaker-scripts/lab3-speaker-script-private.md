# Lab 3 — Speaker Script

*Companion of lab3.md (28 slides).*

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

## 0:00 — Recap and solutions of Lab 2 (slides 1–5, 20 min)

**SAY (slide 1):** Good morning, and welcome back. This is Lab 3: systematics and inference. In Lab 2 we saw the profile likelihood and the on/off problem. Today we ask the real question of every analysis: how do we treat what we do not know? \[PAUSE\] We have three parts. First, how to write a systematic uncertainty. Second, how to make statistical statements with RooStats. Third, a real problem, with correlated uncertainties.

*IT: oggi: come scrivere una sistematica, RooStats, caso reale con correlazioni.*

**\[DO\] slide 2 — Recap**

**SAY:** First a short recap. Please discuss in pairs for two minutes. Question one: slice and profile likelihood. Which is wider, and why? Question two: in the on/off problem, where does the uncertainty on the background come from? Question three: your pull has an RMS of one point three. What does it tell you? Question four: which two notebooks of Lab 2 did you submit? Did the toy study run for you?

**Expected answers:**

1. Profile is wider: nuisance parameters are re-fitted, so their uncertainty adds.
2. From the control region: it is the Poisson uncertainty of n off, divided by tau.
3. The errors are underestimated by thirty percent: the fit errors are too small.
4. Collect two or three answers. Note which notebook of Lab 2 was the hardest, and what students found unclear: those are the first cells to open in the solutions.

**\[DO\] slide 3 — Recap: answers (3 min)**

**SAY:** Here are the answers: all on this slide, you do not need the slides of Lab 2. \[PAUSE\] One: a slice keeps the nuisance parameters fixed, a profile re-fits them, so the profile is wider. Two: the uncertainty on the background comes from the control region: the Poisson uncertainty of n off, divided by tau. Three: an RMS of one point three means that the uncertainty is underestimated, by about thirty percent. Four: the hardest cells, we open them now.

*IT: risposte sulla stessa slide (niente cambio di PDF): slice vs profilo; incertezza sul fondo dalla regione di controllo; RMS > 1 = incertezza sottostimata; celle più difficili → soluzioni.*

**How to run the recap:** show slide 2, two minutes in pairs, one pair per question, then show slide 3. Do not re-explain slides of Lab 2.

**\[DO\] slide 4 — Solutions of Lab 2 (15 min)**

**SAY:** Now the solutions of Lab 2. I show the cells that were the hardest for you, the ones you named in the recap. \[PAUSE\] Open the solution notebooks, run them from the top, and go to the key cells. One minute of explanation and one question for each.

*IT: 15 minuti: soluzioni del Lab 2, solo le celle più difficili. Una domanda per ciascuno.*

- **Exercise A (5 min).** A1: NLL, MIGRAD, HESSE. A2: MINOS. A5: the contour. **Ask:** HESSE and MINOS differ: which one do you trust? **Expected:** MINOS: the likelihood is not a parabola.
- **Exercise B (5 min).** B1: the on/off model, b hat close to 3.8 and s hat close to 13.2. B2: the profile interval against MINOS. B3: slice against profile, with a poorer control region. **Ask:** why is the profile wider than the slice? **Expected:** the nuisance parameter is re-fitted, so its uncertainty adds.
- **Exercise C (5 min).** C1: the toy study and the pulls. C2: low statistics, failed fits and boundaries. **Ask:** what does a pull RMS of 1.3 tell you? **Expected:** the errors are underestimated by about thirty percent.
- If a student asks for another cell, show it. The solutions are in the solutions branch, from today.

**\[DO\] slide 5 — Schedule**

**SAY:** Here is today's plan. Three talks, three hands-on parts, two breaks. **Before each hands-on, we write the first step together, live, for five minutes.** The last fifteen minutes are an open lab: you finish a notebook, and I help you. Every systematic you will write today has a name, a source and a size. Please listen with these three words in mind.

---

## 0:20 — Talk A: Constraints vs auxiliary measurements (slides 6–9, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold line of each slide and come back to the rest at the end of the hands-on.*

**\[DO\] slide 7 — Two ways to model a systematic**

**SAY:** A nuisance parameter is a quantity that we need in the model, but we know it only with an uncertainty. Where does our knowledge come from? \[PAUSE\] There are two ways to write it. The first: an auxiliary measurement. We write the likelihood of the control data. For example, a Poisson for n off. The second: a constraint term. We write a probability distribution for the result of that measurement. For example, a Gaussian centred on the background estimate, with the quoted uncertainty. \[PAUSE\] Look at the table. With the auxiliary measurement, you need the control data. With the constraint, you need only the summary, for example a paper that says: background three point eight, plus or minus zero point six. **Both enter the likelihood as a factor. The second one is an approximation of the first.**

*IT: misura ausiliaria (likelihood dei dati di controllo) vs vincolo (pdf del risultato). Il vincolo è un'approssimazione.*

**\[DO\] slide 8 — From on/off to a Gaussian constraint**

**SAY:** Let us see when the approximation is good. The control measurement gives b hat equal to n off divided by tau. And the uncertainty is the square root of n off, divided by tau. For a large n off, the Poisson is almost Gaussian. This works for about thirty to fifty counts, or more. \[PAUSE\] For few counts, it fails. The Gaussian is symmetric. It allows negative background. And it makes the significance too high. \[PAUSE\] Two alternatives. If the uncertainty is multiplicative and the quantity is positive, for example an efficiency, use a log-normal. If you know the number of control events, the exact partner of the Poisson is the Gamma distribution. **Rule: use the measurement when you have it. Use a constraint when you have only its result.**

*IT: Gauss ok per n\_off grande; per pochi conteggi sovrastima la significatività; log-normale per efficienze, Gamma come coniugata esatta.*

**Ask the class:** A paper says: background zero point five plus or minus zero point four. Can you use a Gaussian? **Answer:** No: the Gaussian gives weight to negative values. Use a log-normal or a Gamma.

**\[DO\] slide 9 — The full model, and global observables**

**SAY:** Now the full model. It is the one from Lab 1: the extended marked Poisson. A Poisson for the number of events, times the product of the densities. And now, a new factor: the product of all the constraint terms. \[PAUSE\] In a constraint term, a j is the result of the auxiliary measurement. We call it a global observable. Remember this rule. **In the fit, the global observables are constants. In toy experiments, they are thrown again, together with the data.** In RooFit, you tell this to createNLL with the option GlobalObservables. In RooStats, with ModelConfig.

*IT: modello completo = marked Poisson × vincoli. Global observables: costanti nel fit, rigenerate nei toy.*

---

## 0:35 — Live coding A1: the Gaussian constraint (5 min)

**\[DO\]** Open the notebook ex A, cell A1. `build_gauss` is already there, with four TODO lines. We fill them on the screen, one at a time.

**SAY:** Now we write step one together. \[PAUSE\] Look at the top of the function: s and b are the parameters, n on is the observable, and **b zero is a global observable**: the result of the auxiliary measurement. It is a number, it is constant, and it is not in the dataset. \[PAUSE\] First line: the expected count in the signal region, mu on, a RooFormulaVar, at zero plus at one, with s and b. Second line: the Poisson for n on. Third line: **the constraint term**, a RooGaussian of b zero, with mean b and width sigma b. \[PAUSE\] Fourth line: the model is the product of the Poisson and the constraint, a RooProdPdf. \[PAUSE\] And look at the last line, which is already written: createNLL with GlobalObservables. **That is how the fit knows that b zero is not a free variable.**

*IT: riempi dal vivo i 4 TODO di build_gauss (circa 5 min): RooFormulaVar s+b; RooPoisson; RooGaussian(b0, b, sb) = termine di vincolo; RooProdPdf. b0 è un osservabile globale: costante, non nel dataset; createNLL con GlobalObservables lo dice al fit.*

**Ask:** Why is b zero not in the dataset? **Expected:** it is the result of the auxiliary measurement: a number that we treat as fixed (a global observable), not a measured event.

---

## 0:40 — Hands-on A: On/off with a Gaussian constraint (slides 10–12, 40 min)

**\[DO\] slide 11 — Exercise A**

**SAY:** Exercise A. We use the top-quark numbers: seventeen events, background three point eight plus or minus zero point six. \[PAUSE\] Step one: build the model with a Gaussian constraint. The function build Poisson aux is given, as a reference. You write build Gauss. Step two: compute the significance for both models. You write the function z zero: a free fit, a fit with s equal to zero, and the square root of two delta NLL. The two models should agree. Step three: repeat with a poor control region, four events. Which model is too optimistic? \[PAUSE\] Open ex A in the lab 3 folder. Forty minutes.

*IT: A1 build\_gauss, A2 z0, A3 controllo povero (4 eventi). Attesi: Z≈4.6 per entrambi; con 4 eventi Poisson 3.06 vs Gauss 3.54.*

**While walking around:**

- What is b zero? Is it in the dataset?
- Is s constant when you fit with s equal to zero?
- Do you get the same significance as the check cell?
- Why do we return a dictionary from the function? (To keep the objects alive.)

**At the end (SAY):** Let's compare. With forty control events, both models give four point six. \[PAUSE\] With four control events, the Poisson gives three, the Gaussian gives three and a half. **The Gaussian is too optimistic. It does not know that four events are a very poor measurement.**


**\[DO\] slide 12 — Key Takeaways from Hands-on A (2 min, at the end)**

**SAY:** Statistics. **A constraint is the pdf of an auxiliary measurement: a Gaussian of b zero around b. The measurement b zero is a number, not a data event.** A poor control region means a large uncertainty on b, and a lower significance. \[PAUSE\] RooFit. The constraint is a RooGaussian of b zero with mean b and width sigma b, multiplied by the model with a RooProdPdf. And create NLL with GlobalObservables tells the fit that b zero is a global observable, not a free variable.

*IT: statistica: il vincolo = pdf di una misura ausiliaria (gaussiana di b0 attorno a b); b0 è un numero, non un evento; controllo povero → incertezza su b grande, significatività minore. RooFit: RooGaussian + RooProdPdf; createNLL(..., GlobalObservables(b0)).*

---

## 1:20 — BREAK (15 min)

**SAY:** Let's take a break. We restart at 10:25.

---

## 1:35 — Talk B: RooStats (slides 13–16, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold line of each slide and come back to the rest at the end of the hands-on.*

**\[DO\] slide 15 —  From the model to a statement**


SAY: “Three questions, one likelihood. Significance, interval, limit. RooFit builds the model, RooStats gives the statement.” (~1 min)

**SAY:** Three questions, three tools. How significant is the excess? The hypothesis test. What is mu, with its uncertainty? The profile likelihood interval, as in Lab 2. Nothing is seen: how large can mu be? The upper limit, with the CLs method. \[PAUSE\] Asymptotic formulae are fast, and good for large samples. With few counts you need toys. **Choose the calculator from the question, not from habit.**

*IT: tre domande, tre strumenti; asintotico vs toy. CLs nel notebook opzionale.*


**\[DO\] slide 16 — Roles in RooStats**

**SAY:** Welcome back. Now we move from RooFit to **RooStats**. Remember the division of labor: RooFit build PDFs and likelihoods, while RooStats is the statistical inference layer on top—it and automates hypothesis tests, confidence intervals, and upper limits. [PAUSE] Unlike a manual `Migrad` fit, RooStats cannot guess what each variable in your model represents. It needs to know the **role** of every element, and we store those roles inside a **`ModelConfig`** object. Look at the table The model: SetPdf. The parameters of interest: for us, the signal strength. The nuisance parameters. The observables, the data. And the global observables. All of these live in an object called ModelConfig. Then the calculators work on a pair: the data, and the ModelConfig. **If you give the right roles, RooStats does the rest.** The calculators we see: the profile likelihood calculator, the asymptotic calculator, the frequentist calculator with toys, and the hypothesis test inverter for limits.

*IT: ModelConfig = ruoli degli elementi. I calcolatori lavorano su (dati, ModelConfig).*

**\[DO\] slide 17 — One ratio, two uses**

SAY: “Same ratio as Lab 2. Fix mu at zero: significance. Fix mu at every value: interval.” The hypothesis test. The null hypothesis is: no signal, mu equal to zero. The test statistic, q zero, is minus two times the log of the profile likelihood ratio. The significance Z is the square root of q zero. And the p-value is one minus the Gaussian cumulative of Z. \[PAUSE\] Poi 3σ/5σ. Two numbers to remember. Three sigma, one in about eight hundred: evidence. Five sigma, about three in ten million: discovery. \[PAUSE\] 
Chiudi con “asymptotic is fast, toys for few counts”. 

*IT: q0, Z=sqrt(q0), p; 3σ=1.3e-3, 5σ=2.9e-7;*

**\[DO\] slide 18 — Estimating Z by hand**

And a useful formula, from the paper of Cowan, Cranmer, Gross and Vitells. When the background is known, the Asimov significance is: square root of two times s plus b, times the log of one plus s over b, minus s. For s much smaller than b it becomes s over square root of b. **But s over root b overestimates the significance when s is not small. Do not use it for a result.**

Chiudi con il link a Ex B4.

*IT: formula di Asimov; s/√b sovrastima.*

---

## 1:50 — Live coding B1: the ModelConfig (5 min)

**\[DO\]** Open the notebook ex B, cell B1. The workspace is already built. We fill the ModelConfig lines on the screen.

**SAY:** Now the ModelConfig. \[PAUSE\] RooStats needs to know the **role** of each variable. We say it five times. The pdf: mc dot SetPdf, with the pdf of the workspace. The parameter of interest: SetParametersOfInterest, a RooArgSet with s. The nuisance parameters: SetNuisanceParameters, with b. The observables: SetObservables, with n on. And the global observables: SetGlobalObservables, with b zero. \[PAUSE\] **Five roles: the parameter we want, the parameter we do not care about, the data, and the result of the auxiliary measurement.** Then mc dot Print, to check.

*IT: riempi dal vivo i TODO del ModelConfig (circa 5 min): SetPdf, SetParametersOfInterest(s), SetNuisanceParameters(b), SetObservables(n_on), SetGlobalObservables(b0); poi Print.*

**Ask:** Which variable is the parameter of interest, which one is nuisance, which one is a global observable? **Expected:** s, b, b zero.

---

## 1:55 — Hands-on B: ModelConfig and hypothesis test (slides 17–19, 40 min)

**\[DO\] slide 18 — Exercise B**

**SAY:** Exercise B. The same top-quark model, now in a workspace. \[PAUSE\] Step one: import the model and the data, and define the roles in the ModelConfig. Step two: the sixty-eight and ninety-five percent intervals on s, with the profile likelihood calculator. Step three: the significance and the p-value. Step four: compare with s over root b, and with the Asimov formula. Which is closest to RooStats? And why? \[PAUSE\] Forty minutes.

*IT: B1 ModelConfig, B2 intervalli, B3 significatività, B4 confronto formule. Attesi: \[9.4,17.7\] al 68%; Z≈4.6; Z\_A=4.95; s/√b=6.8.*

**While walking around:**

- Which are the global observables in your model?
- Did you set the null parameters before the hypothesis test?
- What does the check cell say?
- Why is the Asimov number higher than the RooStats number?

**At the end (SAY):** Let's look at the three numbers. S over root b: six point eight. Asimov: four point nine five. RooStats: four point six. \[PAUSE\] **Each step adds realism: first the Poisson fluctuations, then the uncertainty on the background.** And each number is a good lesson: a simple formula can overestimate a significance by fifty percent.


**\[DO\] slide 19 — Key Takeaways from Hands-on B (2 min, at the end)**

**SAY:** Statistics. **A discovery is a test of the background-only hypothesis: a p-value, expressed in sigma.** An upper limit is a different question. s over square root of b is a rough guide, and the Asimov formula ignores the uncertainty on b. \[PAUSE\] RooStats. The RooWorkspace holds the model and the data. The ModelConfig gives the roles: pdf, parameter of interest, nuisance parameters, observables and global observables. **The ProfileLikelihoodCalculator takes a ModelConfig, and gives the intervals and the p-value.**

*IT: statistica: scoperta = test dell'ipotesi di solo fondo (p-value → sigma); limite superiore = altra domanda; s/√b è una guida, Z_A ignora l'incertezza su b. RooStats: RooWorkspace, ModelConfig (ruoli), ProfileLikelihoodCalculator (intervalli e p-value).*

---

## 2:35 — BREAK (10 min)

**SAY:** Let's take a short break. We restart at 11:35.

---
## 2:45 — Talk C: Correlated systematics (slides 20–24, 12 min)

**\[DO\] slide 21 — Systematics are correlated across channels**
**SAY:** Welcome to the final part: correlated systematics. A systematic rarely affects only one number. A source—for example the luminosity, a tagging efficiency, or a background cross section—moves several channel yields together. \[PAUSE\] We associate an independent, standard-normal nuisance parameter theta k to each physical source k, and v i k tells us how much channel i moves for a one-sigma shift. Across the channels, this induces a covariance matrix: Sigma i j is the sum over sources of v i k times v j k. **Ignoring off-diagonal terms changes both the uncertainty on mu and the significance Z zero.**

**\[DO\] slide 22 — A 2-channel example: two ways to write the same model**
**SAY:** Let's see this on a concrete two-channel example before touching any matrices. Suppose two channels share a single common ten-percent uncertainty, so correlation rho equals one. The covariance matrix Sigma has determinant zero—it is rank one, so you cannot invert it to write a two-dimensional Gaussian! \[PAUSE\] Instead, we use the standard high-energy physics trick: we introduce **just one** standard-normal parameter theta, and write beta one equal to beta zero one plus sigma one times theta, and beta two equal to beta zero two plus sigma two times theta. **A single shared parameter theta automatically enforces one-hundred-percent correlation without inverting Sigma.**

**\[DO\] slide 23 — General case: from any Sigma to independent theta k**
**SAY:** Now, what if we are given a general covariance matrix Sigma? Any symmetric positive-semidefinite Sigma can be diagonalised: U Lambda U transpose. Define A equal to U times the square root of Lambda, keeping only the non-zero eigenvalues. Then beta vector is beta zero plus A times theta vector, with independent standard-normal theta k. \[PAUSE\] **The number of nuisance parameters theta k is the rank of Sigma—never more than the number of channels.** And in RooFit, once A is computed, you only need linear RooFormulaVar expressions and one-dimensional RooGaussian constraints.

**\[DO\] slide 24 — Hands-on problem: a 2-channel search (e and mu)**
**SAY:** Here is our hands-on problem: combining two search channels, electron and muon. Each channel has one hundred expected background events with a fifteen-percent uncertainty, twenty-five expected signal events, and we observe one hundred thirty and one hundred twenty-eight events. \[PAUSE\] Look at what happens as we vary the correlation rho between the two background uncertainties: when rho is zero, independent background fluctuations can partially cancel; when rho is one, a single shared source moves both backgrounds together, widening the interval on mu and lowering the discovery significance Z zero.

---

## 2:57 — Live coding C1: diagonalising Sigma_b (5 min)

**\[DO\]** Open `ex_C.ipynb`, cell C1. We inspect `Sigma_0` and `Sigma_1` and fill `A_0`.

**SAY:** Let's look at cell C1 together. For rho equal to zero, the covariance matrix is diagonal, so `eigh` gives two equal eigenvalues: fifteen squared, two hundred twenty-five. Keeping eigenvalues above ten to the minus ten gives a two-by-two matrix A zero—so two nuisance parameters. \[PAUSE\] Now look right below at rho equal to one: one eigenvalue is zero, and the other is four hundred fifty! So A one has **only one column**: a single shared nuisance parameter theta zero.

---

## 3:02 — Hands-on C: Two channels with correlated background (40 min)

**\[DO\] slide 26 — Exercise C**

**SAY:** In Exercise C, you build this two-channel model in RooFit. First, complete the linear background expressions beta e and beta mu and the Poisson expectations in C2 for rho equal to zero, then compute the sixty-eight percent interval and significance Z zero with RooStats. Next, run C3 to scan rho equal to zero, zero point five, and one, and answer the four questions at the bottom. You have forty minutes.

**At the end (SAY):** Look at the numbers from C3. For uncorrelated backgrounds (rho equal to zero), we get a significance of about two point six sigma. When the background errors are fully correlated (rho equal to one), the model uses just one shared nuisance parameter, the interval on mu becomes nearly thirty percent wider, and the significance drops to about two point one sigma—because both backgrounds can now fluctuate upward together to mimic the excess!

---

**\[DO\] slide 27 — Key Takeaways from Hands-on C (2 min, at the end)**

**SAY:** Statistics. Correlated uncertainties are encoded in the covariance matrix Sigma equal to A times A transpose, assigning **one independent nuisance parameter theta k per non-zero eigenvalue—so the number of parameters equals the rank of Sigma**. For two channels with correlation one, you need just one parameter, not two. And remember what you just saw: positive correlation on the background prevents fluctuations from cancelling across channels, widening the interval on mu and **lowering the significance Z zero**. \[PAUSE\] RooFit. Eigen-decomposition gives A equal to U times square root of Lambda for non-zero eigenvalues. Each channel then gets a linear RooFormulaVar combining the theta k, paired with a one-dimensional RooGaussian constraint centered on the global observable g k equal to zero.

*IT: statistica: covarianza Σ = A·Aᵀ → un nuisance θ_k per autovalore ≠ 0 (numero di nuisance = rango di Σ; 2 canali con ρ=1 → 1 solo parametro); correlazione positiva sul fondo → meno cancellazione tra canali → intervallo più largo e Z₀ più bassa. RooFit: A = U√Λ; RooFormulaVar lineare per canale con θ_k; RooGaussian(g_k, θ_k, 1) con g_k = 0.*


---

## 3:40 — Open lab (slide 27, 15 min)

**SAY:** Now fifteen minutes of open lab. Finish a notebook, or start the one you have not done. The three notebooks of today are independent. \[PAUSE\] For every systematic you write, ask three questions. Is it an auxiliary measurement, or a constraint term? What is the source, and what size can you justify? And how much does the result change, with and without it? **If the answer is almost nothing, write it in your notebook. That is a result.** I walk around.

*IT: lab aperto; una sistematica = nome, sorgente, taglia; risultato con e senza; "quasi nulla" è un risultato.*

**Questions to ask each student:**

- Which notebook are you on? Which two will you submit?
- Is this systematic an auxiliary measurement or a constraint?
- How big is the change on your result?
- In Exercise C: which are the global observables, and which are the nuisance parameters?

---

## 3:55 — Wrap-up (slide 28, 5 min)

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




#### 1. Number of nuisance parameters (\(\rho = 0\) vs \(\rho = 1\)):

For \(\rho = 0\), \[\Sigma _{b}\]⁠ is diagonal with two non-zero eigenvalues (\(\lambda_1 = \lambda_2 = 225\)), so the model needs **2 independent nuisance parameters** (\(\theta_0, \theta_1\)). For \(\rho = 1\), \[\Sigma _{b}\]⁠ has determinant zero and rank 1 (\(\lambda_1 = 450, \lambda_2 = 0\)), so both channels are controlled by **1 shared nuisance parameter** (\[\theta _{0}\]⁠). In general, the number of nuisance parameters equals \(\text{rank}(\Sigma_b)\).

#### 2. Interval width on \[\mu \]⁠ (\(\rho = 0 \to 1\)):

The 68% interval width increases by roughly **25–30%** (from \[\approx 1.06\]⁠ at \(\rho = 0\) to \[\approx 1.36\]⁠ at \(\rho = 1\)). When the two background uncertainties are uncorrelated, independent upward and downward fluctuations partially cancel out when combining the channels; when \(\rho = 1\), both backgrounds shift coherently in the same direction, reducing the precision on \[\mu \]⁠.

#### 3. Why the significance \[Z_{0}\]⁠ drops (\(\approx 2.6\sigma \to \approx 2.1\sigma\)):
Under the background-only hypothesis (\(\mu = 0\)), the observed excesses in both channels (\[130\]⁠ and \[128\]⁠ vs. \[100\]⁠ expected) must be explained by background fluctuations alone. When \(\rho = 1\), a **single** positive pull of the shared nuisance parameter (\(\theta_0 > 0\)) raises both \[\beta _{e}\]⁠ and \[\beta _{\mu }\]⁠ simultaneously at the cost of only one Gaussian penalty term, making the background-only hypothesis much more compatible with the data and lowering \[Z_{0}\]⁠.

#### 4. What if \[\rho \]⁠ were on the signal uncertainty instead of the background?
If the correlation were on the **signal** uncertainty, \[Z_{0}\]⁠ would **not change at all** across \(\rho \in \{0, 0.5, 1\}\). Under the null hypothesis \(\mu = 0\), the expected signal term \(\mu s_i\) vanishes identically in the numerator \(L(\mu=0, \hat{\hat{\theta}})\) of the profile likelihood ratio, so signal nuisance parameters have zero effect on the background-only fit (they only widen the interval on \[\^{\mu }\]⁠).
