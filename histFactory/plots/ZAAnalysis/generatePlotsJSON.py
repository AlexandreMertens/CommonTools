from ZACnC import *

def printInJson(f, g, obj, objName, variables, variableNames, cut, cutName, binnings, isLastEntry):
    for i in range(0, len(variables)) :
        f.write( "        {\n")
        f.write( "        'name': '"+objName+"_"+variableNames[i]+"_"+cutName+"',\n")
        f.write( "        'variable': '"+obj+"."+variables[i]+"',\n")
        f.write( "        'plot_cut': '"+cut+"',\n")
        f.write( "        'binning': '"+binnings[i]+"'\n")
        if (isLastEntry == False or i < len(variables)-1) : 
            f.write( "        },\n")
        else : 
            f.write( "        }\n")
    if (isLastEntry == True) :
        f.write( "        ]\n")

    for i in range(0, len(variables)) :
        g.write("'"+objName+"_"+variableNames[i]+"_"+cutName+"':\n")
        g.write("  x-axis: '"+objName+"_"+variableNames[i]+"_"+cutName+"'\n")
        g.write("  y-axis: 'Evt'\n")
        g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
        g.write("  normalized: false\n")
        g.write("  log-y: both\n")
        g.write("  save-extensions: ['png','pdf']\n")
        g.write("  show-ratio: true\n")

def printInPy(f, g, cut, cutName, binning, isLastEntry):
    f.write( "        {\n")
    f.write( "        'name': '"+cutName+"',\n")
    f.write( "        'variable': '"+cut+"',\n")
    f.write( "        'plot_cut': '"+cut+"',\n")
    f.write( "        'binning': '"+binning+"'\n")
    if (isLastEntry == False or i < len(variables)-1) :
        f.write( "        },\n")
    else :
        f.write( "        }\n")
    if (isLastEntry == True) :
        f.write( "        ]\n")

    g.write("'"+cutName+"':\n")
    g.write("  x-axis: '"+cutName+"'\n")
    g.write("  y-axis: 'Evt'\n")
    g.write("  y-axis-format: '%1% / %2$.0f GeV'\n")
    g.write("  normalized: false\n")
    g.write("  log-y: both\n")
    g.write("  save-extensions: ['png','pdf']\n")
    g.write("  show-ratio: true\n")


# binnings

pt_binning  = "(30, 0, 600)"
eta_binning = "(30, -3, 3)"
phi_binning = "(30, -3.1416, 3.1416"
lepiso_binning = "(30, 0, 0.3)"
mj_binning = "(30, 0, 30)"
csv_binning = "(20,0,1)"
DR_binning = "(15, 0, 6)"
DPhi_binning = "(10, 0, 3.1416)"
ptZ_binning = "80,0,800)"
MZ_binning = "(80,0,400)"
Mjj_binning = "(30,0,600)"
Mlljj_binning = "(40,0,2400)"
met_binning = "(40,0,400)"
Nj_binning = "(8,0,8)"
nPV_binning = "(50,0,50)"


# Leptons variables

l1 = "za_dilep_ptOrdered[0]"
l2 = "za_dilep_ptOrdered[1]"

l1Name = "za_lep_ptOrdered0"
l2Name = "za_lep_ptOrdered1"

l_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "isoValue"]
l_varName = ["Pt", "Eta", "Phi", "isoValue"]

l_binning = [pt_binning, eta_binning, phi_binning, lepiso_binning]

# Jets variables

j1pt = "za_dijet_ptOrdered[0]"
j2pt = "za_dijet_ptOrdered[1]"
j1csv = "za_dijet_CSVv2Ordered[0]"
j2csv = "za_dijet_CSVv2Ordered[1]"

j1ptName = "za_jet_ptOrdered0"
j2ptName = "za_jet_ptOrdered1"
j1csvName = "za_jet_CSVv2Ordered0"
j2csvName = "za_jet_CSVv2Ordered1"

j_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()", "CSVv2", "minDRjl" ]
j_varName = ["Pt", "Eta", "Phi", "M", "CSVv2", "minDRjl"]
j_binning = [pt_binning, eta_binning, phi_binning, mj_binning, csv_binning, DR_binning]


# MET variables

met = "nohf_met_p4"
metName = "nohf_met"

met_var = ["Pt()"]
met_varName = ["Pt"]
met_binning = [met_binning]
# Dilep variables

dilep = "za_diLeptons[0]"
dilepName = "za_diLep"
dilep_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()", "DR", "DEta", "DPhi"]
dilep_varName = ["Pt", "Eta", "Phi", "M", "DR", "DEta", "DPhi"]
dilep_binning = [ptZ_binning, eta_binning, phi_binning, MZ_binning, DR_binning, DR_binning, DPhi_binning]

# Dijet variables

