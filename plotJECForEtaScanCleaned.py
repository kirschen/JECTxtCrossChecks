import ROOT
import os, types
from math import *

import numpy as n



def getGraphs(parametertxtFile="Spring16_25nsV9F_DATA_L2L3Residual_AK4PFchs.txt", testEta=-1000, shortLabel=""):
    
    L2L3ResPars = ROOT.JetCorrectorParameters(parametertxtFile,"");
    
    vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
    vPar.push_back(L2L3ResPars);
    
    JetCorrector = ROOT.FactorizedJetCorrector(vPar)
    
    
    def getCorrection(pt,eta,rho,area,corrector=None):
        if corrector == None: raise RuntimeError('Configuration not supported')
        corrector.setJetEta(eta)
        corrector.setJetPt(pt)
        corrector.setJetA(area)
        corrector.setRho(rho)
        corr = corrector.getCorrection()
        return corr
    
    pt= 5
#    xptlog = n.linspace(log(0.00001),log(1000),10000)
#    xptlog = n.linspace(log(30),log(3000),1000)
    xptlog = n.linspace(log(3),log(3000),1000)
    xpt = n.array([exp(xvalue) for xvalue in xptlog ])
    xeta = n.linspace(-5.5,5.5,1000)
    npt = len(xpt)-1
    relxptincrease = xpt[npt]/xpt[npt-1] -1
    ThirdIncrementIdx = int(round(0.3/relxptincrease))
    #print relxptincrease, ThirdIncrementIdx

    graphlist=[]
    xeta = n.linspace(0,1.3,10)
    if testEta == -1000: #all
        xeta = n.linspace(-5.2,5.2,1000)
    elif testEta == -999: #barrel
        xeta = n.linspace(1.3,1.3,100)
    else: xeta = [testEta]

    
    for eta in xeta:
        y = n.array([getCorrection(xvalue,eta,10,0.5,JetCorrector) for xvalue in xpt ])
        maxy = 3
        miny = 0.3
        if abs(eta)<2.5:
            maxy=2
            miny=0.5

        foundSomethingWeird = False
        for i,yv in enumerate(y):
            pt = xpt[i]
            if (yv>maxy or yv<miny) and foundSomethingWeird is False:
                print "WARNING (only once per eta-bin) for {}: eta: {: 6.2f}; pt: {: 6.1f}; corr. out of range: {: 6.2f}".format(parametertxtFile, eta, pt, yv)
                foundSomethingWeird = True
            if i<(npt-ThirdIncrementIdx) and foundSomethingWeird is False:
                if abs(y[i+ThirdIncrementIdx]/yv)-1 > 0.3:
                    print "WARNING (only once per eta-bin) for {}: eta: {: 6.2f}; from {: 6.1f} to {: 6.1f}, corr. changes rapidly from {: 6.2f} to {: 6.2f} by  {: 6.2f}%".format(parametertxtFile, eta, pt, xpt[i+ThirdIncrementIdx], yv, y[i+ThirdIncrementIdx], (abs(y[i+ThirdIncrementIdx]/yv)-1)*100)
                    foundSomethingWeird = True
                    
        
        graph = ROOT.TGraph(len(xpt), xpt,y)
        graph.SetName(shortLabel+"_Eta_"+str(eta))
        graph.SetTitle(shortLabel+"_Eta_"+str(eta))
        graphlist.append(graph)
    return graphlist
    

def plotGraphList(graphList, setColor):
    for i,g in enumerate(graphList):
        g.SetLineColor(setColor)
        g.Draw("L same")
    
        

#etaForTesting = 4.0
etaForTesting = -1000


class PlotDefinition:
    def __init__(self, txtFile, color, legendCaption):
        self.txtFile = txtFile
        self.color = color
        self.legendCaption= legendCaption

plots = [
    PlotDefinition("textFiles/Fall17_17Nov2017_V22_MC/Fall17_17Nov2017_V22_MC_L2Relative_AK4PFchs.txt",1,"AK4PFchs_Fall17V22"),
    PlotDefinition("textFiles/Fall17_17Nov2017_V23_MC/Fall17_17Nov2017_V23_MC_L2Relative_AK4PFchs.txt",2,"AK4PFchs_Fall17V23"),
]

for plot in plots:
    plot.Graphs = getGraphs(plot.txtFile,etaForTesting,plot.legendCaption)

c1 = ROOT.TCanvas("c1", "c1", 600, 600);
c1.SetLogx()
print len(plots[0].Graphs)

for plot in plots:
    leg = ROOT.TLegend(0.15,0.75,0.5,0.9)
    label=""
    plots[0].Graphs[0].Draw("AL")
    plots[0].Graphs[0].GetYaxis().SetRangeUser(0.5,5.0)
    plotGraphList(plot.Graphs,plot.color)
    leg.AddEntry(plot.Graphs[0],plot.legendCaption,"l")
    label +="_"+plot.legendCaption
    leg.Draw()
    c1.Print("plotJECForEtaScan"+label+".png")
    c1.Print("plotJECForEtaScan"+label+".pdf")
    c1.Print("plotJECForEtaScan"+label+".root")



leg = ROOT.TLegend(0.15,0.75,0.5,0.9)
label=""
plots[0].Graphs[0].Draw("AL")
#plots[0].Graphs[0].GetYaxis().SetRangeUser(0.9,1.25)
plots[0].Graphs[0].GetYaxis().SetRangeUser(0.5,5.0)
for plot in plots:
    plotGraphList(plot.Graphs,plot.color)
    leg.AddEntry(plot.Graphs[0],plot.legendCaption,"l")
    label +="_"+plot.legendCaption
 
leg.Draw()
c1.Print("plotJECForEtaScan"+label+".png")
c1.Print("plotJECForEtaScan"+label+".pdf")
c1.Print("plotJECForEtaScan"+label+".root")
