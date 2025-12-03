import gizeh
import moviepy.editor as mpy
import math

# --- Settings ---
width, height = 640, 480  # video size
duration = 5              # duration in seconds
fps = 30                  # frames per second
trail_length = 30         # number of positions in the fading trail

# --- Initialize trail storage ---
def make_frame(t):
    surface = gizeh.Surface(width, height, bg_color=(0, 0, 0))  # black background

    # rotating arm parameters
    center = (width / 2, height / 2)
    radius = 150
    angle = t * 2 * math.pi / duration  # one full rotation over duration
    arm_tip_pos = (center[0] + radius * math.cos(angle),
                   center[1] + radius * math.sin(angle))

    arm_color = (1, 0, 0, 0.8)  # red arm
    joint_color = (1, 1, 1, 1)  # white joint

    # draw arm
    gizeh.line(start=center, end=arm_tip_pos, stroke=arm_color, stroke_width=6).draw(surface)
    # draw joint at tip
    gizeh.circle(r=10, xy=arm_tip_pos, fill=joint_color).draw(surface)

    # initialize trail positions if not already
    if not hasattr(make_frame, "trail_positions"):
        make_frame.trail_positions = []

    # update trail
    make_frame.trail_positions.append(arm_tip_pos)
    # keep only last N positions
    make_frame.trail_positions = make_frame.trail_positions[-trail_length:]

    # draw fading trail
    for i, pos in enumerate(make_frame.trail_positions):
        alpha = (i + 1) / trail_length
        gizeh.circle(r=8, xy=pos, fill=(1, 1, 1, alpha * 0.5)).draw(surface)

    return surface.get_npimage()

# --- Create and save video ---
clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_videofile("rotating_trails.mp4", fps=fps)
