# About Piano Scale Generator

In this repo, you can generate a visualization of the piano keyboard for learning how to play a given major or harmonic minor scale.

In each image:

- a label is at the top with the scale name (and its enharmonic equivalent)
- keys that belong to the scale are given a different color
- numbers are added to each key to indicate fingering to play the scale
- dots put on the root note to show progression between octaves

If you play just a single octave, use the fingering shown for the second octave. For two or more octaves, use the fingering for the first octave repeatedly, and the second octave shown for the final octave.

# How to set up

```
python -m venv venv
pip install pillow

```

Download the font needed to display the music symbols:

```
# browse to https://github.com/google/fonts/tree/main/ofl/libertinusmath
# and grab the URL for the TTF, e.g.,
wget https://github.com/google/fonts/raw/refs/heads/main/ofl/libertinusmath/LibertinusMath-Regular.ttf
```

# How to run

Run the script to generate the scale images

```
python generate-scales.py
```
