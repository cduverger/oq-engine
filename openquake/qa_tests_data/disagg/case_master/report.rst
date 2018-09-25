disaggregation with a complex logic tree
========================================

============== ===================
checksum32     1,766,748,636      
date           2018-09-25T14:27:47
engine_version 3.3.0-git8ffb37de56
============== ===================

num_sites = 2, num_levels = 102

Parameters
----------
=============================== =================
calculation_mode                'disaggregation' 
number_of_logic_tree_samples    0                
maximum_distance                {'default': 60.0}
investigation_time              50.0             
ses_per_logic_tree_path         1                
truncation_level                3.0              
rupture_mesh_spacing            2.0              
complex_fault_mesh_spacing      2.0              
width_of_mfd_bin                0.1              
area_source_discretization      10.0             
ground_motion_correlation_model None             
minimum_intensity               {}               
random_seed                     24               
master_seed                     0                
ses_seed                        42               
=============================== =================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model_1.xml <source_model_1.xml>`_                  
source                  `source_model_2.xml <source_model_2.xml>`_                  
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        0.25000 complex(2,2)    4/4             
b2        0.75000 complex(2,2)    4/4             
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ===================================== =========== ======================= =================
grp_id gsims                                 distances   siteparams              ruptparams       
====== ===================================== =========== ======================= =================
0      BooreAtkinson2008() ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
1      AkkarBommer2010() ChiouYoungs2008()   rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
2      BooreAtkinson2008() ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
3      AkkarBommer2010() ChiouYoungs2008()   rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
====== ===================================== =========== ======================= =================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=8, rlzs=8)
  0,BooreAtkinson2008(): [0 1]
  0,ChiouYoungs2008(): [2 3]
  1,AkkarBommer2010(): [0 2]
  1,ChiouYoungs2008(): [1 3]
  2,BooreAtkinson2008(): [4 5]
  2,ChiouYoungs2008(): [6 7]
  3,AkkarBommer2010(): [4 6]
  3,ChiouYoungs2008(): [5 7]>

Number of ruptures per tectonic region type
-------------------------------------------
================== ====== ==================== ============ ============
source_model       grp_id trt                  eff_ruptures tot_ruptures
================== ====== ==================== ============ ============
source_model_1.xml 0      Active Shallow Crust 543          543         
source_model_1.xml 1      Stable Shallow Crust 4            4           
source_model_2.xml 2      Active Shallow Crust 543          543         
source_model_2.xml 3      Stable Shallow Crust 1            1           
================== ====== ==================== ============ ============

============= =====
#TRT models   4    
#eff_ruptures 1,091
#tot_ruptures 1,091
#tot_weight   1,543
============= =====

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight 
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======
0      1         S    0     2     543          2.57083   0.00664    30        15        767    
1      2         S    2     4     4            0.02044   2.480E-05  2.00000   1         5.65685
2      1         S    0     2     543          2.48901   0.00525    30        15        767    
3      2         X    2     398   1            0.03084   8.583E-06  2.00000   1         1.41421
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
S    5.08029   3     
X    0.03084   1     
==== ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ======= ======= ======= ======= =========
operation-duration mean    stddev  min     max     num_tasks
read_source_models 0.01468 0.01120 0.00676 0.02260 2        
split_filter       0.03728 NaN     0.03728 0.03728 1        
classical          0.34496 0.11869 0.05615 0.47958 15       
build_hazard_stats 0.01704 0.00266 0.01516 0.01892 2        
================== ======= ======= ======= ======= =========

Fastest task
------------
taskno=15, weight=7, duration=0 s, sources="2"

======== ======= ======= ======= ======= =
variable mean    stddev  min     max     n
======== ======= ======= ======= ======= =
nsites   2.00000 0.0     2       2       2
weight   3.53553 3.00000 1.41421 5.65685 2
======== ======= ======= ======= ======= =

Slowest task
------------
taskno=13, weight=135, duration=0 s, sources="1"

======== ======= ======= === === =
variable mean    stddev  min max n
======== ======= ======= === === =
nsites   2.00000 0.0     2   2   3
weight   45      5.65685 39  50  3
======== ======= ======= === === =

Data transfer
-------------
================== ============================================================================== ========
task               sent                                                                           received
read_source_models monitor=736 B converter=638 B fnames=370 B                                     13.83 KB
split_filter       srcs=12.14 KB monitor=381 B srcfilter=253 B sample_factor=21 B seed=14 B       18.11 KB
classical          group=31.01 KB param=20.21 KB monitor=5.05 KB src_filter=3.22 KB gsims=3.22 KB 60.67 KB
build_hazard_stats pgetter=9.28 KB monitor=708 B hstats=402 B                                     5.89 KB 
================== ============================================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total classical          5.17446   0.84766   15    
make_contexts            3.17773   0.0       1,091 
get_poes                 1.51886   0.0       1,091 
iter_ruptures            0.39859   0.0       32    
updating source_info     0.04534   0.0       1     
store source_info        0.04163   0.0       15    
total split_filter       0.03728   0.0       1     
total build_hazard_stats 0.03408   0.53906   2     
total read_source_models 0.02936   0.12891   2     
combine pmaps            0.02519   0.53906   2     
managing sources         0.00802   0.0       1     
saving probability maps  0.00486   0.0       1     
aggregate curves         0.00465   0.0       15    
compute quantile-0.15    0.00380   0.0       2     
compute quantile-0.85    0.00358   0.0       2     
saving statistics        0.00276   0.0       2     
compute mean             7.215E-04 0.0       2     
======================== ========= ========= ======