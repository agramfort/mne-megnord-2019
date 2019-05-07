The detective challenge
=======================

This folder contains a small example data analysis pipeline. Even though the final output looks reasonable, it contains a critical error, somewhere hidden in the code. Can you find the error?

The scenario
------------

We have produced a ground breaking new result! By using advanced decoding-across-time analysis, we have successfully mapped the cortical dynamics of auditory beeps. The decoding performance is very high and it is nicely resolved over time. The paper, entitled "Tracking the processing of auditory stimuli through time-resolved decoding" has been send to a high impact journal and the reviewers are impressed. Celebrations all around!

However, somethings gnaws at your conscience. The pipeline was written in quite a hurry, and since the final result looked good, nobody dared to ask the hard questions: are the decoding results real? You can't shake the feeling that there is something horribly wrong with the analysis...

Your mission
------------

Carefully plot the data as it moves through the pipeline and check every step. Can you find the critical error that, if discovered, will surely be cause to retract the paper? During the MEG-Nord workshop, you will be instructed in advanced plotting routines, the workings of the beamformer source analysis method, and the decoding-over-time. Use what you have learned to uncover, and fix, the bug!

Details of the analysis pipeline
--------------------------------

Here is an excerpt of the methods section of the paper:

"In the experiment, checkerboard patterns were presented into the left and right visual field, interspersed by tones to the left or right ear. For this study, only the MEG responses to the auditory stimuli were used. The data were acquired with the Neuromag Vectorview system at MGH/HMS/MIT Athinoula A. Martinos Center Biomedical Imaging. The original MRI data set was acquired with a Siemens 1.5 T Sonata scanner using an MPRAGE sequence.

The MEG data was first band-pass filtered between 1-40 Hz. Then, epochs were cut from -0.2 to 0.5 seconds, relative to the onset of the auditory beep. An LCMV beamformer was used to provide an initial source estimation of the evoked responses. This initial estimation was used to determine two regions of interest (ROIs), one on each hemisphere of the brain. The seed points for the ROIs were the vertices with the most source activity, and were subsequently grown into patches of cortical surface with a radius of 2 cm.

Finally, an LCMV beamformer was used to reconstruct, for each epoch, the source timecourse within each ROI. This data was then entered into a logistic regression algorithm to decode left versus right auditory beeps. The decoding was repeated for each time point. The performance of the decoder (roc-auc, using 5-fold crossvalidation) was plotted over time to determine when the signal in the ROIs contained information about the stimuli."

Running the pipeline
--------------------

The pipeline is split up into four scripts, which can be run sequentially to perform the entire analysis:

	python 01_sensor_level.py
	python 02_source_level.py
	python 03_determine_rois.py
	python 04_time_decoding.py

Running the final script (`04_time_decoding.py`) produces a figure `results.pdf` containing the decoding results.
