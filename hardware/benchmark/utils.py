"""
Benchmark utility functions.
"""

import subprocess


def get_value(hw_lst, level1, level2, level3):
    """Get an specific value from the hardware inventory."""
    for entry in hw_lst:
        if level1 == entry[0] and level2 == entry[1] and level3 == entry[2]:
            return entry[3]
    return None


def get_one_cpu_per_socket(hw_lst):
    """Return a list of physical CPU ids."""
    logical = get_value(hw_lst, 'cpu', 'logical', 'number')
    current_phys_package_id = -1
    cpu_list = []
    for processor_num in range(int(logical)):
        cmdline = ("cat /sys/devices/system/cpu/cpu%d/topology"
                   "/physical_package_id" % int(processor_num))
        phys_cmd = subprocess.Popen(cmdline,
                                    shell=True, stdout=subprocess.PIPE)
        for phys_str in phys_cmd.stdout:
            phys_id = int(phys_str.strip())
            if phys_id > current_phys_package_id:
                current_phys_package_id = phys_id
                cpu_list.append(current_phys_package_id)
    return cpu_list
