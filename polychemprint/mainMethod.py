# -*- coding: utf-8 -*-
"""
| The *mainMethod* module runs the command line interface for PolyChemPrint and 'executes' the program.

| First created on Sat Oct 19 21:56:15 2019
| Revised: 20/10/2019 00:34:27
| Author: Bijal Patel

Inputs
---------
    :param test: args
    :param test: args
    
Methods
---------
    :param: args
    :param: args
    
Attributes
------------
    :param test: args
    :param test: args
    
Outputs
---------
    :None: Everything output to terminal window, no return value
"""

import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
class helno:
    def hello(count, name):
        """Simple program that greets NAME for a total of COUNT times.
        
        
        Returns none
        """
        
        
        for x in range(count):
            click.echo('Hello %s!' % name)
            click.echo(click.style('Hello World!', fg='green'))
            click.echo(click.style('ATTENTION!', blink=True))
            click.echo(click.style('Some things', reverse=True, fg='cyan'))
    
    if __name__ == '__main__':
        hello()
        