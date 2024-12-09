import pandas as pd
import numpy as np

files = snakemake.input.files
outfile = snakemake.output.outfile

# Read all CSV files into a single dataframe
dfs = []
# Loop through file paths and read each CSV into a dataframe
for file_path in files:
    dfs.append(pd.read_csv(file_path))
combined_df = pd.concat(dfs, ignore_index=True)

# #get mean of s*count*h for each file
# # convert s, h, and count to numeric
combined_df['s'] = pd.to_numeric(combined_df['s'], errors='coerce')
combined_df['h'] = pd.to_numeric(combined_df['h'], errors='coerce')
combined_df['count'] = pd.to_numeric(combined_df['count'], errors='coerce')
combined_df['n_het']= pd.to_numeric(combined_df['n_het'], errors='coerce')
combined_df['n_homo']= pd.to_numeric(combined_df['n_homo'], errors='coerce')
combined_df['t'] = pd.to_numeric(combined_df['t'], errors='coerce')
# # calculate s*count*h and log10(s*count*h)
combined_df['count_s_h'] = combined_df['count'] * combined_df['s'] * combined_df['h']
combined_df['log10_count_s_h'] = np.log10(combined_df['count_s_h'])
# # output mean of s*count*h for each file in one dataframe, with columns for n, ns, h, and mean of s*count*h
df_group = combined_df.groupby(['n', 's', 'h'])

mean_count_s_h = df_group['count_s_h'].mean().reset_index(name='mean_count_s_h')
mean_t = df_group['t'].mean().reset_index(name='mean_t')
mean_count = df_group['count'].mean().reset_index(name='mean_count')
mean_n_het = df_group['n_het'].mean().reset_index(name='mean_n_het')
mean_n_homo = df_group['n_homo'].mean().reset_index(name='mean_n_homo')

df_group_mean = pd.merge(mean_count_s_h, mean_t, on=['n', 's', 'h'])
df_group_mean = pd.merge(df_group_mean, mean_count, on=['n', 's', 'h'])
df_group_mean = pd.merge(df_group_mean, mean_n_het, on=['n', 's', 'h'])
df_group_mean = pd.merge(df_group_mean, mean_n_homo, on=['n', 's', 'h'])

df_group_mean.to_csv(outfile)