dijet = "za_diJets[0]"
dijetName = "za_diJet"
dijet_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()", "DR", "DEta", "DPhi"]
dijet_varName = ["Pt", "Eta", "Phi", "M", "DR", "DEta", "DPhi"]
dijet_binning = [ptZ_binning, eta_binning, phi_binning, Mjj_binning, DR_binning, DR_binning, DPhi_binning]

# Dilep-Dijet variables

dijetdilep = "za_diLepDiJets[0]"
dijetdilepName = "za_diLepDiJet"
dijetdilep_var = ["p4.Pt()", "p4.Eta()", "p4.Phi()", "p4.M()"]
dijetdilep_varName = ["Pt", "Eta", "Phi", "M"]
dijetdilep_binning = [pt_binning, eta_binning, phi_binning, Mlljj_binning]

# (B-)Jets Counting

selJets = "za_selJets"
selJetsName = "selectedJets"
selJets_var = ["size()"]
selJets_varName = ["N"]
selJets_binning = [Nj_binning]

selBjets = "za_selBjetsM"
selBjetsName = "selectedBjetsM"

# PV N

nPV = "event_true_interactions"
nPVName = "event_true_interactions"
nPV_binning = [nPV_binning]

# Cuts

weights = "* event_pu_weight * event_weight"

twoMu = "(mumu_DileptonIsIDMM_cut && mumu_Mll_cut)"+weights
twoMuName = "mm"

twoEl="(elel_DileptonIsIDMM_cut && elel_Mll_cut)"+weights
twoElName="ee"

twoL_cond = "((mumu_DileptonIsIDMM_cut && mumu_Mll_cut) || (elel_DileptonIsIDMM_cut * elel_Mll_cut))"
twoL=twoL_cond+weights
twoLName="ll"

twoJ_cond="( Length$(za_diJets) > 0 )"  #"(elel_TwoJets_cut || mumu_TwoJets_cut)"
twoLtwoJ = "("+twoL_cond + " && " + twoJ_cond+")"+ weights
twoLtwoJName = "lljj"

twoB_cond= "( Length$(za_diJets) > 0 && za_diJets[0].isMM )" #"(elel_TwoBjets_cut || mumu_TwoBjets_cut)"
twoLtwoB = twoL_cond + " * " + twoB_cond+weights
twoLtwoBName = "llbb"

'''
twoMuTwojets = "(mumu_DileptonIsIDMM_cut && mumu_Mll_cut) * event_weight"
twoMuTwojetsName = "mmjj"

twoMuTwojetsMM = "(mumu_DileptonIsIDMM_cut * mumu_Mll_cut * mumu_DiJetBWP_MM_cut) * event_weight"

twoElTwojets = "(elel_DileptonIsIDMM_cut * elel_Mll_cut) * event_weight"
twoElTwojetsName = "eejj"

twoElTwojetsMM = "(elel_DileptonIsIDMM_cut * elel_Mll_cut * elel_DiJetBWP_MM_cut) * event_weight"

twoLepTwoBjets = "((elel_DileptonIsIDMM_cut && elel_Mll_cut && elel_DiJetBWP_MM_cut) || (mumu_DileptonIsIDMM_cut && mumu_Mll_cut && mumu_DiJetBWP_MM_cut)) * event_weight"
twoLepTwoBjetsName  = "llbb"

test_highMass = "((elel_DileptonIsIDMM_cut * elel_Mll_cut * elel_DiJetBWP_MM_cut) || (mumu_DileptonIsIDMM_cut * mumu_Mll_cut * mumu_DiJetBWP_MM_cut)) * ( Length$(za_diLeptons) > 0 && za_diLeptons[0].p4.Pt() > 200 && za_diJets[0].p4.Pt() > 200) * event_weight"
test_highMassName = "llbb_HM"
'''
#print l_var[0]


# Writing the JSON

## 2 Muons 2 Jets :

fjson = open('plots_all.py', 'w')
fjson.write( "plots = [\n")
fyml = open('plots_all.yml', 'w')


## CandCount variables :

options = options_()
'''
for cutkey in options.cut :
        print 'cutkey : ', cutkey
        ### get M_A and M_H ###
        #mH[0] = float(options.mH_list[cutkey])
        #mA[0] = float(options.mA_list[cutkey])
        printInPy(fjson, fyml, options.cut[cutkey], twoLepTwoBjets+" && "+cutkey,"(2, 0, 2)", 0)
'''
## Control Plots :

# 1) 2L stage
printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoMu, twoMuName, l_binning, 0)
printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoMu, twoMuName, l_binning, 0)
printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoEl, twoElName, l_binning, 0)
printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoEl, twoElName, l_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoMu, twoMuName, dilep_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoEl, twoElName, dilep_binning, 0)
printInJson(fjson, fyml, selJets, selJetsName, selJets_var, selJets_varName, twoL, twoLName, selJets_binning, 0)
printInJson(fjson, fyml, selBjets, selBjetsName, selJets_var, selJets_varName, twoL, twoLName, selJets_binning, 0)
printInJson(fjson, fyml, nPV, nPVName, "", "", twoL, twoLName, nPV_binning, 0)

