import os
from distutils.core import setup

from l1l2py import __version__ as version
README = os.path.join(os.path.dirname(__file__), 'README')
long_description = '\n' + open(README).read()

setup(
    name='l1l2py',
    version=version,

    description='l1l2py is a Python package to perform feature selection '
                'by means of l1l2 regularization with double optimization',
    long_description=long_description,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],

    keywords='...',
    author='Salvatore Masecchia and Annalisa Barla',
    author_email='salvatore.masecchia@.unige.it',
    license='GNU GPL version 3',
    platforms='...',
    url='http://slipguru.disi.unige.it/l1l2py',

    packages=['l1l2py', 'l1l2py.tests'],
    package_data={'l1l2py.tests': ['data.txt']},

    requires=['numpy (>=1.3.0)', 'nose', 'sphinx', 'numpydoc'],

)
