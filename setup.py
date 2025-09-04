#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Leer el contenido del archivo README.md para la descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Leer las dependencias desde el archivo requirements.txt
def read_requirements(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

requirements = read_requirements("requirements.txt")

setup(
    name="heliobio-api",
    version="0.1.0",
    author="Mechmind-dwv",
    author_email="ia.mechmind@gmail.com",
    description="Sistema avanzado para el análisis y predicción de correlaciones heliobiológicas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mechmind-dwv/HelioBio-API",  # Reemplazar con la URL real del repositorio
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Medical Science Apps",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    keywords="heliobiologia, actividad solar, manchas solares, chizhevsky, epidemiologia, prediccion",
    project_urls={
        "Bug Tracker": "https://github.com/mechmind-dwv/HelioBio-API/issues",
        "Documentation": "https://github.com/mechmind-dwv/HelioBio-API/docs",
    },
)
