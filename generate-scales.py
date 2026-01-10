#!/usr/bin/env python3
# Copyright (c) 2026 Alexander Merritt. All Rights Reserved.
"""
Piano Scale Image Generator
Generates piano keyboard images with colorings on keys within a given scale.
Usage: python generate-scales.py [--output-dir OUTPUT_DIR]
"""

from PIL import Image, ImageDraw, ImageFont
import argparse
import os, sys

FONT = None

# Keyboard dimensions
WHITE_KEY_WIDTH = 40
WHITE_KEY_HEIGHT = 200
BLACK_KEY_WIDTH = 24
BLACK_KEY_HEIGHT = 120

# https://colorbrewer2.org/#type=sequential&scheme=YlGn&n=5
WHITE_KEY_SHADE = "#c2e699"
BLACK_KEY_SHADE = "#31a354"

# Note definitions
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
KEY_PATTERN = ["W", "B", "W", "B", "W", "W", "B", "W", "B", "W", "B", "W"]

# Scale intervals (semitones from root)
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
NATURAL_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]
HARMONIC_MINOR_SCALE = [0, 2, 3, 5, 7, 8, 11]

# All root notes for scales (using sharps and flats)
MAJOR_SCALE_ROOTS = ["C", "G", "D", "A", "E", "B", "F#", "C#", "F", "Bb", "Eb", "Ab"]
MINOR_SCALE_ROOTS = ["A", "E", "B", "F#", "C#", "G#", "D#", "A#", "D", "G", "C", "F"]

SCALE_UNICODE = {
    "C": "C",
    "C#": "C♯",
    "Cb": "C♭",
    "D": "D",
    "D#": "D♯",
    "Db": "D♭",
    "E": "E",
    "Eb": "E♭",
    "F": "F",
    "F#": "F♯",
    "G": "G",
    "G#": "G♯",
    "Gb": "G♭",
    "A": "A",
    "A#": "A♯",
    "Ab": "A♭",
    "B": "B",
    "Bb": "B♭",
}

RH_MAJOR_FINGERINGS = {
    "C": [1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4, 5],
    "Gb": [2, 3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2],
    "Db": [2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2],
    "Ab": [3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3],
    "Eb": [3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3],
    "Bb": [4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4],
    "F": [1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 4],
}

for scale in ["G", "D", "A", "E", "B"]:
    RH_MAJOR_FINGERINGS[scale] = RH_MAJOR_FINGERINGS["C"]

RH_MAJOR_FINGERINGS["F#"] = RH_MAJOR_FINGERINGS["Gb"]
RH_MAJOR_FINGERINGS["C#"] = RH_MAJOR_FINGERINGS["Db"]

LH_MAJOR_FINGERINGS = {
    "C": [5, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1],
    "B": [4, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1],
    "Gb": [4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1, 2],
    "Db": [3, 2, 1, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 2],
    "F": [5, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1],
}

for scale in ["G", "D", "A", "E"]:
    LH_MAJOR_FINGERINGS[scale] = LH_MAJOR_FINGERINGS["C"].copy()

for scale in ["Ab", "Eb", "Bb"]:
    LH_MAJOR_FINGERINGS[scale] = LH_MAJOR_FINGERINGS["Db"].copy()

LH_MAJOR_FINGERINGS["F#"] = LH_MAJOR_FINGERINGS["Gb"].copy()
LH_MAJOR_FINGERINGS["C#"] = LH_MAJOR_FINGERINGS["Db"].copy()

# Minor scales use same fingering as major scales, with exceptions
RH_MINOR_FINGERINGS = RH_MAJOR_FINGERINGS.copy()
LH_MINOR_FINGERINGS = LH_MAJOR_FINGERINGS.copy()

RH_MINOR_FINGERINGS["D#"] = RH_MINOR_FINGERINGS["Eb"]

RH_MINOR_FINGERINGS["F#"] = [3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3]
RH_MINOR_FINGERINGS["C#"] = RH_MINOR_FINGERINGS["F#"]

RH_MINOR_FINGERINGS["G#"] = [3, 4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3]
RH_MINOR_FINGERINGS["Ab"] = RH_MINOR_FINGERINGS["G#"]

RH_MINOR_FINGERINGS["A#"] = [4, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 1, 2, 3, 4]
RH_MINOR_FINGERINGS["Bb"] = RH_MINOR_FINGERINGS["A#"]

