# ENUBET: energy deposit in a scintillator pad

**Field:** beam instrumentation · **Used in:** extra case for self-study

**Question.** What is the fraction of events with two particles crossing the pad, and what is the detector resolution?

**Source.** Inspired by Figure 4 of “Status of the ENUBET project”, J. Phys.: Conf. Ser. 1056 (2018) 012047.

**Real measurement.** ENUBET Collaboration, “Status of the ENUBET project”, J. Phys.: Conf. Ser. 1056 (2018) 012047: [doi:10.1088/1742-6596/1056/1/012047](https://doi.org/10.1088/1742-6596/1056/1/012047).

| File | Content |
|---|---|
| `data/enubet_histo.dat` | 95 bins of the energy deposit (first bin centre 0.025, width 0.01; 5334 entries); two columns: bin centre, counts |

## Suggested path (self-study)

- **Lab 1/2:** composite non-extended model. One-particle deposit: Landau (mean in [0, 0.4], sigma in [0.005, 0.05]); two-particle deposit: the Landau convolved with itself; both smeared by a Gaussian resolution (sigma in [0.005, 0.08]). See `course/optional/convolution_resolution.ipynb`.
- **After Lab 3:** the resolution and the Landau parameters as nuisance parameters; effect on the 2-particle fraction.
- **After Lab 4:** binned model with HistFactory.
- *Caveat to watch:* correlation between the resolution and the Landau width.

The original exercise text is `exercise-original.md` (draft extraction). Solutions: see the `solutions` branch, if published.
# ENUBET composite model, non extended (2018) — original exercise text (draft extraction)

> Plain-text extraction from the 2018–2021 tutorial collection. **Equations, figures and tables are missing.** Use the original document for the full statement.

(2018) Exercise 18 -  composite model (non extended)

Inspired by Figure 4 of “Status of the ENUBET project” Journal of Physics: Conf. Series 1056 (2018) 012047
http://inspirehep.net/record/1683606/files/pdf.pdf

The ENUBET project is focused on producing a well-controlled beam of electron neutrinos to allow a solid measurement of CP violation in neutrinos. ENUBET will address its challenge by measuring the positrons that accompany the production of electron neutrinos () in the decay tunnels of traditional beams. In order to tag positrons ENUBET aims to install rings of plastic scintillator pads read by Silicon PhotoMultipliers along the decay tunnel and measure the energy deposit.

The background is given by photon conversion () from π0 gammas. So that, in the first pad, the signal corresponds to energy deposit of 1 m.i.p. (the from decay) and the background to energy deposit of 2 m.i.p.s (from ).

Using RooFit, define a model (non extended) for the energy deposit observed during a test beam where one scintillator pad was exposed to an electron beam. The setup is such that one or two electrons can cross the scintillator at a time.

To build the model, consider that the Landau distribution is well suited for describing the energy loss of charged particles traversing a thin layer of matter. Landau may have a mean in the range [0, 0.4] with starting value of 0.2 and a sigma in the range [0.005, 0.05] with starting value of 0.02.

Hint: the distribution of the energy loss of 2 m.i.p.s is the convolution of the distribution of the energy loss of 1 m.i.p. with itself. Why?

Each energy loss component shall be convolved with a Gaussian to smear detector resulution. Gaussian has a sigma in the range [0.005, 0.08] with starting value of 0.04.

Finally, add to the model a component to take into account the dark current of the SiPM (say an exponential p.d.f. with  coefficient in range [-400, -10] and starting value of -50).

Read a binned dataset from the file enubet_histo.dat, fit the model to the data. Plot data, model and each single component with different color.

Tip:	RooDataHist data{"data", "data", t};

ifstream file("enubet_histo.dat");

double val, weight;

while (!file.eof()) {

file >> val >> weight;

t.setVal(val);

…		data.set(t, weight);

}
