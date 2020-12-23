# %% Import packages

from torch.optim import SGD

from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.constants import num_optim_epochs
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.dataloaders import training_dataloader
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.gradient_descent.optimizer import lr, momentum
# from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.gradient_descent.optimizer import loss_fn, lr, momentum
from bnn_mcmc_examples.examples.mlp.noisy_xor.setting1.model import model
from bnn_mcmc_examples.optim import train

# %% Setup SGD optimizer

optimizer = SGD(model.parameters(), lr=lr, momentum=momentum)

# %% Train model

loss_vals = train(model, training_dataloader, optimizer, num_epochs=num_optim_epochs, save_loss=True)
# loss_vals = train(model, dataloader, optimizer, num_epochs=num_optim_epochs, loss_fn=loss_fn, save_loss=True)
