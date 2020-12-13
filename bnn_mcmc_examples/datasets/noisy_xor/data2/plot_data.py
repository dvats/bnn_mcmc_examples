# %% Import packages

import matplotlib.pyplot as plt
import numpy as np
import torch

from bnn_mcmc_examples.datasets.noisy_xor.data1.constants import num_classes, num_samples, output_path
from bnn_mcmc_examples.datasets.noisy_xor.data1.load_data import load_data

# %% Load data

noisy_xor, _ = load_data(dtype=torch.float32)

# %% Create output directory if it does not exist

output_path.mkdir(parents=True, exist_ok=True)

# %% Plot noisy XOR points

num_samples_cumsum = np.hstack((0, num_samples)).cumsum()

# print(plt.rcParams['axes.prop_cycle'].by_key()['color'])
cols = ['#1f77b4', '#ff7f0e', '#d62728', '#e377c2']

labels = ['(0, 0)', '(0, 1)', '(1, 0)', '(1, 1)']

plt.figure(figsize=[6.4, 6.4])

plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12

fig, ax = plt.subplots()

ax.set_box_aspect(1)

for i in range(num_classes):
    ax.plot(
        noisy_xor.x[num_samples_cumsum[i]:num_samples_cumsum[i+1], 0],
        noisy_xor.x[num_samples_cumsum[i]:num_samples_cumsum[i+1], 1],
        'o',
        color=cols[i],
        marker='o',
        markersize=3,
        label=str(i)
    )

plt.legend(labels=labels, loc='right', ncol=1, bbox_to_anchor=(1.4, 0.5), fancybox=True, shadow=True)

plt.savefig(
    output_path.joinpath('noisy_xor.jpg'),
    pil_kwargs={'quality': 100},
    transparent=True,
    bbox_inches='tight',
    pad_inches=0.1
)
