# Lab 2 — Speaker Script

*Companion of lab2.md (24 slides).*

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

## 0:20 — Talk A: What happens in fitTo (slides 5–9, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. Keep a timer on the desk. No slide is removed: if you are late, say the bold line of slide 9 now, and come back to its table at the end of the hands-on.*

**\[DO\] slide 6 — From pdf to number**

**SAY:** When you write fit-to, four things happen. \[PAUSE\] First, RooFit builds the negative log-likelihood. It is a function of the parameters. Second, the minimiser finds the minimum. The minimiser is MINUIT, the minimisation library of ROOT, used in particle physics since the nineteen seventies. The algorithm is called MIGRAD. Third, HESSE computes the covariance matrix from the second derivatives. Fourth, if you ask, MINOS computes asymmetric errors. **Today we call each step ourselves, with a class called RooMinimizer.**

*IT: fitTo = NLL → MIGRAD → HESSE → (MINOS), tre algoritmi di MINUIT, la libreria di minimizzazione di ROOT. Oggi li chiamiamo uno a uno. Perché MINUIT e i rischi di un altro minimizzatore: slide di backup (link in slide 6).*

**\[DO\] slide 7 — MIGRAD, HESSE, MINOS**

**SAY:** Look at the table. These are three algorithms of MINUIT. MIGRAD follows the gradient. It stops when the estimated distance to the minimum, the EDM, is very small. HESSE computes the matrix of second derivatives, and inverts it. The inverse is the covariance matrix. This gives symmetric errors and the correlations. \[PAUSE\] MINOS is different. It scans the likelihood. For each parameter, it looks for the points where the negative log-likelihood rises by zero point five. This gives asymmetric errors. **HESSE assumes the likelihood is a parabola. MINOS does not.** If they disagree, the likelihood is not a parabola, and we trust MINOS.

*IT: HESSE = parabola, simmetrico. MINOS = scansione, asimmetrico. Se discordano, fidati di MINOS.*

**Ask the class:** Why would the two be different? **Answer:** the likelihood is not a parabola: low statistics, a boundary, a non-linear parameter.

**\[DO\] slide 8 — Is my fit healthy?**

**SAY:** Before we use a result, we check the fit. Status must be zero. The covariance quality must be three. This means a full, accurate covariance matrix. The EDM must be tiny. No parameter should sit at its limit. And no correlation should be close to one. \[PAUSE\] **A parameter at its limit is a warning. It is not a result.**

*IT: checklist: status 0, covQual 3, EDM piccolo, nessun parametro al limite, nessuna correlazione ±1.*

**\[DO\] slide 9 — When fits go wrong**

**SAY:** Fits fail. This is normal. Look at the table. If the fit does not converge, the start values are often bad. Choose start values near the data, and bound the ranges. If you see huge errors and a correlation close to one, two parameters are doing the same job. Fix one, or change the parametrisation. If a parameter is at a limit, look at the model. \[PAUSE\] **A limit that is too narrow puts the best value on the boundary, and the errors there are not reliable. A limit that is too wide gives slow fits, or unphysical regions, like a negative sigma, or a negative number of events.** Start near the value you expect: the starting value is not the range. RooFit also warns you when a parameter has no bounds: please read the warnings. \[PAUSE\] And one question: is your limit physical or numerical? A limit like mu greater than zero is physics: in Lab 3 you will see that it can change the result. A limit only to avoid silly values, like sigma greater than zero, is numerics: it must not touch the best value. **Say which one it is.** If you do not want to fit a parameter, fix it with set constant. \[PAUSE\] A small trick: instead of tau, fit the logarithm of tau. Or use fractions between zero and one. **When a fit works on some toys only, we have a low-statistics problem. We study it at the end of the morning.**

*IT: tabella dei sintomi; limiti dei parametri (troppo stretti: best fit sul bordo, errori non affidabili; troppo larghi: convergenza lenta, regioni non fisiche); fisico o numerico; setConstant; RooFit avvisa se non ci sono limiti. Riparametrizzare aiuta.*

---

## 0:35 — Live coding A1: the NLL and MIGRAD (5 min)

