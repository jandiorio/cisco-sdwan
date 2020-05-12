#!/usr/bin/env python

import click
# Simple Python Test to Learn Click to Build CLI Tools

#print("This is a simple cli tool script")

@click.group()
def cli():
    """ click tool """
    pass

@click.command()
@click.option("-n", help="name for the greeting")
def print_welcome(name):
    if name:
        click.secho(f"Hello {name}!  Welcome to the basic cli tool demo!")
    else:
        click.secho(f"Hello!  Welcome to the basic cli tool demo!")

cli.add_command(print_welcome)

if __name__=="__main__":
    cli()
