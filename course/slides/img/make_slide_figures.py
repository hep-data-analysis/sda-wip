"""Figures of the slides, drawn with RooFit (RooPlot) and ROOT in their default style.
Run from this folder:  python make_slide_figures.py     Output: *.png in this folder"""
import ROOT
from ROOT import RooFit as RF
ROOT.gROOT.SetBatch(True); ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.RooMsgService.instance().getStream(0).minLevel = RF.WARNING
ROOT.RooMsgService.instance().setGlobalKillBelow(RF.WARNING)
OUT = ""
DATA = "../../../gallery/data/lhcb-b0_rarest_decay.dat"

# ---------- the model of Lab 1 (Exercise C) and of Lab 2 (Exercise C)
m     = ROOT.RooRealVar("m", "m [MeV]", 5080, 5540)
mean  = ROOT.RooRealVar("mean", "mean", 5288, 5200, 5350)
sigma = ROOT.RooRealVar("sigma", "sigma", 14.8, 5, 50)
slope = ROOT.RooRealVar("slope", "slope", -0.002, -0.02, 0)
sig   = ROOT.RooGaussian("sig", "sig", m, mean, sigma)
bkg   = ROOT.RooExponential("bkg", "bkg", m, slope)
nsig  = ROOT.RooRealVar("nsig", "#nu_{s}", 33, 0, 400)
nbkg  = ROOT.RooRealVar("nbkg", "#nu_{b}", 133, 0, 600)
model = ROOT.RooAddPdf("model", "sig+bkg", ROOT.RooArgList(sig, bkg), ROOT.RooArgList(nsig, nbkg))

# ---------- Figure 1: likelihood interval, the HESSE parabola against the profile (real data)
data = ROOT.RooDataSet.read(DATA, ROOT.RooArgList(m))
model.fitTo(data, Extended=True, PrintLevel=-1, Hesse=True)
best, err = nsig.getVal(), nsig.getError()
nll = model.createNLL(data, RF.Extended(True))
prof = nll.createProfile(ROOT.RooArgSet(nsig))
model.fitTo(data, Extended=True, PrintLevel=-1, Minos=ROOT.RooArgSet(nsig))
lo, hi = nsig.getErrorLo(), nsig.getErrorHi()
nsig.setVal(best)

c1 = ROOT.TCanvas("c1", "likelihood", 800, 600)
frame = nsig.frame(RF.Range(max(0.5, best - 3.2*err), best + 3.2*err), RF.Title(";#nu_{s};-ln L - (-ln L)_{min}"))
prof.plotOn(frame, RF.ShiftToZero(), RF.Name("profile"))
parab = ROOT.RooFormulaVar("parab", "0.5*pow((@0-%f)/%f,2)" % (best, err), ROOT.RooArgList(nsig))
parab.plotOn(frame, RF.LineColor(ROOT.kRed), RF.LineStyle(ROOT.kDashed), RF.Name("parabola"))
frame.SetMinimum(-0.25); frame.SetMaximum(3.2); frame.Draw()
x1, x2 = frame.GetXaxis().GetXmin(), frame.GetXaxis().GetXmax()
half = ROOT.TLine(x1, 0.5, x2, 0.5); half.SetLineColor(ROOT.kGray + 1); half.Draw()
t_half = ROOT.TLatex(x2 - 0.02*(x2 - x1), 0.58, "#Delta(-ln L) = 0.5"); t_half.SetTextAlign(31); t_half.SetTextSize(0.04); t_half.SetTextColor(ROOT.kGray + 2); t_half.Draw()
b_minos = ROOT.TLine(best + lo, 0.20, best + hi, 0.20); b_minos.SetLineColor(ROOT.kBlue); b_minos.SetLineWidth(8); b_minos.Draw()
b_hesse = ROOT.TLine(best - err, 0.0, best + err, 0.0); b_hesse.SetLineColor(ROOT.kRed); b_hesse.SetLineWidth(8); b_hesse.Draw()
l_minos = ROOT.TLatex(best + hi + 0.025*(x2 - x1), 0.20, "MINOS: %.1f / +%.1f" % (lo, hi)); l_minos.SetTextSize(0.04); l_minos.SetTextColor(ROOT.kBlue); l_minos.SetTextAlign(12); l_minos.Draw()
l_hesse = ROOT.TLatex(best + err + 0.025*(x2 - x1), -0.02, "HESSE: #pm%.1f" % err); l_hesse.SetTextSize(0.04); l_hesse.SetTextColor(ROOT.kRed); l_hesse.SetTextAlign(12); l_hesse.Draw()
leg = ROOT.TLegend(0.40, 0.70, 0.93, 0.87); leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetTextSize(0.04)
leg.AddEntry(frame.findObject("profile"), "profile of -ln L (the real likelihood)", "L")
leg.AddEntry(frame.findObject("parabola"), "parabola: what HESSE assumes", "L"); leg.Draw()
c1.SaveAs(OUT + "likelihood_interval.png")
print("figure 1: nsig = %.1f  HESSE +-%.1f  MINOS %.1f / +%.1f" % (best, err, lo, hi))

