from setuptools import  setup

setup(name='listdir',
      version='0.1.0',
      description='Script for producing a zip and csv file of the path directory provided',
      url='https://github.com/wilcarllopez/listdir/tree/packaging',
      author='Wilcarl D. Lopez',
      author_email='wilcarl_lopez@trendmicro.com',
      license='MIT',
      classifiers=[
            'Development Status :: Alpha',
            'Intended Audience :: Sir Anwar Sumawang',
            'Programming Language :: 3',
            'Programming Language :: 3.7'
      ],
      data_files=None,
      # scripts= ,
      entry_points={
            'console_scripts': [
                  'listdir=listdir.listdir:main'
            ]
      },
      packages=['listdir'])
