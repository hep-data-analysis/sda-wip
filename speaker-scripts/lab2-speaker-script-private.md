# Lab 2 — Speaker Script

*Companion of lab2.md (32 slides).*

## Notes for today

*How to use the scripts, survival phrases and pronunciation help: see `how-to-use-and-pronunciation-private.md`.*

- Il Lab 2 è il più “teorico” dei primi due: tieni il ritmo con le domande alla classe.

## New phrases for today

| Situation | Say | IT |
| --- | --- | --- |
| Recap | Please discuss in pairs for two minutes. | Parlatene in coppie per due minuti |
| Poll | Raise your hand if you think the answer is yes. | Alzi la mano chi pensa di sì |
| Wrong answer | Almost. Let's think about it together. | Quasi, ragioniamoci |
| Right answer | Exactly. Well done. | Esatto, bravi |
| Show | Let me show you on the plot. | Ve lo mostro sul grafico |
| Check | What do you see in the output? | Cosa vedete nell'output? |
| Stuck | Which cell fails? Please read me the error. | Quale cella fallisce? Leggetemi l'errore |
| Time left | You have five more minutes. | Cinque minuti ancora |
| Open lab | Tell me which notebook you are working on. | Dite su quale notebook state lavorando |

---

## 0:00 — Recap and solutions of Lab 1 (slides 1–4, 20 min)

**SAY (slide 1):** Good morning, and welcome back. This is Lab 2: likelihood and fit quality. In Lab 1 we built models and we fitted them. Today we open the box. We want to understand what the fit really does, how much we can trust the errors, and how to test a fit. \[PAUSE\] Then we validate it with toys.

*IT: bentornati, oggi apriamo la scatola nera del fit.*

**\[DO\] slide 2 — Recap**

**SAY:** First, a short recap. Four questions. Please discuss in pairs, for two minutes. \[PAUSE\] Question one: in the marked Poisson model, which factor is the rate, and which is the shape? And what is a channel, and what is a component? Question two: extended fit, or fit with fractions. What information do we lose with fractions? Question three: why is a binned likelihood not a chi-square fit? Question four: which two notebooks of Lab 1 did you submit, and which cell was the hardest?

**After two minutes, SAY:** Let's compare. Question one? \[PAUSE\]

**Expected answers:**

1. Rate = Poisson term for n. Shape = product of the densities. A channel is a subset of the data defined by a selection. A component is the part of the model that describes one physics process.
2. With fractions we lose the total yield: the rate.
3. The binned likelihood is Poisson in each bin: exact also with few or zero counts. Chi-square assumes Gaussian errors.
4. Collect two or three answers. Note the hardest cells on the board: they tell you which cells to open first in the solutions. Remind them of the rule: two notebooks out of three.

*IT: 4 domande, risposte attese sopra. Segna alla lavagna le celle più difficili del Lab 1.*

**\[DO\] slide 3 — Solutions of Lab 1 (15 min)**

**SAY:** Now the solutions of Lab 1. I do not show everything: I show the cells that were the hardest for you, the ones you named in the recap. \[PAUSE\] Open the solution notebooks in the repository, run them from the top, and go to the key cells. For each one, one minute of explanation and one question.

*IT: 15 minuti: soluzioni del Lab 1, solo le celle più difficili (quelle emerse nel recap). Notebook di soluzione aperti e già eseguiti; una domanda per ciascuno.*

- **Exercise A (4 min).** A1: the unbinned fit, the data and the pdf. A3: the ranges. **Ask:** in A3 (a), where did sigma stop, and what about its error? **Expected:** at the limit, close to 2: the error is not meaningful there. *(Check the exact numbers on your machine.)*
- **Exercise B (4 min).** B1: the binned Breit–Wigner fit, Poisson in each bin. B2: the central limit theorem and its tails. **Ask:** why is the tail not Gaussian? **Expected:** the theorem describes the bulk; the tails converge slowly.
- **Exercise C (7 min).** C1: the extended fit, nu s and nu b with their errors. C2: the shape-only fit. **Ask:** how many free parameters in C1 and in C2, besides the shapes? **Expected:** two in C1, one in C2. Link it to slides 20 and 21 of Lab 1.
- If a student asks for another cell, show it. The solutions are in the solutions branch, from today.

**\[DO\] slide 4 — Schedule**

