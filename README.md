# stravaplot

stravaplot is a python library for visualizing Strava (or any other GPX data for that matter) activity tracks.

It can be used to visualize one activity:

```python
import stravaplot as strava

s = strava.plot('activity.gpx')

# display the plot
s.show()

# save it as an image
s.save('filename.png')
```

<img src="http://i.imgur.com/hpNd4lz.png" width="600px" />

or many activities:

<img src="http://imgur.com/Ao6q2f8.png" width="600px" />

```python
s = strava.plot('activities_dir')
s.show()
```

It can also show terrain:

```python
s = strava.plot('activities', terrain='usgs_ned.img')
s.show()
```

<img src="http://i.imgur.com/S87ikOx.png" width="600px" />

See more on plotting terrain below.

## Installation
Installation ranges from simple to hard, depending on your environment. In the simplest case, install the dependencies and you should be good to go. If you're on macOS and using virtualenvs, see below:

### Installing GDAL on macOS
Use homebrew to install GDAL:

```bash
brew install gdal
```

Now we need to install GDAL inside our virtualenv. Note that the version pip installs must be the same as the version homebrew installs (At least to first order - homebrew installed GDAL 1.13.1 and the closest version available via pip is 1.11.2. This doesn't appear to cause any problems.) Inside our virtualenv, install GDAL with pip:

```bash
pip install GDAL==1.11.2
```

### Using matplotlib on macOS inside a virtualenv
The GUI frameworks that matplotlib uses for interactive figures don't play nicely with virtualenvs. Specifically, the default one that is configured for use on (at least) macOS breaks inside a virtualenv. We need to tell matplotlib to use a different framework that works within a virtualenv. With matplotlib installed,

```bash
cd ~/.virtualenvs/<virtualenv name>/lib/python3.5/site-packages/matplotlib/mpl-data
```

We need to edit the `matplotlibrc` fle, so open it up in your favorite editor. Find the line that says

```bash
backend : macosx
```

and change it to

```bash
backend : TkAgg
```



## Settings
stravaplot has a few settings which can be changed.

* `background` -
* `linecolor` -
* `linewidth` -
* `linealpha` -
* `terraincolor` -
* `figwidth` -
* `padding` -
* `dpi` -
* `threshold` -

For example, to change the padding factor:

```python
s.padding = 0.25
```

Print a listing of current settings with

```python
s.settings
```

## Colormaps
Several custom colormaps are included:

* `electricblue` -
* `strava` -
* `gyroscope` -

To change colormaps:

```python
s.color('gyroscope')
```

