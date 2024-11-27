# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Parameters
ns = [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009,
      0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
      0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9,
      10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
n = 1000
h_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

def create_plots(df, output_path, params):
    """Create and save distribution plots for a given dataframe"""
    
    # Create output directory structure: base_output/h_value/
    h_dir = os.path.join(output_path, f'h_{params["h"]}')
    os.makedirs(h_dir, exist_ok=True)
    
    # Set up the figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot 1: Distribution of log10(count)
    df['log10_count'] = np.log10(df['count'])
    ax1.hist(df['log10_count'], bins=50, edgecolor='k')
    ax1.set_xlabel('log10(count)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Distribution of log10(count)')
    
    # Plot 2: Distribution of log10(t)
    df['t'] = pd.to_numeric(df['t'], errors='coerce')
    df['log10_t'] = np.log10(df['t'])
    ax2.hist(df['log10_t'].dropna(), bins=50, edgecolor='k')
    ax2.set_xlabel('log10(t)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of log10(t)')
    
    # Plot 3: Distribution of log10(count*s*h)
    df['count_s_h'] = df['count'] * df['s'] * df['h']
    ax3.hist(np.log10(df['count_s_h']), bins=50, edgecolor='k')
    ax3.set_xlabel('log10(count * s * h)')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Distribution of count * s * h')
    
    # Add overall title with parameters
    plt.suptitle(f'Distributions for n={params["n"]}, ns={params["ns"]}, h={params["h"]}')
    
    # Adjust layout and save
    plt.tight_layout()
    filename = f'dist_n_{params["n"]}_ns_{params["ns"]}_h_{params["h"]}.png'
    plt.savefig(os.path.join(h_dir, filename))
    plt.close()

def process_all_files(base_path, output_path):
    """Process all CSV files for different parameter combinations"""
    
    results_path = Path(base_path)
    
    # Create main output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Track processing statistics
    total_files = 0
    processed_files = 0
    errors = 0
    
    # Process each combination of parameters
    for h_val in h_values:
        print(f"\nProcessing files for h = {h_val}")
        
        for ns_val in ns:
            # Construct filename
            filename = f'popsize_{n}_ns_{ns_val}_dominance_{h_val}.csv'
            file_path = results_path / filename
            
            total_files += 1
            
            # Check if file exists
            if file_path.exists():
                try:
                    # Read the CSV file
                    df = pd.read_csv(file_path)
                    
                    # Create plots
                    params = {'n': n, 'ns': ns_val, 'h': h_val}
                    create_plots(df, output_path, params)
                    
                    processed_files += 1
                    print(f'Processed: {filename}')
                except Exception as e:
                    errors += 1
                    print(f'Error processing {filename}: {str(e)}')
            else:
                print(f'File not found: {filename}')
    
    # Print summary
    print(f"\nProcessing Summary:")
    print(f"Total files expected: {total_files}")
    print(f"Files successfully processed: {processed_files}")
    print(f"Errors encountered: {errors}")
    print(f"Missing files: {total_files - processed_files - errors}")

# Main execution
if __name__ == "__main__":
    base_path = 'results/selected_deaths/summaries/'
    output_path = 'results/distribution_plots/'
    
    process_all_files(base_path, output_path)