**SAY:** This is our plan. Three talks, three hands-on parts, two breaks. **Before each hands-on, we write the first hard step together, live, for five minutes.** At the end, twenty minutes of open lab, to finish a notebook with me. \[PAUSE\] Please do not skip it: it is the most useful time for you.

---

## 0:20 — Talk A: What happens in fitTo (slides 5–10, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. Keep a timer on the desk. No slide is removed: if you are late, say the bold line of slide 9 now, and come back to its table at the end of the hands-on.*

**\[DO\] slide 6 — What happens in fitTo**

**SAY:** When you write fit-to, four things happen. \[PAUSE\] First, RooFit builds the negative log-likelihood. It is a function of the parameters. Second, the minimiser finds the minimum. The minimiser is MINUIT, the minimisation library of ROOT, used in particle physics since the nineteen seventies. The algorithm is called MIGRAD. Third, HESSE computes the covariance matrix from the second derivatives. Fourth, if you ask, MINOS computes asymmetric errors. **Today we call each step ourselves, with a class called RooMinimizer.**

*IT: fitTo = NLL → MIGRAD → HESSE → (MINOS), tre algoritmi di MINUIT, la libreria di minimizzazione di ROOT. Oggi li chiamiamo uno a uno. Perché MINUIT e i rischi di un altro minimizzatore: slide di backup (link in slide 6).*

**\[DO\] slide 7 — MIGRAD, HESSE, MINOS**

**SAY:** Look at the table. These are three algorithms of MINUIT. MIGRAD follows the gradient. It stops when the estimated distance to the minimum, the EDM, is very small. HESSE computes the matrix of second derivatives, and inverts it. The inverse is the covariance matrix. This gives symmetric errors and the correlations. \[PAUSE\] MINOS is different. It scans the likelihood. For each parameter, it looks for the points where the negative log-likelihood rises by zero point five. This gives asymmetric errors. **HESSE assumes the likelihood is a parabola. MINOS does not.** If they disagree, the likelihood is not a parabola, and we trust MINOS.

*IT: HESSE = parabola, simmetrico. MINOS = scansione, asimmetrico. Se discordano, fidati di MINOS.*

**Ask the class:** Why would the two be different? **Answer:** the likelihood is not a parabola: low statistics, a boundary, a non-linear parameter.

**\[DO\] slide 8 — Is my fit healthy?**

**SAY:** Before we use a result, we check the fit. Status must be zero. The covariance quality must be three. This means a full, accurate covariance matrix. The EDM must be tiny. No parameter should sit at its limit. And no correlation should be close to one. \[PAUSE\] **A parameter at its limit is a warning. It is not a result.**

*IT: checklist: status 0, covQual 3, EDM piccolo, nessun parametro al limite, nessuna correlazione ±1.*

**\[DO\] slide 9 — When fits go wrong — Debug Flowchart (1/2)**

**SAY:** Fits fail. This is normal. When a fit fails, follow this checklist, in this order. \[PAUSE\] **One: it does not converge.** MIGRAD does not find the minimum. The ranges are too wide, or the start values are too far from the minimum. Fix: make the ranges narrower with set range, and put a reasonable start value with set val. Start near the value that you expect: the starting value is not the range. \[PAUSE\] **Two: it converges, but the errors are huge, or a correlation is close to one.** The parameters are degenerate: the fit cannot distinguish them. Fix one of the two, or reformulate the model.

*IT: checklist in ordine. 1) non converge: range troppo larghi o valori iniziali lontani → setRange più stretto, setVal ragionevole (il valore iniziale non è il range). 2) errori enormi o |ρ|≈1: parametri degeneri → fissarne uno o riformulare.*

**\[DO\] slide 10 — When fits go wrong — Debug Flowchart (2/2)**

**SAY:** **Three: it converges, but a parameter is at its limit.** For example a fraction equal to zero or one. The limit is too tight, or the model is wrong. Fix: widen the range if it makes sense, or reparametrise: for example fit the logarithm of tau instead of tau. \[PAUSE\] A question that I want you to ask yourself: is the limit physical or numerical? A limit like mu greater than zero is physics: in Lab 3 you will see that it can change the result. A limit only to avoid silly values, like sigma greater than zero, is numerics: it must not touch the best value. **Say which one it is.** *(This point is no longer on the slide: say it, or skip it if you are late.)* RooFit also warns you when a parameter has no bounds: please read the warnings. If you do not want to fit a parameter, fix it with set constant. \[PAUSE\] **Four: it works only on some toys.** Low statistics: the likelihood is not parabolic. Fix: use MINOS, or switch to Neyman intervals, which we see in Lab 3. **We study this case at the end of the morning.**

