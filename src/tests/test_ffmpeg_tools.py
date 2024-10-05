"""FFmpeg tools tests for cinemapy."""

import contextlib
import os
import shutil

import pytest

from cinemapy.video.io.ffmpeg_tools import (
    ffmpeg_extract_subclip,
    ffmpeg_resize,
    ffmpeg_stabilize_video,
)
from cinemapy.video.io.VideoFileClip import VideoFileClip


def test_ffmpeg_extract_subclip(util):
    extract_subclip_tempdir = os.path.join(
        util.TMP_DIR, "cinemapy_ffmpeg_extract_subclip"
    )
    if os.path.isdir(extract_subclip_tempdir):
        shutil.rmtree(extract_subclip_tempdir)
    os.mkdir(extract_subclip_tempdir)

    inputfile = os.path.join(extract_subclip_tempdir, "fire2.mp4")
    shutil.copyfile("media/fire2.mp4", inputfile)

    # default name
    expected_outputfile = os.path.join(extract_subclip_tempdir, "fire2SUB300_500.mp4")
    ffmpeg_extract_subclip(inputfile, 0.3, "00:00:00,5", logger=None)
    assert os.path.isfile(expected_outputfile)

    # custom name
    expected_outputfile = os.path.join(extract_subclip_tempdir, "foo.mp4")
    ffmpeg_extract_subclip(
        inputfile, 0.3, "00:00:00,5", outputfile=expected_outputfile, logger=None
    )
    assert os.path.isfile(expected_outputfile)

    # assert subclip duration
    clip = VideoFileClip(expected_outputfile)
    assert 0.18 <= clip.duration <= 0.22  # not accurate

    if os.path.isdir(extract_subclip_tempdir):
        with contextlib.suppress(PermissionError):
            shutil.rmtree(extract_subclip_tempdir)


def test_ffmpeg_resize(util):
    outputfile = os.path.join(util.TMP_DIR, "cinemapy_ffmpeg_resize.mp4")
    if os.path.isfile(outputfile):
        os.remove(outputfile)

    expected_size = (30, 30)

    ffmpeg_resize("media/bitmap.mp4", outputfile, expected_size, logger=None)
    assert os.path.isfile(outputfile)

    # overwrite file
    with pytest.raises(OSError):
        ffmpeg_resize("media/bitmap.mp4", outputfile, expected_size, logger=None)

    clip = VideoFileClip(outputfile)
    assert clip.size[0] == expected_size[0]
    assert clip.size[1] == expected_size[1]

    if os.path.isfile(outputfile):
        with contextlib.suppress(PermissionError):
            os.remove(outputfile)


def test_ffmpeg_stabilize_video(util):
    stabilize_video_tempdir = os.path.join(util.TMP_DIR, "cinemapy_ffmpeg_stabilize")
    if os.path.isdir(stabilize_video_tempdir):
        shutil.rmtree(stabilize_video_tempdir)
    os.mkdir(stabilize_video_tempdir)

    # no output file
    ffmpeg_stabilize_video(
        "media/bitmap.mp4",
        output_dir=stabilize_video_tempdir,
        logger=None,
    )

    expected_filepath = os.path.join(stabilize_video_tempdir, "bitmap_stabilized.mp4")
    assert os.path.isfile(expected_filepath)

    # with output file
    ffmpeg_stabilize_video(
        "media/bitmap.mp4",
        output_dir=stabilize_video_tempdir,
        outputfile="foo.mp4",
        logger=None,
    )
    expected_filepath = os.path.join(stabilize_video_tempdir, "foo.mp4")
    assert os.path.isfile(expected_filepath)

    # don't overwrite file
    with pytest.raises(OSError):
        ffmpeg_stabilize_video(
            "media/bitmap.mp4",
            output_dir=stabilize_video_tempdir,
            outputfile="foo.mp4",
            overwrite_file=False,
            logger=None,
        )

    if os.path.isdir(stabilize_video_tempdir):
        with contextlib.suppress(PermissionError):
            shutil.rmtree(stabilize_video_tempdir)


if __name__ == "__main__":
    pytest.main()
