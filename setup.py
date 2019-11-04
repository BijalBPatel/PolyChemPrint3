from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='polychemprint',
      version='3.0',
      description='Free and Open Source 3D Printer control software (Python) targeted at Research Users (Polymer/Paste/BioPrinting) ',
      long_description= readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: Illinois NCSA Open Source License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Chemistry',
      ],
      keywords='3D Printing Additive Manufacturing',
      url='https://github.com/BijalBPatel/PolyChemPrint',
      author='Bijal Patel',
      author_email='bbpatel2@illinois.edu',
      license='Illinois NCSA',
      packages=['polychemprint'],
      install_requires=[
          'pyserial',
      ],
      include_package_data=True,
      zip_safe=False)