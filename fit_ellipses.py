import click
import geopandas
import pandas as pd
import numpy as np
from tqdm import tqdm
from skimage.measure import EllipseModel

def normalize_point_spread(points):
    distances = np.array([
        np.linalg.norm(points[i-1] - points[i])
        for i in range(1, points.shape[0]) # first and last point are the same
    ])
    min_distance = distances.min()
    while distances.max() > min_distance + (min_distance / 4):
        new_points = []
        for i, distance in enumerate(distances):
            new_points.append(points[i])
            if distance > min_distance + (min_distance / 4):
                new_point = points[i:i+2].mean(axis=0)
                new_points.append(new_point)
        new_points.append(points[-1]) # complete the ring
        points = np.array(new_points)
        distances = np.array([
            np.linalg.norm(points[i-1] - points[i])
            for i in range(1, points.shape[0]) # first and last point are the same
        ])
    return points

def center_points(points):
    return points - points.mean(axis=0), points.mean(axis=0)

@click.command()
@click.option("--file", help=".shp file location", required=True)
def main(file):
    df = geopandas.read_file(file)
    rows = []
    for shape in tqdm(df['geometry'].values):
        points = np.array(shape.boundary.coords)
        centered_points, center = center_points(points)
        normed_points = normalize_point_spread(centered_points)
        model = EllipseModel()
        model.estimate(normed_points)
        xc, yc, a, b, theta = model.params
        xc += center[0]
        yc += center[1]
        rows.append({
            'center_x': xc,
            'center_y': yc,
            'radius_a': a,
            'radius_b': b,
            'theta': theta 
        })
    fit_df = pd.DataFrame(rows)
    fit_df.to_csv(file[:-4] + '_ellipse_fits.csv', index=False)


if __name__ == '__main__':
    main()

