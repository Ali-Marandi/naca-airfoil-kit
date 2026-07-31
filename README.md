# NACA Airfoil Kit

Generate cosine-spaced upper and lower coordinates for classic NACA four-digit
airfoils using the published analytical construction.

```python
from airfoil import naca4

upper, lower = naca4("2412", points=101)
```

Run `python -m unittest -v`. Coordinates are normalized by chord. The tool
generates geometry only; it does not predict lift, drag, separation or
compressibility effects.
