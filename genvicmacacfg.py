#!/usr/bin/env python

from configobj import ConfigObj

import pandas as pd

import os

class ModCfg:
    def __init__(self, co_cfg):
        self.cfg = co_cfg
#     def gen_id(self):
#         pass
# 
#     def gen_descriptiion(self):
#         pass
    def set_value(self, key, val, section="GLOBAL_ATTRIBUTES"):
        self.cfg[section][key] = val
#         pass    
    def write_cfg(self, cfgname):
        self.cfg.filename = cfgname
        self.cfg.write()
#         icfg = ConfigObj(write_empty_values=True, indent_type=' ')
# # #         outfilename = os.path.join('cfgparts',filename+"_"+sect)
# #             
# #         outfilename = os.path.join(partsdir,'%s_'%(str(count).zfill(2))+sect)
#         icfg.filename = cfgname
#         icfg[sect] = config[sect]
# #         print icfg[sect]
# #         icfg.create_emtpy = True
# 
#         icfg.write()
    
def readtxt_key_recs(ftable,*args,**kwargs):
    '''Return dictionary for active keys'''
    df_gcm = pd.read_csv('gcm_info_name-institute.txt', header=None, delimiter=";;", names=['gcmid','institute'], engine='python')
    return df_gcm

def gen_periods_daily(periods_daily={}):
    dates_hist0=range(1950,2006,10)
    dates_histF=range(1959,2006,10) 
    dates_histF.append(2005)
    dates_rcp0=[2006]
    dates_rcp0.extend(range(2010,2099,10))
    dates_rcpF=range(2009,2100,10) 
    #dates_rcp0=[2006]
    #dates_rcp0.extend(dates_rcp0)
#     print dates_rcp0
    
    perhist=[]
    perrcp=[]
    for t0,tF in zip(dates_hist0,dates_histF):
        dp=tF-t0+1
        perhist.append([str(t0)+'-01-01',str(tF)+'-12-31','P1D','P'+str(dp)+'Y'])
        #print t0,tF
    for t0,tF in zip(dates_rcp0,dates_rcpF):
        dp=tF-t0+1
        perrcp.append([str(t0)+'-01-01',str(tF)+'-12-31','P1D','P'+str(dp)+'Y'])
    periods_daily['historical']=perhist
    periods_daily['rcp45']=perrcp
    periods_daily['rcp85']=perrcp
    return periods_daily

def gen_periods_monthly(periods_daily={}):
    
    perhist=[]
    perrcp=[]
    perhist.append(['1950-01-01','2005-12-31','P1M','P56Y'])
        #print t0,tF
    perrcp.append(['2006-01-01','2099-12-31','P1M','P94Y'])
    periods_daily['historical']=perhist
    periods_daily['rcp45']=perrcp
    periods_daily['rcp85']=perrcp
    return periods_daily
    
## Config file
cfgfile = 'globalatts-vic.cfg' 

ocfgdir = 'testcfgs_daily_vic-livneh'
#ocfgdir = 'testcfgs_summ_vic-livneh'
#ocfgdir = 'testcfgs_summ_vic'
#ocfgdir = 'testcfgs2'

os.mkdir(ocfgdir)

## GCMS
#gcm_active_list = 'GCM_list.txt'
#gcms = 'CSIRO-Mk3-6-0 CanESM2 CNRM-CM5 IPSL-CM5A-MR MIROC5 NorESM1-M CCSM4 bcc-csm1-1-m HadGEM2-ES365 HadGEM2-CC365'.split()
gcms = ['livneh-CANv1.1-USv1.0']
#gcms = ['CCSM4']
gcm_source_list = 'gcm_info_name-institute.txt'

periods_daily=gen_periods_daily()
periods_monthly=gen_periods_monthly()

# Either daily or monthly
#periods=periods_monthly
periods=periods_daily

# periods_daily = {'historical':('1950-01-01','2005-12-31','P1D','P56Y'),
#            'rcp45':('2006-01-01','2099-12-31','P1D','P94Y'),
#            'rcp85':('2006-01-01','2099-12-31','P1D','P94Y')}
# periods_monthly = {'historical':('1950-01-01','2005-12-31','P1D','P56Y'),
#            'rcp45':('2006-01-01','2099-12-31','P1D','P94Y'),
#            'rcp85':('2006-01-01','2099-12-31','P1D','P94Y')}
# periods_monthly = {'historical':[['1950-01-01','2005-12-31','P1D','P56Y']],
#            'rcp45':[['2006-01-01','2099-12-31','P1D','P94Y']],
#            'rcp85':[['2006-01-01','2099-12-31','P1D','P94Y']]}