*IT: 3) parametro al limite: limite troppo stretto o modello sbagliato → allargare, riparametrizzare (ln τ). Limite fisico o numerico? (punto non più in slide). 4) funziona solo su alcuni toy: bassa statistica → MINOS o Neyman (Lab 3); lo vediamo a fine mattina.*

---

## 0:35 — Live coding A1: the NLL and MIGRAD (5 min)

**\[DO\]** Open the notebook ex A, cell A1. The model, the data, and the printing lines are already there. We fill the TODO lines on the screen, one at a time. Students may follow, but it is not required.

**SAY:** Now we write step one together. \[PAUSE\] First, the negative log-likelihood: nll equals model dot createNLL, data, and Extended True. We write Extended explicitly, to make clear that the model is extended. \[PAUSE\] Second, the minimiser: minim equals RooMinimizer of nll. \[PAUSE\] Third, three calls: set print level to minus one, to keep the output short; minimize, Minuit2, Migrad, which is MIGRAD; and hesse, which is HESSE. Fourth, we save the result: res equals minim dot save. \[PAUSE\] **Look at the line that is already in the notebook: err hesse equals nsig dot getError. We keep the HESSE error now, because MINOS will change the error object later.** \[PAUSE\] The last lines print three numbers: the status, the covariance quality, and the EDM.

*IT: riempi dal vivo i TODO di A1 (circa 5 min): createNLL con Extended(True) esplicito → RooMinimizer → setPrintLevel(-1), minimize Migrad, hesse → save. La riga err_hesse c'è già: spiega perché (MINOS cambia l'errore). Si stampano status, covQual, EDM.*

**Expected:** status 0, covQual 3, EDM very small. **If it fails:** the model is probably not defined: run the cells above.

---

## 0:40 — Hands-on A: Anatomy of a fit (slides 11–13, 45 min)

**\[DO\] slide 12 — Exercise A**

**SAY:** Now it is your turn. We use the same data and the same model as in Lab 1, exercise C. \[PAUSE\] Step one. Build the negative log-likelihood. Run MIGRAD and HESSE with RooMinimizer. Read the status, the EDM and the covariance quality. Step two. Run MINOS on the signal yield. Are the errors symmetric? Do they agree with HESSE? Step three. Print the correlation matrix. Which two parameters are most correlated? Step four. Plot the likelihood scan, the profile, and the HESSE parabola together. Step five. Draw the one-sigma and two-sigma contours of signal against background. \[PAUSE\] Open ex A in the lab 2 folder. You have forty-five minutes.

*IT: 5 passi. Leggili lentamente. Poi circola.*

**While walking around:**

- Did the first cell run? Did you set your student number?
- What does the check say?
- Compare the red curve and the dashed curve. Where do they separate?
- Why is the correlation negative?

**At the end (SAY):** Let's stop. Who can tell me the HESSE error and the MINOS errors? \[PAUSE\] **Notice: the MINOS interval is not symmetric. The likelihood is steeper at low signal, because the signal cannot be negative.** And the signal and the background are anti-correlated: they compete for the same events under the peak.

---

**\[DO\] slide 13 — Key Takeaways from Hands-on A (2 min, at the end)**

**SAY:** Five points to remember. \[PAUSE\] fitTo is not magic: it creates the NLL, runs MIGRAD, then HESSE. After a fit, the variables update their value and their error: use get val and get error. For plotting one component, use Components, with a dashed line. The profile re-minimises the nuisance parameters at every point of the parameter of interest. **And for a contour: run HESSE immediately before, to have a clean error matrix, and to avoid stray points.**

*IT: riepilogo A: fitTo = NLL + MIGRAD + HESSE; le variabili si aggiornano; Components per le componenti; profilo = ri-minimizza le nuisance; contour: prima HESSE.*

---

## 1:25 — BREAK (15 min)

**SAY:** Let's take a break. We restart at 10:30.

---

## 1:40 — Talk B: Intervals and nuisance parameters (slides 14–17, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold sentence of slide 14 now, and come back to the rest at the end of the hands-on.*

