from setuptools import setup
from distutils.extension import Extension


setup(name='LatexFootnotesToHTML',
      version='0.1',
      description='Helps converting Latex footnotes to HTML',
      long_description='',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 3.5',
      ],
      author='Gabriel Kabbe',
      license='GPLv3',
      packages=["leibniz"],
      install_requires=["ipdb", "sh"],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['tag=leibniz.set_footnote_markers_in_tex:main',
                              'marker2modal=leibniz.find_all_footnotes_in_html:main'
                              ],
      },
      include_package_data=True,
      zip_safe=False,
      )
