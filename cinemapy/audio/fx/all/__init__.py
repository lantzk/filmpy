"""
cinemapy.audio.fx.all is deprecated.

Use the fx method directly from the clip instance (e.g. ``clip.audio_normalize(...)``)
or import the function from cinemapy.audio.fx instead.
"""

import warnings

from .. import *  # noqa 401,F403

warnings.warn(f"\ncinemapy: {__doc__}", UserWarning)
