import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

from track import make_track


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.15, bottom=0.35)

bumps = [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 0.99)]
_, inner, outer = make_track(bumps=bumps)

ax.scatter(inner[:, 0], inner[:, 1], s=1)
ax.scatter(outer[:, 0], outer[:, 1], s=1)

ax.set_aspect('equal', adjustable='box')

axcolor = 'lightgoldenrodyellow'
a_sigma = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
a_gauss = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
a_density = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
a_bump = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
a_u = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
a_v = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)


sigma_slider = Slider(a_sigma, 'Sigma', 0.1, 2.0, valinit=0.6, valstep=0.01)
track_slider = Slider(a_gauss, 'Track width', 0.5, 5, valinit=1, valstep=0.1)
density_slider = Slider(a_density, 'Density', 0.01, 0.3, valinit=0.05, valstep=0.01)
bump_slider = Slider(a_bump, 'Scale', 1.0, 40.0, valinit=20, valstep=0.1)

ellispse_u_slider = Slider(a_u, 'Stretch horizontally', 1.0, 100, valinit=40, valstep=0.5)
ellispse_v_slider = Slider(a_v, 'Stretch vertically', 1.0, 100.0, valinit=24, valstep=0.5)



def update(val):
    sigma = sigma_slider.val
    track_width = track_slider.val
    density = density_slider.val
    scale = bump_slider.val
    u = ellispse_u_slider.val
    v = ellispse_v_slider.val

    ax.clear()
    _, inner, outer = make_track(
        sigma=sigma, track_width=track_width, bumps=bumps,
        density=density, bump_scale=scale, ellipse_shape=(u, v)
    )
    ax.scatter(inner[:, 0], inner[:, 1], s=1)
    ax.scatter(outer[:, 0], outer[:, 1], s=1)
    ax.set_aspect('equal', adjustable='box')
    fig.canvas.draw_idle()


sigma_slider.on_changed(update)
track_slider.on_changed(update)
density_slider.on_changed(update)
bump_slider.on_changed(update)
ellispse_u_slider.on_changed(update)
ellispse_v_slider.on_changed(update)


plt.show()