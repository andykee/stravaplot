import numpy as np
from osgeo import gdal


def terrain(north,south,east,west,terrain_data):
    ds = gdal.Open(terrain_data)
    x1 = west 
    y1 = north
    x2 = east 
    y2 = south 
    
    ds_info = ds.GetGeoTransform()
    
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    bands = ds.RasterCount
    
    x_origin = ds_info[0]  # top-left x
    y_origin = ds_info[3]  # top-left y
    dx = ds_info[1]
    dy = ds_info[5]

    x_offset = int(np.floor((x1 - x_origin)/dx))
    y_offset = int(np.floor((y1 - y_origin)/dy))
    x_size = int(np.ceil((x2-x1)/dx))
    y_size = int(np.ceil((y2-y1)/dy))
    
    x = np.linspace(x1,x2,x_size)
    y = np.linspace(y1,y2,y_size)
    
    topo = ds.ReadAsArray(x_offset,y_offset,x_size,y_size)

    # close file
    ds = None

    return x,y,topo

