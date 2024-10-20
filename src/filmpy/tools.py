import os
import subprocess as sp
import warnings

import proglog

OS_NAME = os.name


def cross_platform_popen_params(popen_params):
    """Adjust subprocess parameters for cross-platform compatibility.
    Parameters:
        - popen_params (dict): Dictionary containing parameters for the subprocess.
    Returns:
        - dict: Updated dictionary of subprocess parameters with platform-specific adjustments.
    Example:
        - cross_platform_popen_params({"some_param": "value"}) -> {"some_param": "value", "creationflags": 0x08000000} on Windows
    """
    if OS_NAME == "nt":
        popen_params["creationflags"] = 0x08000000
    return popen_params


def subprocess_call(cmd, logger="bar"):
    """Execute a subprocess command and log its status.
    Parameters:
        - cmd (list of str): The command to execute as a list of strings.
        - logger (str or Logger, optional): Logger for status messages, default is "bar".
    Returns:
        - None: This function does not return a value but raises an OSError on failure.
    Example:
        - subprocess_call(["echo", "Hello World"], logger="bar") -> None
    """
    logger = proglog.default_bar_logger(logger)
    logger(message="filmpy - Running:\n>>> " + " ".join(cmd))

    popen_params = cross_platform_popen_params(
        {"stdout": sp.DEVNULL, "stderr": sp.PIPE, "stdin": sp.DEVNULL}
    )

    proc = sp.Popen(cmd, **popen_params)

    _out, err = proc.communicate()  # proc.wait()
    proc.stderr.close()

    if proc.returncode:
        logger(message="filmpy - Command returned an error")
        raise OSError(err.decode("utf8"))
    else:
        logger(message="filmpy - Command successful")

    del proc


def convert_to_seconds(time):
    """Convert a time value to seconds.
    Parameters:
        - time (str or list/tuple of floats): The time input to convert, either as a string in "HH:MM:SS" format or as a list/tuple of floats representing hours, minutes, and seconds.
    Returns:
        - float: The time converted into seconds.
    Example:
        - convert_to_seconds("1:30:15") -> 5415.0
    """
    factors = (1, 60, 3600)

    if isinstance(time, str):
        time = [float(part.replace(",", ".")) for part in time.split(":")]

    if not isinstance(time, (tuple, list)):
        return time

    return sum(mult * part for mult, part in zip(factors, reversed(time)))


# Non-exhaustive dictionary to store default information.
# Any addition is most welcome.
# Note that 'gif' is complicated to place. From a VideoFileClip point of view,
# it is a video, but from a HTML5 point of view, it is an image.

extensions_dict = {
    "mp4": {"type": "video", "codec": ["libx264", "libmpeg4", "aac"]},
    "mkv": {"type": "video", "codec": ["libx264", "libmpeg4", "aac"]},
    "ogv": {"type": "video", "codec": ["libtheora"]},
    "webm": {"type": "video", "codec": ["libvpx"]},
    "avi": {"type": "video"},
    "mov": {"type": "video"},
    "ogg": {"type": "audio", "codec": ["libvorbis"]},
    "mp3": {"type": "audio", "codec": ["libmp3lame"]},
    "wav": {"type": "audio", "codec": ["pcm_s16le", "pcm_s24le", "pcm_s32le"]},
    "m4a": {"type": "audio", "codec": ["libfdk_aac"]},
    **{ext: {"type": "image"} for ext in ["jpg", "jpeg", "png", "bmp", "tiff"]},
}


def find_extension(codec):
    """Finds the file extension for a given codec.
    Parameters:
        - codec (str): The codec for which the file extension is needed.
    Returns:
        - str: The file extension associated with the given codec.
    Example:
        - find_extension('aac') -> 'mp4'
    """
    if codec in extensions_dict:
        # codec is already the extension
        return codec

    for ext, infos in extensions_dict.items():
        if codec in infos.get("codec", []):
            return ext
    raise ValueError(
        "The audio_codec you chose is unknown by filmpy. "
        "You should report this. In the meantime, you can "
        "specify a temp_audiofile with the right extension "
        "in write_videofile."
    )
