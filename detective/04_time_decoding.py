# encoding: utf-8
'''
Picks up where 03_determine_rois.py left off. It uses a beamformer to
reconstruct the source level timecourses in the ROIs for each epoch. This is
then used in a decoding model, operating across time. Finally, the decoding
performance over time is plotted.

This is part of a toy pipeline created to play a detection game. There is a
subtle mistake being made somewhere. By visualizing the data after each
processing step, you can play detective. Can you find the the error?

Author: Marijn van Vliet <w.m.vanvliet@gmail.com>
'''
import numpy as np
from scipy.stats import zscore
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt
import mne
sample_path = mne.datasets.sample.data_path()

# Read everything in
epochs = mne.read_epochs('data/detective-epo.fif')
fwd = mne.read_forward_solution(sample_path + '/MEG/sample/sample_audvis-meg-oct-6-fwd.fif')
data_cov = mne.read_cov('data/detective-cov.fif')
roi_lh = mne.read_label('data/roi-lh.label')
roi_rh = mne.read_label('data/roi-rh.label')

# Use the LCMV beamformer to create source timecourses for each epoch in the ROIs
lcmv_lh = mne.beamformer.make_lcmv(epochs.info, fwd, data_cov, label=roi_lh,
                                   reg=0.05, pick_ori='max-power', weight_norm='unit-noise-gain')
lcmv_rh = mne.beamformer.make_lcmv(epochs.info, fwd, data_cov, label=roi_rh,
                                   reg=0.05, pick_ori='max-power', weight_norm='unit-noise-gain')
stc_lh = mne.beamformer.apply_lcmv_epochs(epochs, lcmv_lh)
stc_rh = mne.beamformer.apply_lcmv_epochs(epochs, lcmv_rh)

# Construct X and y matrices for decoding
X_lh = np.array([stc.data for stc in stc_lh])
X_rh = np.array([stc.data for stc in stc_rh])
X = np.concatenate((X_lh, X_rh), axis=1)
X = zscore(X, axis=0)  # Normalize the data
y = epochs.events[:, 2]

# Perform decoding along time
lr = LogisticRegression(C=0.1, solver='lbfgs')
se = mne.decoding.SlidingEstimator(lr, scoring='roc_auc').fit(X, y)
score = mne.decoding.cross_val_multiscore(se, X, y, cv=5)

# Plot the decoding results
fig_results = plt.figure()
plt.plot(epochs.times, score.mean(axis=0))
plt.axvline(0, linestyle='--', color='black')
plt.axhline(0.5, color='black')
plt.ylim(0.3, 1.0)
plt.xlabel('Time (s)')
plt.ylabel('Performance (ROC-AUC)')
plt.title('Decoding left vs. right auditory beeps')

# Save the coveted results figure
plt.savefig('results.pdf')
