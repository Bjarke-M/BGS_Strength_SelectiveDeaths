# ns = [0,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,
#     0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,
#     0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1, 
#     10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
ns = [0,0.001,0.005,0.01,0.05,0.1,0.5,1,10, 50, 100]
n = 1000
#h = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
# ns = 0.01
# n = 1000
h = 0.5
replicate = [i for i in range(20000)]


include: 'rules/simple_model.smk'

#snakemake --executor slurm -j 10 --groups selective_deaths=group0 --group-components group0=10 --use-conda --default-resources slurm_account=primatediversity
rule all:
    input:
        expand('results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.csv',n=n ,ns=ns, h=h, replicate=replicate),
        expand('results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.log',n=n, ns=ns, h=h, replicate=replicate),
        expand('results/selected_deaths/summaries/popsize_{n}_ns_{ns}_dominance_{h}.csv',n=n, ns=ns, h=h)

