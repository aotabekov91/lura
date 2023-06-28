from setuptools import setup, find_packages

setup(name='lura', 
      version='1.0.0', 
      description='Lura',
      packages=['lura.render', 'lura.core'],
      entry_points = {
          'console_scripts': [
              'lura = lura.run:main',
              ],              
          },
      )
