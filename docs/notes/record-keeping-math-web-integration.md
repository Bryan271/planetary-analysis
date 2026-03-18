-   The formula for declination (δ) of the Earth based on the day of the
    year (t) is:

> $(\delta) = - \left\lbrack {\sin^{- 1}(}{\sin{(23.44{^\circ})}}x\cos\left( \left( \frac{2\pi}{360} \right)x(t + 10) \right) \right\rbrack$

-   *δ*(*t*) is the declination angle.

-   *t* is the day of the year.

-   Sin(23.44°) represents the sine of the Earth\'s axial tilt
    (approximately 23.44°).

-   $\left( \frac{t + 10}{365} \right)\ $adjusts the formula to account
    for solstice.

```{=html}
<!-- -->
```
-   Developed a Python function to compute the declination angle based
    on the current UTC time and a user-input adjustment. This function
    is crucial for dynamically adjusting the website\'s view based on
    the Earth\'s position relative to the sun.

-   The computed declination value, adjusted for the user\'s input, is
    integrated into the web link
    \"<https://earth.nullschool.net/#current/wind/surface/level/overlay=temp/orthographic=-107.56,11.34,200>\",
    where \'107.56\' is the longitude, \'11.34\' is the declination
    (delta t), and \'200\' is the zoom feature of the Earth. This web
    link hosts all 11 profiles of Earth, and the declination value
    ensures that the website\'s view is oriented correctly based on the
    Earth\'s current tilt and position relative to the sun.

> **Compute declination and adjust for UTC**

import datetime

import math

def compute_declination(utc_adjustment=0):

    \# Get the current UTC time

    current_utc_time = datetime.datetime.utcnow()

   

    \# Adjust the UTC time based on user input

    adjusted_time = current_utc_time +
datetime.timedelta(hours=utc_adjustment)

   

    \# Determine the day of the year from the adjusted time

    day_of_year = adjusted_time.timetuple().tm_yday

   

    \# Compute the declination angle using the formula

    declination_rad = -math.asin(math.sin(math.radians(23.44)) \*
math.cos(2 \* math.pi \* (day_of_year + 10) / 365))

   

    \# Convert declination from radians to degrees

    declination_deg = math.degrees(declination_rad)

   

    return declination_deg

\# Get UTC adjustment from the user

utc_adjustment = float(input(\"Enter the UTC adjustment in hours (e.g.,
9 for PST): \"))

\# Compute and display the declination value

declination_value = compute_declination(utc_adjustment)

print(f\"Adjusted Declination Value: {declination_value:.2f} degrees\")

-   Current NOAA for radar in 5 minute intervals\
    https://www.ncei.noaa.gov/maps/radar/

    -   Replacement views:

        -   World ("<https://www.ventusky.com/?p=27;-102;2&l=radar>")

        -   N. American Continent
            ("<https://www.ventusky.com/?p=36.2;-97.2;3&l=radar>")

        -   U.S. ("https://www.ventusky.com/?p=39.4;-96.3;4&l=radar")

        -   Local
            ("<https://www.ventusky.com/?p=43.42;-76.38;6&l=radar>")