# vars = 'Qs Qsb'.split()
vars = 'Evaporation Qs Qsb SoilMoist SoilTemp SWE Sensible Latent LatentSub Ground Rnet SurfTemp Shortwave ShortwaveNet Longwave LongwaveNet Precip Qair petSatSoil petH2OSurf petShort petTall petNatVeg Transp Qsm TotalSoilMoist TotalRunoff'.split()
#vars = 'EVAP RUNOFF BASEFLOW SOIL_MOIST1 SOIL_MOIST2 SOIL_MOIST3 SOIL_TEMP1 SOIL_TEMP2 SOIL_TEMP3 SWE SENSIBLE LATENT LATENT_SUB GRND_FLUX R_NET SURF_TEMP SHORTWAVE NET_SHORT IN_LONG NET_LONG PREC QAIR'.split()
time_coverage_resolution = {'daily':'P1D',
                            'monthly':'P1M'}
## P56Y|P94Y
# rawoutput = " of the Variable Infiltration Capacity (VIC) Macroscale Hydrologic Model output."

# vars_optype={'monday1': ['SWE', 'Evaporation', 'petNatVeg', 'petShort', 'petTall', 'TotalRunoff', 'TotalSoilMoist'],
#               'monmax': ['Qsm', 'TotalRunoff'],
#               'monmean': 'SoilTemp Sensible Latent LatentSub Ground Rnet SurfTemp Shortwave ShortwaveNet Longwave LongwaveNet Qair Qsm TotalSoilMoist'.split(),
#               'monsum': ['Qs', 'Qsb', 'Qsm', 'TotalRunoff', 'Precip', 'Evaporation', 'Transp', 'petNatVeg', 'petShort', 'petTall'],
#                }



## VIC ops
map_var2ops = {'Evaporation':['daily', 'monday1', 'monsum'],
               'Qs':['daily', 'monsum'],
               'Qsb':['daily', 'monsum'],
               'SoilMoist':['daily',],
               'SoilTemp':['daily', 'monmean'],
               'SWE':['daily', 'monday1'], 
               'Sensible':['daily', 'monmean'], 
               'Latent':['daily', 'monmean'],
               'LatentSub':['daily', 'monmean'],
               'Ground':['daily', 'monmean'],
               'Rnet':['daily', 'monmean'],
               'SurfTemp':['daily', 'monmean'],
               'Shortwave':['daily', 'monmean'],
               'ShortwaveNet':['daily', 'monmean'],
               'Longwave':['daily', 'monmean'], 
               'LongwaveNet':['daily', 'monmean'],
               'Precip':['daily', 'monsum'],
               'Qair':['daily', 'monmean'],
               'petSatSoil':['daily'],
               'petH2OSurf':['daily'],
               'petShort':['daily', 'monday1', 'monsum'],
               'petTall':['daily', 'monday1', 'monsum'],
               'petNatVeg':['daily', 'monday1', 'monsum'],
               'Transp':['daily', 'monsum'],
               'Qsm':['daily', 'monmax','monmean', 'monsum'],
               'TotalSoilMoist':['daily', 'monday1', 'monmean'],
               'TotalRunoff':['daily', 'monday1', 'monmax', 'monsum']
               }
rawoutput = ""

summary_comment = {'daily': 'Daily output'+rawoutput,
                   'monday1': 'First day of month summary'+rawoutput,
                   'monmax': 'Monthly maximum summary'+rawoutput,
                  'monmean': 'Monthly mean summary'+rawoutput,
                  'monmean.calclim': 'Calendar month mean summary'+rawoutput,
                  'monmin':  'Monthly minimum summary'+rawoutput,
                  'monstd1': 'Monthly standard deviation summary'+rawoutput,
                  'monsum': 'Monthly accumulation summary'+rawoutput,
                  'timmax':  'Full-time extent maximum summary'+rawoutput,
                  'timmean': 'Full-time extent mean summary'+rawoutput,
                  'timmin':  'Full-time extent minimum summary'+rawoutput,
                  'timstd1': 'Full-time extent standard deviation summary'+rawoutput,
                  'timssum': 'Full-time extent accumulation summary'+rawoutput
                   }

model_comment = "VIC 4.1.2.(k,l)"

cfg = ConfigObj(cfgfile)
keywords_stock=cfg['GLOBAL_ATTRIBUTES']['keywords']

cfg_vars = ConfigObj('vars-vic.cfg')

#optypes=['daily']
GCM_source='NOT IMPLEMENTED'

df_gcm = readtxt_key_recs(gcm_source_list)
 
for gcm in gcms:
    if gcm == 'CCSM4':
        ensemble_name='r6i1p1'
        GCM_source=df_gcm[df_gcm.gcmid==gcm]["institute"].values[0]        
    elif gcm == 'livneh-CANv1.1-USv1.0':
        ensemble_name='None'
    else:
        ensemble_name='r1i1p1'         
        GCM_source=df_gcm[df_gcm.gcmid==gcm]["institute"].values[0]
        
    for per in periods.keys():
        for perper in periods[per]:
            if (gcm == 'livneh-CANv1.1-USv1.0' and per != 'historical'):
                pass
            else:
                for var in vars:
                    for optype in map_var2ops[var]:
                        if optype != 'daily': # skip monthly summaries, do daily          
