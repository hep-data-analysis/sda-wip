"""Figure of the final analysis of the LHCb case: the fit of the candidate masses (Lab 1, Exercise C), with RooFit. Run: python make_figure.py"""
import ROOT
from ROOT import RooFit as RF
ROOT.gROOT.SetBatch(True); ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.RooMsgService.instance().setGlobalKillBelow(RF.WARNING)
st = ROOT.gStyle; st.SetOptStat(0); st.SetPadLeftMargin(0.14); st.SetPadBottomMargin(0.15); st.SetPadTopMargin(0.10)
for ax in "xyz": st.SetLabelSize(0.045, ax); st.SetTitleSize(0.055, ax)
m = ROOT.RooRealVar("m", "m [MeV]", 5080, 5540); mean = ROOT.RooRealVar("mean", "mean", 5288, 5200, 5350)
sigma = ROOT.RooRealVar("sigma", "sigma", 14.8, 5, 50); slope = ROOT.RooRealVar("slope", "slope", -0.002, -0.02, 0)
sig = ROOT.RooGaussian("sig", "sig", m, mean, sigma); bkg = ROOT.RooExponential("bkg", "bkg", m, slope)
nsig = ROOT.RooRealVar("nsig", "#nu_{s}", 33, 0, 400); nbkg = ROOT.RooRealVar("nbkg", "#nu_{b}", 133, 0, 600)
model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(sig, bkg), ROOT.RooArgList(nsig, nbkg))
data = ROOT.RooDataSet("data", "data", ROOT.RooArgSet(m))
for line in open("data/rarest_b0_decay.dat"):
    v = float(line.split()[0])
    if 5080 < v < 5540: m.setVal(v); data.add(ROOT.RooArgSet(m))
model.fitTo(data, Extended=True, PrintLevel=-1)
c = ROOT.TCanvas("c", "fit", 900, 580)
frame = m.frame(RF.Bins(46), RF.Title(";m(p#bar{p}) [MeV];candidates / 10 MeV"))
data.plotOn(frame, RF.Name("data"))
model.plotOn(frame, RF.LineColor(ROOT.kAzure + 1), RF.LineWidth(4), RF.Name("model"))
model.plotOn(frame, RF.Components("bkg"), RF.LineColor(ROOT.kOrange + 7), RF.LineStyle(ROOT.kDashed), RF.LineWidth(3), RF.Name("bkg"))
frame.Draw()
leg = ROOT.TLegend(0.62, 0.68, 0.93, 0.88); leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetTextSize(0.045)
leg.AddEntry(frame.findObject("data"), "candidates", "PE"); leg.AddEntry(frame.findObject("model"), "signal + background", "L"); leg.AddEntry(frame.findObject("bkg"), "background", "L"); leg.Draw()
t = ROOT.TLatex(0.18, 0.83, "#nu_{s} = %.0f #pm %.0f" % (nsig.getVal(), nsig.getError())); t.SetNDC(); t.SetTextSize(0.05); t.Draw()
c.SaveAs("fit_result.png")
print("nsig = %.1f +- %.1f" % (nsig.getVal(), nsig.getError()))
