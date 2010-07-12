import os
from distutils.core import setup

# Package path
pkg_path = os.path.dirname(__file__)

# Package description
README = os.path.join(pkg_path, 'README')
lines = open(README).readlines()
description = ''.join(lines[:2])
long_description = ''.join(lines[2:])

# Package Version
from l1l2py import __version__ as version
from mercurial import ui, hg
repo = hg.repository(ui.ui(), pkg_path)
rev = repo['tip'].rev()
if repo[str(rev-1)].tags != version and repo['tip'].tags != version:
    import datetime
    today = datetime.date.today()
    version += '-%s-%s%s%s' % (repo['tip'].hex()[:12],
                               today.year, today.month, today.day)
    
setup(
    name='L1L2Py',
    version=version,
    url='http://slipguru.disi.unige.it/Research/L1L2Py',
    description=description,
    long_description=long_description,
    keywords='feature selection, regularization, regression, classification,'
             'l1-norm, l2-norm',
    author='L1L2Py developers - SlipGURU',
    author_email='salvatore.masecchia@disi.unige.it',
    license='GNU GPL version 3',
    download_url = 'http://slipguru.disi.unige.it/Research/L1L2Py/L1L2Py-%s.tar.gz' % version,
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

    packages=['l1l2py', 'l1l2py.tests'],
    package_data={'l1l2py.tests': ['data.txt']},
    requires=['numpy (>=1.3.0)']
)
