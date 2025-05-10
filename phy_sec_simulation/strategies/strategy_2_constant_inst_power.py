import numpy as np
from scipy.linalg import null_space
from .utils import generate_channel_vector

def strategy_2_constant_inst_power(P_total, N, alpha, sigma_n_sq_val, M_g_sims, R_thresh):
    """
    Implements Strategy 2: Constant Power Allocation for Beamforming and Artificial Noise
    (Constant Instantaneous Power for w and z).
    Returns instantaneous secrecy rate and outage event (1 if R_s > R_thresh, 0 otherwise).
    """
    h = generate_channel_vector(N) # Channel Alice to Bob
    h_H = h.conj().T
    h_norm = np.linalg.norm(h)

    if h_norm < 1e-9: # Avoid division by zero if h is effectively zero
        return 0.0, 0

    # Power allocation based on description_2.md
    # lambda is power for w, mu is power for z
    # P = lambda + mu
    # alpha = lambda / P  => lambda = alpha * P
    # So, mu = P - lambda = P * (1 - alpha)
    lambda_val = alpha * P_total
    mu_val = (1 - alpha) * P_total

    # Beamforming Vector w: w = sqrt(lambda) * (h / |h|)
    w = np.sqrt(lambda_val) * (h / h_norm)
    # w is already a column vector (N,1)

    # Artificial Noise z: z = sqrt(mu) * (gamma * v / |gamma * v|)
    if N > 1:
        gamma_basis = null_space(h_H) # Orthonormal basis for null space of h_H, (N, N-1)
        
        if gamma_basis.shape[1] < (N - 1) and N - 1 > 0:
             z = np.zeros((N,1))
        elif gamma_basis.shape[1] == 0 and N > 1:
            z = np.zeros((N,1))
        else:
            # v is a random vector, e.g., CN(0, I_{N-1})
            # Our generate_channel_vector(N-1) produces elements with variance 2.
            # For CN(0, I_{N-1}), each element has variance 1. So scale by 1/sqrt(2).
            v_rand = (np.random.randn(N - 1, 1) + 1j * np.random.randn(N - 1, 1)) / np.sqrt(2 * (N - 1))
            
            gamma_v = gamma_basis @ v_rand # (N, N-1) @ (N-1, 1) = (N, 1)
            norm_gamma_v = np.linalg.norm(gamma_v)
            
            if norm_gamma_v > 1e-9:
                z = np.sqrt(mu_val) * (gamma_v / norm_gamma_v)
            else: # gamma_v is zero (e.g. if v is zero, or N=1 and gamma_basis is empty)
                z = np.zeros((N, 1))
    else: # N=1, null space is empty for h_H (scalar h_H means null space is {0} if h_H !=0, or C^N if h_H=0 - handled by h_norm check)
          # If N=1, AN is not typically generated in this manner as null space is trivial.
        z = np.zeros((N, 1))

    # Bob's rate: R_b = log2(1 + |h^H w|^2 / sigma_n^2)
    # h^H z = 0 by design of z using null space of h^H.
    signal_power_bob = np.abs(h_H @ w)**2
    R_b = np.log2(1 + signal_power_bob / sigma_n_sq_val)

    # Eve's rate (Monte Carlo)
    R_s = 0.0 # Default R_s
    R_e_sum = 0.0
    if np.linalg.norm(w) < 1e-9: # If w is zero (e.g. lambda_val is zero)
        R_s = 0.0
    # Check if z is effectively zero (e.g. mu_val is zero or N=1 or gamma_v became zero)
    elif (N > 1 and np.linalg.norm(z) < 1e-9) or N == 1:
        for _ in range(M_g_sims):
            g = generate_channel_vector(N) # Channel Alice to Eve
            g_H = g.conj().T
            signal_power_eve = np.abs(g_H @ w)**2
            R_e_sum += np.log2(1 + signal_power_eve / sigma_n_sq_val)
    else: # General case with AN (N > 1 and z is non-zero)
        for _ in range(M_g_sims):
            g = generate_channel_vector(N)
            g_H = g.conj().T
            signal_power_eve = np.abs(g_H @ w)**2
            noise_power_eve = np.abs(g_H @ z)**2 + sigma_n_sq_val
            R_e_sum += np.log2(1 + signal_power_eve / (noise_power_eve if noise_power_eve > 1e-9 else 1e-9))
    
    if np.linalg.norm(w) >= 1e-9:
        R_e = R_e_sum / M_g_sims if M_g_sims > 0 else 0.0
        R_s = np.maximum(0.0, R_b - R_e)

    event_rs_greater_R = 1 if R_s > R_thresh else 0
    return float(R_s), event_rs_greater_R 