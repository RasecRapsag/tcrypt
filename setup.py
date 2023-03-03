from setuptools import find_packages, setup


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='tcrypt',
    version='1.0',
    description='Truecrypt volume management tool',
    package_dir={'': 'tcrypt'},
    packages=find_packages(where='tcrypt'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RasecRapsag/tcrypt',
    author='Cesar Gaspar',
    author_email='rasec.rapsag@gmail.com',
    license='Apache',
    classifiers=[
        'License :: Apache License'
        'Programming Language :: Python :: 3.10',
        'Operating System :: Linux'
    ],
    install_requires=[''],
    extras_require={
        'dev': ['pytest>=7.2', 'pylint>=2.15'],
    },
    python_requires='>=3.10',
)
