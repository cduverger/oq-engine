Event Based Risk for Turkey reduced
===================================

============== ===================
checksum32     3,454,425,156      
date           2018-09-25T14:28:22
engine_version 3.3.0-git8ffb37de56
============== ===================

num_sites = 14, num_levels = 91

Parameters
----------
=============================== ==================
calculation_mode                'event_based_risk'
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              10.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            4.0               
complex_fault_mesh_spacing      4.0               
width_of_mfd_bin                0.1               
area_source_discretization      20.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     323               
master_seed                     42                
ses_seed                        323               
avg_losses                      True              
=============================== ==================

Input files
-----------
======================== ==========================================================================
Name                     File                                                                      
======================== ==========================================================================
exposure                 `exposure.xml <exposure.xml>`_                                            
gsim_logic_tree          `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                              
job_ini                  `job.ini <job.ini>`_                                                      
site_model               `site_model.xml <site_model.xml>`_                                        
source                   `as_model.xml <as_model.xml>`_                                            
source                   `fsbg_model.xml <fsbg_model.xml>`_                                        
source                   `ss_model.xml <ss_model.xml>`_                                            
source_model_logic_tree  `source_model_logic_tree.xml <source_model_logic_tree.xml>`_              
structural_vulnerability `structural_vulnerability_model.xml <structural_vulnerability_model.xml>`_
======================== ==========================================================================

Composite source model
----------------------
======================== ======= ===================== ================
smlt_path                weight  gsim_logic_tree       num_realizations
======================== ======= ===================== ================
AreaSource               0.50000 simple(4,0,0,0,0,0,0) 4/4             
FaultSourceAndBackground 0.20000 simple(4,0,0,0,0,0,0) 4/4             
SeiFaCrust               0.30000 simple(4,0,0,0,0,0,0) 0/4             
======================== ======= ===================== ================

Required parameters per tectonic region type
--------------------------------------------
====== ========================================================================== ================= ======================= ============================
grp_id gsims                                                                      distances         siteparams              ruptparams                  
====== ========================================================================== ================= ======================= ============================
0      AkkarBommer2010() CauzziFaccioli2008() ChiouYoungs2008() ZhaoEtAl2006Asc() rhypo rjb rrup rx vs30 vs30measured z1pt0 dip hypo_depth mag rake ztor
1      AkkarBommer2010() CauzziFaccioli2008() ChiouYoungs2008() ZhaoEtAl2006Asc() rhypo rjb rrup rx vs30 vs30measured z1pt0 dip hypo_depth mag rake ztor
2      AkkarBommer2010() CauzziFaccioli2008() ChiouYoungs2008() ZhaoEtAl2006Asc() rhypo rjb rrup rx vs30 vs30measured z1pt0 dip hypo_depth mag rake ztor
====== ========================================================================== ================= ======================= ============================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=8, rlzs=8)
  0,AkkarBommer2010(): [0]
  0,CauzziFaccioli2008(): [1]
  0,ChiouYoungs2008(): [2]
  0,ZhaoEtAl2006Asc(): [3]
  1,AkkarBommer2010(): [4]
  1,CauzziFaccioli2008(): [5]
  1,ChiouYoungs2008(): [6]
  1,ZhaoEtAl2006Asc(): [7]>

Number of ruptures per tectonic region type
-------------------------------------------
===================== ====== ==================== ============ ============
source_model          grp_id trt                  eff_ruptures tot_ruptures
===================== ====== ==================== ============ ============
../src/as_model.xml   0      Active Shallow Crust 8,946        8,946       
../src/fsbg_model.xml 1      Active Shallow Crust 216          324         
===================== ====== ==================== ============ ============

============= =====
#TRT models   2    
#eff_ruptures 9,162
#tot_ruptures 9,297
#tot_weight   0    
============= =====

Estimated data transfer for the avglosses
-----------------------------------------
14 asset(s) x 8 realization(s) x 1 loss type(s) x 1 losses x 8 bytes x 64 tasks = 56 KB

Exposure model
--------------
=============== ========
#assets         14      
#taxonomies     9       
deductibile     absolute
insurance_limit absolute
=============== ========

======== ======= ====== === === ========= ==========
taxonomy mean    stddev min max num_sites num_assets
RC_LR    1.00000 0.0    1   1   3         3         
RC_MR    1.00000 NaN    1   1   1         1         
RC_HR    1.00000 NaN    1   1   1         1         
URM_1S   1.00000 0.0    1   1   2         2         
URM_2S   1.00000 0.0    1   1   2         2         
SAM_1S   1.00000 NaN    1   1   1         1         
SAM_2S   1.00000 0.0    1   1   2         2         
SAM_3S   1.00000 NaN    1   1   1         1         
SAM_4S   1.00000 NaN    1   1   1         1         
*ALL*    1.00000 0.0    1   1   14        14        
======== ======= ====== === === ========= ==========

Slowest sources
---------------
====== ============ ==== ===== ===== ============ ========= ========== ========= ========= =======
grp_id source_id    code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight 
====== ============ ==== ===== ===== ============ ========= ========== ========= ========= =======
0      AS_TRAS334   A    0     23    2,280        2.14837   0.86121    308       38        9.00000
0      AS_TRAS346   A    23    36    1,581        1.43061   0.37222    128       31        1.00000
0      AS_TRAS360   A    36    44    1,872        1.57623   0.30547    132       39        9.00000
0      AS_TRAS395   A    44    52    1,296        1.18467   0.17162    109       27        5.00000
0      AS_TRAS410   A    52    61    720          0.56611   0.03807    84        12        1.00000
0      AS_TRAS458   A    61    67    1,197        1.01009   0.29342    46        21        3.00000
1      FSBG_TRBG989 A    0     7     324          0.14250   0.03577    14        8         2.00000
2      100041       P    0     1     27           0.0       0.0        0.0       0         0.0    
====== ============ ==== ===== ===== ============ ========= ========== ========= ========= =======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    8.05857   7     
P    0.0       1     
==== ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ======= ======= ======= ======= =========
operation-duration mean    stddev  min     max     num_tasks
read_source_models 0.02969 0.03691 0.00291 0.07180 3        
split_filter       0.08247 NaN     0.08247 0.08247 1        
build_ruptures     0.10948 0.02665 0.04771 0.21831 76       
compute_gmfs       0.13178 0.14422 0.02981 0.23376 2        
================== ======= ======= ======= ======= =========

Data transfer
-------------
================== =============================================================================================== ========
task               sent                                                                                            received
read_source_models monitor=1.08 KB converter=957 B fnames=587 B                                                    13.16 KB
split_filter       srcs=46.86 KB monitor=381 B srcfilter=220 B sample_factor=21 B seed=15 B                        92.27 KB
build_ruptures     srcs=194.79 KB param=120.75 KB monitor=28.43 KB srcfilter=16.33 KB                              269.3 KB
compute_gmfs       sources_or_ruptures=74.25 KB param=13.54 KB rlzs_by_gsim=1.28 KB monitor=690 B src_filter=440 B 91.47 KB
================== =============================================================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total build_ruptures     8.32035   0.46875   76    
total compute_gmfs       0.26357   0.25000   2     
building hazard          0.24226   0.25000   2     
updating source_info     0.10244   0.0       1     
total read_source_models 0.08908   0.28516   3     
total split_filter       0.08247   0.0       1     
saving ruptures          0.07380   0.0       28    
making contexts          0.04118   0.0       31    
store source_info        0.03808   0.0       1     
building riskinputs      0.01887   0.0       1     
managing sources         0.00785   0.0       1     
building ruptures        0.00712   0.0       2     
saving gmf_data/indices  0.00623   0.0       1     
GmfGetter.init           0.00604   0.0       2     
building hazard curves   0.00576   0.0       44    
saving gmfs              0.00458   0.0       2     
aggregating hcurves      0.00164   0.0       2     
setting event years      0.00126   0.0       1     
reading exposure         6.611E-04 0.0       1     
======================== ========= ========= ======