**\[DO\]** Open the notebook ex A, cell A1. The model, the data, and the printing lines are already there. We fill the TODO lines on the screen, one at a time. Students may follow, but it is not required.

**SAY:** Now we write step one together. \[PAUSE\] First, the negative log-likelihood: nll equals model dot createNLL, data, and Extended True. We write Extended explicitly, to make clear that the model is extended. \[PAUSE\] Second, the minimiser: minim equals RooMinimizer of nll. \[PAUSE\] Third, three calls: set print level to minus one, to keep the output short; minimize, Minuit2, Migrad, which is MIGRAD; and hesse, which is HESSE. Fourth, we save the result: res equals minim dot save. \[PAUSE\] **Look at the line that is already in the notebook: err hesse equals nsig dot getError. We keep the HESSE error now, because MINOS will change the error object later.** \[PAUSE\] The last lines print three numbers: the status, the covariance quality, and the EDM.

*IT: riempi dal vivo i TODO di A1 (circa 5 min): createNLL con Extended(True) esplicito → RooMinimizer → setPrintLevel(-1), minimize Migrad, hesse → save. La riga err_hesse c'è già: spiega perché (MINOS cambia l'errore). Si stampano status, covQual, EDM.*

**Expected:** status 0, covQual 3, EDM very small. **If it fails:** the model is probably not defined: run the cells above.

---

## 0:40 — Hands-on A: Anatomy of a fit (slides 10–11, 45 min)

**\[DO\] slide 11 — Exercise A**

**SAY:** Now it is your turn. We use the same data and the same model as in Lab 1, exercise C. \[PAUSE\] Step one. Build the negative log-likelihood. Run MIGRAD and HESSE with RooMinimizer. Read the status, the EDM and the covariance quality. Step two. Run MINOS on the signal yield. Are the errors symmetric? Do they agree with HESSE? Step three. Print the correlation matrix. Which two parameters are most correlated? Step four. Plot the likelihood scan, the profile, and the HESSE parabola together. Step five. Draw the one-sigma and two-sigma contours of signal against background. \[PAUSE\] Open ex A in the lab 2 folder. You have forty-five minutes.

*IT: 5 passi. Leggili lentamente. Poi circola.*

**While walking around:**

- Did the first cell run? Did you set your student number?
- What does the check say?
- Compare the red curve and the dashed curve. Where do they separate?
- Why is the correlation negative?

**At the end (SAY):** Let's stop. Who can tell me the HESSE error and the MINOS errors? \[PAUSE\] **Notice: the MINOS interval is not symmetric. The likelihood is steeper at low signal, because the signal cannot be negative.** And the signal and the background are anti-correlated: they compete for the same events under the peak.

---

## 1:25 — BREAK (15 min)

**SAY:** Let's take a break. We restart at 10:30.

---

## 1:40 — Talk B: Intervals and nuisance parameters (slides 12–15, 15 min)

*Time-box: 15 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold sentence of slide 14 now, and come back to the rest at the end of the hands-on.*

**\[DO\] slide 13 — Likelihood-ratio intervals**

**SAY:** Welcome back. Now the main idea of the day: likelihood-ratio intervals. For a single parameter, in the large-sample limit, minus two times the log of the likelihood ratio follows a chi-square distribution with one degree of freedom. This is Wilks theorem. \[PAUSE\] Practically: for a sixty-eight percent interval, we look where the negative log-likelihood rises by zero point five. For ninety-five percent, by one point nine two. **The interval is where the curve is below the minimum plus one half. It does not need to be symmetric.** This is the MINOS interval.

*IT: Wilks; 0.5 per il 68%, 1.92 per il 95%; intervallo = dove la curva sta sotto min + 0.5.*

**\[DO\] slide 14 — Nuisance parameters**

**SAY:** A real model has parameters of interest, and nuisance parameters. A nuisance parameter is something we need in the model, but we do not care about. For example, the background rate, the resolution, or an efficiency. \[PAUSE\] There are two ways to draw the likelihood. The slice: we fix the nuisance parameters at their best-fit value. This is too optimistic, because it ignores what we do not know. The profile: for each value of the parameter of interest, we fit the nuisance parameters again. **The profile is wider than the slice. The difference is the cost of the nuisance parameter.**

