# SoundCloud to Tiermaker

Create Tiermaker-ready images from a SoundCloud profile quickly and easily.

<div align="center">
  <img width="40%" height="40%" alt="image" src="https://github.com/user-attachments/assets/d0972853-7b82-4d47-a41b-fc5456657d1d" />
  <img width="38%" height="38%" alt="image" src="https://github.com/user-attachments/assets/02362011-be1c-46a7-9575-0f8880efe3f0" />
</div>

What it does
- Downloads track covers from a SoundCloud profile (or uses images you provide).
- Adds the track title as readable text above or below each image.
- Saves finished 256×(256+text) images into the `output` folder so you can import them into Tiermaker.

## Setup
### Compiled
1. Download the latest release from the [Releases](https://github.com/Lenochxd/soundcloud-tiermaker-maker/releases).
2. Run the `soundcloud-to-tiermaker.exe` file.

### From source
1. Install dependencies: `pip install -r requirements.txt`.
2. Run the app: `python gui.py`.

## Usage
### GUI (recommended)
1. Enter the SoundCloud profile URL (for example: `https://soundcloud.com/artistname`).
2. (Optional) Click **Add Images** to include your own images instead of downloading covers.
3. Set font size and choose whether the text appears on top or bottom.
4. Click **Process**. When finished, click **Open Output** to view the results.

### Command Line (source only)
- Basic: `python main.py <soundcloud_profile_url>`
- Options: `--top` (place text above images), `--font-size <size>`, `--custom-images <path1> <path2> ...`, `--use-temp` (skip download and use existing `temp` folder).

Where to find your images
- Finished images are written to the `output` folder next to the app.


Notes & tips
- If something looks wrong with text size or wrapping, try a different font size in the GUI or with `--font-size`.
- The app creates `temp` and `output` folders in the project directory, you can clear or back them up as needed.

Enjoy making Tiermaker lists from SoundCloud profiles!
