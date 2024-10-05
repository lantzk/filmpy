import math
import warnings
import numpy as np

try:
    from PIL import Image, ImageChops
    PIL_INSTALLED = True
except ImportError:
    PIL_INSTALLED = False
    Image = None
    ImageChops = None

PIL_rotate_kwargs_supported = {
    "fillcolor": ["bg_color", False, (5, 2, 0)],
    "center": ["center", False, (4, 0, 0)],
    "translate": ["translate", False, (4, 0, 0)],
}

if PIL_INSTALLED and hasattr(Image, "__version__"):
    PIL__version_info__ = tuple(int(n) for n in Image.__version__.split('.') if n.isdigit())
    for PIL_rotate_kw_name, support_data in PIL_rotate_kwargs_supported.items():
        if PIL__version_info__ >= support_data[2]:
            PIL_rotate_kwargs_supported[PIL_rotate_kw_name][1] = True

def rotate(
    clip,
    angle,
    unit="deg",
    resample="bicubic",
    expand=True,
    center=None,
    translate=None,
    bg_color=None,
):
    if resample not in ["bilinear", "nearest", "bicubic"]:
        raise ValueError(
            "'resample' argument must be either 'bilinear', 'nearest' or 'bicubic'"
        )

    def simple_rotate_90(frame, k):
        return np.rot90(frame, k)

    def filter(get_frame, t):
        frame = get_frame(t)
        current_angle = angle(t) if callable(angle) else angle
        
        if unit == "rad":
            current_angle = math.degrees(current_angle)

        # Handle simple 90-degree rotations without PIL
        if current_angle % 90 == 0 and not center and not translate and not bg_color:
            k = int(current_angle // 90 % 4)
            return simple_rotate_90(frame, k)

        if not PIL_INSTALLED or Image is None:
            raise ValueError(
                'Without "Pillow" installed, only angles that are a multiple of 90'
                ' degrees are supported, and "center", "translate", and "bg_color"'
                ' must not be used.'
            )

        # PIL-based rotation
        if isinstance(frame, list):
            frame = np.array([[ord(char) for char in row] for row in frame])
        
        # Handle mask clips
        if clip.is_mask:
            frame = (frame * 255).astype(np.uint8)
            img = Image.fromarray(frame, mode='L')
        else:
            img = Image.fromarray(frame.astype(np.uint8))

        _bg_color = bg_color if bg_color is not None else (0 if clip.is_mask else (0, 0, 0))

        kwargs = {'expand': expand}
        for PIL_rotate_kw_name, (kw_name, supported, min_version) in PIL_rotate_kwargs_supported.items():
            kw_value = locals().get(kw_name)
            if kw_value is not None:
                if supported:
                    kwargs[PIL_rotate_kw_name] = kw_value
                else:
                    warnings.warn(
                        f"rotate '{kw_name}' argument is not supported by your"
                        " Pillow version and is being ignored. Minimum Pillow version"
                        f" required: v{'.'.join(str(n) for n in min_version)}"
                    )

        # Ensure 'fillcolor' is always in kwargs
        if 'fillcolor' not in kwargs:
            kwargs['fillcolor'] = _bg_color

        rotated = img.rotate(
            current_angle,
            resample=getattr(Image, resample.upper()),
            **kwargs
        )

        if translate and PIL_rotate_kwargs_supported["translate"][1]:
            rotated = ImageChops.offset(rotated, int(translate[0]), int(translate[1]))

        result = np.array(rotated)
        
        # Convert back to float for mask clips
        if clip.is_mask:
            result = result.astype(float) / 255.0

        return result

    return clip.transform(filter, apply_to=["mask"])