# ---------- Figure 2: how a pull distribution looks (schematic), generated and drawn with RooFit
ROOT.RooRandom.randomGenerator().SetSeed(3)
pull = ROOT.RooRealVar("pull", "pull", -4, 4)
zero = ROOT.RooRealVar("zero", "zero", 0); one = ROOT.RooRealVar("one", "one", 1)
standard = ROOT.RooGaussian("standard", "standard", pull, zero, one)          # what a healthy fit gives
cases = [("healthy", 0.0, 1.0), ("mean #neq 0: bias", 0.6, 1.0), ("RMS > 1: underestimated", 0.0, 1.6), ("RMS < 1: overestimated", 0.0, 0.6)]
c2 = ROOT.TCanvas("c2", "pulls", 1600, 440); c2.Divide(4, 1)
keep = []
for k, (title, mu, rms) in enumerate(cases, 1):
    c2.cd(k)
    mu_v = ROOT.RooRealVar("mu%d" % k, "mu", mu); rms_v = ROOT.RooRealVar("rms%d" % k, "rms", rms)
    true = ROOT.RooGaussian("true%d" % k, "true", pull, mu_v, rms_v)
    d = true.generate(ROOT.RooArgSet(pull), 6000)
    fr = pull.frame(RF.Bins(40), RF.Title(title))
    d.plotOn(fr); standard.plotOn(fr)
    fr.GetYaxis().SetTitle(""); fr.GetYaxis().SetLabelSize(0); fr.Draw()
    keep += [mu_v, rms_v, true, d, fr]
c2.SaveAs(OUT + "pull_diagnosis.png")

# ---------- Figure 3: the pulls of Exercise C, real toys with RooMCStudy and plotPull
TRUTH = {mean: 5288, sigma: 14.8, slope: -0.002, nbkg: 133}
def study(ns, seed, n=1000):
    ROOT.RooRandom.randomGenerator().SetSeed(seed)
    for v, t in TRUTH.items(): v.setVal(t)
    nsig.setVal(ns)
    mcs = ROOT.RooMCStudy(model, ROOT.RooArgSet(m), RF.Silence(), RF.Extended(True))
    mcs.generateAndFit(n)
    return mcs
c3 = ROOT.TCanvas("c3", "pulls of Exercise C", 1500, 560); c3.Divide(2, 1)
mc = []
for k, ns in enumerate((33, 5), 1):
    c3.cd(k)
    mcs = study(ns, 123); mc.append(mcs)
    fr = mcs.plotPull(nsig, RF.FitGauss(True), RF.Bins(40), RF.FrameRange(-4, 4))
    fr.SetTitle("#nu_{s} = %d" % ns)
    fr.SetMaximum(1.45*fr.GetMaximum())       # room for the box of the Gaussian fit
    fr.Draw()
c3.SaveAs(OUT + "pull_33_vs_5.png")

