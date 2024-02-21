#!/bin/bash

# Creating a conda environment
conda create -n italian-lyrics-retrieval-system-test python=3.9

# Activating the conda environment
source activate italian-lyrics-retrieval-system-test

# Installing requirements
pip install -r requirements.txt

# Installing specific versions of lingua packages
pip install lingua==4.15.0
pip install lingua-language-detector==2.0.2