# Documentation, Record-Keeping, Mathematical Formulation & Web Integration

## Solar declination formula

$$\delta(t) = -\sin^{-1}\Big(\sin(23.44^\circ) \cdot \cos\big(\tfrac{2\pi}{365}(t + 10)\big)\Big)$$

- $\delta(t)$: declination angle in degrees.
- $t$: day of year (1–365/366).
- $\sin(23.44^\circ)$: Earth\'s axial tilt.
- $(t+10)/365$: shifts the phase to align with the solstice.

This is the same expression in the original DOCX/PDF, but wrapped in GitHub-compatible math notation so it renders consistently on mobile.

## Python helper

```python
import datetime
import math

def compute_declination(utc_adjustment: float = 0.0) -> float:
    'Return the solar declination angle (degrees) for the adjusted UTC time.'
    current_utc_time = datetime.datetime.utcnow()
    adjusted_time = current_utc_time + datetime.timedelta(hours=utc_adjustment)
    day_of_year = adjusted_time.timetuple().tm_yday
    declination_rad = -math.asin(
        math.sin(math.radians(23.44)) * math.cos(2 * math.pi * (day_of_year + 10) / 365)
    )
    return math.degrees(declination_rad)

if __name__ == "__main__":
    utc_adjustment = float(input("Enter the UTC adjustment in hours (e.g., 9 for PST): "))
    declination_value = compute_declination(utc_adjustment)
    print(f"Adjusted Declination Value: {declination_value:.2f} degrees")
```

## Map references

- NOAA 5-minute radar: <https://www.ncei.noaa.gov/maps/radar/>
- Ventusky replacements:
  - World: <https://www.ventusky.com/?p=27;-102;2&l=radar>
  - North American continent: <https://www.ventusky.com/?p=36.2;-97.2;3&l=radar>
  - United States: <https://www.ventusky.com/?p=39.4;-96.3;4&l=radar>
  - Local NY example: <https://www.ventusky.com/?p=43.42;-76.38;6&l=radar>
