from setuptools import setup


setup(
    name='mdes',
    version='0.1.0',
    description='Modular Discrete Event Simulator',
    classifiers=[
          'License :: OSI Approved :: MIT License',
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering',
    ],
    author='Kolokotronis Panagiotis',
    url='https://github.com/panagiks/MDES',
    license='MIT',
    packages=['mdes'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'mdes=mdes.cmd:main',
        ]
    }
)
