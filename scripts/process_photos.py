"""Convert photos to WebP (640/1280/2000), apply EXIF rotation, strip all metadata (GPS/EXIF), write the gallery list.
usage: python3 scripts/process_photos.py photos-src assets/photos [FIRST_NAME ...]
Photo ids are the file names (e.g. TP108947). Names given after the folders go first in the gallery."""
import glob, json, os, sys
from PIL import Image, ImageOps
src, out, first = sys.argv[1], sys.argv[2], sys.argv[3:]
os.makedirs(out, exist_ok=True)
files = {os.path.splitext(os.path.basename(f))[0]: f for f in glob.glob(os.path.join(src, '*.[Jj][Pp][Gg]'))}
order = [n for n in first if n in files] + sorted(n for n in files if n not in first)
items = []
for name in order:
    im = ImageOps.exif_transpose(Image.open(files[name])).convert('RGB')  # the new image carries no EXIF / GPS
    for w in (640, 1280, 2000):
        r = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
        r.save(os.path.join(out, f'{name}-{w}.webp'), 'WEBP', quality=80 if w < 2000 else 78, method=6)
    items.append({'id': name, 'w': im.width, 'h': im.height})
json.dump(items, open(os.path.join(out, 'gallery.json'), 'w'))
print(len(items), 'photos')
