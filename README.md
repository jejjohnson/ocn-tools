# OceanTools

[**About**](#about) 
| [**Installation**](#installation)

![pyver](https://img.shields.io/badge/python-3.9%203.10%203.11_-red)
![codestyle](https://img.shields.io/badge/codestyle-black-black)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jejjohnson/xrpatcher/blob/main/notebooks/pytorch_integration.ipynb)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jejjohnson/oceanbench)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## About<a id="about"></a>

**OceanTools** are a set of useful functions that are necessary for OceanBench.

> An agnostic suite of geoprocessing tools for [xarray](https://docs.xarray.dev/en/stable/) datasets that were aggregated from different sources


It is lightweight in terms of the core functionality.
We keep the code base simple and focus more on how the user can combine each piece.
We adopt a strict functional style because it is easier to maintain and combine sequential transformations.



## Installation<a id="installation"></a>

### `conda` (RECOMMENDED)

We use conda/mamba as our package manager. To install from the provided environment files
run the following command.

```bash
git clone https://github.com/jejjohnson/oceanbench.git
cd oceanbench
mamba env create -n environments/linux.yaml
```

#### Jupyter 
if you want to add the oceanbench conda environment as a jupyter kernel, you need to set the ESMF environment variable:

```
conda activate oceanbench
mamba install ipykernel -y 
python -m ipykernel install --user --name=oceanbench --env ESMFMKFILE "$ESMFMKFILE"
```

### `pip`

We can directly install it via pip from the.

```bash
conda create -n ocntools
cd ocntools
mamba install xesmf -c conda-forge
pip install "git+https://github.com/jejjohnson/ocn-tools.git"
```

**Note**: There are some known dependency issues related to `pyinterp` and `xesmf`. 
You will need to manually install some of the dependencies before installing oceanbench via pip.
See the [pyinterp](https://pangeo-pyinterp.readthedocs.io/en/latest/setup/pip.html) and [xesmf](https://xesmf.readthedocs.io/en/latest/installation.html) packages for more information.

### `poetry`

For developers who want all of the dependencies via pip, we can use poetry to install the package.


```bash
git clone https://github.com/jejjohnson/ocn-tools.git
cd ocntools
conda create -n ocntools python=3.11 poetry
poetry install
```

## Acknowledgements

We would like to acknowledge the [Ocean-Data-Challenge Group](https://ocean-data-challenges.github.io/) for all of their work for providing open source data and a tutorial of metrics for SSH interpolation.



[jbook-badge]: https://raw.githubusercontent.com/executablebooks/jupyter-book/master/docs/images/badge.svg
[jbook-link]: https://jejjohnson.github.io/oceanbench/content/overview.html
