import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from pathlib import Path
   # Add this near the imports

# Add the phy_sec_simulation directory to the Python path if needed
script_dir = Path(__file__).parent
phy_sec_dir = script_dir / "phy_sec_simulation"
if phy_sec_dir.exists() and str(phy_sec_dir) not in sys.path:
    sys.path.append(str(phy_sec_dir))

# Import the phy_sec_simulation modules
import phy_sec_simulation.config as default_config
from phy_sec_simulation.strategies import (
    strategy_1, strategy_1_2, strategy_2_constant_inst_power,
    strategy_3_1, strategy_3_2, snr_to_total_power
)

# Define the strategy map similar to what we added to main.py
STRATEGIES = {
    "S1 (Const Power)": {"func": strategy_1, "marker": 'o', "linestyle": '-'},
    "S1.2 (Var Power)": {"func": strategy_1_2, "marker": 'x', "linestyle": '--'},
    "S2 (Const Inst Power)": {"func": strategy_2_constant_inst_power, "marker": 's', "linestyle": ':'},
    "S3.1": {"func": strategy_3_1, "marker": '^', "linestyle": '-.'},
    "S3.2": {"func": strategy_3_2, "marker": 'd', "linestyle": '-'}
}

# Set page config
st.set_page_config(
    page_title="Physical Layer Security Simulator",
    page_icon="📡",
    layout="wide"
)

# Title and description
st.title("📡 Physical Layer Security Strategy Simulator")
st.markdown("""
This dashboard allows you to run and compare different physical layer security strategies 
with customizable parameters. Select which strategies to run and adjust parameters as needed.
""")

# Create two columns for the layout
col1, col2 = st.columns([1, 3])

# Sidebar for strategy selection and parameters
with col1:
    st.header("Simulation Parameters")
    
    # Strategy selection
    st.subheader("Strategies")
    selected_strategies = {}
    for strategy_name in STRATEGIES:
        selected_strategies[strategy_name] = st.checkbox(strategy_name, value=strategy_name in ["S1 (Const Power)", "S3.2"])
    
    strategies_to_run = [name for name, selected in selected_strategies.items() if selected]
    
    if not strategies_to_run:
        st.warning("Please select at least one strategy.")
    
    # Parameter adjustments
    st.subheader("Parameters")
    
    # SNR Range
    st.write("**SNR Range (dB)**")
    snr_min = st.number_input("Min SNR", value=float(min(default_config.SNR_DB_RANGE)), step=1.0)
    snr_max = st.number_input("Max SNR", value=float(max(default_config.SNR_DB_RANGE)), step=1.0)
    snr_step = st.number_input("Step", value=1.0, min_value=0.1, step=0.1)
    
    # Calculate the SNR range
    SNR_DB_RANGE = np.arange(snr_min, snr_max + snr_step, snr_step)
    
    # Other parameters
    N_ANTENNAS = st.number_input("Number of Antennas (N)", 
                               value=default_config.N_ANTENNAS, 
                               min_value=1, 
                               max_value=100,
                               step=1)
    
    ALPHA_VAL = st.slider("Power Allocation Factor (α)", 
                        min_value=0.0, 
                        max_value=1.0, 
                        value=default_config.ALPHA_VAL,
                        step=0.05)
    
    SIGMA_N_SQ = st.number_input("Noise Variance (σ²)", 
                              value=default_config.SIGMA_N_SQ,
                              min_value=0.01,
                              step=0.1,
                              format="%.2f")
    
    R_THRESHOLD = st.number_input("Rate Threshold (R_th)", 
                                value=float(default_config.R_THRESHOLD),
                                min_value=0.0,
                                step=0.1,
                                format="%.1f")
    
    # Monte Carlo simulations
    st.subheader("Monte Carlo Settings")
    
    M_MONTE_CARLO_H = st.number_input("Bob's Channel Simulations", 
                                    value=default_config.M_MONTE_CARLO_H,
                                    min_value=10,
                                    max_value=10000,
                                    step=10)
    
    M_MONTE_CARLO_G = st.number_input("Eve's Channel Simulations", 
                                    value=default_config.M_MONTE_CARLO_G,
                                    min_value=10,
                                    max_value=10000,
                                    step=10)
    
    # Plot settings
    st.subheader("Plot Settings")
    use_semilogy = st.checkbox("Use Semi-log Y-axis (log scale)", value=False)
    show_legend = st.checkbox("Show Legend", value=True)
    
    # Run button
    run_simulation = st.button("Run Simulation", type="primary")


# Function to run simulation (adapted from the refactored main.py)
def run_security_simulation(selected_strategies_names, config_params):
    """Runs simulation for selected strategies with given parameters"""
    results = {name: {'secrecy_rates': [], 'outage_probs': []} for name in selected_strategies_names}
    
    progress_bar = st.progress(0.0)
    status_text = st.empty()
    
    snr_count = len(config_params["SNR_DB_RANGE"])
    
    for i, snr_db in enumerate(config_params["SNR_DB_RANGE"]):
        status_text.text(f"Processing SNR: {snr_db} dB ({i+1}/{snr_count})")
        P = snr_to_total_power(snr_db, config_params["SIGMA_N_SQ"])
        
        # Current SNR results for each strategy
        current_snr_results = {name: {'secrecy': [], 'outage': []} for name in selected_strategies_names}
        
        for mc_iter in range(config_params["M_MONTE_CARLO_H"]):
            for name in selected_strategies_names:
                if name not in STRATEGIES:
                    continue
                
                strategy_func = STRATEGIES[name]["func"]
                
                rs, event_rs_gt_Rthresh = strategy_func(
                    P, 
                    config_params["N_ANTENNAS"], 
                    config_params["ALPHA_VAL"],
                    config_params["SIGMA_N_SQ"], 
                    config_params["M_MONTE_CARLO_G"], 
                    config_params["R_THRESHOLD"]
                )
                current_snr_results[name]['secrecy'].append(rs)
                current_snr_results[name]['outage'].append(event_rs_gt_Rthresh)
        
        # Average results for the current SNR
        for name in selected_strategies_names:
            if name in STRATEGIES:
                avg_rs = np.mean(current_snr_results[name]['secrecy'] if current_snr_results[name]['secrecy'] else [0])
                avg_outage_prob = np.mean(current_snr_results[name]['outage'] if current_snr_results[name]['outage'] else [0])
                
                results[name]['secrecy_rates'].append(avg_rs)
                results[name]['outage_probs'].append(avg_outage_prob)
        
        # Update progress bar
        progress_bar.progress((i + 1) / snr_count)
    
    status_text.text("Simulation completed!")
    return results


