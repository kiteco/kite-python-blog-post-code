# Campfire Burn Severity Prediction
This repo contains the code (Jupyter Notebook) for a research project I was involed in which studied
the use ofconvolutional neural networks to predict the burn severity of affect human structures from
the 2018 Campfire using post-wildfire aerial imagery. 

We recommend running the code outside of Jupyter notebooks, as you may see performance advantages 
on your machine (not to mention better tools and environments).


## Sample dataset 
The sample dataset provides a CSV as well as 180 total images from the original data.

-----

## Vanilla Python Instructions

Set up your project normally and install dependencies with:

```bash
pip install -r requirements.txt
pip install git+https://github.com/gustaver/imbalanced-learn.git
```
You can run most of the code with packages from PyPI, but the second instruction will allow
you to run the forked version of imblearn.

If using venv, activate your venv and run the code in snippets against the python console
with the article. 

###  Common Errors and Solutions:
  Try installing the major packages independently, these are:
  pandas, numpy, matplotlib, tensorflow, sklearn, imblearn, scipy, and imutils

  Also you may need to install
  opencv-python (in case you get a `no module named cv2` error) and
  Pillow (in case you get a `Could not import PIL.Image` error

  Try setting up placeholder log files:
  model_checkpoints/baseline/log.csv and 
  model_checkpoints/baseline_datagen/log.csv

Note for PyCharm users:
tensorflow.keras imports return inspection errors even though the code will run fine. 
The reason for this is a "won't fix" issue with Tensorflow and is beyond the scope of this tutorial.

------

## Jupyter Notebook Instructions

The Jupyter Notebook contains code for building and creating the dataset (images and labels), as
well as train/test split, model building, training, and test evaluation. The notebook has headers
for each of these sections. Some extras are included at the bottom of the notebook. 

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
