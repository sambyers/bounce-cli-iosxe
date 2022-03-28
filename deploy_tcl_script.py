from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import  netmiko_file_transfer
from nornir_scrapli.tasks import send_configs


def main() -> None:
    # Configuration and commands
    alias_cfg = [
        'alias exec bounce tclsh bounce.tcl'
    ]

    # Initialize Nornir
    nr = InitNornir(config_file='config.yaml')

    # Copy script file to device flash
    script_file_result = nr.run(
        task=netmiko_file_transfer,
        source_file='bounce_en.tcl',
        dest_file='bounce.tcl',
        overwrite_file=True,
        name='Copy bounce.tcl script to network device.'
    )
    print_result(script_file_result)
'''
    # Create alias for bounce
    alias_result = nr.run(
        task=send_configs,
        configs=alias_cfg,
        name='Create CLI alias.'
    )
    print_result(alias_result)
'''
if __name__ == '__main__':
    main()