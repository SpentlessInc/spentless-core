from setuptools import setup, find_packages

NAME = "sws.core"
VERSION = "0.1"
AUTHOR = "Sheet Without Sheet"
INSTALL_REQUIRES = [
    "aiohttp==3.6.2",
    "aioredis==1.3.1",
    "hiredis==1.0.1",
    "asyncpg==0.20.1"
]


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
)
