from time import sleep
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import  netmiko_file_transfer
from nornir_scrapli.tasks import send_commands, send_configs, send_interactive


def put_script_file(task: Task, actions: dict) -> Result:
    task.run(
        task=send_commands,
        commands=actions['del_script_exec'],
        name='Delete previous script.'
    )
    task.run(
        task=netmiko_file_transfer,
        source_file='bounce.py',
        dest_file='bounce.py',
        overwrite_file=True,
        name='Copy script to network device.'
    )
    task.run(
        task=send_interactive,
        interact_events=actions['copy_interact'],
        name='Copy script to guest-share directory.'
    )
    task.run(
        task=send_commands,
        commands=actions['del_root_script_exec'],
        name='Delete script from root directory on flash.'
    )
    return Result(host=task.host,
        result='Successfully copied script file to device.'
    )

def main():
    # Configuration and commands
    guestshell_cfg = [
        'iox',
        'app-hosting appid guestshell',
        'app-vnic management guest-interface 0'
    ]

    guestshell_exec = [
        'guestshell enable',
        'guestshell run python3 -V'
    ]

    script_file_actions = {
        'copy_interact': [
            ('copy flash: flash:', 'Source filename []?', False),
            ('bounce.py', 'Destination filename [bounce.py]?', False),
            ('guest-share/bounce.py', '#', False)
        ],
        'del_script_exec': [
            'delete /force flash:guest-share/bounce.py',
            'delete /force flash:bounce.py'
        ],
        'del_root_script_exec': [
            'delete /force flash:bounce.py'
        ]
    }

    alias_cfg = [
        'alias exec bounce guestshell run python3 /flash/guest-share/bounce.py'
    ]

    # Initialize Nornir
    nr = InitNornir(config_file='config.yaml')

    # Configure iox and app hosting for guestshell
    guestshell_config_results = nr.run(
        task=send_configs,
        configs=guestshell_cfg,
        name='Configure IOx and app hosting.',
        stop_on_failed=True
        )
    print_result(guestshell_config_results)

    # Sleep because it can take 2 minutes for IOx to start
    # https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/175/b_175_programmability_cg/m_175_prog_guestshell.html
    sleep(120)

    # Enable guestshell
    guestshell_enable_results = nr.run(
        task=send_commands,
        commands=guestshell_exec,
        name='Enable guestshell.',
        stop_on_failed=True
    )
    print_result(guestshell_enable_results)

    # Copy script file to device flash
    script_file_result = nr.run(
        task=put_script_file,
        actions=script_file_actions,
        name='Copy script file to device.'
    )
    print_result(script_file_result)

    # Create alias for bounce
    alias_result = nr.run(
        task=send_configs,
        configs=alias_cfg,
        name='Create CLI alias.'
    )
    print_result(alias_result)

if __name__ == '__main__':
    main()