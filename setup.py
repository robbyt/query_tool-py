try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'query_tool',
    'author': 'Rob Terhaar',
    'url': 'AtlanticDynamic.com',
    'download_url': 'AtlanticDynamic.com',
    'version': '0.1',
    'install_requires': ['nose', 'yaml', 'pycurl', 'StringIO', 'urllib', 'argparse'],
    'packages': ['query_tool'],
    'scripts': [],
    'name': 'query_tool'
}

setup(**config)
