#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(name='three2fifteen-api',
      version='0.0.1',
      description='Three2Fifteen API',
      url='http://github.com/three2fifteen/api',
      author='Ghislain Rodrigues',
      author_email='three2fifteen@ghislain-rodrigues.fr',
      license='MIT',
      packages=['app'],
      long_description=open('README.rst').read(),
      install_requires=[
          'psycopg2',
          'flask',
          'pyjwt',
          'flask-cors',
          'requests'
      ],
      entry_points={
          'console_scripts': [
              'three2fifteen-api = app.app:main'
          ],
      },
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6'
      ],
      zip_safe=True)
