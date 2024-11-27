rule selective_deaths:
    output:
        outfile = 'results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.csv',
    params:
        ns = lambda wildcards: wildcards.ns,
        h = lambda wildcards: wildcards.h,
        n = lambda wildcards: wildcards.n,
        s = lambda wildcards: float(wildcards.ns) / float(wildcards.n),
        replicates_per_job = 20000
    resources:
        mem_mb = 8000,
        runtime = 10
    conda:
        '../envs/slim.yaml'
    shell:
        '''
        slim -d n={params.n} -d h={params.h} -d s={params.s} -d replicates={params.replicates_per_job} -d "output_file='{output.outfile}'" src/SLiM/replicating_simple_model.slim
        '''    


rule collect_results:
    input:
        files = expand('results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.csv', replicate=replicate,
                                                                                        n= lambda wildcards: wildcards.n,
                                                                                        ns= lambda wildcards: wildcards.ns, 
                                                                                        h= lambda wildcards: wildcards.h) 
    output:
        outfile = 'results/selected_deaths/summaries/popsize_{n}_ns_{ns}_dominance_{h}.csv'
    resources:
        mem_mb = 16000,
        runtime = 10
    script:
        "../src/scripts/combine_replicates.py"

#Snakemake -c 60 --sdm conda --rerun-incomplete  