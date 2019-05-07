# encoding: utf-8
'''
Picks up where 02_source_level.py left off. Finds for each hemisphere, the
location of peak activity and uses it as a seed to define a region of interest
(ROI).

This is part of a toy pipeline created to play a detection game. There is a
subtle mistake being made somewhere. By visualizing the data after each
processing step, you can play detective. Can you find the the error?

Author: Marijn van Vliet <w.m.vanvliet@gmail.com>
'''
import numpy as np
import mne
from mayavi import mlab
mlab.options.offscreen = True  # Render mayavi figures offscreen
sample_path = mne.datasets.sample.data_path()

# Read everything in
epochs = mne.read_epochs('data/detective-epo.fif')
fwd = mne.read_forward_solution(sample_path + '/MEG/sample/sample_audvis-meg-oct-6-fwd.fif')
data_cov = mne.read_cov('data/detective-cov.fif')
stc_all = mne.read_source_estimate('data/detective')

# For the location of the ROIs, only focus on the primary auditory response
stc_all = stc_all.crop(0.04, 0.15)

# Find for each hemisphere, the vertex with maximum activity
peak_location_lh = stc_all.vertices[0][np.argmax(np.sum(stc_all.lh_data ** 2, axis=1))]
peak_location_rh = stc_all.vertices[1][np.argmax(np.sum(stc_all.rh_data ** 2, axis=1))]

# Grow ROI labels around the peak locations
roi_lh, roi_rh = mne.grow_labels(
    'sample', [peak_location_lh, peak_location_rh],
    extents=[20, 20], hemis=[0, 1], subjects_dir=sample_path + '/subjects'
)

# Save the ROIs so that 04_time_decoding.py may make use of them
roi_lh.save('data/roi-lh.label')
roi_rh.save('data/roi-rh.label')
