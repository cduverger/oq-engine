Classical Hazard QA Test, Case 25, topographic surface1 (Mt Etna)
=================================================================

============== ===================
checksum32     3,398,720,512      
date           2018-09-25T14:28:38
engine_version 3.3.0-git8ffb37de56
============== ===================

num_sites = 6, num_levels = 3

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              50.0              
ses_per_logic_tree_path         1                 
truncation_level                3.0               
rupture_mesh_spacing            1.0               
complex_fault_mesh_spacing      1.0               
width_of_mfd_bin                0.1               
area_source_discretization      1.0               
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     23                
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
sites                   `sites.csv <sites.csv>`_                                    
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
====== ===================== ========== ========== ==========
grp_id gsims                 distances  siteparams ruptparams
====== ===================== ========== ========== ==========
0      TusaLanger2016Rhypo() rhypo rrup vs30       mag       
====== ===================== ========== ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=1, rlzs=1)
  0,TusaLanger2016Rhypo(): [0]>

Number of ruptures per tectonic region type
-------------------------------------------
================ ====== ======== ============ ============
source_model     grp_id trt      eff_ruptures tot_ruptures
================ ====== ======== ============ ============
source_model.xml 0      Volcanic 440          440         
================ ====== ======== ============ ============

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======
0      1         A    0     8     440          0.0       0.15756    0.0       20        0.0   
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
A    0.0       1     
==== ========= ======

Duplicated sources
------------------
There are no duplicated sources

Information about the tasks
---------------------------
================== ======= ====== ======= ======= =========
operation-duration mean    stddev min     max     num_tasks
read_source_models 0.00848 NaN    0.00848 0.00848 1        
split_filter       0.01130 NaN    0.01130 0.01130 1        
================== ======= ====== ======= ======= =========

Data transfer
-------------
================== ==================================================================== ========
task               sent                                                                 received
read_source_models monitor=0 B fnames=0 B converter=0 B                                 2.35 KB 
split_filter       srcs=2 KB monitor=432 B srcfilter=253 B sample_factor=21 B seed=14 B 5.71 KB 
================== ==================================================================== ========

Slowest operations
------------------
======================== ======== ========= ======
operation                time_sec memory_mb counts
======================== ======== ========= ======
updating source_info     0.01730  0.0       1     
total split_filter       0.01130  0.0       1     
total read_source_models 0.00848  0.0       1     
======================== ======== ========= ======