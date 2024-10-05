"""Implements all the functions to communicate with other Python modules (PIL,
matplotlib, mayavi, etc.)
"""

import numpy as np


def mplfig_to_npimage(fig):
    """Converts a matplotlib figure to a RGB frame after updating the canvas."""
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    canvas = FigureCanvasAgg(fig)
    canvas.draw()  # update/draw the elements

    # get the width and the height to resize the matrix
    _l, _b, w, h = canvas.figure.bbox.bounds
    w, h = int(w), int(h)

    #  exports the canvas to a numpy array using buffer_rgba
    buf = canvas.buffer_rgba()
    # Convert RGBA to RGB
    image = np.asarray(buf)[:, :, :3]
    return image
