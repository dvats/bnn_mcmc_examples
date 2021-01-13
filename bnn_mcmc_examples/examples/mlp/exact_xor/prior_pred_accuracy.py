# %% Load packages

import numpy as np
import torch

from sklearn.metrics import accuracy_score

from bnn_mcmc_examples.examples.mlp.exact_xor.constants import num_chains, output_path
from bnn_mcmc_examples.examples.mlp.exact_xor.dataloader import dataloader
from bnn_mcmc_examples.examples.mlp.exact_xor.model import model

# %% Load test data and labels

test_data, test_labels = next(iter(dataloader))

# %% Draw samples from the prior

prior_samples = torch.stack([model.prior.sample() for i in range(num_chains)])

# %% Compute predictive accuracies

accuracies = np.empty(num_chains)

for i in range(num_chains):
    # Initialize model parameters
    model.set_params(prior_samples[i, :].clone().detach())

    # Compute test logits
    test_logits = model(test_data)

    # Make test predictions
    test_preds = test_logits.squeeze() > 0.5

    # Compute test accuracy
    accuracies[i] = accuracy_score(test_preds, test_labels.squeeze())

# %% Save prior samples

np.savetxt(output_path.joinpath('prior_samples.csv'), prior_samples.detach().cpu().numpy(), delimiter=',')

# %% Save predictive accuracies

np.savetxt(output_path.joinpath('prior_accuracy.txt'), accuracies)