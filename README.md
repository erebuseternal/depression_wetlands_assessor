# depression_wetlands_assessor

## Fitting Ellipses
To fit ellipses to shapes from a shapefile simply run:
```bash
python fit_ellipses.py --file /path/to/shapefile.shp
```
This will create a file at `/path/to/shapefile_ellipse_fits.csv` which has the ellipse fit data. 

To see the quality of the fit simply run:
```bash
python view_fit.py --file /path/to/shapefile.shp --index <index of the shape>
```
If you index was 0 this would create a png plot at `path/to/shapefile_0_fit.png

### Starting Jupyter Lab
```jupyter lab --ip=0.0.0.0 --allow-root```
