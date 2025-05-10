import numpy as np
from scipy.linalg import null_space
from .utils import generate_channel_vector

def strategy_1(P_total, N, alpha, sigma_n_sq_val, M_g_sims, R_thresh):
    """
    Implements Strategy 1: Constant Power Allocation.
    Returns instantaneous secrecy rate and outage event (1 if R_s > R_thresh, 0 otherwise).
    """
    h = generate_channel_vector(N)
    h_H = h.conj().T
    h_norm_sq = np.abs(np.vdot(h, h))

    if h_norm_sq < 1e-9:
        return 0.0, 0

    lambda_val = 2 * (N - 1) * alpha * P_total
    mu_val = P_total - lambda_val/(2*(N-1))

    w = np.sqrt(lambda_val) * (h / h_norm_sq)

    if N > 1:
        gamma_basis = null_space(h_H)
        # Ensure gamma_basis has enough columns if N > 1
        if gamma_basis.shape[1] < (N - 1) and N -1 > 0: # Should not happen if h is not zero vector for N > 1
             # This case implies h might be nearly zero or some numerical issue, 
             # effectively no real null-space to work with for AN of desired dimension.
             z = np.zeros((N,1))
        elif gamma_basis.shape[1] == 0 and N > 1: # N > 1 but null space is 0-dim (e.g. if h was a full rank matrix instead of vector)
            z = np.zeros((N,1))
        else: 
            v_for_gamma_v = (np.random.randn(N - 1, 1) + 1j * np.random.randn(N - 1, 1)) / np.sqrt(2)
            gamma_v = gamma_basis @ v_for_gamma_v
            norm_gamma_v = np.linalg.norm(gamma_v)
            z = np.sqrt(mu_val) * (gamma_v / norm_gamma_v) if norm_gamma_v > 1e-9 else np.zeros((N, 1))
    else: # N=1
        z = np.zeros((N, 1))

    signal_power_bob = np.abs(h_H @ w)**2
    R_b = np.log2(1 + signal_power_bob / sigma_n_sq_val)

    R_s = 0.0 # Default R_s
    R_e_sum = 0.0
    if np.linalg.norm(w) < 1e-9:
        R_s = 0.0
    elif (N > 1 and np.linalg.norm(z) < 1e-9) or N == 1: # No artificial noise contribution or N=1
        for _ in range(M_g_sims):
            g = generate_channel_vector(N)
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

    event_rs_greater_R = 1 if R_s > R_thresh else 0 # Corrected logic for Pr(R_s > R)
    return float(R_s), event_rs_greater_R 