# Bella Vista Lakefront — photos

Drop the original full-size photos in this folder. Any filename is fine; I'll rename,
resize, and generate the responsive variants. Don't pre-crop or compress — starting
from the largest originals available gives the best result, and the hero treatment
needs the resolution.

**Wanted, roughly in priority order:**

1. **The hero** — the one shot that sells the house. Usually the exterior with the lake,
   or the main living space with the view through it. Landscape orientation.
2. Exterior: front approach, and the lake side
3. Main living area
4. Kitchen
5. Dining
6. Every bedroom (one clean shot each, note which is which)
7. Every bathroom
8. Deck, dock, firepit, outdoor seating
9. Anything with a story — the view at sunset, the boat, the game room

**Format:** JPEG or PNG, landscape where possible, at least 2000px on the long edge.
Phone photos are fine if that's what exists. Vertical shots work for bedrooms and
bathrooms but not for the hero.

Per the build spec, photography is the hero of this design and the copy supports it —
so a dozen good photos beats forty mediocre ones.

**These are temporary.** Serving images from `public/` is fine for local development,
but they move to Supabase Storage before launch so they get a CDN and don't bloat the
git repo. Don't build anything that assumes this path is permanent.
