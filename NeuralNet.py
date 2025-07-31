"""
Program to optimize parameters for a Bose-Einstein Condensate (BEC) experiment using Bayesian optimization.
This script defines an objective function to score the atom cloud/ BEC based on input parameters, then uses the `skopt`
library to perform Bayesian optimization over a defined search space of hyperparameters.



NOTE: need to remove the random_state=42 line for production use, this is only for debugging purposes!
"""
import numpy as np
from skopt.space import Real, Integer
from skopt import gp_minimize
import codecs
import re

#extract image analysis from txt file
def get_experiment_results(filename):
     # This function should retrieve the results from the image analysis.
    #wait for signal that the sequence is finished then retrieve the results from the analysis code 
    with codecs.open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    T_val = None
    N_val = None

    for line in lines:
        line = line.strip()

        if line.startswith("T :"):
            # Extract number after "T :" using regex
            match = re.search(r"T\s*:\s*([\d\.]+)", line)
            if match:
                T_val = match.group(1)

        elif line.startswith("N :"):
            match = re.search(r"N\s*:\s*([\d\.]+)", line)
            if match:
                N_val = match.group(1)

    if T_val:
        print(float(T_val)*0.000001)
    else:
        print("T value not found.")

    if N_val:
        print(float(N_val)*1000)
    else:
        print("N value not found.")

    return(float(T_val)*0.000001, float(N_val)*1000)  # Return temperature in Kelvin and number of atoms
  

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
     10000
     0.000000010


     score = (temp*1e8) - (num_atoms/10000)     
     return (score)
   

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

    results = get_experiment_results("output.txt")  #retrieve the results from the sequencer

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
