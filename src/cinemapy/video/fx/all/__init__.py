"""
cinemapy.video.fx.all is deprecated.

Use the fx method directly from the clip instance (e.g. ``clip.resize(...)``)
or import the function from cinemapy.video.fx instead.
"""

import warnings

from cinemapy.video.fx import *  # noqa F401,F403

warnings.warn(f"\ncinemapy: {__doc__}", UserWarning)
