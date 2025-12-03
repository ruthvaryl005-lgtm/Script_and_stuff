import gizeh
import moviepy.editor as mpy
import numpy as np
from math import sin, cos, pi

# --- Animation settings ---
W, H = 512, 512          # Frame width & height
duration = 5             # Video duration in seconds
fps = 24
center = (W / 2, H / 2)
num_arms = 4
arm_length = W / 4

def make_frame(t):
    # Create a black background surface
    surface = gizeh.Surface(W, H, bg_color=(0, 0, 0))

    # Draw reference circle
    gizeh.circle(r=W / 2.2, xy=center, stroke=(0.1, 0.1, 0.1), stroke_width=5).draw(surface)

    # Initialize trail storage if it doesn't exist
    if not hasattr(make_frame, "trail_positions"):
        make_frame.trail_positions = []

    for i in range(num_arms):
        # Calculate rotation
        angle = 2 * pi * ((i + 1) * 0.1 * t + i * 0.5)
        x = center[0] + arm_length * cos(angle)
        y = center[1] + arm_length * sin(angle)
        arm_tip_pos = (x, y)

        # Color gradient
        r = (sin(i + t * 0.5) + 1) / 2
        g = (sin(i + t * 0.5 + 2 * pi / 3) + 1) / 2
        b = (sin(i + t * 0.5 + 4 * pi / 3) + 1) / 2
        arm_color = (r, g, b, 0.8)

        # Draw the arm
        arm = gizeh.rectangle(
            lx=arm_length * 2,
            ly=20,
            xy=(center[0] + arm_length / 2, center[1]),
            fill=arm_color,
            angle=angle
        )
        arm.draw(surface)

        # Draw joint circle
        joint_circle = gizeh.circle(
            r=10 + sin(t * 3) * 3,
            xy=arm_tip_pos,
            fill=arm_color
        )
        joint_circle.draw(surface)

        # Update trail
        make_frame.trail_positions.append(arm_tip_pos)

    # Keep only the last N positions for fading trail
    trail_length = 30
    make_frame.trail_positions = make_frame.trail_positions[-trail_length:]

    # Draw fading trail
    for j, pos in enumerate(make_frame.trail_positions):
        alpha = (j + 1) / trail_length
        gizeh.circle(r=8, xy=pos, fill=(1, 1, 1, alpha * 0.5)).draw(surface)

    return surface.get_npimage()

# --- Create the video ---
clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_videofile("rotating_trails.mp4", fps=fps)
