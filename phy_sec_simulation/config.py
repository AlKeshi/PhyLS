import numpy as np

# Common Simulation Parameters
N_ANTENNAS = 10  # Number of antennas at Alice
ALPHA_VAL = 0.5  # Power allocation factor for w
SIGMA_N_SQ = 1.0  # Natural noise variance
R_THRESHOLD = 3  # Constant threshold rate for outage probability
M_MONTE_CARLO_G = 1000  # Number of Monte Carlo simulations for g (Eve's channel)
M_MONTE_CARLO_H = 1000 # Number of Monte Carlo simulations for h (Bob's channel)
SNR_DB_RANGE = np.arange(-5, 21, 1) # SNR range in dB 