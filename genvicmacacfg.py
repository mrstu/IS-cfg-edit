#!/usr/bin/env python

from configobj import ConfigObj

import pandas as pd

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
    df_gcm = pd.read_csv('gcm_info_name-institute.txt', header=None, delimiter=";;", names=['gcmid','institute'])
    return df_gcm
    
## Config file
cfgfile = 'nctmpco.cfg'    

## GCMS
#gcm_active_list = 'GCM_list.txt'
gcms = 'CSIRO-Mk3-6-0 CanESM2 CNRM-CM5 IPSL-CM5A-MR MIROC5 NorESM1-M CCSM4 bcc-csm1-1-m HadGEM2-ES365 HadGEM2-CC365'.split()
gcm_source_list = 'gcm_info_name-institute.txt'
periods = {'historical':('1950-01-01','2005-12-31','P1D','P56Y'),
           'rcp45':('2006-01-01','2099-12-31','P1D','P94Y'),
           'rcp85':('2006-01-01','2099-12-31','P1D','P94Y')}
vars = 'EVAP RUNOFF BASEFLOW SOIL_MOIST1 SOIL_MOIST2 SOIL_MOIST3 SOIL_TEMP1 SOIL_TEMP2 SOIL_TEMP3 SWE SENSIBLE LATENT LATENT_SUB GRND_FLUX R_NET SURF_TEMP SHORTWAVE NET_SHORT IN_LONG NET_LONG PREC QAIR'.split()
time_coverage_resolution = {'daily':'P1D',
                            'monthly':'P1M'}
# rawoutput = " of the Variable Infiltration Capacity (VIC) Macroscale Hydrologic Model output."
rawoutput = ""
summary_comment = {'daily': 'Daily output'+rawoutput,
                   'monmax': 'Monthly maximum summary'+rawoutput,
                  'monmean': 'Monthly mean summary'+rawoutput,
                  'monmean.calclim': 'Calendar month mean summary'+rawoutput,
                  'monmin':  'Monthly minimum summary'+rawoutput,
                  'monstd1': 'Monthly standard deviation summary'+rawoutput,
                  'monssum': 'Monthly accumulation summary'+rawoutput,
                  'timmax':  'Full-time extent maximum summary'+rawoutput,
                  'timmean': 'Full-time extent mean summary'+rawoutput,
                  'timmin':  'Full-time extent minimum summary'+rawoutput,
                  'timstd1': 'Full-time extent standard deviation summary'+rawoutput,
                  'timssum': 'Full-time extent accumulation summary'+rawoutput
                   }

cfg = ConfigObj(cfgfile)

optypes=['daily']
GCM_source='NOT IMPLEMENTED'

df_gcm = readtxt_key_recs(gcm_source_list)

for gcm in gcms:
    if gcm == 'CCSM4':
        ensemble_name='r6i1p1'
    else:
        ensemble_name='r1i1p1'
        
    GCM_source=df_gcm[df_gcm.gcmid==gcm]["institute"].values[0]
    for per in periods.keys():
        for var in vars:
            for optype in optypes:
                id = '__'.join([gcm, ensemble_name, per, var, optype])
                cfgname='testcfgs2/'+id+'.cfg'
                newcfg = ModCfg(cfg)
                dt0=periods[per][0]+"-00"
                dtF=periods[per][1]+"-00"                               
                newcfg.set_value('start_date', dt0, 'OPTIONS')
                newcfg.set_value('end_date', dtF, 'OPTIONS')
#                 title=cfg['GLOBAL_ATTRIBUTES']['title']+" Output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)
#                 newcfg.set_value('title', cfg['GLOBAL_ATTRIBUTES']['title']+" Output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)) #, section)
                #desc="VIC-MACA output for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)                
                #newcfg.set_value('description', desc) #, section)
                newcfg.set_value('id', id) #, section)
                newcfg.set_value('time_coverage_start', periods[per][0]+'T00:0')
                newcfg.set_value('time_coverage_end', periods[per][1]+'T00:0')
                newcfg.set_value('time_coverage_duration', periods[per][3])
                newcfg.set_value('time_coverage_resolution', periods[per][2])                
                newcfg.set_value('comment', summary_comment[optype]+" of VIC-MACA simulation for %s scenario, %s ensemble, %s GCM (from %s)"%(per, ensemble_name, gcm, GCM_source)) #, section)
                newcfg.write_cfg(cfgname)


