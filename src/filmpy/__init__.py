"""Imports everything that you need from the filmpy submodules so that every thing
can be directly imported like `from filmpy import VideoFileClip`.

In particular it loads all effects from the video.fx and audio.fx folders
and turns them into VideoClip and AudioClip methods, so that instead of
``clip.fx(vfx.resize, 2)`` or ``vfx.resize(clip, 2)``
you can write ``clip.resize(2)``.
"""

import inspect

from filmpy.audio import fx as afx
from filmpy.audio.AudioClip import (
    AudioClip,
    CompositeAudioClip,
    concatenate_audioclips,
)
from filmpy.audio.io.AudioFileClip import AudioFileClip
from filmpy.tools import convert_to_seconds
from filmpy.version import __version__
from filmpy.video import fx as vfx
from filmpy.video import tools as videotools
from filmpy.video.compositing import transitions as transfx
from filmpy.video.compositing.CompositeVideoClip import (
    CompositeVideoClip,
    clips_array,
)
from filmpy.video.compositing.concatenate import concatenate_videoclips
from filmpy.video.io import ffmpeg_tools
from filmpy.video.io.downloader import download_webfile
from filmpy.video.io.ImageSequenceClip import ImageSequenceClip
from filmpy.video.io.VideoFileClip import VideoFileClip
from filmpy.video.VideoClip import (
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
    """NOT AVAILABLE: clip.preview requires importing from filmpy.editor"""
    raise ImportError("clip.preview requires importing from filmpy.editor")


def show(self, *args, **kwargs):
    """NOT AVAILABLE: clip.show requires importing from filmpy.editor"""
    raise ImportError("clip.show requires importing from filmpy.editor")


VideoClip.preview = preview
VideoClip.show = show
AudioClip.preview = preview

# Cleanup namespace
del audio_fxs, video_fxs, name, function, preview, show
del inspect

# Importing with `from filmpy import *` will only import these names
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
