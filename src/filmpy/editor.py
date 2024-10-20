import os

import filmpy  # So that we can access filmpy.__all__ later
from filmpy import *
from filmpy.video.io.html_tools import ipython_display

try:
    from filmpy.video.io.sliders import sliders
except ImportError:

    def sliders(*args, **kwargs):
        """NOT AVAILABLE: sliders requires matplotlib installed."""
        raise ImportError("sliders requires matplotlib installed")


# adds easy ipython integration
VideoClip.ipython_display = ipython_display
AudioClip.ipython_display = ipython_display

# Hide the welcome message from pygame: https://github.com/pygame/pygame/issues/542
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Add methods preview and show (only if pygame installed)
try:
    from filmpy.video.io.preview import preview, show
except ImportError:

    def preview(self, *args, **kwargs):
        """NOT AVAILABLE: clip.preview requires Pygame installed."""
        raise ImportError("clip.preview requires Pygame installed")

    def show(self, *args, **kwargs):
        """NOT AVAILABLE: clip.show requires Pygame installed."""
        raise ImportError("clip.show requires Pygame installed")


VideoClip.preview = preview
VideoClip.show = show

try:
    from filmpy.audio.io.preview import preview
except ImportError:

    def preview(self, *args, **kwargs):
        """NOT AVAILABLE: clip.preview requires Pygame installed."""
        raise ImportError("clip.preview requires Pygame installed")


AudioClip.preview = preview

__all__ = filmpy.__all__ + ["ipython_display", "sliders"]

del preview, show
