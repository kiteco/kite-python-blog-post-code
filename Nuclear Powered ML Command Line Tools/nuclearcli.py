"""
Nuclear Powered Cli

* GPU parallization
* Machine Learning/Clustering
* JIT
* Multi-threading
* Colored output

"""


import click

from numba import (cuda, vectorize)
import numba
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

from functools import wraps
from time import time

@click.group()
def cli():
    pass

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"fun: {f.__name__}, args: [{args}, {kw}] took: {te-ts} sec")
        return result
    return wrap


def real_estate_df():
    """30 Years of Housing Prices"""

    df = pd.read_csv("https://raw.githubusercontent.com/noahgift/real_estate_ml/master/data/Zip_Zhvi_SingleFamilyResidence.csv")
    df.rename(columns={"RegionName":"ZipCode"}, inplace=True)
    df["ZipCode"]=df["ZipCode"].map(lambda x: "{:.0f}".format(x))
    df["RegionID"]=df["RegionID"].map(lambda x: "{:.0f}".format(x))
    return df

def numerical_real_estate_array(df):
    """Converts df to numpy numerical array"""

    columns_to_drop = ['RegionID', 'ZipCode', 'City', 'State', 'Metro', 'CountyName']
    df_numerical = df.dropna()
    df_numerical = df_numerical.drop(columns_to_drop, axis=1)
    return df_numerical.values

def real_estate_array():
    """Returns Real Estate Array"""

    df = real_estate_df()
    rea = numerical_real_estate_array(df)
    return np.float32(rea)

def kmeans_cluster_housing(clusters=3):
    """Kmeans cluster a dataframe"""
    
    val_housing_win_df =\
        pd.read_csv("https://raw.githubusercontent.com/noahgift/socialpowernba/master/data/nba_2017_att_val_elo_win_housing.csv")
    numerical_df =\
        val_housing_win_df.loc[:,["TOTAL_ATTENDANCE_MILLIONS", "ELO", 
        "VALUE_MILLIONS", "MEDIAN_HOME_PRICE_COUNTY_MILLIONS"]]
    #scale data
    scaler = MinMaxScaler()
    scaler.fit(numerical_df)
    scaler.transform(numerical_df)
    #cluster data
    k_means = KMeans(n_clusters=clusters)
    kmeans = k_means.fit(scaler.transform(numerical_df))
    val_housing_win_df['cluster'] = kmeans.labels_
    return val_housing_win_df

@timing
def expmean(rea):
    """Regular Function"""

    val = rea.mean() ** 2
    return val

@timing
@numba.jit(nopython=True)
def expmean_jit(rea):
    """Perform multiple mean calculations"""

    val = rea.mean() ** 2
    return val

@vectorize(['float32(float32, float32)'], target='cuda')
def add_ufunc(x, y):
    return x + y


@timing
@numba.jit(parallel=True)
def add_sum_threaded(rea):
    """Use all the cores"""

    x,_ = rea.shape
    total = 0
    for _ in numba.prange(x):
        total += rea.sum()  
        print(total)

@timing
def add_sum(rea):
    """traditional for loop"""

    x,_ = rea.shape
    total = 0
    for _ in numba.prange(x):
        total += rea.sum()  
        print(total)

@cli.command()
@click.option('--threads/--no-jit', default=False)
def thread_test(threads):
    rea = real_estate_array()
    if threads:
        click.echo(click.style('Running with multicore threads', fg='green'))
        add_sum_threaded(rea)
    else:
        click.echo(click.style('Running NO THREADS', fg='red'))
        add_sum(rea)



@cli.command()
def cuda_operation():
    """Performs Vectorized Operations on GPU"""

    x = real_estate_array()
    y = real_estate_array()

    print("Moving calculations to GPU memory")
    x_device = cuda.to_device(x)
    y_device = cuda.to_device(y)
    out_device = cuda.device_array(
        shape=(x_device.shape[0],x_device.shape[1]), dtype=np.float32)
    print(x_device)
    print(x_device.shape)
    print(x_device.dtype)

    print("Calculating on GPU")
    add_ufunc(x_device,y_device, out=out_device)

    out_host = out_device.copy_to_host()
    print(f"Calculations from GPU {out_host}")


@cli.command()
@click.option('--jit/--no-jit', default=False)
def jit_test(jit):
    rea = real_estate_array()
    if jit:
        click.echo(click.style('Running with JIT', fg='green'))
        expmean_jit(rea)
    else:
        click.echo(click.style('Running NO JIT', fg='red'))
        expmean(rea)

@cli.command()
@click.option("--num", default=3, help="number of clusters")
def cluster(num):
    df = kmeans_cluster_housing(clusters=num)
    click.echo("Clustered DataFrame")
    click.echo(df.head())


if __name__ == "__main__":
    cli()
