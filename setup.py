from setuptools import setup, find_packages

setup(
    name='spotify_connect_scrobbler',
    version='0.4',
    license='MIT',
    packages=find_packages(),
    install_requires=['click', 'python-dateutil', 'requests', 'pymongo'],
    entry_points={
      'console_scripts': ['scrobbler-auth=spotify_connect_scrobbler.auth:main']
    }
    )
