# Atmos Weather

Interactive weather app with live 3D Blender models, city search, current location, hourly and weekly forecasts, themes, and horizontal tap/drag rotation.

Live app: https://atmos-weather.ubaidsardar002.chatgpt.site

## Run locally

With Python installed, run from the repository folder:

```sh
python -m http.server 8000 --directory dist
```

Open http://localhost:8000 in your browser. Internet access is required for weather data. Location access requires browser permission. Haptic feedback depends on browser support.

## Files

- `dist/`: ready-to-serve HTML, CSS, JavaScript, and assets.
- `*.blend`: editable Blender source scenes.
- `*.py`: Blender asset generation and export scripts (some contain original workspace paths; adjust before regenerating).
- `BebasNeue-OFL.txt`: bundled font license.

Serve `dist/` using any static web host. No build step is required.
