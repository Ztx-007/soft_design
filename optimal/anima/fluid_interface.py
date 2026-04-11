#流畅接口模式
#pandas
#sqlalchemy
#每部操作都返回一个操作对象，可以连续调用方法，即流畅接口模式
#pandas中连续调用方法最终还是返回一个dataframe,而sql中则是构建一个sql操作
#通常流水线工具也是流畅接口模式的绝佳选择


import tkinter as tk
from typing import Any

from animation import Animation, Fade, Move, Rotate, Scale, Shape, play_scene
from graphics import GraphicsRenderer

def main() -> None:
    root = tk.Tk()
    root.title("Optimal Anima")
    canvas = tk.Canvas(root, width=800, height=600, background="white")
    canvas.pack()

    renderer = GraphicsRenderer(canvas)

    #First Version
    # square_animation = Animation(
    #     steps=[
    #         Rotate(60),
    #         Move(200,0),
    #         Scale(1.3),
    #         Fade(200),
    #         Move(0,120),
    #         Fade(40)
    #     ],
    #     durations=[
    #         1.0,
    #         1.0,
    #         1.0,
    #         0.8,
    #         1.0,
    #         0.8
    #     ],
    #     start_time=0.0,
    # )


    #流畅接口模式，a way return self, can chain call
    square_animation = (
        Animation(start_time=0.0)
        .rotate(60,duration=1.0)
        .move(200,0,duration=1.0)
        .scale(1.3,duration=1.0)
        .fade_to(200, duration=0.8)
        .move(0,120, duration=1.0)
        .fade_to(40, duration=0.8)
    )
    #
    square = Shape(
        shape_id="square",
        points=[(250,200),(350,200),(350,300),(250,300)],
        color="#444444",
        animation=square_animation
    )

    shapes = [square]

    #event binding
    def start_animation(event: Any) -> None:
        play_scene(renderer, shapes)

    canvas.bind("<Button-1>", start_animation)
    root.bind("<Key>", start_animation)

    root.mainloop()


if __name__ == "__main__":
    main()