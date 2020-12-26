from datetime import timedelta
from pathlib import Path
from timeit import default_timer as timer

from .train import train

def set_verbose_benchmark_msg(self, num_solutions):
    return 'Simulating solution {:' \
        + str(len(str(num_solutions))) \
        + '} out of ' \
        + str(num_solutions) \
        + ' ({:' \
        + str(len(str(num_solutions))) \
        + '} failures due to not meeting conditions and {:' \
        + str(len(str(num_solutions))) \
        + '} failures due to runtime error)...'

def benchmark(
    model,
    training_loader,
    optimizer,
    num_solutions,
    num_epochs,
    path,
    loss_fn=None,
    validation_loader=None,
    pred_fn=None,
    metric_fn=None,
    check_fn=None,
    verbose=False,
    verbose_step=100,
    print_runtime=True
):
    if (validation_loader is not None):
        validation_output, validation_target = next(iter(validation_loader))

    if verbose:
        verbose_msg = set_verbose_benchmark_msg(num_solutions)

    i, j, k = 0, 0, 0

    while i < num_solutions:
        if verbose:
            print(verbose_msg.format(i+1, j, k))

        output_filenames = ['solutions.csv', 'runtimes.txt']
        if validation_loader is not None:
            output_filenames.append('metric_vals.txt')

        for filename in output_filenames:
            Path(path).joinpath(filename).unlink(missing_ok=True)
            Path(path).joinpath(filename).touch()

        try:
            model.set_params(model.prior.sample())

            start_time = timer()
            train(
                model,
                training_loader,
                optimizer,
                num_epochs,
                loss_fn=loss_fn,
                monitor_step=None,
                save_loss=False,
                save_metric=False,
                save_metric_mean=False,
                pred_fn=None,
                metric_fn=None
            )
            end_time = timer()
            runtime = end_time - start_time

            if (validation_loader is not None):
                metric_val = metric_fn(pred_fn(validation_output), validation_target)
                accept = True if check_fn(metric_val) else False
            else:
                accept = True

            if accept:
                with open(Path(path).joinpath('solutions.csv'), 'a') as file:
                    file.write("{}\n".format(model.get_params().cpu().detach().numpy()))

                with open(Path(path).joinpath('runtime.txt'), 'a') as file:
                    file.write("{}\n".format(runtime))

                if (validation_loader is not None):
                    with open(Path(path).joinpath('metric_vals.txt'), 'a') as file:
                        file.write("{}\n".format(metric_val))

                i = i + 1

                if verbose:
                    print('Succeeded', end='')
            else:
                j = j + 1

                if verbose:
                    print('Failed due to not meeting quality metric', end='')

            if verbose:
                if print_runtime:
                    print('; runtime = {}'.format(timedelta(seconds=runtime)), end='')
                print('\n')
        except RuntimeError as error:
            with open(Path(path).joinpath('errors', 'error'+str(k+1).zfill(num_solutions)), 'w') as file:
                file.write("{}\n".format(error))

            k = k + 1

            if verbose:
                print('Failed due to runtime error\n')

    with open(Path(path).joinpath('run_counts.txt'), 'w') as file:
        file.write("{},succesful\n".format(i))
        file.write("{},unmet_conditions\n".format(j))
        file.write("{},runtime_errors\n".format(k))
