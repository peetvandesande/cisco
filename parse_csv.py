#!/usr/bin/env python3
""" This script parses a CSV file and produces a Cisco config file.

This file parses a UTF8 encoded and signed CSV file containing interface
information and produces Cisco configuration for these interfaces.

At the moment it only produces Nexus compatible output.

--

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Peet van de Sande"
__contact__ = "pvandesande@tmhcc.com"
__license__ = "GPLv3"

import argparse
import csv

def main():
    # Read input arguments
    argp = argparse.ArgumentParser(description = 'Create Cisco config files based on CSV input.')
    argp.add_argument('infile', type=str, nargs=1, help='UTF8 encoded input CSV file')
    argp.add_argument('outfile', type=str, nargs=1, help='Output text file')
    args = argp.parse_args()

    # Clean library of interfaces
    interfaces = {}

    # Open infile
    with open(args.infile[0], 'r', encoding='utf-8-sig') as data_file:
        csv_reader = csv.DictReader(data_file)

        for line in csv_reader:
            name = line['interface'].lower()
            interfaces[name] = []
            description  = 'description'
            description += ' ' + ('l3' if line['ip address'] else 'l2')
            description += '|' + (line['usage'].lower() if line['usage'] else '-')
            description += '|' + (line['isp'].lower() if line['isp'] else '-')
            description += '|' + (line['circuit id'].lower() if line['circuit id'] else '-')
            description += '|' + (line['remote device'].lower() if line['remote device'] else '-')
            description += '|' + (line['remote interface'].lower() if line['remote interface'] else '-')
            description += '|' + (line['comment'].lower() if line['comment'] else '-')
            interfaces[name].append(description)
            if line['switchport mode']:
                interfaces[name].append('switchport mode ' + line['switchport mode'])
            if line['switchport access vlan']:
                interfaces[name].append('switchport access vlan ' + line['switchport access vlan'])
            if line['switchport trunk allowed vlan']:
                interfaces[name].append('switchport trunk allowed vlan ' + line['switchport trunk allowed vlan'])
            if line['channel-group']:
                interfaces[name].append('channel-group ' + line['channel-group'] + ' mode active')
            if line['vrf']:
                interfaces[name].append('vrf member ' + line['vrf'])
            if line['ip address']:
                interfaces[name].append('ip address ' + line['ip address'])
            if line['spanning-tree port type']:
                interfaces[name].append('spanning-tree port type ' + line['spanning-tree port type'])
            if line['vpc']:
                interfaces[name].append('vpc ' + line['vpc'])
            if line['shutdown']:
                interfaces[name].append(line['shutdown'])

    # Write interfaces config
    with open(args.outfile[0], 'w', encoding='utf-8-sig') as outfile:
        for interface, config in interfaces.items():
            outfile.write('int ' + interface + '\n')
            for line in config:
                outfile.write('  ' + line + '\n')
            outfile.write('\n')

if __name__ == "__main__":
    main()