# Display area for plots
with col2:
    if run_simulation and strategies_to_run:
        st.header("Simulation Results")
        
        with st.spinner("Running simulation, please wait..."):
            # Create config params dictionary
            config_params = {
                "SNR_DB_RANGE": SNR_DB_RANGE,
                "N_ANTENNAS": N_ANTENNAS,
                "ALPHA_VAL": ALPHA_VAL,
                "SIGMA_N_SQ": SIGMA_N_SQ,
                "R_THRESHOLD": R_THRESHOLD,
                "M_MONTE_CARLO_H": M_MONTE_CARLO_H,
                "M_MONTE_CARLO_G": M_MONTE_CARLO_G
            }
            
            # Run simulation
            simulation_results = run_security_simulation(strategies_to_run, config_params)
        
        # Create tabs for different plot types
        plot_tab1, plot_tab2, data_tab = st.tabs(["Secrecy Rate", "P(Rs > R_th)", "Raw Data"])
        
        with plot_tab1:
            # Secrecy Rate Plot
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            
            for name in strategies_to_run:
                if name in simulation_results:
                    style = STRATEGIES[name]
                    data_to_plot = simulation_results[name]['secrecy_rates']
                    
                    if use_semilogy:
                        ax1.semilogy(SNR_DB_RANGE, data_to_plot, marker=style["marker"], 
                                   linestyle=style["linestyle"], label=name)
                    else:
                        ax1.plot(SNR_DB_RANGE, data_to_plot, marker=style["marker"], 
                               linestyle=style["linestyle"], label=name)
            
            ax1.set_xlabel('SNR (dB)')
            ax1.set_ylabel('Average Secrecy Rate (bits/s/Hz)')
            ax1.set_title(f'Average Secrecy Rate (N={N_ANTENNAS}, α={ALPHA_VAL})')
            ax1.grid(True, which="both" if use_semilogy else "major")
            
            if show_legend:
                ax1.legend()
            
            st.pyplot(fig1)
        
        with plot_tab2:
            # Outage Probability Plot
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            
            for name in strategies_to_run:
                if name in simulation_results:
                    style = STRATEGIES[name]
                    data_to_plot = simulation_results[name]['outage_probs']
                    
                    if use_semilogy:
                        ax2.semilogy(SNR_DB_RANGE, data_to_plot, marker=style["marker"], 
                                   linestyle=style["linestyle"], label=name)
                    else:
                        ax2.plot(SNR_DB_RANGE, data_to_plot, marker=style["marker"], 
                               linestyle=style["linestyle"], label=name)
            
            ax2.set_xlabel('SNR (dB)')
            ax2.set_ylabel(f'P(Rs > R_th={R_THRESHOLD})')
            ax2.set_title(f'P(Rs > R_th={R_THRESHOLD}) (N={N_ANTENNAS}, α={ALPHA_VAL})')
            ax2.grid(True, which="both" if use_semilogy else "major")
            
            if not use_semilogy:
                ax2.set_ylim(bottom=0, top=max(1.0, ax2.get_ylim()[1]))
                
            if show_legend:
                ax2.legend()
            
            st.pyplot(fig2)
        
        with data_tab:
            # Display raw data in table format
            st.subheader("Simulation Data")
            
            # Create DataFrame for display
            import pandas as pd
            
            data_rows = []
            for snr_idx, snr in enumerate(SNR_DB_RANGE):
                for name in strategies_to_run:
                    if name in simulation_results:
                        data_rows.append({
                            "Strategy": name,
                            "SNR (dB)": snr,
                            "Secrecy Rate": simulation_results[name]['secrecy_rates'][snr_idx],
                            "P(Rs > R_th)": simulation_results[name]['outage_probs'][snr_idx]
                        })
            
            df = pd.DataFrame(data_rows)
            st.dataframe(df)
            
            # Add download button for the data
            csv = df.to_csv(index=False)
            param_str = f"N{N_ANTENNAS}_alpha{ALPHA_VAL}_R{R_THRESHOLD}"
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name=f"phy_sec_sim_results_{param_str}.csv",
                mime="text/csv",
            )
    
    elif not strategies_to_run and run_simulation:
        st.error("Please select at least one strategy before running the simulation.")
    
    else:
        st.info("Select parameters and strategies on the left, then click 'Run Simulation' to start.")
        
        # Display some information about the strategies
        st.subheader("Available Strategies")
        
        st.markdown("""
        - **S1 (Const Power)**: Strategy 1 with constant power allocation
        - **S1.2 (Var Power)**: Strategy 1.2 with variable power allocation
        - **S2 (Const Inst Power)**: Strategy 2 with constant instantaneous power
        - **S3.1**: Strategy 3.1 
        - **S3.2**: Strategy 3.2
        
        Use the checkboxes on the left to select which strategies you want to compare.
        """) 