LH_MINOR_FINGERINGS["D#"] = [2, 1, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 3, 2]
LH_MINOR_FINGERINGS["Eb"] = LH_MINOR_FINGERINGS["D#"]

LH_MINOR_FINGERINGS["G#"] = [3, 2, 1, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2, 1, 3]
LH_MINOR_FINGERINGS["Ab"] = LH_MINOR_FINGERINGS["G#"]

LH_MINOR_FINGERINGS["A#"] = [2, 1, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1, 4, 3, 2]
LH_MINOR_FINGERINGS["Bb"] = LH_MINOR_FINGERINGS["A#"]

def load_font():
    global FONT
    try:
        FONT = ImageFont.truetype("LibertinusMath-Regular.ttf", 32)
    except:
        print("Libertinus Math font missing. Download the ttf from:")
        print("https://github.com/google/fonts/tree/main/ofl/libertinusmath")
        sys.exit(1)

def get_note_index(note_name):
    """Get the index of a note in the chromatic scale."""
    # Map flats/sharps to their enharmonic sharps/flats for indexing
    note_map = {
        "C": 0,
        "C#": 1,
        "Db": 1,
        "D": 2,
        "D#": 3,
        "Eb": 3,
        "E": 4,
        "Fb": 4,
        "F": 5,
        "E#": 5,
        "F#": 6,
        "Gb": 6,
        "G": 7,
        "G#": 8,
        "Ab": 8,
        "A": 9,
        "A#": 10,
        "Bb": 10,
        "B": 11,
        "Cb": 11,
        "B#": 0,
    }
    return note_map[note_name]


def generate_scale_notes(root, intervals, octaves=3):
    """Generate all notes in a scale across multiple octaves.
    Returns a dict mapping note indices to their position in the scale (0-7) and scale octave."""
    root_index = get_note_index(root)
    scale_notes_dict = {}

    # First, collect all scale notes
    all_notes = []
    for octave in range(octaves):
        for scale_position, interval in enumerate(intervals):
            note_index = (root_index + interval) % 12 + octave * 12
            all_notes.append((note_index, scale_position))

    # Sort by note index to get them in order
    all_notes.sort(key=lambda x: x[0])

    # Find the first root note (scale_position == 0)
    first_root_idx = None
    for i, (note_idx, scale_pos) in enumerate(all_notes):
        if scale_pos == 0:
            first_root_idx = i
            break

    # Now assign scale octaves relative to the first root
    for i, (note_idx, scale_pos) in enumerate(all_notes):
        if first_root_idx is not None and i >= first_root_idx:
            # Calculate scale octave from first root
            position_from_root = i - first_root_idx
            scale_octave = position_from_root // 7
        else:
            scale_octave = -1  # Before the first root

        scale_notes_dict[note_idx] = (scale_pos, scale_octave)

    return scale_notes_dict


