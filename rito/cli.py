import click

@click.command()
@click.option('--slack', default=None, help='Slack channels to message, comma-separated without spaces')
@click.argument('message')
def cli(slack, message):
    # Make a matrix of Rito modules to the list of recipients they should send to
    message_matrix = {}
    
    if slack != None:
        from . import slack as slack_module
        slack_channels_to_message=slack.split(",")
        message_matrix[slack_module] = slack_channels_to_message

    if len(message_matrix) == 0:
        print("Your rito command wouldn't send any messages. Check your arguments")
        exit(1)
    
    for module, recipients in message_matrix.items():
        for recipient in recipients:
            module.send_message(recipient, message)