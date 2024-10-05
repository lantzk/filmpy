"""filmpy editor tests."""

import importlib
import io
import sys
from contextlib import redirect_stdout

import pytest

from filmpy.audio.AudioClip import AudioClip
from filmpy.video.VideoClip import VideoClip


def test_preview_methods():
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        try:
            preview_module = importlib.import_module("filmpy.video.io.preview")
            assert preview_module.preview.__hash__() != VideoClip.preview.__hash__()
        except ImportError:
            editor_module = importlib.import_module("filmpy.editor")
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
            editor_module = importlib.import_module("filmpy.editor")
            assert (
                editor_module.VideoClip.preview.__hash__()
                == preview_module.preview.__hash__()
            )
        finally:
            if "filmpy.editor" in sys.modules:
                del sys.modules["filmpy.editor"]

        try:
            importlib.import_module("matplotlib.pyplot")
        except ImportError:
            editor_module = importlib.import_module("filmpy.editor")
            with pytest.raises(ImportError) as exc:
                editor_module.sliders()

            assert str(exc.value) == "sliders requires matplotlib installed"

            del sys.modules["filmpy.editor"]
        else:
            del sys.modules["matplotlib.pyplot"]

    del sys.modules["filmpy"]


def test__init__preview_methods():
    filmpy_module = importlib.import_module("filmpy")

    with pytest.raises(ImportError) as exc:
        filmpy_module.VideoClip.preview(True)
    assert str(exc.value) == "clip.preview requires importing from filmpy.editor"

    with pytest.raises(ImportError) as exc:
        filmpy_module.VideoClip.show(True)
    assert str(exc.value) == "clip.show requires importing from filmpy.editor"

    del sys.modules["filmpy"]


if __name__ == "__main__":
    pytest.main()
