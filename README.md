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


### Using matplotlib on macOS inside a virtualenv


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

To change colormaps,

```python
s.colormap('gyroscope')
```

