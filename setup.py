from setuptools import setup, find_packages


def get_install_requires():
    requirements = []
    with open('requirements.txt', 'r') as infile:
        for line in infile:
            if not line.startswith('#'):
                requirements.append(line)
    return requirements


setup(name='blue-ocean-python',
      version='0.1',
      description='Sample web application being served',
      url='https://github.com/axel-sirota/blue-ocean-python',
      author='Axel Sirota',
      author_email='axel.sirota@example.com',
      license='GPL-3.0',
      KEYWORDS=["class", "attribute", "boilerplate"],
      CLASSIFIERS=[
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
      packages=find_packages(exclude='tests'),
      install_requires=get_install_requires(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      entry_points={
          'console_scripts': [
              'flasky = app.__main__:main'
          ]
      }
      )
