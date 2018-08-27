import click

file = open('ccd_base_config.txt', 'w')

@click.command()
@click.option('--directory', type=str, help='directory which images are saved in')
@click.option('--hosts', type=str, help='tuple of hosts')
def config_cli(directory, hosts):
    file.write(directory + '\n')
    file.write(hosts)
    file.close()


def config(directory, hosts):
    file = open('ccd_base_config.txt', 'w')
    file.write(directory + '\n')
    file.write(hosts)
    file.close()