# ---------- Figure 4 (Lab 3): Poisson likelihood against its Gaussian approximation
c4 = ROOT.TCanvas("c4", "Poisson or Gauss", 1400, 520); c4.Divide(2, 1)
fs = []
for k, n in enumerate((5, 40), 1):
    c4.cd(k)
    xmin, xmax = (-3.0, 14.0) if n == 5 else (0.5, 90.0)
    fp = ROOT.TF1("fp%d" % k, "exp([0]*log(x) - x - ([0]*log([0]) - [0]))", 0.05, xmax); fp.SetParameter(0, n)
    fg = ROOT.TF1("fg%d" % k, "exp(-pow([0]-x,2)/(2*[0]))", xmin, xmax); fg.SetParameter(0, n)
    fg.SetTitle("n_{off} = %d;b;likelihood (peak = 1)" % n); fg.SetLineColor(ROOT.kRed); fg.SetLineStyle(2)
    fp.SetLineColor(ROOT.kBlue)
    fg.SetMinimum(0); fg.SetMaximum(1.15); fg.Draw(); fp.Draw("same")
    if k == 1:
        lg = ROOT.TLegend(0.50, 0.70, 0.93, 0.86); lg.SetBorderSize(0); lg.SetFillStyle(0)
        lg.AddEntry(fp, "Poisson (exact)", "L"); lg.AddEntry(fg, "Gaussian constraint", "L"); lg.Draw(); fs.append(lg)
    fs += [fp, fg]
c4.SaveAs(OUT + "poisson_vs_gauss.png")

# ---------- Figure 5 (Lab 3 backup): the constraint shapes for b_hat = 3.8, as functions of beta
# Each curve is scaled to 1 at its maximum. Moment matching: Gamma k = (b0/sigma_b)^2 = n_off, rate = b0/sigma_b^2 = tau;
# log-normal with ln(kappa) = sigma_b/b0.
c5 = ROOT.TCanvas("c5", "constraints", 1400, 520); c5.Divide(2, 1)
keep5 = []
for k, (n, tau) in enumerate(((40, 10.53), (4, 1.053)), 1):
    c5.cd(k)
    b0, sb = n / tau, n**0.5 / tau
    xmin, xmax = (2.0, 6.0) if n == 40 else (-2.5, 12.0)
    # Gaussian: defined also for beta < 0
    fg = ROOT.TF1("c5g%d" % k, "exp(-0.5*pow((x-%g)/%g,2))" % (b0, sb), xmin, xmax)
    fg.SetTitle("n_{off} = %d  (#sigma_{b} = %.1f);#beta;likelihood (peak = 1)" % (n, sb))
    fg.SetLineColor(ROOT.kRed); fg.SetLineStyle(2)
    fg.SetMinimum(0); fg.SetMaximum(1.15)
    # Poisson, as a function of beta: beta^n exp(-tau beta)
    fp = ROOT.TF1("c5p%d" % k, "exp(%g*log(%g*x/%g) - %g*x + %g)" % (n, tau, n, tau, n), 0.02, xmax)
    fp.SetLineColor(ROOT.kBlue)
    # Gamma, moment matched: beta^(k-1) exp(-rate beta), k = n_off
    fm = ROOT.TF1("c5m%d" % k, "exp(%g*log(%g*x/%g) - %g*x + %g)" % (n - 1, tau, n - 1, tau, n - 1), 0.02, xmax)
    fm.SetLineColor(ROOT.kGreen + 2); fm.SetLineStyle(3); fm.SetLineWidth(3)
    # log-normal: exp(-ln^2(beta/b0) / (2 s^2)), s = sigma_b/b0
    fl = ROOT.TF1("c5l%d" % k, "exp(-0.5*pow(log(x/%g)/%g,2))" % (b0, sb / b0), 0.02, xmax)
    fl.SetLineColor(ROOT.kMagenta + 1); fl.SetLineStyle(4)
    fg.Draw()
    for f in (fp, fm, fl):
        f.Draw("same")
    if k == 1:
        lg = ROOT.TLegend(0.60, 0.62, 0.93, 0.86); lg.SetBorderSize(0); lg.SetFillStyle(0)
        lg.AddEntry(fp, "Poisson (exact)", "L"); lg.AddEntry(fm, "Gamma", "L")
        lg.AddEntry(fg, "Gaussian", "L"); lg.AddEntry(fl, "log-normal", "L"); lg.Draw(); keep5.append(lg)
    keep5 += [fg, fp, fm, fl]
c5.SaveAs(OUT + "constraints_comparison.png")


print("figures done")
