# encoding: utf-8
'''
Performs sensor level analysis. Raw -> filter -> epochs -> cov

This is part of a toy pipeline created to play a detection game. There is a
subtle mistake being made somewhere. By visualizing the data after each
processing step, you can play detective. Can you find the the error?

Author: Marijn van Vliet <w.m.vanvliet@gmail.com>
'''
import mne
sample_path = mne.datasets.sample.data_path()

# Read in the continuous, raw, data
raw = mne.io.read_raw_fif(sample_path + '/MEG/sample/sample_audvis_raw.fif', preload=True)

# Let's save memory and processing time early on and only pick the channels we need
raw = raw.pick_types(meg='grad', eeg=False, stim=True)

# Bandpass filter the data
raw = raw.filter(1, 40)

# Define our events. While the experiment had both visual and auditory
# stimulation, we are only interested in the auditory conditions.
events = mne.find_events(raw)
event_id = dict(left_aud=3, right_aud=4)

# Create Epochs around the event onsets
epochs = mne.Epochs(
    raw, events, event_id,
    tmin=-0.2, tmax=0.5,  # these parameters define the time window
    decim=3,  # Use only every 3rd sample to save memory and processing time
    preload=True,  # Load everything into memory
)

# Create evokeds for left and right auditory beeps
evoked_left = epochs['left_aud'].average()
evoked_right = epochs['right_aud'].average()

# Compute the data covariance matrix (needed for the LCMV beamformer)
data_cov = mne.compute_covariance(epochs, tmin=0.04, tmax=0.15, method='shrunk')

# Save everything. It will be processed further in 02_source_level.py.
mne.write_events('data/detective-eve.fif', events)
epochs.save('data/detective-epo.fif', overwrite=True)
mne.write_evokeds('data/detective-ave.fif', [evoked_left, evoked_right])
data_cov.save('data/detective-cov.fif')
