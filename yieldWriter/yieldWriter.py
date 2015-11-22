
import ROOT

#### To be modified by the user

#luminosity
lumi = 1280.23

# directory where the files are located
dir_path = "/home/fynu/amertens/scratch/cmssw/CMSSW_7_4_15/src/cp3_llbb/CommonTools/histFactory/all_histos_15_11_21/build/"

# write [name, file, xsec, gen events]
bkgFiles = [
  ['TT'      ,"TT_TuneCUETP8M1_13TeV-powheg-pythia8_MiniAODv2_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root", 831.76, 19757200.0],
  ["DY_10-50","DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root",18610.0, 8.43221e+11],
  ["DY_50","DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX_MiniAODv2_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root", 6025.2, 432201000000]
]

dataFiles = [
  ['data','DoubleEG_Run2015D-05Oct2015-v1_2015-10-20_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root'],
  ['data','DoubleEG_Run2015D-PromptReco-v4_2015-10-20_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root'],
  ['data','DoubleMuon_Run2015D-05Oct2015-v1_2015-10-20_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root'],
  ['data','DoubleMuon_Run2015D-PromptReco-v4_2015-10-20_v1.0.0+7415-10-gcf61438_ZAAnalysis_dd80b32_histos.root']
]

# Write [ categoryName,variable] 
# variable should be the histograms name that will provide the correct yiels when integrated
variable = [
  ['$2\mu$','za_diLep_Phi_mm'],
  ['$2e$','za_diLep_Phi_ee'],
  ['$2l2j$','za_diLep_Phi_lljj'],
  ['$2l2b$','za_diLep_Phi_llbb']
]




#### Configuration ends here

print "Category & ",

for file_idx in range(len(bkgFiles)) :
  print bkgFiles[file_idx][0]+ " & ",

print "tot. bkg. & data \\\\"

for var_idx in range(len(variable)):
  print variable[var_idx][0], ' & ',
  total_bkg = 0
  for file_idx in range(len(bkgFiles)) :
    file_path=dir_path+bkgFiles[file_idx][1]
    #print file_path
    f = ROOT.TFile.Open(file_path)
    h = f.Get(variable[var_idx][1])

    val = int(h.Integral()) * lumi * bkgFiles[file_idx][2] / bkgFiles[file_idx][3]
    total_bkg = total_bkg + val
    print "%.2f" % val,
    print ' & ',
  print "%.2f" % total_bkg, ' & ',

  dataCount=0
  for dataFile_idx in range(len(dataFiles)) :
    file_path=dir_path+dataFiles[dataFile_idx][1]
    f = ROOT.TFile.Open(file_path)
    h = f.Get(variable[var_idx][1])

    val = int(h.Integral())
    dataCount=dataCount+val
  print str(dataCount)+' \\\\'