**\[DO\] slide 15 — Likelihood-ratio intervals**

**SAY:** Welcome back. Now the main idea of the day: likelihood-ratio intervals. For a single parameter, in the large-sample limit, minus two times the log of the likelihood ratio follows a chi-square distribution with one degree of freedom. This is Wilks theorem. \[PAUSE\] Practically: for a sixty-eight percent interval, we look where the negative log-likelihood rises by zero point five. For ninety-five percent, by one point nine two. **The interval is where the curve is below the minimum plus one half. It does not need to be symmetric.** This is the MINOS interval.

*IT: Wilks; 0.5 per il 68%, 1.92 per il 95%; intervallo = dove la curva sta sotto min + 0.5.*

**\[DO\] slide 16 — Nuisance parameters**

**SAY:** A real model has parameters of interest, and nuisance parameters. A nuisance parameter is something we need in the model, but we do not care about. For example, the background rate, the resolution, or an efficiency. \[PAUSE\] There are two ways to draw the likelihood. The slice: we fix the nuisance parameters at their best-fit value. This is too optimistic, because it ignores what we do not know. The profile: for each value of the parameter of interest, we fit the nuisance parameters again. **The profile is wider than the slice. The difference is the cost of the nuisance parameter.**

*IT: slice (parametri fissi, ottimista) vs profile (rifit dei nuisance). Profile più largo.*

**\[DO\] slide 17 — The on/off problem**

**SAY:** Here is a classical example. We count events in the signal region: n on. We count events in a control region: n off. The control region measures the background. The expected counts are s plus b in the signal region, and tau times b in the control region. Tau is the ratio of the sizes of the two regions. \[PAUSE\] The best fit is simple. b hat is n off divided by tau. And s hat is n on minus b hat. **The uncertainty on the background is not an input. It comes from the control region.** When you read a result like background three point eight plus or minus zero point six, this is the model behind it. In Lab 3 we add constraint terms.

*IT: on/off: due Poisson. b = n\_off/tau; s = n\_on − b. L'incertezza su b viene dalla regione di controllo.*

**Ask the class:** If tau is small, what happens to the uncertainty on b? **Answer:** it gets larger: the control region is small.

---

## 1:55 — Live coding B1: the on/off model (5 min)

**\[DO\]** Open the notebook ex B, cell B1. The parameters, the observables and the dataset are already there. We fill the five model lines on the screen. The students write the NLL and the minimiser, which they have just seen in step A1.

**SAY:** Now we write the model of step one together. \[PAUSE\] Look at the top of the cell: s and b are the parameters, n on and n off are the observables, and tau is a constant. \[PAUSE\] The expected count in the signal region is s plus b: we write it with a RooFormulaVar, at zero plus at one. The expected count in the control region is tau times b. \[PAUSE\] For each region, a RooPoisson: the observable, and the expected count. And the model is the product of the two, with RooProdPdf. **Two regions: two Poisson, one product. Notice that b appears in both.** \[PAUSE\] Now it is your turn: the NLL and the minimiser, as in exercise A.

*IT: riempi dal vivo i 5 TODO del modello di B1 (circa 5 min): RooFormulaVar s+b e tau*b; due RooPoisson; RooProdPdf. NLL e minimizer li scrivono loro, come in A1. Nota: b compare in entrambe le regioni.*

**Expected at the end of B1 (for the students):** b hat close to 3.80, s hat close to 13.2, error on b close to 0.60.

---

## 2:00 — Hands-on B: the on/off problem (slides 18–20, 45 min)

**\[DO\] slide 19 — Exercise B**

**SAY:** Exercise B uses the top-quark numbers. Seventeen events observed in the signal region. Forty in the control region. Tau equal to ten point five three. \[PAUSE\] Step one. Build the model with two Poisson distributions. Fit, and read s hat and b hat. Step two. Compute the sixty-eight percent interval on s in two ways: scan the profile, and use MINOS. Compare them. Step three. Compare with the slice. Step four. Repeat with a poorer control region: n off equal to four, tau equal to one point zero five three. The best-fit background is the same. What changes? \[PAUSE\] Forty-five minutes. Please start with the model.

*IT: B1 modello, B2 profile vs MINOS, B3 slice, B4 controllo povero.*

**While walking around:**

