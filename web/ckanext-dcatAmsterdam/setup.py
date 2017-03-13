from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

version = '0.1.0'
here = path.abspath(path.dirname(__file__))

setup(
    name='ckanext-dcatAmsterdam',
    version=version,
    description='CKAN Extension - DCAT-NL Fields, Amsterdam',
    long_description='This is a long description',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='dcat, DCAT-NL, Amsterdam, Civity',
    author='Gil Hilario',
    author_email='gil@civity.nl',
    url='http://www.civity.nl/',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests','contrib', 'docs']),
    namespace_packages=['ckanext', 'ckanext.dcatAmsterdam'],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'nose>=1.3.0'
    ],
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    tests_require=[
    ],
    test_suite='nosetests',
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        dcatAmsterdam=ckanext.dcatAmsterdam.plugin:DCATAmsterdam
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
)
