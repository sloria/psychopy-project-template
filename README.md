# Psychopy project template

## Running the experiment
Open `run.py` in the PsychoPy Coder window and click Run.

## For experiment designers
Edit `experiment.py` to your liking.

## For developers
Edit `run.py` to display the correct stimuli based on what is in `experiment.py`

Put experiment-specific stimuli classes in `custom_stimli.py`.

## Settings
* Global settings are defined in `settings/base.py`.
* Environment-specific settings have their own file modules, e.g. `mri.py` and `dev.py` (development).
* The environment can be switched by changing the `ENV` variable in `settings/base.py`