*IT: slice (parametri fissi, ottimista) vs profile (rifit dei nuisance). Profile più largo.*

**\[DO\] slide 15 — The on/off problem**

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

## 2:00 — Hands-on B: the on/off problem (slides 16–17, 45 min)

**\[DO\] slide 17 — Exercise B**

**SAY:** Exercise B uses the top-quark numbers. Seventeen events observed in the signal region. Forty in the control region. Tau equal to ten point five three. \[PAUSE\] Step one. Build the model with two Poisson distributions. Fit, and read s hat and b hat. Step two. Compute the sixty-eight percent interval on s in two ways: scan the profile, and use MINOS. Compare them. Step three. Compare with the slice. Step four. Repeat with a poorer control region: n off equal to four, tau equal to one point zero five three. The best-fit background is the same. What changes? \[PAUSE\] Forty-five minutes. Please start with the model.

*IT: B1 modello, B2 profile vs MINOS, B3 slice, B4 controllo povero.*

**While walking around:**

- What is the observable here? And the parameters?
- Is tau constant in your code?
- Check: b hat should be about three point eight.
- Is the profile the same as MINOS? It should be.

**At the end (SAY):** Let's compare. With tau equal to ten, profile and slice are almost the same. \[PAUSE\] With the poor control region, the profile is wider. **This is exactly the cost of not knowing the background.** \[PAUSE\] Question: in the notebooks you are working on, where is the control region, and what does it tell you about the background?

---

## 2:45 — BREAK (10 min)

**SAY:** Let's take a short break. Ten minutes. We restart at 11:45.

---

## 2:55 — Talk C: Validate with toys (slides 18–20, 10 min)

*Time-box: 10 minutes, plus the 5-minute live coding. No slide is removed: if you are late, say the bold sentence of slide 20 now, and come back to it at the end of the hands-on.*

**\[DO\] slide 19 — Why toys?**

**SAY:** One last question. How do we know that the errors are correct? HESSE and MINOS are approximations. We can test them with toys. \[PAUSE\] The recipe has three steps. One: generate a dataset with known true parameters. Two: fit it. Three: save the result. Repeat three hundred times, or more. \[PAUSE\] We define the pull. It is the fitted value, minus the true value, divided by the estimated error. **If everything is fine, the pull has mean zero and RMS one.** The mean tells us about bias. The RMS tells us if the errors have the right size. And about sixty-eight percent of the toys should have a pull between minus one and plus one. This is the coverage.

*IT: toy → fit → pull. Media 0 = nessun bias, RMS 1 = errori giusti, copertura \~68%.*

**\[DO\] slide 20 — Low statistics**

**SAY:** What happens with few events? The likelihood is no longer a parabola. Parameters hit boundaries, for example the signal yield cannot be negative. The pulls are not Gaussian. \[PAUSE\] The remedy: report profile or MINOS intervals. Or use a full toy construction, which we see in Lab 3. And please count the failed fits. **A toy that fails is not a missing result. It is information about your model.**

*IT: bassa statistica: parametri al bordo, pull non gaussiani; riportare intervalli MINOS/profile; contare i fit falliti.*

---

## 3:05 — Live coding C1: the toy study with RooMCStudy (5 min)

**\[DO\]** Open the notebook ex C, cell C1. The setup and the model are already there. We fill the two TODO lines on the screen. The study takes about a second for a thousand toys: run it with the full number.

**SAY:** Now the toy study. \[PAUSE\] We do not write the loop by hand: RooFit has a class for it, **RooMCStudy**. It repeats generate and fit, resets the parameters at every toy, and keeps the results. \[PAUSE\] First line: the study. We give it the model, the observable m inside a RooArgSet, and two options. **Extended True: the number of events fluctuates, as in the data. Silence: keeps the output short.** \[PAUSE\] Second line: generate and fit, with the number of toys. \[PAUSE\] **Look at the line above: set truth, thirty-three. The study generates with the current values of the parameters, and it starts the fits from them.** That is why the truth must be set before creating the study. \[PAUSE\] Now run it. About a second. In the next cell, plot pull draws the histogram of the pulls with a Gaussian fit, and the helper computes mean, RMS and coverage.

