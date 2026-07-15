from hexgrid import HexGridGenerator

grid = HexGridGenerator()

points = grid.generate(
    width_mm=450,
    height_mm=600,
    max_diameter=4,
    bridge=2.5
)

print("Количество точек:", len(points))

print("\nПервые 10 точек:\n")

for p in points[:10]:
    print(p)