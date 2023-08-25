# ML lectures - Rodolphe Clédassou summer school 2023

> **Marc Huertas-Company** (IAC) and **Alexandre Boucaud** (APC)  
> August 2023

## Lectures

### Cycle 1

- [Introduction to machine learning with (probabilistic) neural networks](https://aboucaud.github.io/slides/2023/euclid-school-ml-cycle1)

### Cycle 2

- [Introduction and neural networks recap from cycle 1](https://aboucaud.github.io/slides/2023/euclid-school-ml-cycle2) - _HTML slides_
- [Probabilistic neural networks](slides/cycle2_cours1_2023.pdf) - _PDF_
- [Convolutional networks](slides/cycle2_cours2a_2023.pdf) - _PDF_
- [Image2image networks and Transformers](slides/cycle2_cours2b_2023.pdf) - _PDF_
- [Attention mechanism and Graph networks](slides/cycle2_cours2c_2023.pdf) - _PDF_
- [Introduction to MLOps](https://aboucaud.github.io/slides/2023/euclid-school-mlops) - _HTML slides_

### Cycle 3

- Slides to come soon
- [Friday Zoom recording](https://u-paris.zoom.us/rec/play/jTDV8v9lMMaJ1I9wAYtU-OEZxA8kUqfutphYk5TOh5KW3uSNFD6Rnds5OTCM1pRZl1I31--O0y59eC9d.FPLI8i2AqyXNsXCQ) | 
Recording code: CqBP?5b!Y^

## Notebooks

### Cycle 1

#### Setup

To run the notebooks locally, install the dependencies from the `requirements.txt`
```shell
python -m pip install -r requirements.txt
```

> [!WARNING]
> macOS users with M1/M2 processors please follow the instructions below to install TensorFlow (otherwise the notebook kernel will die at the beginning)
> [Apple M1/M2 specific TensorFlow installation](https://developer.apple.com/metal/tensorflow-plugin/)

- [Neural regression with classic and probabilistic neural networks](notebooks/cycle1_intro_nn_logprob.ipynb)
- [Same notebook with MLFlow examples](notebooks/cycle1_intro_nn-mlflow-example.ipynb)

### Cycle 2

> [!WARNING]
> For cycle 2 and 3, those not using Google Colab links must first run the [dataset creation](datasets/README.md) steps below before starting with the notebooks.

Instructions for the [notebook](notebooks/cycle2_cosmology_with_one_galaxy.ipynb):

1. choose one simulation between `IllustrisTNG` (dataset version `1.0.0`) and `SIMBA` (dataset version `1.0.1`)
2. execute Part 1 and 2 whose goal is to predict $\Omega_M$ and try to improve the results of the MLP
3. try to apply the networks trained with one simulation to the other one
4. move on to Part 3 where we try to predict $\sigma_8$ and $\Omega_M$

An alternative is to try [the notebook on Google Colab](https://colab.research.google.com/drive/14IVaCDcwd-EIhOMfGofRmtii5R75N0qN?usp=sharing) (need a Google account).

### Cycle 3

> [!WARNING]
> For cycle 2 and 3, those not using Google Colab links must first run the [dataset creation](datasets/README.md) steps below before starting with the notebooks.



## References

- https://arxiv.org/abs/2201.02202
- https://camels.readthedocs.io/en/latest/index.html
