from dataclasses import dataclass


@dataclass
class Settings:
    # Размер изделия
    panel_width_mm: float = 450.0
    panel_height_mm: float = 600.0

    # Отверстия
    min_diameter: float = 1.0
    max_diameter: float = 4.0
    bridge: float = 2.5

    # Инструмент
    vbit_angle: float = 90.0
    tip_diameter: float = 0.5

    # Алгоритм
    gamma: float = 1.8

    # Обработка изображения
    clahe_clip: float = 2.0
    blur: int = 1
    sharpen: bool = False

    # Сетка
    grid_step: float = 5.0
    rotate_grid: float = 0.0

    preview_pixels_per_mm: int = 2
    export_pixels_per_mm: int = 10

    # Положение изображения
    image_scale: float = 1.0
    offset_x_mm: float = 0.0
    offset_y_mm: float = 0.0