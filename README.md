# About Piano Scale Generator

In this repo, you can generate a visualization of the piano keyboard for
learning how to play a given major or harmonic minor scale.

I created this project because I am learning to play piano, and it has been
challenging to find a useful resource that

- provides all major and minors
- illustrates fingering
- shows multiple octaves
- in a way that can be composed into other resources (not a giant poster)

In each image:

- a label is at the top with the scale name (and its enharmonic equivalent)
- keys that belong to the scale are given a different color
- numbers are added to each key to indicate fingering to play the scale
- dots put on the root note to show progression between octaves

If you play just a single octave, use the fingering shown for the second
octave. For two or more octaves, use the fingering for the first octave
repeatedly, and the second octave shown for the final octave.

## How to set up

Download the font needed to display the music symbols:

```
# browse to https://github.com/google/fonts/tree/main/ofl/libertinusmath
# and grab the URL for the TTF, e.g.,
wget https://github.com/google/fonts/raw/refs/heads/main/ofl/libertinusmath/LibertinusMath-Regular.ttf
```

## How to run

Run the script to generate the scale images

```
source venv/bin/activate # or activate.fish
pip install -r python_requirements.txt
python generate-scales.py
```

## References

*The Complete Book of Scales, Chords, Arpeggios & Cadences* by Willard A.
Palmer, Morton Manus, and Amanda Vick Lethco:

Where to find:

- <https://www.alfred.com/the-complete-book-of-scales-chords-arpeggios-cadences/p/00-5743/>
- (on archive.org) <https://archive.org/details/pdfy-QFjQChOFF0dsYVPr>

*Technique Skills - Scales, Chords and Key Signatures* by PianoBox (?).

Where to find:

- <https://pianobox.net/products/technique-skills-scales-chords-and-key-signatures>

This book is great, except it does not show how to play multiple octaves.
