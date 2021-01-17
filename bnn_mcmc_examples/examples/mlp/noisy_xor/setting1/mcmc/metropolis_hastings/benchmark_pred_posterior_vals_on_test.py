# %% Load packages

import numpy as np

from eeyore.chains import ChainLists

from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.constants import dtype
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.mcmc.constants import num_chains, pred_iter_thres
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.mcmc.metropolis_hastings.constants import sampler_output_run_paths
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.model import model
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.mcmc.datascanners import test_dataloader

# %% Load chain lists

chain_lists = ChainLists.from_file(sampler_output_run_paths, keys=['sample'], dtype=dtype)

# %% Drop burn-in samples

for i in range(num_chains):
    chain_lists.vals['sample'][i] = chain_lists.vals['sample'][i][pred_iter_thres:]

# %% Compute and save predictive posteriors

pred_posterior = np.empty([num_chains, len(test_dataloader)])

verbose_msg = 'Evaluating predictive posterior based on chain {:' \
    + str(len(str(num_chains))) \
    + '} out of ' \
    + str(num_chains) \
    + ' at test point {:' \
    + str(len(str(len(test_dataloader)))) \
    + '} out of ' \
    + str(len(test_dataloader)) \
    + '...'

for k in range(num_chains):
    for i, (x, y) in enumerate(test_dataloader):
        print(verbose_msg.format(k+1, i+1))

        pred_posterior[k, i] = model.predictive_posterior(chain_lists.vals['sample'][k], x.squeeze(), y.squeeze(-1))

    np.savetxt(sampler_output_run_paths[k].joinpath('pred_posterior_on_test.csv'), pred_posterior[k], delimiter=',')