"""Useful utilities working with filmpy."""

from filmpy.audio.io.AudioFileClip import AudioFileClip
from filmpy.video.io.VideoFileClip import VideoFileClip
from filmpy.video.VideoClip import ImageClip

CLIP_TYPES = {
    "audio": AudioFileClip,
    "video": VideoFileClip,
    "image": ImageClip,
}


def close_all_clips(objects="globals", types=("audio", "video", "image")):
    """Close all clips of specified types within a given scope.
    Parameters:
        - objects (str or dict-like, optional): Source of objects to inspect and close clips. Defaults to "globals".
        - types (tuple, optional): Tuple of clip types to close, specified by keys in CLIP_TYPES. Defaults to ("audio", "video", "image").
    Returns:
        - None
    Example:
        - close_all_clips() -> Closes all global audio, video, and image clips.
    """
    if objects == "globals":  # pragma: no cover
        objects = globals()
    if hasattr(objects, "values"):
        objects = objects.values()
    types_tuple = tuple(CLIP_TYPES[key] for key in types)
    for obj in objects:
        if isinstance(obj, types_tuple):
            obj.close()
