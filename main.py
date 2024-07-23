import asyncio

import numpy as np
from scipy.spatial.distance import cdist


class Scena:
    def __init__(self, sides=3):
        self.sides = sides

    def generate_polygon_points(self, n, radius, center):
        angle_step = 2.0 / n
        points = [
            (
                center[0] + radius * np.cos(i * angle_step),
                center[1] + radius * np.sin(i * angle_step),
            )
            for i in range(n)
        ]
        return points

    def calculate_perimeter(self, points):
        points_array = np.array(points)
        n = len(points_array)
        perimeter = 0
        for i in range(n - 1):
            perimeter += np.linalg.norm(points_array[i] - points_array[i + 1])
        perimeter += np.linalg.norm(points_array[-1] - points_array[0])
        return perimeter

    def calculate_diameter(self, points):
        points_array = np.array(points)
        distances = cdist(points_array, points_array)
        return np.max(distances)

    async def update_polygon(self):
        while True:
            points = self.generate_polygon_points(self.sides, 100, (150, 150))
            perimeter = self.calculate_perimeter(points)
            diameter = self.calculate_diameter(points)
            pi_estimate = perimeter / diameter if diameter != 0 else 0
            print("\033[H\033[J", end="")
            print(f"Number of Sides: {self.sides}")
            print(f"Diameter: {diameter}")
            print(f"Perimeter: {perimeter}")
            print(f"Pi Estimate: {pi_estimate}")
            print()

            self.sides += 1
            await asyncio.sleep(0.01)


async def main():
    ping = Scena()
    await ping.update_polygon()


asyncio.run(main())
