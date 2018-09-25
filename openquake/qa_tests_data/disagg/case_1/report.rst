QA test for disaggregation case_1, taken from the disagg demo
=============================================================

============== ===================
checksum32     1,811,660,702      
date           2018-09-25T14:27:48
engine_version 3.3.0-git8ffb37de56
============== ===================

num_sites = 2, num_levels = 38

Parameters
----------
=============================== ==================
calculation_mode                'disaggregation'  
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 100.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            5.0               
complex_fault_mesh_spacing      5.0               
width_of_mfd_bin                0.2               
area_source_discretization      10.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     9000              
master_seed                     0                 
ses_seed                        42                
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gmpe_logic_tree.xml <gmpe_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model.xml <source_model.xml>`_                      
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        1.00000 trivial(1)      1/1             
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================= =========== ======================= =================
grp_id gsims             distances   siteparams              ruptparams       
====== ================= =========== ======================= =================
0      ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
1      ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
2      ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
3      ChiouYoungs2008() rjb rrup rx vs30 vs30measured z1pt0 dip mag rake ztor
====== ================= =========== ======================= =================

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=4, rlzs=1)
  0,ChiouYoungs2008(): [0]
  1,ChiouYoungs2008(): [0]
  2,ChiouYoungs2008(): [0]
  3,ChiouYoungs2008(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 15           15          
source_model.xml 1      Active Shallow Crust 1,440        1,440       
source_model.xml 2      Active Shallow Crust 617          617         
source_model.xml 3      Active Shallow Crust 164          164         
================ ====== ==================== ============ ============

============= =====
#TRT models   4    
#eff_ruptures 2,236
#tot_ruptures 2,236
#tot_weight   1,418
============= =====

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight 
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======
0      1         P    0     1     15           0.02713   1.836E-05  1.00000   1         1.50000
1      2         A    1     5     1,440        2.03822   1.43678    96        96        144    
2      3         S    5     7     617          1.18707   0.00143    10        10        617    
3      4         C    7     11    164          0.69332   0.00185    10        10        656    
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= =======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    2.03822   1     
C    0.69332   1     
P    0.02713   1     
S    1.18707   1     
==== ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ======= ======= ======= ======= =========
operation-duration mean    stddev  min     max     num_tasks
read_source_models 0.03912 NaN     0.03912 0.03912 1        
split_filter       0.03833 NaN     0.03833 0.03833 1        
classical          0.79376 0.89002 0.23456 2.36952 5        
build_hazard_stats 0.00862 0.00340 0.00622 0.01102 2        
================== ======= ======= ======= ======= =========

Fastest task
------------
taskno=5, weight=152, duration=0 s, sources="4"

======== ======= ====== ======= === =
variable mean    stddev min     max n
======== ======= ====== ======= === =
nsites   1.00000 0.0    1       1   4
weight   38      26     4.00000 64  4
======== ======= ====== ======= === =

Slowest task
------------
taskno=1, weight=321, duration=2 s, sources="1 2 3"

======== ======= ====== ======= === ==
variable mean    stddev min     max n 
======== ======= ====== ======= === ==
nsites   1.00000 0.0    1       1   99
weight   3.24747 12     1.50000 88  99
======== ======= ====== ======= === ==

Data transfer
-------------
================== =========================================================================== ========
task               sent                                                                        received
read_source_models monitor=0 B fnames=0 B converter=0 B                                        3.87 KB 
split_filter       srcs=3.3 KB monitor=446 B srcfilter=253 B sample_factor=21 B seed=15 B      26.8 KB 
classical          group=30.17 KB param=4.23 KB monitor=1.68 KB src_filter=1.07 KB gsims=635 B 5.62 KB 
build_hazard_stats pgetter=5.45 KB monitor=708 B hstats=134 B                                  684 B   
================== =========================================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
total classical          3.96880   0.50000   5     
make_contexts            1.88386   0.0       2,236 
get_poes                 1.03215   0.0       2,236 
iter_ruptures            1.00548   0.0       117   
updating source_info     0.04689   0.0       1     
total read_source_models 0.03928   0.0       3     
total split_filter       0.03833   0.0       1     
total build_hazard_stats 0.01724   0.0       2     
combine pmaps            0.01627   0.0       2     
store source_info        0.01560   0.0       5     
managing sources         0.00685   0.0       1     
saving probability maps  0.00594   0.0       1     
aggregate curves         0.00181   0.0       5     
saving statistics        8.168E-04 0.0       2     
compute mean             3.171E-04 0.0       1     
======================== ========= ========= ======