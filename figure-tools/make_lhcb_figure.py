"""Final figure of the LHCb example: the fit of the candidate masses (Lab 1, Exercise C), with RooFit.
Run from this folder:  python make_lhcb_figure.py     Output: ../examples/lhcb-b0-ppbar/fit_result.png"""
import ROOT
from ROOT import RooFit as RF
ROOT.gROOT.SetBatch(True); ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.RooMsgService.instance().setGlobalKillBelow(RF.WARNING)
m = ROOT.RooRealVar("m", "m(p#bar{p}) [MeV]", 5080, 5540); mean = ROOT.RooRealVar("mean", "mean", 5288, 5200, 5350)
sigma = ROOT.RooRealVar("sigma", "sigma", 14.8, 5, 50); slope = ROOT.RooRealVar("slope", "slope", -0.002, -0.02, 0)
sig = ROOT.RooGaussian("sig", "sig", m, mean, sigma); bkg = ROOT.RooExponential("bkg", "bkg", m, slope)
nsig = ROOT.RooRealVar("nsig", "#nu_{s}", 33, 0, 400); nbkg = ROOT.RooRealVar("nbkg", "#nu_{b}", 133, 0, 600)
model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(sig, bkg), ROOT.RooArgList(nsig, nbkg))
data = ROOT.RooDataSet.read("../examples/lhcb-b0-ppbar/data/rarest_b0_decay.dat", ROOT.RooArgList(m))
model.fitTo(data, Extended=True, PrintLevel=-1)
c = ROOT.TCanvas("c", "fit", 800, 600)
frame = m.frame(RF.Bins(46), RF.Title(""))
data.plotOn(frame, RF.Name("data"))
model.plotOn(frame, RF.Name("model"))
model.plotOn(frame, RF.Components("bkg"), RF.LineColor(ROOT.kRed), RF.LineStyle(ROOT.kDashed), RF.Name("bkg"))
frame.Draw()
leg = ROOT.TLegend(0.60, 0.68, 0.93, 0.88); leg.SetBorderSize(0); leg.SetFillStyle(0)
leg.AddEntry(frame.findObject("data"), "data", "PE"); leg.AddEntry(frame.findObject("model"), "signal + background", "L"); leg.AddEntry(frame.findObject("bkg"), "background", "L"); leg.Draw()
t = ROOT.TLatex(0.17, 0.83, "#nu_{s} = %.0f #pm %.0f" % (nsig.getVal(), nsig.getError())); t.SetNDC(); t.SetTextSize(0.045); t.Draw()
c.SaveAs("../examples/lhcb-b0-ppbar/fit_result.png")
print("nsig = %.1f +- %.1f" % (nsig.getVal(), nsig.getError()))
