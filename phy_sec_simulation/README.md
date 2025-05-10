# Physical Layer Security Simulation

This project implements and compares two strategies for enhancing outage probability and secrecy rate in physical layer security using artificial noise, as described in `description.md`.

## Project Structure

```
phy_sec_simulation/
├── main.py                     # Main script to run simulations and plot results
├── config.py                   # Contains common simulation parameters
├── strategies/                 # Package for strategy implementations and utilities
│   ├── __init__.py             # Makes strategies a package, exports functions
│   ├── constant_power.py       # Implements Strategy 1 (from description.md)
│   ├── variable_power.py       # Implements Strategy 1.2 (from description.md)
│   ├── strategy_2_constant_inst_power.py # Implements Strategy 2 (from description_2.md)
│   └── utils.py                # Contains helper functions (channel generation, etc.)
├── results/                    # Directory where plots are saved
├── requirements.txt            # Python package dependencies
└── README.md                   # Project description
```

## Implemented Strategies

1.  **Strategy 1 (Constant Power Allocation)**: Based on `description.md`. Uses fixed expected power allocation for beamforming and artificial noise. AN is orthogonal to Bob's channel.
2.  **Strategy 1.2 (Variable Power Allocation)**: Based on `description.md`. Similar to Strategy 1, but AN power is scaled by `1/|h|^2`.
3.  **Strategy 2 (Constant Instantaneous Power)**: Based on `description_2.md`. Configures beamforming and AN for constant instantaneous powers.

## Setup

1.  Ensure you have Python 3 installed.
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Simulation

Navigate to the `phy_sec_simulation` directory (if not already there) and run the main script from the parent directory of `phy_sec_simulation` or ensure `phy_sec_simulation` is in your PYTHONPATH.

If you are inside the `phy_sec_simulation` directory, you can run:
```bash
python main.py 
```
Alternatively, from the parent directory:
```bash
python phy_sec_simulation/main.py
```

The simulation will run, print progress to the console, and then display the plots comparing the implemented strategies. The plots will also be saved in the `results` directory.

## Parameters

Simulation parameters (number of antennas, alpha, SNR range, Monte Carlo iterations, etc.) can be modified in `config.py`.

 