# encoding: utf-8
'''
Picks up where 01_sensor_level.py left off. It uses a beamformer to perform
source level analysis. epochs -> source timecourses

This is part of a toy pipeline created to play a detection game. There is a
subtle mistake being made somewhere. By visualizing the data after each
processing step, you can play detective. Can you find the the error?

Author: Marijn van Vliet <w.m.vanvliet@gmail.com>
'''
import mne
sample_path = mne.datasets.sample.data_path()

# Read in the epochs and data_cov produced by 01_sensor_level.py
epochs = mne.read_epochs('data/detective-epo.fif')
data_cov = mne.read_cov('data/detective-cov.fif')

# Read in the forward operator
fwd = mne.read_forward_solution(sample_path + '/MEG/sample/sample_audvis-meg-oct-6-fwd.fif')

# Construct an LCMV beamformer
lcmv_all = mne.beamformer.make_lcmv(
    epochs.info, fwd, data_cov, reg=0.05,
    pick_ori='max-power', weight_norm='unit-noise-gain' )

# Make a source estimate using the evoked potential
stc_all = mne.beamformer.apply_lcmv(epochs.average(), lcmv_all)

# Save everything, so that 03_determine_rois.py can make use of it
stc_all.save('data/detective')
