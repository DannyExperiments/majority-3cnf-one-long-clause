"""Render the graph join at the inclusive threshold from a rotating 3D view."""

from math import cos, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 800, 480
BACKGROUND, PANEL = "#101b2e", "#182942"
INK, MUTED = "#f3f7ff", "#bacce4"
SOURCE, PADDING, CROSS = "#7be4d3", "#ffc48a", "#829bbd"
NODES = [
    ("A", -0.96, -0.67, -0.78), ("B", 0.96, -0.67, -0.78),
    ("C", 0.96, 0.67, -0.78), ("D", -0.96, 0.67, -0.78),
    ("E", -0.62, -0.13, 0.80), ("F", 0.62, 0.13, 0.80),
]
SOURCE_EDGES = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
PADDING_EDGES = [(4, 5)]
JOIN_EDGES = [(u, v) for u in range(4) for v in range(4, 6)]


def font(name, size):
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default(size=size)


def project(node, angle):
    label, x, y, z = node
    screen_x = x * cos(angle) - y * sin(angle)
    toward = x * sin(angle) + y * cos(angle)
    screen_y = z * cos(.33) - toward * sin(.33)
    depth = toward * cos(.33) + z * sin(.33)
    zoom = 7 / (7 - depth)
    return label, 430 + screen_x * 149 * zoom, 232 - screen_y * 84 * zoom, depth, zoom


def draw_frame(angle, fonts):
    title, label, node_label, equation = fonts
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.text((29, 23), "Shift the threshold to eight", fill=INK, font=title)
    draw.rounded_rectangle((27, 91, 773, 368), 15, fill=PANEL)

    projected = [project(node, angle) for node in NODES]
    for edges, color, width in [(JOIN_EDGES, CROSS, 2), (SOURCE_EDGES, SOURCE, 5),
                                (PADDING_EDGES, PADDING, 5)]:
        for u, v in edges:
            draw.line([projected[u][1:3], projected[v][1:3]], fill=color, width=width)
    for index in sorted(range(len(projected)), key=lambda i: projected[i][3]):
        name, x, y, _, zoom = projected[index]
        radius = 15 * zoom
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=SOURCE if index < 4 else PADDING,
                     outline=PANEL, width=2)
        draw.text((x, y+1), name, fill=BACKGROUND, font=node_label, anchor="mm")

    draw.text((47, 121), "Padding", fill=PADDING, font=label)
    draw.text((48, 161), "3 sets", fill=INK, font=label)
    draw.text((47, 271), "Input", fill=SOURCE, font=label)
    draw.text((48, 311), "6 sets", fill=INK, font=label)
    draw.text((29, 385), "6 + 3 − 1 = 8", fill=INK, font=equation)
    draw.text((352, 392), "Equal to eight. Accept.", fill=SOURCE, font=label)
    draw.text((30, 442), "Subtract one for the shared empty set.", fill=MUTED, font=label)
    return image


def main():
    fonts = (font("Arial Bold.ttf", 45), font("Arial.ttf", 28),
             font("Arial Bold.ttf", 19), font("Arial Bold.ttf", 40))
    frames = [draw_frame(tau*i/72 - .23, fonts) for i in range(72)]
    frames[0].save(Path(__file__).with_name("threshold-join.gif"), save_all=True,
                   append_images=frames[1:], duration=86, loop=0, optimize=False)


if __name__ == "__main__":
    main()
