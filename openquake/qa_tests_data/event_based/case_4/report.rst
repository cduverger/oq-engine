Event-Based Hazard QA Test, Case 4
==================================

============== ===================
checksum32     336,991,371        
date           2018-09-25T14:28:01
engine_version 3.3.0-git8ffb37de56
============== ===================

num_sites = 1, num_levels = 3

Parameters
----------
=============================== ==================
calculation_mode                'event_based'     
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         50                
truncation_level                0.0               
rupture_mesh_spacing            2.0               
complex_fault_mesh_spacing      2.0               
width_of_mfd_bin                1.0               
area_source_discretization      20.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     42                
master_seed                     0                 
ses_seed                        1066              
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
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
====== ================ ========= ========== ==========
grp_id gsims            distances siteparams ruptparams
====== ================ ========= ========== ==========
0      SadighEtAl1997() rrup      vs30       mag rake  
====== ================ ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,SadighEtAl1997(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ==================== ============ ============
source_model     grp_id trt                  eff_ruptures tot_ruptures
================ ====== ==================== ============ ============
source_model.xml 0      Active Shallow Crust 5            5           
================ ====== ==================== ============ ============

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======
0      1         S    0     2     5            0.00404   3.457E-05  1.00000   1         56    
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
S    0.00404   1     
==== ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ======= ====== ======= ======= =========
operation-duration mean    stddev min     max     num_tasks
read_source_models 0.00223 NaN    0.00223 0.00223 1        
split_filter       0.00528 NaN    0.00528 0.00528 1        
build_ruptures     0.00549 NaN    0.00549 0.00549 1        
================== ======= ====== ======= ======= =========

Data transfer
-------------
================== ====================================================================== ========
task               sent                                                                   received
read_source_models monitor=0 B fnames=0 B converter=0 B                                   1.47 KB 
split_filter       srcs=1.2 KB monitor=432 B srcfilter=220 B sample_factor=21 B seed=14 B 1.23 KB 
build_ruptures     srcs=0 B srcfilter=0 B param=0 B monitor=0 B                           6.26 KB 
================== ====================================================================== ========

Slowest operations
------------------
======================== ========= ========= ======
operation                time_sec  memory_mb counts
======================== ========= ========= ======
updating source_info     0.01489   0.0       1     
total build_ruptures     0.00549   0.0       1     
total split_filter       0.00528   0.0       1     
store source_info        0.00458   0.0       1     
saving ruptures          0.00354   0.0       1     
total read_source_models 0.00223   0.0       1     
making contexts          6.146E-04 0.0       5     
======================== ========= ========= ======