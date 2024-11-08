import pandas as pd 

outfile = snakemake.output[0]
input_files = list(snakemake.input)
# Initialize an empty list to store dataframes
dfs = []
# Loop through file paths and read each CSV into a dataframe
for file_path in input_files:
    dfs.append(pd.read_csv(file_path))

# Combine all dataframes into a single dataframe
combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv(outfile, index=False)