# Week 5 - Kinetic Dance Generative Poster
# Arts and Advanced Big Data
# Streamlit web app: from Colab-style generative drawing to the Web

import random
import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import streamlit as st


# ---------- Generative drawing functions ----------

def make_palette(k=7, mode="pastel"):
    """Create a reproducible palette in HSV color space."""
    colors = []

    for _ in range(k):
        if mode == "pastel":
            h = random.random()
            s = random.uniform(0.15, 0.35)
            v = random.uniform(0.88, 1.0)
        elif mode == "vivid":
            h = random.random()
            s = random.uniform(0.75, 1.0)
            v = random.uniform(0.75, 1.0)
        elif mode == "mono":
            h = 0.60
            s = random.uniform(0.20, 0.55)
            v = random.uniform(0.55, 1.0)
        else:
            h = random.random()
            s = random.uniform(0.35, 1.0)
            v = random.uniform(0.55, 1.0)

        colors.append(tuple(hsv_to_rgb([h, s, v])))

    return colors


def blob(center=(0.5, 0.5), radius=0.2, points=180, wobble=0.15):
    """Make an organic blob shape."""
    angles = np.linspace(0, 2 * math.pi, points, endpoint=False)
    radii = radius * (
        1 + wobble * (np.random.rand(points) - 0.5)
    )

    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)

    return x, y


def draw_dance_poster(
    layers=10,
    wobble=0.16,
    palette_mode="pastel",
    motion=0.55,
    seed=7,
):
    """
    Generate a dance-inspired abstract poster.

    The same seed produces the same poster, so the result is reproducible.
    """
    random.seed(seed)
    np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor((0.97, 0.97, 0.97))

    palette = make_palette(7, palette_mode)

    # Organic forms
    for i in range(layers):
        cx = random.uniform(0.18, 0.82)
        cy = random.uniform(0.15, 0.85)

        radius = random.uniform(0.08, 0.23)
        x, y = blob(
            center=(cx, cy),
            radius=radius,
            wobble=wobble,
        )

        # Motion changes the amount of directional distortion.
        direction = random.uniform(-1, 1) * motion
        y = y + direction * (x - cx) * 0.18

        color = random.choice(palette)
        alpha = random.uniform(0.24, 0.52)

        ax.fill(
            x,
            y,
            color=color,
            alpha=alpha,
            edgecolor="none",
        )

    # Flowing "dance" trajectories
    for _ in range(max(2, int(layers / 2))):
        start_x = random.uniform(0.05, 0.35)
        start_y = random.uniform(0.10, 0.90)
        length = random.uniform(0.45, 0.95)

        t = np.linspace(0, 1, 180)
        x = start_x + length * t
        amplitude = random.uniform(0.015, 0.07) * (0.5 + motion)
        frequency = random.uniform(1.2, 3.0)

        y = (
            start_y
            + amplitude * np.sin(2 * math.pi * frequency * t)
            + random.uniform(-0.03, 0.03) * t
        )

        mask = (x >= 0) & (x <= 1) & (y >= 0) & (y <= 1)

        ax.plot(
            x[mask],
            y[mask],
            linewidth=random.uniform(0.7, 2.0),
            alpha=random.uniform(0.22, 0.55),
            color=random.choice(palette),
        )

    # Typography
    ax.text(
        0.06,
        0.94,
        "KINETIC DANCE",
        transform=ax.transAxes,
        fontsize=17,
        weight="bold",
        color=(0.08, 0.08, 0.08),
    )

    ax.text(
        0.06,
        0.905,
        f"GENERATIVE POSTER  /  SEED {seed}",
        transform=ax.transAxes,
        fontsize=7.5,
        color=(0.25, 0.25, 0.25),
    )

    ax.text(
        0.94,
        0.045,
        "ARTS × CODE × DATA",
        transform=ax.transAxes,
        fontsize=7,
        ha="right",
        color=(0.30, 0.30, 0.30),
    )

    fig.tight_layout(pad=0)
    return fig


# ---------- Streamlit UI ----------

st.set_page_config(
    page_title="Kinetic Dance Poster",
    page_icon="✦",
    layout="centered",
)

st.title("Kinetic Dance Generative Poster")
st.caption(
    "Arts and Advanced Big Data | Interactive Web-based Generative Art"
)

st.sidebar.header("Controls")

layers = st.sidebar.slider(
    "Layers",
    min_value=4,
    max_value=22,
    value=10,
    step=1,
)

wobble = st.sidebar.slider(
    "Wobble",
    min_value=0.01,
    max_value=0.35,
    value=0.16,
    step=0.01,
)

palette_mode = st.sidebar.selectbox(
    "Palette mode",
    ["pastel", "vivid", "mono", "random"],
    index=0,
)

motion = st.sidebar.slider(
    "Motion",
    min_value=0.0,
    max_value=1.0,
    value=0.55,
    step=0.05,
)

seed = st.sidebar.slider(
    "Seed",
    min_value=0,
    max_value=9999,
    value=7,
    step=1,
)

fig = draw_dance_poster(
    layers=layers,
    wobble=wobble,
    palette_mode=palette_mode,
    motion=motion,
    seed=seed,
)

st.pyplot(fig)

st.markdown(
    """
    **How it works**

    Change the controls on the left to create a new composition.
    The **Seed** controls reproducibility: the same seed recreates
    the same generative result.
    """
)