# 2) 2L2J stage
printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoLtwoJ, twoLtwoJName, l_binning, 0)
printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoLtwoJ, twoLtwoJName, l_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLtwoJ, twoLtwoJName, dilep_binning, 0)
printInJson(fjson, fyml, selJets, selJetsName, selJets_var, selJets_varName, twoLtwoJ, twoLtwoJName, selJets_binning, 0)
printInJson(fjson, fyml, selBjets, selBjetsName, selJets_var, selJets_varName, twoLtwoJ, twoLtwoJName, selJets_binning, 0)
printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoLtwoJ, twoLtwoJName, j_binning, 0)
printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoLtwoJ, twoLtwoJName, j_binning, 0)
#printInJson(fjson, fyml, j1csv, j1csvName, j_var, j_varName, twoLtwoJ, twoLtwoJName, j_binning, 0)
#printInJson(fjson, fyml, j2csv, j2csvName, j_var, j_varName, twoLtwoJ, twoLtwoJName, j_binning, 0)


# 3) 2L2B stage

printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLtwoB, twoLtwoBName, dilep_binning, 0)
printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoLtwoB, twoLtwoBName, j_binning, 0)
printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoLtwoB, twoLtwoBName, j_binning, 0)
printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoLtwoB, twoLtwoBName, dijet_binning, 1)


'''
printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoMuTwojets, twoMuTwojetsName, j_binning, 0)
printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoMuTwojets, twoMuTwojetsName, j_binning, 0)
printInJson(fjson, fyml, j1csv, j1csvName, j_var, j_varName, twoMuTwojets, twoMuTwojetsName, j_binning, 0)
printInJson(fjson, fyml, j2csv, j2csvName, j_var, j_varName, twoMuTwojets, twoMuTwojetsName, j_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoMuTwojets, twoMuTwojetsName, dilep_binning, 0)
printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoMuTwojets, twoMuTwojetsName, dijet_binning, 0)
printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, twoMuTwojets, twoMuTwojetsName, dijetdilep_binning, 0)

## 2 Electrons 2 Jets :

printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoElTwojets, twoElTwojetsName, l_binning, 0)
printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoElTwojets, twoElTwojetsName, l_binning, 0)
printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoElTwojets, twoElTwojetsName, j_binning, 0)
printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoElTwojets, twoElTwojetsName, j_binning, 0)
printInJson(fjson, fyml, j1csv, j1csvName, j_var, j_varName, twoElTwojets, twoElTwojetsName, j_binning, 0)
printInJson(fjson, fyml, j2csv, j2csvName, j_var, j_varName, twoElTwojets, twoElTwojetsName, j_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoElTwojets, twoElTwojetsName, dilep_binning, 0)
printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoElTwojets, twoElTwojetsName, dijet_binning, 0)
printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, twoElTwojets, twoElTwojetsName, dijetdilep_binning, 0)

## 2 leptons, 2 BJets :

printInJson(fjson, fyml, l1, l1Name, l_var, l_varName, twoLepTwoBjets, twoLepTwoBjetsName, l_binning, 0)
printInJson(fjson, fyml, l2, l2Name, l_var, l_varName, twoLepTwoBjets, twoLepTwoBjetsName, l_binning, 0)
printInJson(fjson, fyml, j1pt, j1ptName, j_var, j_varName, twoLepTwoBjets, twoLepTwoBjetsName, j_binning, 0)
printInJson(fjson, fyml, j2pt, j2ptName, j_var, j_varName, twoLepTwoBjets, twoLepTwoBjetsName, j_binning, 0)
printInJson(fjson, fyml, j1csv, j1csvName, j_var, j_varName, twoLepTwoBjets, twoLepTwoBjetsName, j_binning, 0)
printInJson(fjson, fyml, j2csv, j2csvName, j_var, j_varName, twoLepTwoBjets, twoLepTwoBjetsName, j_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, twoLepTwoBjets, twoLepTwoBjetsName, dilep_binning, 0)
printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, twoLepTwoBjets, twoLepTwoBjetsName, dijet_binning, 0)
printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, twoLepTwoBjets, twoLepTwoBjetsName, dijetdilep_binning, 0)
printInJson(fjson, fyml, met, metName, met_var, met_varName, twoLepTwoBjets, twoLepTwoBjetsName, met_binning, 0)

## test high mass
printInJson(fjson, fyml, dijetdilep, dijetdilepName, dijetdilep_var, dijetdilep_varName, test_highMass, test_highMassName, dijetdilep_binning, 0)
printInJson(fjson, fyml, dilep, dilepName, dilep_var, dilep_varName, test_highMass, test_highMassName, dilep_binning, 0)
printInJson(fjson, fyml, dijet, dijetName, dijet_var, dijet_varName, test_highMass, test_highMassName, dijet_binning, 0)
printInJson(fjson, fyml, met, metName, met_var, met_varName, test_highMass, test_highMassName, met_binning, 1)

'''
