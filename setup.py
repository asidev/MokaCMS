#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid>=1.3',
    'pyramid_debugtoolbar',
    'waitress',
    'cement',
    "colander",
    "beautifulsoup4",
    "mako",
    'pymongo'
    ]

setup(name='MokaCMS',
      version='0.1dev',
      description='MokaCMS',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Asidev S.r.l.',
      author_email='info@asidev.com',
      url='https://github.com/asidev/MokaCMS',
      keywords='web pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="mokacms",
      entry_points="""\
      [paste.app_factory]
      main = mokacms:main
      [console_scripts]
      moka = mokacms.cli.app:main
      """,
      )
