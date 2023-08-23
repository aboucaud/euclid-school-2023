# Dataset creation

For most of these tutorials, we will use large datasets hosted in the Flatiron (USA).

Follow these steps in order to run the `*cosmology_with_one_galaxy*` notebooks.

## Step 1 – Cloning

Clone this folder on your computer

```shell
git clone https://github.com/aboucaud/euclid-school-2023
```

## Step 2 - JupyterHub

Connect to the Flatiron JupyterHub instance augmented with CAMELS public data: https://binder.flatironinstitute.org/~sgenel/CAMELS_PUBLIC

## Step 3 - Uploading files

Upload the content of the `euclid-school-2023/dataset` folder content inside the `~/home` directory on JupyterHub (<kbd>Upload</kbd> button at the top right)

The `home` folder online should look like this
```
├── README.md
├── cosmo_1_galaxy.tar
├── create_galaxy_properties_data.py
├── latin_hypercube_params_IllustrisTNG.txt
├── latin_hypercube_params_SIMBA.txt
├── multifield.tar
└── requirements.txt
```

## Step 4 - Untar the cosmo_1_galaxy and multifield folders

Open a terminal on the JupyterHub instance : `New > Terminal`

```shell
cd home
tar -xvf cosmo_1_galaxy.tar
tar -xvf multifield.tar
```

## Step 5 - Creation of the galaxy properties tables

In the same terminal run the following script

```shell
python create_galaxy_properties_data.py --n_realizations 1000
```

> [!IMPORTANT]
> The `n_realizations` arguments will be directly correlated with the size of the final dataset. If at some point you lack memory to run the notebooks and the TF code, try reducing the number of realizations and re-running steps 6 and 6-bis

## Step 6 - Creation of the TF catalog dataset

Install the dependencies

```shell
python -m pip install -r requirements.txt
```

and run the TensorFlow dataset creation

```shell
cd ~/home/cosmo_1_galaxy
tfds build --manual_dir=/home/jovyan/home/
```

This should build the SIMBA dataset on `/home/jovyan/tensorflow_datasets/cosmo_1_galaxy/1.0.1`

## Step 6-bis - TNG dataset

To build the IllustrisTNG dataset, from the main JupyterHub menu open `~/home/cosmo_1_galaxy/cosmo_1_galaxy_dataset_builder.py`
and replace on line 14

```python
tfds.core.Version('1.0.1')
```

with

```python
tfds.core.Version('1.0.0')
```

and on line 41

```python
sim         = 'SIMBA'
```

with

```python
sim         = 'IllustrisTNG' 
```

and rerun 

```shell
tfds build --manual_dir=/home/jovyan/home/
```

## Step 7 - Creation of the TF image dataset

Similar to step 6

```shell
cd ~/home/multifield
tfds build --manual_dir=/home/jovyan/home/
```

and repeat for the other simulation by manually editing `~/home/multifield/multifield_dataset_builder.py` like step 6-bis

> [!NOTE]
> This image dataset is much heavier and the processing with CNNs is extremely slow on CPUs. If you have access to a machine with GPUs, you can download the Tensorflow datasets created on this JupyterHub to process them elsewhere. Relevant files will be stored in `/home/jovyan/tensorflow_datasets`.  
> 
> Refer to the "Downloading data" section on https://wiki.flatironinstitute.org/Public/UsingFiBinder for more options.