- What is the observable here? And the parameters?
- Is tau constant in your code?
- Check: b hat should be about three point eight.
- Is the profile the same as MINOS? It should be.

**At the end (SAY):** Let's compare. With tau equal to ten, profile and slice are almost the same. \[PAUSE\] With the poor control region, the profile is wider. **This is exactly the cost of not knowing the background.** \[PAUSE\] Question: in the notebooks you are working on, where is the control region, and what does it tell you about the background?

---

**\[DO\] slide 20 — Key Takeaways from Hands-on B (2 min, at the end)**

**SAY:** Three points. \[PAUSE\] A slice fixes the nuisance parameters. A profile re-optimises them. **MINOS is exactly the profile scan: the two must agree.** And tau carries the uncertainty on the background from the control region to the signal region.

*IT: riepilogo B: slice fissa le nuisance, profilo le ri-ottimizza; MINOS = scansione del profilo (devono coincidere); τ porta l'incertezza sul fondo dalla regione di controllo a quella di segnale.*

---

## 2:45 — BREAK (10 min)

**SAY:** Let's take a short break. Ten minutes. We restart at 11:45.

---

## 2:55 — Talk C: Toy MC, pulls and residuals (slides 21–26, 10 min)

*Time-box: 10 minutes, plus the 5-minute live coding. No slide is removed: about 2 minutes for each of slides 22, 23 and 24, and 1.5 minutes for slides 25 and 26. If you are late, say the bold sentence of each slide and come back to the rest at the end of the hands-on.*

**\[DO\] slide 22 — Testing the fit with Toy MC**

**SAY:** One last question. How do we know that the errors of the fit are correct? HESSE and MINOS are approximations: they assume that the likelihood is close to a parabola. Is it true for my model, with my number of events? \[PAUSE\] We can test it with a toy study. Four steps. One: generate a dataset from the model, with known true parameters. Two: fit it, exactly as we fit the data. Three: record the fitted values and their errors. Four: repeat, three hundred or a thousand times, and look at the distribution of the results. \[PAUSE\] **In RooFit, a class does this loop for us: RooMCStudy.** We use it in a few minutes.

*IT: toy = molti esperimenti finti con verità nota: genera → fit → registra → ripeti; poi guarda la distribuzione. In RooFit: RooMCStudy.*

**\[DO\] slide 23 — The pull**

**SAY:** For each toy, we compare the fit with the truth. But in which unit? **In units of the error that the fit quotes.** This is the pull: the fitted value, minus the true value, divided by the fitted error. \[PAUSE\] Think about it. The numerator is how far the fit is from the truth. The denominator is how large the fit says its error is. If the estimator is unbiased, and the error is its true spread, then the pull has mean zero and standard deviation one. **A healthy fit gives a standard Gaussian.** \[PAUSE\] One important point: the pull is one number per toy. We need many toys to see its distribution.

*IT: pull = (valore fittato − vero) / errore fittato; fit sano → gaussiana standard; un numero per toy, serve la distribuzione.*

**\[DO\] slide 24 — What to look at in the pull distribution**

**SAY:** Now, what do we look at? Five things. \[PAUSE\] **The mean.** If it is not zero, the estimator is biased. A mean of plus point four means that, on average, the fit is point four sigma above the truth. **The RMS.** If it is larger than one, the errors are underestimated: the fit is too optimistic. If it is smaller than one, the errors are overestimated: the fit is conservative. \[PAUSE\] **The coverage.** The fraction of toys where the pull is between minus one and plus one. It should be about sixty-eight percent. It tells us the same as the RMS, but in a way that does not depend on the shape. \[PAUSE\] **The shape.** A skew or tails mean that the likelihood is not a parabola. And finally the **failed fits**: count them, because they are information about your model.

*IT: media ≠ 0 = bias; RMS > 1 errori sottostimati, < 1 sovrastimati; copertura ~68%; forma non gaussiana = verosimiglianza non parabolica; contare i fit falliti.*

**Ask the class:** A pull distribution has mean plus 0.4 and RMS 0.8. What do you conclude? **Expected answer:** the estimator is biased high, and the uncertainty is overestimated, so the errors are conservative. **If nobody answers, SAY:** The mean is not zero: bias. The RMS is below one: the quoted error is larger than the real spread.

**\[DO\] slide 25 — What goes wrong at low statistics**

