"""
Program to optimize parameters for a Bose-Einstein Condensate (BEC) experiment using Bayesian optimization.
This script defines an objective function to score the atom cloud/ BEC based on input parameters, then uses the `skopt`
library to perform Bayesian optimization over a defined search space of hyperparameters.



NOTE: need to remove the random_state=42 line for production use, this is only for debugging purposes!
"""



import numpy as np
from skopt.space import Real, Integer
from skopt import gp_minimize


#Build objective function to score the BEC
def cloud_score(temp, num_atoms):
    """
    Calculate the BEC score based on the given parameters.
    
    Parameters:
    temperature (float): Temperature of the system in Kelvin.
    num_atoms (int): Total number of atoms in the system.

    Returns:
    float: Calculated BEC score.
    """

    #either higher is better or lower is better, network will work to maximise or minimise
    # this value
    #need to decide on a scoring function using these parameters

    #example, this scales the values to make them easier to work with and comparable. 
    #higher condensate fraction, lower temperature, and number of atoms are better, hence the positive and negative
    # signs.
    # return(
    #    2.0 * r["condensate_fraction"] +
    #    0.5 * np.log10(r["atom_number"]) -
    #    5.0 * (r["temperature"] * 1e9)  # scale to nK
    # )
    return (-np.log(num_atoms)+temp)

def get_experiment_results():
    # This function should retrieve the results from the image analysis.
    #wait for signal that the sequence is finished then retrieve the results from the analysis code
    return()# return(resuling paramters from the experiment) 

def send_to_sequence(parameters):
    """
    Send the current hyperparameters to the sequencer/api.
    This function should interface with the sequencer to set the parameters for the experiment.
    
    Parameters:
    parameters (dict): Dictionary containing the hyperparameters to be sent.
    """

    #send paramters to cicero/API etc etc

    print("Sending parameters to sequencer:", parameters)


#Define a funtion to send the currect values of the parameters to the sequencer
def run_experiment(tof, parameter2, parameter3, parameter4):
    """
    Run the experiment with the current hyperparameters.
    This function should interface with the sequencer to execute the experiment.
    """
    send_to_sequence({
        'tof': tof,
        'parameter2': parameter2,
        'parameter3': parameter3,
        'parameter4': parameter4

    })

    results = get_experiment_results()  #retrieve the results from the sequencer

    return (-cloud_score(results))  # Replace with actual implementation


#Define the search space for the hyperparameters
param_space = [
    #define each parameter with a range for the optimization algorithm to search over
    #Each parameter is defined with a Real or Integer type, specifying the range and name.    
    #Real(*number*,*number*, name='parameter_name'),
    #or
    #integer(*number*,*number*, name='parameter_name')]
    #The Real() function is for continuous parameters, while Integer() is for discrete parameters, func(upper bound, lower bound).
    #this is from scikit-optimize, which is a library for Bayesian optimization.
    
    #example parameters
    Real(0.1, 3.0, name=''),                     # Time-of-flight in ms
    Real(0.0, 1.0, name=''),                     # 
    Real(100.0, 400.0, name=''),                 # in MHz
    Real(5.0, 25.0, name=''),                    # evaporation ramp time is ms
]


#Use Skopt to perform Bayesian optimization
res = gp_minimize(
    run_experiment, # Objective function to minimize
    dimensions=param_space, # Search space
    n_calls=50, # Number of evaluations 
    n_initial_points=10, # Number of initial random guesses to try before using bayesian optimization
    random_state=42, # For reproducibility, makes all random guesses the same for each run, for DEBUGGING ONLY
)

print("Best parameters found: ")
for name, val in zip(param_space, res.x):
    print(f"{name}: {val}")


print(f"Best score: {res.fun}")  # The best score achieved by the optimization
print(f"Number of evaluations: {len(res.func_vals)}")  # Total number of evaluations made
print(f"Number of iterations: {res.n_iter}")  # Number of iterations performed
