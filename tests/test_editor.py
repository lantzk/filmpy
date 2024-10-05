"""cinemapy editor tests."""

import importlib
import io
import sys
from contextlib import redirect_stdout

import pytest

from cinemapy.audio.AudioClip import AudioClip
from cinemapy.video.VideoClip import VideoClip


def test_preview_methods():
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        try:
            preview_module = importlib.import_module("cinemapy.video.io.preview")
            assert preview_module.preview.__hash__() != VideoClip.preview.__hash__()
        except ImportError:
            editor_module = importlib.import_module("cinemapy.editor")
            with pytest.raises(ImportError) as exc:
                VideoClip.preview(True)
            assert str(exc.value) == "clip.preview requires Pygame installed"

            with pytest.raises(ImportError) as exc:
                VideoClip.show(True)
            assert str(exc.value) == "clip.show requires Pygame installed"

            with pytest.raises(ImportError) as exc:
                AudioClip.preview(True)
            assert str(exc.value) == "clip.preview requires Pygame installed"
        else:
            editor_module = importlib.import_module("cinemapy.editor")
            assert (
                editor_module.VideoClip.preview.__hash__()
                == preview_module.preview.__hash__()
            )
        finally:
            if "cinemapy.editor" in sys.modules:
                del sys.modules["cinemapy.editor"]

        try:
            importlib.import_module("matplotlib.pyplot")
        except ImportError:
            editor_module = importlib.import_module("cinemapy.editor")
            with pytest.raises(ImportError) as exc:
                editor_module.sliders()

            assert str(exc.value) == "sliders requires matplotlib installed"

            del sys.modules["cinemapy.editor"]
        else:
            del sys.modules["matplotlib.pyplot"]

    del sys.modules["cinemapy"]


def test__init__preview_methods():
    cinemapy_module = importlib.import_module("cinemapy")

    with pytest.raises(ImportError) as exc:
        cinemapy_module.VideoClip.preview(True)
    assert str(exc.value) == "clip.preview requires importing from cinemapy.editor"

    with pytest.raises(ImportError) as exc:
        cinemapy_module.VideoClip.show(True)
    assert str(exc.value) == "clip.show requires importing from cinemapy.editor"

    del sys.modules["cinemapy"]


if __name__ == "__main__":
    pytest.main()