#                         if optype == 'daily': # skip daily
                            pass
                        else:
        #                 for optype in optypes:
                            id = '__'.join([gcm, ensemble_name, per, perper[0]+'-'+perper[1], var, optype])
                            cfgname=os.path.join(ocfgdir,id+'.cfg')
                            newcfg = ModCfg(cfg)
        
                            newcfg.set_value('keywords',keywords_stock+", "+var+", "+cfg_vars[var]['standard_name']+", "+cfg_vars[var]['long_name'],'GLOBAL_ATTRIBUTES')
                            
        #                     dt0=periods[per][0]+"-00"
        #                     dtF=periods[per][1]+"-00"                               
                            dt0=perper[0]+"-00"
                            dtF=perper[1]+"-00"                               
                            newcfg.set_value('start_date', dt0, 'OPTIONS')
                            newcfg.set_value('end_date', dtF, 'OPTIONS')
            #                 title=cfg['GLOBAL_ATTRIBUTES']['title']+" Output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)
            #                 newcfg.set_value('title', cfg['GLOBAL_ATTRIBUTES']['title']+" Output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)) #, section)
                            #desc="VIC-MACA output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)                
                            #newcfg.set_value('description', desc) #, section)
                            #newcfg.set_value('id', id) #, section)
                            newcfg.set_value('time_coverage_start', perper[0]+'T00:0')
                            newcfg.set_value('time_coverage_end', perper[1]+'T00:0')
                            newcfg.set_value('time_coverage_duration', perper[3])
                            newcfg.set_value('time_coverage_resolution', perper[2])                
                            if (gcm == 'livneh-CANv1.1-USv1.0' and per == 'historical'):
                                newcfg.set_value('comment', summary_comment[optype]+" for %s historical period gridded surface observations, %s."%(gcm, model_comment)) #, section)                        
    #                         newcfg.set_value('comment', summary_comment[optype]+" for %s scenario, %s ensemble, %s GCM (from %s), %s."%(per, ensemble_name, gcm, GCM_source, model_comment)) #, section)
    
                            else:
                                newcfg.set_value('comment', summary_comment[optype]+" for %s scenario, %s ensemble, %s GCM (from %s), %s."%(per, ensemble_name, gcm, GCM_source, model_comment)) #, section)                        
                            newcfg.write_cfg(cfgname)

                        
    #                     #varsec = {}
    # #                     varsec=cfg_vars[var]
    # # #                     for var in vars:
    # # # #                         varsec[key]=cfg_vars[var][key]
    # # # #                         print varsec
    # #                     for key in vars:
    # # #                         varsec[key]=cfg_vars[var][key]
    # # #                         print varsec
    # 
    #                     print var
    #                     print cfg_vars[var]
    # #                     print varsec
    #                     keys=cfg_vars[var].keys()
    #                     print keys
    #                     atts={}
    #                     for key in keys:
    #                         print var, key
    #                         atts[key]=cfg_vars[var][key]
    #                     print var, atts
    #                     newcfg.cfg[var] = atts #cfg_vars[var][key] #varsec
    # #                     newcfg.cfg[var] = cfg_vars[var]
    # #                     newcfg.cfg[var] = cfg_vars[var]
                        

#     GCM_source=df_gcm[df_gcm.gcmid==gcm]["institute"].values[0]
#     for per in periods.keys():
#         for var in vars:
#             for optype in optypes:
#                 id = '__'.join([gcm, ensemble_name, per, var, optype])
#                 cfgname='testcfgs2/'+id+'.cfg'
#                 newcfg = ModCfg(cfg)
#                 dt0=periods[per][0]+"-00"
#                 dtF=periods[per][1]+"-00"                               
#                 newcfg.set_value('start_date', dt0, 'OPTIONS')
#                 newcfg.set_value('end_date', dtF, 'OPTIONS')
# #                 title=cfg['GLOBAL_ATTRIBUTES']['title']+" Output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)
# #                 newcfg.set_value('title', cfg['GLOBAL_ATTRIBUTES']['title']+" Output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)) #, section)
#                 #desc="VIC-MACA output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)                
#                 #newcfg.set_value('description', desc) #, section)
#                 newcfg.set_value('id', id) #, section)
#                 newcfg.set_value('time_coverage_start', periods[per][0]+'T00:0')
#                 newcfg.set_value('time_coverage_end', periods[per][1]+'T00:0')
#                 newcfg.set_value('time_coverage_duration', periods[per][3])
#                 newcfg.set_value('time_coverage_resolution', periods[per][2])                
#                 newcfg.set_value('comment', summary_comment[optype]+" of VIC-MACA simulation for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)) #, section)
#                 newcfg.write_cfg(cfgname)


