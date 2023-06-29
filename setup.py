from setuptools import setup

setup(name='lura', 
      version='1.0.0', 
      description='Lura',
      entry_points = {
          'console_scripts': [
              'lura = lura.run:main',
              ],              
          },
      )
