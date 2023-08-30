#!/bin/bash -l
#SBATCH --job-name=GE-conda
#  the partition is the queue your submit your job to 
# there is a day partition max walltime 24:00:00
# there is a week partition maxx walltime is 7-00:00:00
#SBATCH --partition=gpu
# the nodes is the number computes
#SBATCH --nodes=1
# the ntasks is number of cpu cores  max number is 34
#SBATCH --ntasks=4
#  gres defines the number of gpus: 1 or 2 
#SBATCH --gres=gpu:v100:1
#  walltime the max time is dependent on partition
#SBATCH --time=12:00:00
#SBATCH --export=ALL
#SBATCH --mem=0

# To configure GNU Environment for Mothur
module load Anaconda3/2020.11
conda activate CEED
# leave in, it lists the environment loaded by the modules
module list

#  Note: SLURM_JOBID is a unique number for every job.
#  These are generic variables
SCRIPT=testing_custom.py
# qqto use NVMe uncomment this following line
# SCRATCH=/tmp/$USER/run_conda/$SLURM_JOBID
# to use MYSCRATCH space
SCRATCH=$MYSCRATCH/CEED/pipe_bends2_txt
RESULTS=$MYGROUP/CEED_results

###############################################
# Creates a unique directory in the SCRATCH directory for this job to run in.
if [ ! -d $SCRATCH ]; then 
    mkdir -p $SCRATCH 
fi 
echo Working SCRATCH directory is $SCRATCH

###############################################
# Creates a unique directory in your GROUP directory for the results of this job
if [ ! -d $RESULTS ]; then 
     mkdir -p $RESULTS
fi 
echo Results will be store in $RESULTS/$SLURM_JOBID

#############################################
#   Copy input files to $SCRATCH
#   then change directory to $SCRATCH
cd ${SLURM_SUBMIT_DIR}

#cp ${DATA_DIR}/* ${SCRATCH}
# copy the mothur analysis script to SCRATCH
cp $SCRIPT ${SCRATCH}

cd ${SCRATCH}

ls -al

python $SCRIPT

#############################################
#    $OUTPUT file to the unique results dir
# note this can be a copy or move  
#cd $HOME
#mv ${SCRATCH} ${RESULTS}

###########################
# Clean up $SCRATCH 

#rm -r $SCRATCH

echo Conda ML gpu job finished at  `date`


