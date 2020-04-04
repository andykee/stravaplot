from math import sqrt
from os import listdir
from os.path import isdir, isfile, join, split

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import gpxpy

from .terrain import terrain

COLORMAP = {'electricblue' : {
                'linecolor'    : 'deepskyblue',
                'terraincolor' : '0.2',
                'background'   : '0.05'},
            'strava' : {
                'linecolor'    : '#FFFFFF',
                'terraincolor' : 'coral',
                'background'   : 'orangered'},
            'gyroscope' : {
                'linecolor'    : '#68D2E2',
                'terraincolor' : '0.05',
                'background'   : '#132029'}
}

class plot:

    def __init__(self, strava_path, terrain_path = None):
        
        # Prepare strava data list
        if isfile(strava_path):
            self.strava_data = [strava_path]
        elif isdir(strava_path):
            self.strava_data = [join(strava_path,f) for f in listdir(strava_path) if
                                f.endswith(".gpx") and isfile(join(strava_path,f))]
        else:
            raise TypeError('Invalid strava data path')

        # Prepare terrain data list
        if terrain_path is not None:
            if isfile(terrain_path):
                self.terrain_data = [terrain_path]
            elif isdir(terrain_path):
                self.terrain_data = [join(terrain_path,f) for f in listdir(terrain_path) if isfile(join(terrain_path,f))]
            else:
                raise TypeError('Invalid terrain data path')
        else:
            self.terrain_data = None

        # defaults
        self.dpi = 300
        self.background = '0.05'
        self.padding = 0.05
        self.linewidth = 0.2
        self.linecolor = 'deepskyblue'
        self.linealpha = 0.8
        self.terraincolor = '0.2'
        self.terrainlinewidth = 0.2
        self.threshold = 0.006
        self.figwidth = None
        self.fig = None

        self._north = None
        self._east = None
        self._south = None
        self._west = None


    def _draw(self):
        self.fig = plt.figure(frameon=False)
        if self.figwidth is not None:
            self.fig.set_figwidth(self.figwidth)
        ax = plt.Axes(self.fig,[0,0,1,1],)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_axis_off()
        self.fig.add_axes(ax)

        for f in self.strava_data:
            with open(f) as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                for track in gpx.tracks:
                    lat = []
                    lon = []
                    for segment in track.segments:
                        for point in segment.points:
                            lat.append(point.latitude)
                            lon.append(point.longitude)
                    lat,lon = _deline(lat,lon,self.threshold)
                    ax.plot(lon,lat,color=self.linecolor,lw=self.linewidth,alpha=self.linealpha)

        self._west,self._east = ax.get_xlim()
        self._south,self._north = ax.get_ylim()

        # include padding
        if self.padding > 0:
            dlat = self._north - self._south
            dlon = self._west - self._east
            
            pad_lat = self.padding * abs(dlat)
            pad_lon = self.padding * abs(dlon)

            self._north = self._north + pad_lat
            self._south = self._south - pad_lat
            self._east = self._east + pad_lon
            self._west = self._west - pad_lon

        
        # get terrain data
        if self.terrain_data is not None:
            for f in self.terrain_data:
                x,y,topo = terrain(self._north,self._south,self._east,self._west,f)
                ax.contourf(x,y,topo,1,cmap=colors.ListedColormap([self.background,self.background]))
                ax.contour(x,y,topo,50,hold='on',colors=self.terraincolor,linewidths=self.terrainlinewidth)
        else:
        # no terrain data available; we need to fake the background color
            x = np.linspace(self._west,self._east,2)
            y = np.linspace(self._north,self._south,2)
            topo = np.array([[0,0],[0,0]])
            ax.contourf(x,y,topo,1,cmap=colors.ListedColormap([self.background,self.background]))

    def show(self):
        self._draw()
        plt.show()


    def save(self,filename=None):
        self._draw()
        if filename is None:
            filename = 'stravaplot.png'
        plt.savefig(filename,
                    facecolor=self.background,
                    bbox_inches='tight',
                    pad_inches=0,
                    dpi=self.dpi,
                    transparent=True)


    def color(self,name):
        if name in COLORMAP:
            self.linecolor = COLORMAP[name]['linecolor']
            self.terraincolor = COLORMAP[name]['terraincolor']
            self.background = COLORMAP[name]['background']
        else:
            raise ValueError('Invalid colormap')

    @property
    def settings(self):
        print('strava_data  : ', self.strava_data)
        print('background   : ', self.background)
        print('padding      : ', self.padding)
        print('linecolor    : ', self.linecolor)
        print('linewidth    : ', self.linewidth)
        print('linealpha    : ', self.linealpha)
        print('terraincolor : ', self.terraincolor)
        print('threshold    : ', self.threshold)
        print('figwidth     : ', self.figwidth)
        print('dpi          : ', self.dpi)



def _deline(lat, lon,threshold):
    """ A very simple attempt at removing data collection errors (which appear
    as jumps between locations. Ideally the data will be more appropriately 
    filtered before plotting."""
    if len(lat) == len(lon):
        length = len(lat)
        i = 1
        while i < length:
            lat2 = lat[i]
            lat1 = lat[i-1]
            lon2 = lon[i]
            lon1 = lon[i-1]
            d = sqrt((lon2-lon1)**2 + (lat2-lat1)**2)
            if d > threshold:
                lat.insert(i,np.nan)
                lon.insert(i,np.nan)
                i += 2
            else:
                i += 1
        return lat, lon
    else:
        print("Cannot deline data, lists must be same length")
        return lat, lon

