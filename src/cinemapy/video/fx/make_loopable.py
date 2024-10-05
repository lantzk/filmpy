import filmpy.video.compositing.transitions as transfx
from filmpy.decorators import requires_duration
from filmpy.video.compositing.CompositeVideoClip import CompositeVideoClip


@requires_duration
def make_loopable(clip, overlap_duration):
    """Makes the clip fade in progressively at its own end, this way it can be
    looped indefinitely.

    Parameters
    ----------

    overlap_duration : float
      Duration of the fade-in (in seconds).
    """
    clip2 = clip.fx(transfx.crossfadein, overlap_duration).with_start(
        clip.duration - overlap_duration
    )
    return CompositeVideoClip([clip, clip2]).subclip(overlap_duration, clip.duration)
