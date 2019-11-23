import numpy as np
import matplotlib.pyplot as plt
import time
import math

def gaussian(x, sigma):
    """
    centered gaussian

    :param x: 
    :param sigma: 
    """

    return np.exp(-np.power(x, 2.) / (2 * np.power(sigma, 2.)))


def make_track(density = 0.05, ellipse_shape = (40, 24),
        bumps = [(0.05, 0.5), (0.4, 0.75), (0.65, 0.995)], track_width = 1,
        bump_scale=20, gauss_range=5, sigma=0.6
    ):
    """
    Creates 3 sets of 2D points defining a closed track
        

    :param density: point density
    :param ellipse_shape: length of the major & minor axis (stretching)
    :param bumps: list of 2-tuples, location of bumps (deformations) on the track e.g. [(0, 0.2)] = a single bump at the beginning.
        Values between 0 & 1.

    :param track_width: distance between corresponding inner & outer points
    :param bump_scale: the "size" of the bump
    :param sigma: gauss sigma

    :returns: 3-tuple -> points on the center line, points on the inside of track, points on the outside of the track
    """


    N_POINTS = 2000

    points = np.zeros((N_POINTS, 2))
    u, v = ellipse_shape

    for i in range(N_POINTS):
        angle = i/N_POINTS * 2*math.pi
        points[i] = [u * math.cos(angle), v * math.sin(angle)]

    for start, stop in bumps:
        start = int(start * N_POINTS)
        stop = int(stop * N_POINTS)

        sample = points[start:stop, :]
        size = stop - start
        middle = points[start + int(size /2), :]
        middle = middle / np.linalg.norm(middle)

        for i in range(stop-start):
            x = gauss_range * (i - size/2) / size
            shift = bump_scale * middle * gaussian(x, sigma)
            sample[i] = sample[i] - shift

        points[start:stop, :] = sample



    points_inner = np.zeros((N_POINTS, 2))
    points_outer = np.zeros((N_POINTS, 2))

    for i in range(N_POINTS - 1):
        a = points[i, :]
        b = points[i+1, :]

        p1, p2 = perpendicular_points(a, b, width=track_width)
        points_inner[i] = p1
        points_outer[i] = p2

    p1, p2 = perpendicular_points(points[-1, :], points[0, :], width=track_width)
    points_inner[-1] = p1
    points_outer[-1] = p2

    step = int(N_POINTS / (density * N_POINTS))

    return points[::step], points_inner[::step], points_outer[::step]




def perpendicular_points(a, b, width=1):
    """
    Creates two points perpendicular to the vector joining a & b

    :param a: 2D point on the centerline
    :param b: 2D point on the centerline
    :param width=1: the track width
    """

    x1, y1 = a
    x2, y2 = b

    vec = [x2-x1, y2-y1]
    perp = [-vec[1], vec[0]]
    perp = np.array(perp)
    perp = perp / np.linalg.norm(perp)

    p1 = a + width*perp
    p2 = a - width*perp

    return p1, p2



if __name__ == '__main__':
    center, inner, outer = make_track()

    # center, inner, outer = make_track(bumps=[(0.1, 0.5), (0.6, 0.9)])

    # center, inner, outer = make_track(bumps=[(0.5, 0.9)], sigma=0.5, bump_scale=25)



    # plt.scatter(center[:, 0], center[:, 1], s=1)
    plt.scatter(inner[:, 0], inner[:, 1], s=1)
    plt.scatter(outer[:, 0], outer[:, 1], s=1)
    plt.axis('equal')
    plt.show()


    # save the track
    # np.save('center.npy', center)
    # np.save('inner.npy', center)
    # np.save('outer.npy', center)

