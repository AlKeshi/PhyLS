import numpy as np
from scipy.linalg import null_space
from .utils import generate_channel_vector

def strategy_3_2(P_total, N, alpha, sigma_n_sq_val, M_g_sims, R_thresh):
    """
    Implements Strategy 3.2.
    Beamforming w = sqrt(lambda) * h
    Artificial Noise z = sqrt(mu) * |h| * gamma_v / ||gamma_v||
    E[|w|^2] = alpha * P_total
    E[|z|^2] = (1 - alpha) * P_total
    h is from generate_channel_vector, so E[|h|^2] = 2N
    lambda_val = alpha * P_total / (2N)
    mu_val = (1-alpha) * P_total / (2N)
    """
    h = generate_channel_vector(N) # Shape (N, 1), E[|h|^2] = 2N
    h_H = h.conj().T # Shape (1, N)
    h_norm_sq = np.abs(np.vdot(h, h)) # Scalar, |h|^2

    if h_norm_sq < 1e-9 or N == 0: # N=0 check for robustness
        return 0.0, 0

    # Power allocation constants
    # lambda_val * E[|h|^2] = alpha * P_total => lambda_val * 2 * N = alpha * P_total
    lambda_val = (alpha * P_total) / (2 * N) if N > 0 else 0
    # mu_val * E[|h|^2] = (1-alpha) * P_total => mu_val * 2 * N = (1-alpha) * P_total
    mu_val = ((1 - alpha) * P_total) / (2 * N) if N > 0 else 0

    # Beamforming vector w
    w = np.sqrt(lambda_val) * h # Shape (N, 1)

    # Artificial noise vector z
    if N > 1:
        gamma_basis = null_space(h_H) # Shape (N, N-1)
        
        if gamma_basis.shape[1] < (N - 1):
            z = np.zeros((N,1))
        else:
            v_rand = (np.random.randn(N - 1, 1) + 1j * np.random.randn(N - 1, 1)) / np.sqrt(2)
            gamma_v = gamma_basis @ v_rand # Shape (N, 1)
            norm_gamma_v = np.linalg.norm(gamma_v)
            
            if norm_gamma_v > 1e-9:
                # Key difference from 3.1: scaling by |h|
                z = np.sqrt(mu_val) * np.sqrt(h_norm_sq) * (gamma_v / norm_gamma_v) # Shape (N, 1)
            else:
                z = np.zeros((N,1))
    else: # N=1
        z = np.zeros((N, 1))

    # Calculate Secrecy Rate
    signal_power_bob = np.abs(h_H @ w)**2
    R_b = np.log2(1 + signal_power_bob / sigma_n_sq_val)

    R_e_sum = 0.0
    w_is_zero = np.linalg.norm(w) < 1e-9
    z_is_zero = N <= 1 or np.linalg.norm(z) < 1e-9

    if w_is_zero:
        R_s = 0.0
    else:
        for _ in range(M_g_sims):
            g = generate_channel_vector(N)
            g_H = g.conj().T
            
            signal_power_eve = np.abs(g_H @ w)**2
            
            if z_is_zero:
                R_e_sum += np.log2(1 + signal_power_eve / sigma_n_sq_val)
            else:
                noise_power_eve_an = np.abs(g_H @ z)**2
                total_noise_eve = noise_power_eve_an + sigma_n_sq_val
                R_e_sum += np.log2(1 + signal_power_eve / (total_noise_eve if total_noise_eve > 1e-9 else 1e-9))
        
        R_e = R_e_sum / M_g_sims if M_g_sims > 0 else 0.0
        R_s = np.maximum(0.0, R_b - R_e)

    event_rs_greater_R = 1 if R_s > R_thresh else 0
    return float(R_s), event_rs_greater_R 