*IT: riempi dal vivo i 2 TODO di C1 (circa 5 min): RooMCStudy(model, RooArgSet(m), Silence(), Extended(True)) e generateAndFit(NTOYS). Il set_truth viene PRIMA di creare lo studio: genera e parte dai valori correnti. Mille toy in circa un secondo. La cella successiva (già scritta) fa plotPull, media, RMS, copertura e i check.*

**Expected (to verify on your machine):** with 1000 toys and nsig = 33: pull mean close to 0, RMS about 1.05 to 1.1, coverage about 0.68. No fit fails.

---

## 3:10 — Hands-on C: pulls, bias, coverage (slides 21–22, 25 min)

**\[DO\] slide 22 — Exercise C**

**SAY:** Exercise C is short. We use the LHCb model again, with RooMCStudy. \[PAUSE\] Step one: the study with thirty-three signal events, which we wrote together. Look at the pulls: the mean, the RMS and the coverage. The checks tell you if they are right. Step two: repeat with five signal events. What happens to the pulls? How many fits fail, and how many sit at the boundary? \[PAUSE\] A study takes a few seconds. Then read the questions in the notebook, and answer them with the numbers you see.

*IT: studio toy con RooMCStudy; nu\_s=33 (scritto insieme) poi nu\_s=5: media, RMS, copertura, fit falliti, frazione al bordo. Pochi secondi per studio.*

**While walking around:**

- Did you call set truth before creating the study? (The study generates with the current values.)
- Is the study extended? What changes if it is not?
- How many fits failed? (Number of toys minus the rows of the dataset.)
- What is the shape of the pull for five events, and where is its mean?

**At the end (SAY):** Look at the result for thirty-three events. \[PAUSE\] Mean close to zero. RMS close to one. **The errors are reliable.** Now five events. The distribution is distorted: the mean moves to about plus point four, and the RMS goes down to about point eight. A few fits fail, and a small fraction sits at zero. **Here a symmetric error is wrong. We need another tool.** We will build it in Lab 3. *(Numbers from a test with 1000 toys: check them on your machine.)*

---

## 3:35 — Open lab (slide 23, 20 min)

**SAY:** Now twenty minutes of open lab. \[PAUSE\] Work on the notebook you have not finished. If you have finished, look at the third one: we see the solutions at the next lab. All the notebooks of today are independent, so you can start from any. Run it from the top, and check that every check says PASS. \[PAUSE\] I walk around. Please call me early.

*IT: 30 minuti di lab aperto. Gira tra i banchi. Chiedi: su quale notebook sei? Converge? HESSE e MINOS cosa dicono?*

**Questions to ask each student:**

- Which notebook are you on? Which two will you submit?
- Does the fit converge? What does the status say?
- HESSE or MINOS: which error do you trust here, and why?
- What would break this fit?

---

## 3:55 — Wrap-up (slide 24, 5 min)

**SAY:** Let's finish. \[PAUSE\] Today you learned three things. First, what the fit does: the likelihood, MIGRAD, HESSE, MINOS. Second, the profile likelihood, and why nuisance parameters make intervals wider. Third, toys: pulls, bias and coverage. \[PAUSE\] For the next lab, in two weeks: submit two of the three notebooks, the ones you prefer, on Virtuale. At the beginning of Lab 3, we look together at the solutions of all three. And please read the first two sections of the paper by Cowan, Cranmer, Gross and Vitells. The reference is on the slide. \[PAUSE\] **In Lab 3 we model systematic uncertainties, we use RooStats, and we study a real problem with correlated uncertainties.** Thank you very much. See you in two weeks.

*IT: 3 cose imparate; compiti: consegnare 2 notebook su 3 su Virtuale, leggere Cowan et al. (sez. 1-2). Anteprima Lab 3.*

---

## Emergency notes

- **Talk time-boxes:** A 15 min, B 15 min, C 10 min. Keep a timer on the desk: in Lab 1 the talks were too long for some students.
- **Running late?** Shorten slide 9 (when fits go wrong) and skip the contour in A5. Do not skip the toys: it is the bridge to Lab 3.
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
