rule selective_deaths:
    output:
        outfile = 'results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.csv',
        logfile = 'results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.log'
    params:
        ns = lambda wildcards: wildcards.ns,
        h = lambda wildcards: wildcards.h,
        n = lambda wildcards: wildcards.n,
        s = lambda wildcards: float(wildcards.ns) / float(wildcards.n)
    resources:
        mem_mb = 100,
        runtime = 10
    conda:
        '../envs/slim.yaml'
    shell:
        '''
        slim -d n={params.n} -d h={params.h} -d s={params.s} -d "outfile='{output.outfile}'" -d "logfile='{output.logfile}'" src/SLiM/simple_model.slim
        '''    


# replicate = [i for i in range(10000)]
rule collect_results:
    input:
        files = expand('results/selected_deaths/{n}/{ns}/{h}/replicate.{replicate}.csv', replicate=replicate,
                                                                                        n= lambda wildcards: wildcards.n,
                                                                                        ns= lambda wildcards: wildcards.ns, 
                                                                                        h= lambda wildcards: wildcards.h) ## fix this 
    output:
        outfile = 'results/selected_deaths/summaries/popsize_{n}_ns_{ns}_dominance_{h}.csv'
    resources:
        mem_mb = 16000,
        runtime = 10
    script:
        "../src/scripts/combine_replicates.py"