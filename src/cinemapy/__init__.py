"""Imports everything that you need from the cinemapy submodules so that every thing
can be directly imported like `from cinemapy import VideoFileClip`.

In particular it loads all effects from the video.fx and audio.fx folders
and turns them into VideoClip and AudioClip methods, so that instead of
``clip.fx(vfx.resize, 2)`` or ``vfx.resize(clip, 2)``
you can write ``clip.resize(2)``.
"""

import inspect

from cinemapy.audio import fx as afx
from cinemapy.audio.AudioClip import (
    AudioClip,
    CompositeAudioClip,
    concatenate_audioclips,
)
from cinemapy.audio.io.AudioFileClip import AudioFileClip
from cinemapy.tools import convert_to_seconds
from cinemapy.version import __version__
from cinemapy.video import fx as vfx
from cinemapy.video import tools as videotools
from cinemapy.video.compositing import transitions as transfx
from cinemapy.video.compositing.CompositeVideoClip import (
    CompositeVideoClip,
    clips_array,
)
from cinemapy.video.compositing.concatenate import concatenate_videoclips
from cinemapy.video.io import ffmpeg_tools
from cinemapy.video.io.downloader import download_webfile
from cinemapy.video.io.ImageSequenceClip import ImageSequenceClip
from cinemapy.video.io.VideoFileClip import VideoFileClip
from cinemapy.video.VideoClip import (
    BitmapClip,
    ColorClip,
    ImageClip,
    TextClip,
    VideoClip,
)

# Transforms the effects into Clip methods so that
# they can be called with clip.resize(width=500) instead of
# clip.fx(vfx.resize, width=500)
audio_fxs = inspect.getmembers(afx, inspect.isfunction) + [("loop", vfx.loop)]
video_fxs = (
    inspect.getmembers(vfx, inspect.isfunction)
    + inspect.getmembers(transfx, inspect.isfunction)
    + audio_fxs
)

for name, function in video_fxs:
    setattr(VideoClip, name, function)

for name, function in audio_fxs:
    setattr(AudioClip, name, function)


def preview(self, *args, **kwargs):
    """NOT AVAILABLE: clip.preview requires importing from cinemapy.editor"""
    raise ImportError("clip.preview requires importing from cinemapy.editor")


def show(self, *args, **kwargs):
    """NOT AVAILABLE: clip.show requires importing from cinemapy.editor"""
    raise ImportError("clip.show requires importing from cinemapy.editor")


VideoClip.preview = preview
VideoClip.show = show
AudioClip.preview = preview

# Cleanup namespace
del audio_fxs, video_fxs, name, function, preview, show
del inspect

# Importing with `from cinemapy import *` will only import these names
__all__ = [
    "__version__",
    "VideoClip",
    "ImageClip",
    "ColorClip",
    "TextClip",
    "BitmapClip",
    "VideoFileClip",
    "CompositeVideoClip",
    "clips_array",
    "ImageSequenceClip",
    "concatenate_videoclips",
    "download_webfile",
    "AudioClip",
    "CompositeAudioClip",
    "concatenate_audioclips",
    "AudioFileClip",
    "vfx",
    "afx",
    "transfx",
    "videotools",
    "ffmpeg_tools",
    "convert_to_seconds",
]
