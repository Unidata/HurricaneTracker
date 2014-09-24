HurricaneTracker
================

Hurricane Track Visualization in Python

### How to run this notebook

First clone this notebook:

```
git clone https://github.com/Unidata/HurricaneTracker
```

Once you have the notebook files, you will need to install a number of Python packages. The easiest way to install these packages is via the conda package manager which you can download for free [here](https://store.continuum.io/cshop/anaconda/).

After conda is installed, open a Unix shell or the Windows Conda command prompt and issue these commands:

```
conda create -n hurricane ipython pyzmq jinja2 tornado pandas basemap

[source] activate hurricane

cd HurricaneTracker

ipython notebook
```

The first of these commands will install the necessary packages to run this notebook. 

The second command will activate the notebook. `source` is required in the Unix shell but not on Windows.

The last command will start the notebook server. You should be able to access the HurricaneTracker notebook at [http://localhost:8888/notebooks/hurTrackerGui.ipynb](http://localhost:8888/notebooks/hurTrackerGui.ipynb#)