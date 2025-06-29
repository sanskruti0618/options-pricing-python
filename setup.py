from setuptools import setup, find_packages

setup(
    name='options_pricing',
    version='0.1.0',
    author='Sanskruti Kureel',
    description='A Python package for pricing options and computing option Greeks',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)
install_requires=[
    'numpy',
    'scipy',
    'matplotlib'
],
entry_points={
    'console_scripts': [
        'options-price=cli:main'
    ]
},
