# Campfire Burn Severity Prediction
This repo contains the code (Jupyter Notebook) for a research project I was involed in which studied
the use ofconvolutional neural networks to predict the burn severity of affect human structures from
the 2018 Campfire using post-wildfire aerial imagery. 

## Jupyter Notebook 
The Jupyter Notebook contains code for building and creating the dataset (images and labels), as
well as train/test split, model building, training, and test evaluation. The notebook has headers
for each of these sections. Some extras are included at the bottom of the notebook. 

## Sample dataset 
The sample dataset provides a CSV as well as one example of each image for each class. 

## Conda environment 
Conda can be used to install the necessary packages to run the code in this project. This can be
done by running the command: 
```bash
conda env create -f environment.yml -n campfire
```
And then activating the environment: 
```bash
source activate campfire
```
Since n-dimensional arrays are not currently supported in 
[Imbalanced-Learn](https://github.com/scikit-learn-contrib/imbalanced-learn), I created a forked
version which can be installed by running the command: 
```bash
pip install git+https://github.com/gustaver/imbalanced-learn.git
```
