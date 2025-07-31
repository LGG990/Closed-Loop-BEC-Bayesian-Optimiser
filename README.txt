Flow of code is as follows



call the Skopt function to run bayesian estimation.
feed it the run_experiment function, the estimation parameters, and other settings.
run_experiment, given the current estimated parameters calls the send_to_sequence function, handing over the parameters.
    >send_to_sequence gives the parameters to Cicero API and triggers the experiment to run.
    >in the background, the image analysis should be running, which will generate a new set of both num_atoms and temperature.
    >run_experiment then calls get_experiment_results to fetch the atom_number and temperature from image analysis output file, then assigns to the results variable.
    the output file contains all output fit parameters, including errors.
    >run_experiment then gives these results to the cloud_score function in order to score how good the experiment parameters performed based on the
    scoring function.
    >run_experiment then returns the scoring value from cloud_score
scoring value is then read by skopt which then calculates a new parameter set within the given bounds.


