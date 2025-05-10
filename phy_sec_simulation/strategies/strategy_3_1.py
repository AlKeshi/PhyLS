import numpy as np
from scipy.linalg import null_space
from .utils import generate_channel_vector

def strategy_3_1(P_total, N, alpha, sigma_n_sq_val, M_g_sims, R_thresh):
    """
    Implements Strategy 3.1.
    Beamforming w = sqrt(lambda) * h
    Artificial Noise z = sqrt(mu) * gamma_v / ||gamma_v||
    E[|w|^2] = alpha * P_total
    E[|z|^2] = (1 - alpha) * P_total
    h is from generate_channel_vector, so E[|h|^2] = 2N
    lambda_val = alpha * P_total / (2N)
    mu_val = (1-alpha) * P_total
    """
    h = generate_channel_vector(N) # Shape (N, 1), E[|h|^2] = 2N
    h_H = h.conj().T # Shape (1, N)
    h_norm_sq = np.abs(np.vdot(h, h)) # Scalar, |h|^2

    if h_norm_sq < 1e-9 or N == 0: # N=0 check for robustness
        return 0.0, 0
    
    # Adjust for N=0 or issues if N=1 and alpha is extreme for lambda_val
    if N == 0 : # Should not happen with typical inputs but good for robustness
        return 0.0, 0
    
    # Power allocation constants
    # lambda_val * E[|h|^2] = alpha * P_total => lambda_val * 2 * N = alpha * P_total
    lambda_val = (alpha * P_total) / (2 * N) if N > 0 else 0
    mu_val = (1 - alpha) * P_total

    # Beamforming vector w
    w = np.sqrt(lambda_val) * h # Shape (N, 1)

    # Artificial noise vector z
    if N > 1:
        # Null space of h_H (1xN) gives vectors orthogonal to h.
        # h_H x = 0. Basis for null space will be N-1 vectors if h is not zero.
        gamma_basis = null_space(h_H) # Basis vectors are columns, shape (N, N-1)
        
        if gamma_basis.shape[1] < (N - 1): 
            # This case implies h might be nearly zero or some numerical issue.
            # Fallback: no AN if proper null space dimension not found.
            z = np.zeros((N,1))
        else:
            # Create a random vector in the null space
            # v ~ CN(0, I_{N-1}/(N-1)) from description for normalized gamma_v effectively.
            # Here, using random normal and then normalizing gamma_v achieves this.
            v_rand = (np.random.randn(N - 1, 1) + 1j * np.random.randn(N - 1, 1)) / np.sqrt(2) # Each element var 1
            gamma_v = gamma_basis @ v_rand # Shape (N, 1)
            norm_gamma_v = np.linalg.norm(gamma_v)
            
            if norm_gamma_v > 1e-9:
                z = np.sqrt(mu_val) * (gamma_v / norm_gamma_v) # Shape (N, 1)
            else: # gamma_v is zero (e.g. if v_rand was zero, or numerical precision)
                z = np.zeros((N,1))
    else: # N=1, null space is trivial (zero vector)
        z = np.zeros((N, 1))

    # Calculate Secrecy Rate
    # Bob's side
    signal_power_bob = np.abs(h_H @ w)**2 # Scalar
    R_b = np.log2(1 + signal_power_bob / sigma_n_sq_val)

    # Eve's side (averaged over M_g_sims realizations of g)
    R_e_sum = 0.0
    # Check if w or z are effectively zero to avoid issues or save computation
    w_is_zero = np.linalg.norm(w) < 1e-9
    z_is_zero = N <= 1 or np.linalg.norm(z) < 1e-9
    
    if w_is_zero: # If no signal beamformed, R_s is 0
        R_s = 0.0
    else:
        for _ in range(M_g_sims):
            g = generate_channel_vector(N) # Shape (N, 1)
            g_H = g.conj().T # Shape (1, N)
            
            signal_power_eve = np.abs(g_H @ w)**2 # Scalar
            
            if z_is_zero: # No artificial noise
                R_e_sum += np.log2(1 + signal_power_eve / sigma_n_sq_val)
            else: # With artificial noise
                noise_power_eve_an = np.abs(g_H @ z)**2 # Scalar
                total_noise_eve = noise_power_eve_an + sigma_n_sq_val
                R_e_sum += np.log2(1 + signal_power_eve / (total_noise_eve if total_noise_eve > 1e-9 else 1e-9))
        
        R_e = R_e_sum / M_g_sims if M_g_sims > 0 else 0.0
        R_s = np.maximum(0.0, R_b - R_e)

    event_rs_greater_R = 1 if R_s > R_thresh else 0
    return float(R_s), event_rs_greater_R 