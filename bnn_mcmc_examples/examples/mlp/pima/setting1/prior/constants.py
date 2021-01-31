# %% Import packages

from bnn_mcmc_examples.examples.mlp.pima.setting1.constants import num_chains, output_path

# %% Define sampler-specific output directories

sampler_output_path = output_path.joinpath('prior')
sampler_output_run_paths = [
    sampler_output_path.joinpath('run'+str(i+1).zfill(len(str(num_chains)))) for i in range(num_chains)
]
