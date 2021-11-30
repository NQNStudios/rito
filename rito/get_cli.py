import click
import pkgutil
import importlib
import os
import sys
import time

def receiver_options(function):
    receivers_module_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'receivers')
    receiver_names = [module_info.name for module_info in pkgutil.iter_modules([receivers_module_path])]
    for receiver in receiver_names:
        function = click.option(f'--{receiver}', default=None, help=f'{receiver} sources to check, comma-separated without spaces')(function)
    return function

@click.command()
@receiver_options
@click.option('--timeout', required=True, default=None, help='number of seconds to keep waiting for a message')
@click.argument('pattern')
def get_cli(pattern, **kwargs):
    # Make a matrix of Rito receiver modules to the list of sources they should receive from
    message_matrix = {}
    
    timeout = None
    for receiver_arg, source_arg in kwargs.items():
        if receiver_arg == 'timeout':
            timeout = int(source_arg)
            continue
        if source_arg == None:
            continue
        receiver_module = importlib.import_module(f'rito.receivers.{receiver_arg}')
        sources=source_arg.split(",")
        message_matrix[receiver_module] = sources

    if len(message_matrix) == 0:
        print("Your rito-get command wouldn't receive any messages. Check your arguments")
        exit(1)
    
    # Manage the timeout/retry loop for receivers
    for t in range(timeout):
        for module, sources in message_matrix.items():
            if t % module.check_interval == 0:
                for source in sources:
                    m = module.get_message(source, pattern, timeout)
                    if m != None and len(m) > 0:
                        print(m)
                        sys.exit(0)
        time.sleep(1)
    sys.stderr.write(f"rito-get timeout after {timeout}.{os.linesep}")
    sys.exit(1)