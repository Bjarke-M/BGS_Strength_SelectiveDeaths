ns = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,
    0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.15,
    0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,
    0.8,0.85,0.9,0.95,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,
    7,7.5,8,8.5,9,9.5,10,20,30,40,50,60,70,80,90,100]
n = 1000

h = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
replicate = [i for i in range(20)] #20


include: 'rules/simple_model.smk'

#snakemake --executor slurm -j 10 --sdm conda --default-resources slurm_account=primatediversity
rule all:
    input:
        expand('results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.csv',n=n ,ns=ns, h=h, replicate=replicate),
        expand('results/selected_deaths/summaries/popsize_{n}_ns_{ns}_dominance_{h}.csv',n=n, ns=ns, h=h),
        'results/selected_deaths/summaries/mean_results.csv'

