import numpy as np
import matplotlib.pyplot as plt
import os

import config
# import strategies # Old import
from strategies import strategy_1, strategy_1_2, strategy_2_constant_inst_power, strategy_3_1, strategy_3_2, snr_to_total_power # New import

def run_simulation():
    avg_secrecy_rates_s1 = []
    outage_probs_s1 = [] 

    avg_secrecy_rates_s1_2 = []
    outage_probs_s1_2 = []

    avg_secrecy_rates_s2 = []
    outage_probs_s2 = []

    avg_secrecy_rates_s3_1 = []
    outage_probs_s3_1 = []

    avg_secrecy_rates_s3_2 = []
    outage_probs_s3_2 = []

    print("Starting simulation...")
    for snr_db in config.SNR_DB_RANGE:
        P = snr_to_total_power(snr_db, config.SIGMA_N_SQ) # Updated usage
        
        current_snr_secrecy_s1 = []
        current_snr_outage_events_s1 = []
        
        current_snr_secrecy_s1_2 = []
        current_snr_outage_events_s1_2 = []

        current_snr_secrecy_s2 = []
        current_snr_outage_events_s2 = []

        current_snr_secrecy_s3_1 = []
        current_snr_outage_events_s3_1 = []

        current_snr_secrecy_s3_2 = []
        current_snr_outage_events_s3_2 = []

        for i in range(config.M_MONTE_CARLO_H):
            # Strategy 1
            rs_s1, event_s1 = strategy_1( # Updated usage
                P, config.N_ANTENNAS, config.ALPHA_VAL, 
                config.SIGMA_N_SQ, config.M_MONTE_CARLO_G, config.R_THRESHOLD
            )
            current_snr_secrecy_s1.append(rs_s1)
            current_snr_outage_events_s1.append(event_s1)
            
            # Strategy 1.2
            rs_s1_2, event_s1_2 = strategy_1_2( # Updated usage
                P, config.N_ANTENNAS, config.ALPHA_VAL, 
                config.SIGMA_N_SQ, config.M_MONTE_CARLO_G, config.R_THRESHOLD
            )
            current_snr_secrecy_s1_2.append(rs_s1_2)
            current_snr_outage_events_s1_2.append(event_s1_2)

            # Strategy 2
            rs_s2, event_s2 = strategy_2_constant_inst_power(
                P, config.N_ANTENNAS, config.ALPHA_VAL, 
                config.SIGMA_N_SQ, config.M_MONTE_CARLO_G, config.R_THRESHOLD
            )
            current_snr_secrecy_s2.append(rs_s2)
            current_snr_outage_events_s2.append(event_s2)

            # Strategy 3.1
            rs_s3_1, event_s3_1 = strategy_3_1(
                P, config.N_ANTENNAS, config.ALPHA_VAL, 
                config.SIGMA_N_SQ, config.M_MONTE_CARLO_G, config.R_THRESHOLD
            )
            current_snr_secrecy_s3_1.append(rs_s3_1)
            current_snr_outage_events_s3_1.append(event_s3_1)

            # Strategy 3.2
            rs_s3_2, event_s3_2 = strategy_3_2(
                P, config.N_ANTENNAS, config.ALPHA_VAL, 
                config.SIGMA_N_SQ, config.M_MONTE_CARLO_G, config.R_THRESHOLD
            )
            current_snr_secrecy_s3_2.append(rs_s3_2)
            current_snr_outage_events_s3_2.append(event_s3_2)
            
            if (i + 1) % (config.M_MONTE_CARLO_H // 10) == 0: 
                 if config.M_MONTE_CARLO_H >= 10 : # Avoid division by zero if M_MONTE_CARLO_H < 10
                    print(f"  SNR: {snr_db} dB, Monte Carlo for h: {i+1}/{config.M_MONTE_CARLO_H}")
                 elif i == config.M_MONTE_CARLO_H -1: # Print at the end for small M_MONTE_CARLO_H
                    print(f"  SNR: {snr_db} dB, Monte Carlo for h: {i+1}/{config.M_MONTE_CARLO_H}")

        avg_secrecy_rates_s1.append(np.mean(current_snr_secrecy_s1 if current_snr_secrecy_s1 else [0]))
        outage_probs_s1.append(np.mean(current_snr_outage_events_s1 if current_snr_outage_events_s1 else [0]))
        
        avg_secrecy_rates_s1_2.append(np.mean(current_snr_secrecy_s1_2 if current_snr_secrecy_s1_2 else [0]))
        outage_probs_s1_2.append(np.mean(current_snr_outage_events_s1_2 if current_snr_outage_events_s1_2 else [0]))

        avg_secrecy_rates_s2.append(np.mean(current_snr_secrecy_s2 if current_snr_secrecy_s2 else [0]))
        outage_probs_s2.append(np.mean(current_snr_outage_events_s2 if current_snr_outage_events_s2 else [0]))

        avg_secrecy_rates_s3_1.append(np.mean(current_snr_secrecy_s3_1 if current_snr_secrecy_s3_1 else [0]))
        outage_probs_s3_1.append(np.mean(current_snr_outage_events_s3_1 if current_snr_outage_events_s3_1 else [0]))

        avg_secrecy_rates_s3_2.append(np.mean(current_snr_secrecy_s3_2 if current_snr_secrecy_s3_2 else [0]))
        outage_probs_s3_2.append(np.mean(current_snr_outage_events_s3_2 if current_snr_outage_events_s3_2 else [0]))

        print(f"SNR: {snr_db} dB processed. S1: Rs={avg_secrecy_rates_s1[-1]:.2f}, P(>R)={outage_probs_s1[-1]:.2f} | "
              f"S1.2: Rs={avg_secrecy_rates_s1_2[-1]:.2f}, P(>R)={outage_probs_s1_2[-1]:.2f} | "
              f"S2: Rs={avg_secrecy_rates_s2[-1]:.2f}, P(>R)={outage_probs_s2[-1]:.2f} | "
              f"S3.1: Rs={avg_secrecy_rates_s3_1[-1]:.2f}, P(>R)={outage_probs_s3_1[-1]:.2f} | "
              f"S3.2: Rs={avg_secrecy_rates_s3_2[-1]:.2f}, P(>R)={outage_probs_s3_2[-1]:.2f}")
    
    print("Simulation finished.")
    return (avg_secrecy_rates_s1, outage_probs_s1, 
            avg_secrecy_rates_s1_2, outage_probs_s1_2, 
            avg_secrecy_rates_s2, outage_probs_s2,
            avg_secrecy_rates_s3_1, outage_probs_s3_1,
            avg_secrecy_rates_s3_2, outage_probs_s3_2)

def plot_results(snr_db_range, 
                 avg_secrecy_s1, outage_s1, 
                 avg_secrecy_s1_2, outage_s1_2, 
                 avg_secrecy_s2, outage_s2,
                 avg_secrecy_s3_1, outage_s3_1,
                 avg_secrecy_s3_2, outage_s3_2):
    print("Plotting results...")
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.plot(snr_db_range, avg_secrecy_s1, marker='o', linestyle='-', label='Strategy 1')
    plt.plot(snr_db_range, avg_secrecy_s1_2, marker='x', linestyle='--', label='Strategy 1.2')
    plt.plot(snr_db_range, avg_secrecy_s2, marker='s', linestyle=':', label='Strategy 2')
    plt.plot(snr_db_range, avg_secrecy_s3_1, marker='^', linestyle='-.', label='Strategy 3.1')
    plt.plot(snr_db_range, avg_secrecy_s3_2, marker='d', linestyle='-', label='Strategy 3.2') # Consider a different linestyle if overlapping with S1
    plt.title(f'Average Secrecy Rate (N={config.N_ANTENNAS}, alpha={config.ALPHA_VAL})')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Average Secrecy Rate (bits/s/Hz)')
    plt.grid(True)
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(snr_db_range, outage_s1, marker='o', linestyle='-', label='Strategy 1')
    plt.plot(snr_db_range, outage_s1_2, marker='x', linestyle='--', label='Strategy 1.2')
    plt.plot(snr_db_range, outage_s2, marker='s', linestyle=':', label='Strategy 2')
    plt.plot(snr_db_range, outage_s3_1, marker='^', linestyle='-.', label='Strategy 3.1')
    plt.plot(snr_db_range, outage_s3_2, marker='d', linestyle='-', label='Strategy 3.2') # Consider a different linestyle
    plt.title(f'P(Rs > R={config.R_THRESHOLD}) (N={config.N_ANTENNAS}, alpha={config.ALPHA_VAL})')
    plt.xlabel('SNR (dB)')
    plt.ylabel(f'P(Rs > R={config.R_THRESHOLD})') 
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    plot_filename = os.path.join(results_dir, f'comparison_N{config.N_ANTENNAS}_alpha{config.ALPHA_VAL}_M{config.M_MONTE_CARLO_H}.png')
    plt.savefig(plot_filename)
    print(f"Plot saved to {plot_filename}")
    plt.show()

if __name__ == "__main__":
    s1_rs, s1_out, \
    s1_2_rs, s1_2_out, \
    s2_rs, s2_out, \
    s3_1_rs, s3_1_out, \
    s3_2_rs, s3_2_out = run_simulation()
    
    plot_results(
        config.SNR_DB_RANGE, 
        s1_rs, s1_out, 
        s1_2_rs, s1_2_out,
        s2_rs, s2_out,
        s3_1_rs, s3_1_out,
        s3_2_rs, s3_2_out
    ) 