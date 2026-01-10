Set up:

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

Run the script to generate the scale images

```
python generate-scales.py
```
