import click
import geopandas
import pandas as pd 
import seaborn as sns
import numpy as np
from skimage.measure import EllipseModel

@click.command()
@click.option('--file', help='.shp file location', required=True)
@click.option('--index', help='0 based index of shape', required=True, type=int)
def main(file, index):
    shapes = geopandas.read_file(file)
    fit_df = pd.read_csv(file[:-4] + '_ellipse_fits.csv')
    shape = shapes['geometry'].values[index]
    fit_row = fit_df.iloc[index]
    xc, yc = fit_row['center_x'], fit_row['center_y']
    a, b = fit_row['radius_a'], fit_row['radius_b']
    theta = fit_row['theta']
    rows = []
    # get actual points
    for x, y in shape.boundary.coords:
        rows.append({
            'x': x,
            'y': y,
            'case': 'actual'
        })
    model = EllipseModel()
    for x, y in model.predict_xy(
            np.linspace(0, 2 * np.pi, 25), 
            params=(xc, yc, a, b, theta)
        ):
        rows.append({
            'x': x,
            'y': y,
            'case': 'fit'
        })
    df = pd.DataFrame(rows)
    plot = sns.scatterplot(data=df, x='x', y='y', hue='case')
    plot.get_figure().savefig(file[:-4] + '_' + str(index) + '_fit.png')


if __name__ == '__main__':
    main()