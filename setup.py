from setuptools import setup

setup(name='jenkins-sample',
      version='0.1',
      description='Sample web application being served',
      url='https://github.com/axel-sirota/jenkins-audition',
      author='Axel Sirota',
      author_email='axel.sirota@example.com',
      license='GPL-3.0',
      KEYWORDS = ["class", "attribute", "boilerplate"],
      CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ],
      packages=['app'],
      install_requires=[
        'nose',
        'pylint',
        'coverage',
        'nosexcover',
        'flake8',
        'twine',
        'flask'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': [
              'flasky = app.__main__:main'
          ]
      }
      )