def draw_piano_keyboard(
    scale_notes, root_note, root_name, fingering, hand, label, octaves=3
):
    """Draw a piano keyboard with colored scale keys, root note marker, and fingerings for one hand."""
    # Calculate dimensions
    total_keys = octaves * 12
    white_keys = [i for i in range(total_keys) if KEY_PATTERN[i % 12] == "W"]
    black_keys = [i for i in range(total_keys) if KEY_PATTERN[i % 12] == "B"]

    # Add space above keyboard for label
    label_height = 40
    width = len(white_keys) * WHITE_KEY_WIDTH
    height = WHITE_KEY_HEIGHT + label_height

    # Create image
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Draw label on top with scale name
    bbox = draw.textbbox((0, 0), label, font=FONT)
    text_width = bbox[2] - bbox[0]
    draw.text((100, 2), label, fill="black", font=FONT)

    # Offset for keyboard (below label area)
    y_offset = label_height

    # Draw white keys
    white_key_positions = {}
    for idx, key_num in enumerate(white_keys):
        x = idx * WHITE_KEY_WIDTH

        # Draw key background
        is_in_scale = key_num in scale_notes

        # Only color keys in the first 2 scale octaves
        if is_in_scale:
            scale_pos, scale_octave = scale_notes[key_num]
            fill_color = (
                WHITE_KEY_SHADE
                if (
                    (scale_octave >= 0 and scale_octave < 2)
                    or (scale_notes[key_num] == (0, 2))
                )
                else "white"
            )
        else:
            fill_color = "white"

        draw.rectangle(
            [x, y_offset, x + WHITE_KEY_WIDTH, y_offset + WHITE_KEY_HEIGHT],
            fill=fill_color,
            outline="black",
            width=2,
        )

        # Mark root note with a circle at the bottom (only in first 2 octaves)
        if is_in_scale:
            scale_pos, scale_octave = scale_notes[key_num]
            if key_num % 12 == root_note and (
                (scale_octave >= 0 and scale_octave < 2)
                or (scale_notes[key_num] == (0, 2))
            ):
                circle_x = x + WHITE_KEY_WIDTH // 2
                circle_y = y_offset + WHITE_KEY_HEIGHT - 20
                circle_radius = 8
                draw.ellipse(
                    [
                        circle_x - circle_radius,
                        circle_y - circle_radius,
                        circle_x + circle_radius,
                        circle_y + circle_radius,
                    ],
                    fill="black",
                    outline="black",
                    width=2,
                )

        # Add fingering numbers above keyboard (only for first 2 octaves of scale)
        if is_in_scale:
            scale_pos, scale_octave = scale_notes[key_num]

            # Only show fingering for first 2 scale octaves (starting from root)
            if (scale_octave >= 0 and scale_octave < 2) or (
                scale_notes[key_num] == (0, 2)
            ):
                text = str(fingering[scale_octave * 7 + scale_pos])

                # Center the text above the key
                bbox = draw.textbbox((0, 0), text, font=FONT)
                text_width = bbox[2] - bbox[0]
                text_x = x + (WHITE_KEY_WIDTH - text_width) // 2
                text_y = 170
                draw.text((text_x, text_y), text, fill="black", font=FONT)

        white_key_positions[key_num] = x

    # Draw black keys (on top of white keys)
    white_idx = 0
    for key_num in range(total_keys):
        if KEY_PATTERN[key_num % 12] == "W":
            white_idx += 1
        elif KEY_PATTERN[key_num % 12] == "B":
            # Position black key between white keys
            x = white_idx * WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2

            is_in_scale = key_num in scale_notes

            # Only color keys in the first 2 scale octaves
            if is_in_scale:
                scale_pos, scale_octave = scale_notes[key_num]
                fill_color = (
                    BLACK_KEY_SHADE
                    if (
                        (scale_octave >= 0 and scale_octave < 2)
                        or (scale_notes[key_num] == (0, 2))
                    )
                    else "black"
                )
            else:
                fill_color = "black"

            draw.rectangle(
                [x, y_offset, x + BLACK_KEY_WIDTH, y_offset + BLACK_KEY_HEIGHT],
                fill=fill_color,
                outline="black",
                width=2,
            )

            # Mark root note with a circle (only in first 2 octaves)
            if is_in_scale:
                scale_pos, scale_octave = scale_notes[key_num]
                if key_num % 12 == root_note and (
                    (scale_octave >= 0 and scale_octave < 2)
                    or (scale_notes[key_num] == (0, 2))
                ):
                    circle_x = x + BLACK_KEY_WIDTH // 2
                    circle_y = y_offset + 20
                    circle_radius = 6
                    draw.ellipse(
                        [
                            circle_x - circle_radius,
                            circle_y - circle_radius,
                            circle_x + circle_radius,
                            circle_y + circle_radius,
                        ],
                        fill="white",
                        outline="white",
                        width=2,
                    )

            # Add fingering numbers above keyboard (only for first 2 octaves of scale)
            if is_in_scale:
                scale_pos, scale_octave = scale_notes[key_num]

                # Only show fingering for first 2 scale octaves (starting from root)
                if (scale_octave >= 0 and scale_octave < 2) or (
                    scale_notes[key_num] == (0, 2)
                ):
                    text = str(fingering[scale_pos])

                    bbox = draw.textbbox((0, 0), text, font=FONT)
                    text_width = bbox[2] - bbox[0]
                    text_x = x + (BLACK_KEY_WIDTH - text_width) // 2
                    text_y = 120
                    draw.text((text_x, text_y), text, fill="white", font=FONT)

    return img


def sanitize_filename(name):
    """Sanitize scale name for use in filename."""
    return name.replace("#", "sharp").replace("b", "flat").replace(" ", "_").lower()