**SAY:** What happens with few events? The likelihood is no longer a parabola. Parameters hit boundaries, for example the signal yield cannot be negative. The pulls are not Gaussian. \[PAUSE\] The remedy: report profile or MINOS intervals. Or use a full toy construction, which we see in Lab 3. **A toy that fails is not a missing result. It is information about your model.** In Exercise C you will see this with five signal events.

*IT: bassa statistica: parametri al bordo, pull non gaussiani; riportare intervalli MINOS/profile; contare i fit falliti. Collegare all'esercizio C (ν_s = 5).*

**\[DO\] slide 26 — Residuals vs. pulls**

**SAY:** One last slide, to avoid a common confusion. Residuals and pulls are both normalised differences, but they answer different questions. \[PAUSE\] **Residuals** are computed on the observable, for one dataset, real or simulated. They are the data minus the model, divided by the uncertainty, bin by bin. They test the shape of the model: the goodness of fit. \[PAUSE\] **Pulls** are computed on the parameters, and they need many toys. They test the fitter: bias, size of the errors, and coverage. **Residuals: one dataset, many bins, the model. Pulls: many datasets, one parameter, the fitter.**

*IT: residui = su un dataset, sull'osservabile, bontà della forma del modello; pull = sui parametri, servono molti toy, proprietà statistiche del fitter.*

---

## 3:05 — Live coding C1: the toy study with RooMCStudy (5 min)

**\[DO\]** Open the notebook ex C, cell C1. The setup and the model are already there. We fill the two TODO lines on the screen. The study takes about a second for a thousand toys: run it with the full number.

**SAY:** Now the toy study. \[PAUSE\] We do not write the loop by hand: RooFit has a class for it, **RooMCStudy**. It repeats generate and fit, resets the parameters at every toy, and keeps the results. \[PAUSE\] First line: the study. We give it the model, the observable m inside a RooArgSet, and two options. **Extended True: the number of events fluctuates, as in the data. Silence: keeps the output short.** \[PAUSE\] Second line: generate and fit, with the number of toys. \[PAUSE\] **Look at the line above: set truth, thirty-three. The study generates with the current values of the parameters, and it starts the fits from them.** That is why the truth must be set before creating the study. \[PAUSE\] Now run it. About a second. In the next cell, plot pull draws the histogram of the pulls with a Gaussian fit, and the helper computes mean, RMS and coverage.

*IT: riempi dal vivo i 2 TODO di C1 (circa 5 min): RooMCStudy(model, RooArgSet(m), Silence(), Extended(True)) e generateAndFit(NTOYS). Il set_truth viene PRIMA di creare lo studio: genera e parte dai valori correnti. Mille toy in circa un secondo. La cella successiva (già scritta) fa plotPull, media, RMS, copertura e i check.*

**Expected (to verify on your machine):** with 1000 toys and nsig = 33: pull mean close to 0, RMS about 1.05 to 1.1, coverage about 0.68. No fit fails.

---

## 3:10 — Hands-on C: pulls, bias, coverage (slides 27–30, 25 min)

**\[DO\] slide 29 — Exercise C**

**SAY:** Exercise C is short. We use the LHCb model again, with RooMCStudy. \[PAUSE\] Step one: the study with thirty-three signal events, which we wrote together. Look at the pulls: the mean, the RMS and the coverage. The checks tell you if they are right. Step two: repeat with five signal events. What happens to the pulls? How many fits fail, and how many sit at the boundary? \[PAUSE\] A study takes a few seconds. Then read the questions in the notebook, and answer them with the numbers you see.

*IT: studio toy con RooMCStudy; nu\_s=33 (scritto insieme) poi nu\_s=5: media, RMS, copertura, fit falliti, frazione al bordo. Pochi secondi per studio.*

**While walking around:**

- Did you call set truth before creating the study? (The study generates with the current values.)
- Is the study extended? What changes if it is not?
- How many fits failed? (Number of toys minus the rows of the dataset.)
- What is the shape of the pull for five events, and where is its mean?

**At the end (SAY):** Look at the result for thirty-three events. \[PAUSE\] Mean close to zero. RMS close to one. **The errors are reliable.** Now five events. The distribution is distorted: the mean moves to about plus point four, and the RMS goes down to about point eight. A few fits fail, and a small fraction sits at zero. **Here a symmetric error is wrong. We need another tool.** We will build it in Lab 3. *(Numbers from a test with 1000 toys: check them on your machine.)*

