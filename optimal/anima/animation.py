import math
import time
from dataclasses import dataclass, field
from typing import Protocol, Self

from graphics import GraphicsRenderer, Color, ShapeData

class AnimationStep(Protocol):
    def apply(self, shape: ShapeData, color: Color, t: float) -> tuple[ShapeData, Color]:
        """

        :param shape:
        :param color:
        :param t: 0-1,the local progress through this step.
        :return: position and color after moving the shape.
        """
        ...

#helper function for interpolation
def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


@dataclass
class Move:
    dx: float
    dy: float

    def apply(
            self,
            shape: ShapeData,
            color: Color,
            t: float,
    ) -> tuple[ShapeData, Color]:
        new_points = [(x + self.dx * t, y +self.dy * t) for (x, y) in shape]
        return new_points, color

@dataclass
class Rotate:
    angle: float

    def apply(
        self,
        shape: ShapeData,
        color: Color,
        t: float,
    ) -> tuple[ShapeData, Color]:
        theta = math.radians(self.angle * t)
        #center point
        cx = sum(x for (x, _) in shape) / len(shape)
        cy = sum(y for (_, y) in shape) / len(shape)

        out: ShapeData = []
        for (x, y) in shape:
            nx = cx + (x -cx) * math.cos(theta) - (y - cy) * math.sin(theta)
            ny = cy + (x -cx) * math.sin(theta) + (y - cy) * math.cos(theta)
            out.append((nx, ny))

        return out, color

@dataclass
class Scale:
    factor: float
    def apply(
            self, shape: ShapeData, color: Color, t: float) -> tuple[ShapeData, Color]:
        cx = sum(x for x, _ in shape) / len(shape)
        cy = sum(y for _, y in shape) / len(shape)

        s = lerp(1.0, self.factor, t)
        new_points = [(cx + (x-cx) * s, cy + (y-cy) * s) for (x,y) in shape]

        return new_points, color

@dataclass
class Fade:
    brightness: float
    def apply(
        self, shape: ShapeData, color: Color, t: float
    ) -> tuple[ShapeData, Color]:
        current_val = int(color[1:3], 16)
        new_val = int(lerp(current_val, self.brightness, t))
        new_color = f"#{new_val:02x}{new_val:02x}{new_val:02x}"
        return shape, new_color

@dataclass
class Animation:
    steps: list[AnimationStep] = field(default_factory=list)
    durations: list[float] = field(default_factory=list)
    start_time: float = 0.0

    def add(self, step: AnimationStep, duration: float) -> Self:
        self.steps.append(step)
        self.durations.append(duration)
        return self

    def move(self, dx: float, dy: float, duration: float) -> Self:
        return self.add(Move(dx, dy), duration)

    def rotate(self, angle: float, duration: float) -> Self:
        return self.add(Rotate(angle), duration)

    def scale(self, factor: float, duration: float) -> Self:
        return self.add(Scale(factor), duration)

    def fade_to(self, brightness: float, duration: float) -> Self:
        return self.add(Fade(brightness), duration)

    @property
    def duration(self) -> float:
        return sum(self.durations)

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration


@dataclass
class Shape:
    shape_id: str
    points: ShapeData
    color: Color = "#444444"
    animation: Animation | None = None

def play_scene(renderer: GraphicsRenderer, shapes: list[Shape]) -> None:
    animations = [s.animation for s in shapes if s.animation is not None]
    if not animations:
        return

    global_end = max(anim.end_time for anim in animations)
    t0 = time.time()

    while True:
        now = time.time() - t0
        finished = True
        for shape in shapes:
            anim = shape.animation
            if anim is None:
                continue

            if not (anim.start_time <= now <= anim.end_time):
                continue

            finished = False

            t_anim = now - anim.start_time
            time_cursor = 0.0

            points = shape.points
            color = shape.color

            for step, duration in zip(anim.steps, anim.durations):
                if duration <= 0:
                    continue

                local_t_raw = (t_anim - time_cursor) / duration
                local_t = max(0.0, min(1.0, local_t_raw))

                points, color = step.apply(points, color, local_t)

                if local_t < 1.0:
                    break

                time_cursor += duration

            renderer.render(shape.shape_id, points, color)

        if finished and now >= global_end:
            break

        time.sleep(0.01)


