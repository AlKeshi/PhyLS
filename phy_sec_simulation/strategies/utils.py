import numpy as np

def generate_channel_vector(N):
    """Generates a complex channel vector h ~ CN(0, 2I_N)."""
    real_part = np.random.normal(0, 1, (N, 1))
    imag_part = np.random.normal(0, 1, (N, 1))
    return (real_part + 1j * imag_part)

def db_to_linear(db_value):
    """Converts dB to linear scale."""
    return 10**(db_value / 10)

def snr_to_total_power(snr_db, noise_variance):
    """Calculates total power P from SNR in dB."""
    snr_linear = db_to_linear(snr_db) # Corrected: was using undefined db_value
    return snr_linear * noise_variance 