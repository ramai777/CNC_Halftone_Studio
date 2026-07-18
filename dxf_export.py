class DXFExporter:
    """
    Экспорт отверстий в DXF R12.
    Пока сохраняет окружности.
    """

    def export(self, filename, holes):

        with open(filename, "w") as f:

            # HEADER
            f.write("0\nSECTION\n")
            f.write("2\nHEADER\n")
            f.write("0\nENDSEC\n")

            # TABLES
            f.write("0\nSECTION\n")
            f.write("2\nTABLES\n")
            f.write("0\nENDSEC\n")

            # ENTITIES
            f.write("0\nSECTION\n")
            f.write("2\nENTITIES\n")

            for hole in holes:

                radius = hole.diameter / 2

                f.write("0\nCIRCLE\n")
                f.write("8\n0\n")          # слой
                f.write(f"10\n{hole.x}\n") # X
                f.write(f"20\n{hole.y}\n") # Y
                f.write("30\n0\n")         # Z
                f.write(f"40\n{radius}\n") # Радиус

            f.write("0\nENDSEC\n")
            f.write("0\nEOF\n")