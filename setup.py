from setuptools import setup, find_packages

# The requirements variable contains all the external dependencies that PerSeO requires to function, it must be kept up to date with the data in the requirements.txt file.
requirements = [
    'cycler==0.11.0',
    'fonttools==4.31.2',
    'joblib==1.1.0',
    'kiwisolver==1.4.2',
    'matplotlib==3.5.1',
    'numpy==1.22.3',
    'packaging==21.3',
    'pandas==1.4.2',
    'Pillow==9.1.0',
    'pyparsing==3.0.7',
    'python-dateutil==2.8.2',
    'pytz==2022.1',
    'scikit-learn==1.1.1',
    'scipy==1.8.1',
    'six==1.16.0',
    'threadpoolctl==3.1.0'
]

setup(
    name="PerSeO",
    version="2.0.0",
    packages=find_packages(),
    install_requires=requirements,
    author="German Chaparro, Jorge Cardenas,Oscar Restrepo, Sergio Mora, Jhon Vera, Daniela Paez, and Jaime Angel",
    author_email="andres_angel@live.com.ar",
    description="PerSeO: PSO Applied to RF Device Design",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ERA-2022/PerSeO',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license='MIT'
)
