from setuptools import setup, find_packages

setup(
    # Basic info
    name='pycats',
    version='0.1.0',
    author='Matthew Nicol',
    author_email='matthew.b.nicol@gmail.com',
    description='Python categories system.',
    long_description='Python categories system.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python 3',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'pycats': 'pycats'},
    packages=['pycats'],
    install_requires=[],

    # Scripts
    entry_points={
        'console_scripts': [],
    },
)
