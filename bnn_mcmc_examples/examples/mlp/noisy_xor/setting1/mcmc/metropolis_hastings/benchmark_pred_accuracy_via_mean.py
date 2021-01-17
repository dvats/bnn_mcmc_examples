# %% Load packages

import numpy as np

from sklearn.metrics import accuracy_score

from eeyore.chains import ChainLists

from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.constants import dtype
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.mcmc.constants import diagnostic_iter_thres, num_chains
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.mcmc.metropolis_hastings.constants import (
    sampler_output_path, sampler_output_run_paths
)
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.model import model
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.mcmc.dataloaders import test_dataloader

# %% Load chain lists

chain_lists = ChainLists.from_file(sampler_output_run_paths, keys=['sample'], dtype=dtype)

# %% Drop burn-in samples

for i in range(num_chains):
    chain_lists.vals['sample'][i] = chain_lists.vals['sample'][i][diagnostic_iter_thres:]

# %% Load test data and labels

test_data, test_labels = next(iter(test_dataloader))

# %% Compute chain means

means = chain_lists.mean()

# %% Compute predictive accuracies

accuracies = np.empty(num_chains)

for i in range(num_chains):
    # Initialize model parameters
    model.set_params(means[i, :].clone().detach())

    # Compute test logits
    test_logits = model(test_data)

    # Make test predictions
    test_preds = test_logits.squeeze() > 0.5

    # Compute test accuracy
    accuracies[i] = accuracy_score(test_preds, test_labels.squeeze())

# %% Save predictive accuracies

np.savetxt(sampler_output_path.joinpath('accuracies_via_mean.txt'), accuracies)