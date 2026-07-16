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
    rotate_grid: float = 0.0