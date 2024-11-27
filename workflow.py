from gwf import Workflow
import itertools

gwf = Workflow()

ns = [0,0.001,0.005,0.01,0.05,0.1,0.5,1,5,10, 50, 100]
n = [1000]
h = [0.5]
replicate = [i for i in range(20)]

batch_size = 10

paramter_space = itertools.product(ns, replicate, n, h)

print(list(paramter_space))

for batch_id, smaller_space in enumerate(itertools.batched(paramter_space, batch_size)):
    cmds = []
    outputs = []
    for ns, replicate, n, h in smaller_space:
        outfile = f"sim_{n}_{h}_{ns}_{replicate}.csv"
        logfile = f"sim_{n}_{h}_{ns}_{replicate}.log"
        outputs.append(outfile)
        outputs.append(logfile)
        cmds.append(f"slim -d n={n} -d h={h} -d s={ns} -d 'outfile={outfile}' -d 'logfile={logfile}' src/SLiM/simple_model.slim")
    spec = "\n".join(cmds)

    gwf.target(
        name=f"sim_{batch_id}",
        inputs=[],
        outputs=outputs,
        cores=1,
        memory="4g",
        walltime="00:10:00",
    ) << spec