def unicode_major_root(root):
    """Present major scale root and any enharmonic as unicode for display."""
    if root in ["F#", "Gb"]:
        return "{}/{}".format(SCALE_UNICODE["F#"], SCALE_UNICODE["Gb"])
    elif root in ["C#", "Db"]:
        return "{}/{}".format(SCALE_UNICODE["C#"], SCALE_UNICODE["Db"])
    elif root in ["B", "Cb"]:
        return "{}/{}".format(SCALE_UNICODE["B"], SCALE_UNICODE["Cb"])
    else:
        return SCALE_UNICODE[root]

def unicode_hminor_root(root):
    """Present minor scale root and any enharmonic as unicode for display."""
    if root in ["G#", "Ab"]:
        return "{}/{}".format(SCALE_UNICODE["G#"], SCALE_UNICODE["Ab"])
    elif root in ["D#", "Eb"]:
        return "{}/{}".format(SCALE_UNICODE["D#"], SCALE_UNICODE["Eb"])
    elif root in ["A#", "Bb"]:
        return "{}/{}".format(SCALE_UNICODE["A#"], SCALE_UNICODE["Bb"])
    else:
        return SCALE_UNICODE[root]

def generate_majors(scale_roots, output_dir="piano_scales", octaves=3):
    """Generate images for all major and minor scales."""
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating piano scale images in '{output_dir}/'...")
    print(f"Keyboard: {octaves} octaves\n")

    # Generate major scales
    print("Generating major scales...")
    for root in scale_roots:
        root_index = get_note_index(root)
        scale_notes = generate_scale_notes(root, MAJOR_SCALE, octaves)

        root_name = unicode_major_root(root)

        # Right hand
        rh_fingering = RH_MAJOR_FINGERINGS[root]
        label = "{} major for RH".format(root_name)
        img_rh = draw_piano_keyboard(
            scale_notes, root_index, root, rh_fingering, "RH", label, octaves
        )
        filename_rh = f"{sanitize_filename(root)}_major_rh.png"
        filepath_rh = os.path.join(output_dir, filename_rh)
        img_rh.save(filepath_rh)

        # Left hand
        lh_fingering = LH_MAJOR_FINGERINGS[root]
        label = "{} major for LH".format(root_name)
        img_lh = draw_piano_keyboard(
            scale_notes, root_index, root, lh_fingering, "LH", label, octaves
        )
        filename_lh = f"{sanitize_filename(root)}_major_lh.png"
        filepath_lh = os.path.join(output_dir, filename_lh)
        img_lh.save(filepath_lh)

        print(f"  ✓ {root} Major -> {filename_rh}, {filename_lh}")


def generate_hminors(scale_roots, output_dir="piano_scales", octaves=3):
    ## Generate harmonic minor scales
    print("\nGenerating harmonic minor scales...")
    for root in scale_roots:
        root_index = get_note_index(root)
        scale_notes = generate_scale_notes(root, HARMONIC_MINOR_SCALE, octaves)

        root_name = unicode_hminor_root(root)

        # Right hand
        rh_fingering = RH_MINOR_FINGERINGS[root]
        label = "{} harmonic minor for RH".format(root_name)
        img_rh = draw_piano_keyboard(
            scale_notes, root_index, root, rh_fingering, "RH", label, octaves
        )
        filename_rh = f"{sanitize_filename(root)}_harmonic_minor_rh.png"
        filepath_rh = os.path.join(output_dir, filename_rh)
        img_rh.save(filepath_rh)

        # Left hand
        lh_fingering = LH_MINOR_FINGERINGS[root]
        label = "{} harmonic minor for LH".format(root_name)
        img_lh = draw_piano_keyboard(
            scale_notes, root_index, root, lh_fingering, "LH", label, octaves
        )
        filename_lh = f"{sanitize_filename(root)}_harmonic_minor_lh.png"
        filepath_lh = os.path.join(output_dir, filename_lh)
        img_lh.save(filepath_lh)

        print(f"  ✓ {root} Harmonic Minor -> {filename_rh}, {filename_lh}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate piano keyboard images for all major and minor scales"
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for generated images (default: output)",
    )

    args = parser.parse_args()
    load_font()
    generate_majors(MAJOR_SCALE_ROOTS, args.output_dir)
    generate_hminors(MINOR_SCALE_ROOTS, args.output_dir)


if __name__ == "__main__":
    main()
