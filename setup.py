"""Bot pendu"""

from setuptools import setup, find_packages

setup(
    name='Pendu',
    version='1.0',
    description="Hanged game bot for Slack",
    url="https://github.com/Diogo-Ferreira/the_real_bot",
    packages=['Pendu','PenduController'],
    install_requires=(
        'aiohttp',
        'asyncio'
    ),
    extras_requires={
        'doc': ('Sphinx','sphinx_rtd_theme'),
    }
)