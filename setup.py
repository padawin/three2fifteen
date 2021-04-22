#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(name='three2fifteen',
      version='0.0.1',
      description='Three2Fifteen',
      url='http://github.com/three2fifteen/api',
      author='Ghislain Rodrigues',
      author_email='three2fifteen@ghislain-rodrigues.fr',
      license='MIT',
      packages=['.'],
      long_description=open('README.rst').read(),
      install_requires=[
          'flask',
          'pyjwt',
          'tornado',
          'requests'
      ],
      entry_points={
          'console_scripts': [
              'three2fifteen = app.app:main'
          ],
      },
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6'
      ],
      zip_safe=True)