---

**\[DO\] slide 30 — Key Takeaways from Hands-on C (2 min, at the end)**

**SAY:** Four points. \[PAUSE\] RooMCStudy runs the generate-and-fit loop and keeps the results. Plot pull, with FitGauss True, draws the pull with a Gaussian fit. The dataset of the fit parameters, fit par data set, has one row for each converged toy, with the value, the error and the pull. **So the failed fits are the number of toys minus the number of rows.** And remember: RooMCStudy generates with the current values of the parameters, so set the truth before creating the study.

*IT: riepilogo C: RooMCStudy; plotPull(FitGauss(True)); fitParDataSet = una riga per toy convergente (nsig, nsigerr, nsigpull) → falliti = toy − righe; set_truth PRIMA di creare lo studio.*

---

## 3:35 — Open lab (slide 31, 20 min)

**SAY:** Now twenty minutes of open lab. \[PAUSE\] Work on the notebook you have not finished. If you have finished, look at the third one: we see the solutions at the next lab. All the notebooks of today are independent, so you can start from any. Run it from the top, and check that every check says PASS. \[PAUSE\] I walk around. Please call me early.

*IT: 30 minuti di lab aperto. Gira tra i banchi. Chiedi: su quale notebook sei? Converge? HESSE e MINOS cosa dicono?*

**Questions to ask each student:**

- Which notebook are you on? Which two will you submit?
- Does the fit converge? What does the status say?
- HESSE or MINOS: which error do you trust here, and why?
- What would break this fit?

---

## 3:55 — Wrap-up (slide 32, 5 min)

**SAY:** Let's finish. \[PAUSE\] Today you learned three things. First, what the fit does: the likelihood, MIGRAD, HESSE, MINOS. Second, the profile likelihood, and why nuisance parameters make intervals wider. Third, toys: pulls, bias and coverage. \[PAUSE\] For the next lab, in two weeks: submit two of the three notebooks, the ones you prefer, on Virtuale. At the beginning of Lab 3, we look together at the solutions of all three. And please read the first two sections of the paper by Cowan, Cranmer, Gross and Vitells. The reference is on the slide. \[PAUSE\] **In Lab 3 we model systematic uncertainties, we use RooStats, and we study a real problem with correlated uncertainties.** Thank you very much. See you in two weeks.

*IT: 3 cose imparate; compiti: consegnare 2 notebook su 3 su Virtuale, leggere Cowan et al. (sez. 1-2). Anteprima Lab 3.*

---

## Emergency notes

- **Talk time-boxes:** A 15 min, B 15 min, C 10 min. Keep a timer on the desk: in Lab 1 the talks were too long for some students.
- **Running late?** Shorten slides 9 and 10 (when fits go wrong) and skip the contour in A5. Do not skip the toys: it is the bridge to Lab 3.
- **Toy study too slow?** Say: Please set NTOYS to two hundred. A thousand toys take about a second here.
- **A student asks about RDataFrame?** Say: Good question. There is a short backup slide in lab1 backup, and we use it again in Lab 4. Come to me at the break.
- **A student asks about Bayesian intervals?** Say: Good question. We see the frequentist and Bayesian tools in Lab 3, with RooStats.
- **Confusion between slice and profile?** Draw two curves on the board: the narrow one is the slice, the wide one is the profile.

---

## Setup reminders (ROOT on the student laptops)

**SAY (first minutes, after the recap):** One practical point. Who still has a problem with ROOT on the laptop? Please raise your hand. \[PAUSE\] If ROOT does not work, please use GitHub Codespaces in your browser. You need a free GitHub account. Please come to me in the first break, and we fix it together.

*IT: chi ha ancora problemi? Codespaces come piano B; risolvi in pausa.*

**Notes for you:**

- Ask who used Codespaces in Lab 1 and whether the quota is enough. Remind them to stop the codespace when they finish.
- The toy study of Exercise C takes a few seconds for 1000 toys. On a very slow laptop suggest NTOYS = 200.
- If a student works in Codespaces, they download the notebooks and upload them on Virtuale.

| Situation | Say | IT |
| --- | --- | --- |
| Problem | Does the check setup say PASS? | check\_setup dice PASS? |
| Fallback | Please use Codespaces in your browser. | Usate Codespaces |
| Slow | Please use fewer toys. | Usate meno toy |
