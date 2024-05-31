#! /usr/bin/python3.11
# -*- coding: utf-8 -*-

# Displays current terminal theme color palette
# Requires: Python 3

# Usage:
# display-colors [--help | --version] COMMAND [OPTIONS]

# Copyright (C) 2024 Joe Rodrigue <joe.rodrigue at gmail dot com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click

from display_colors.cmd.effects   import display_effects
from display_colors.cmd.four_bit  import display_4_bit
from display_colors.cmd.eight_bit import display_8_bit
from display_colors.init          import init_mappings

@click.group()
@click.version_option(package_name = 'display-colors')
def cli():
	"""Prints test patterns to show the color and display effect capabilities of a terminal emulator"""
	init_mappings()

cli.add_command(display_4_bit)
cli.add_command(display_8_bit)
cli.add_command(display_effects)

if __name__ == '__main__':
	cli()
