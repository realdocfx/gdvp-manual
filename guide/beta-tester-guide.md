# GDVP Beta Tester: Download & Activation Guide

Welcome to the General Digital Voicing Program (GDVP) beta. Follow these steps to redeem your invite, download the software, and activate your machine-bound license.

## Phase 1: Redeem Your Invite and Download

1. **Open the Portal:** Navigate to the GDVP web portal URL provided by your admin.
2. **Redeem Your Code:** On the "Redeem" page, enter the invite code you received (it looks like `GDVP-XXXX-XXXX-XXXX`), your email address, and optionally your name. Click **Redeem**. Note that invite codes are limited to one per tester.
3. **Download the Software:** Once redeemed, you will be taken to your personal **Dashboard**. Click **Download GDVP** to retrieve the latest build.
4. **Install:** Extract the downloaded files or run the installer to set up the GDVP standalone app and the VST3 plug-in on your machine.

*(Note: Unlicensed copies run in DEMO mode and will be interrupted by a short burst of noise about once a minute until activated.)*

## Phase 2: Generate and Apply Your License

1. **Find Your Machine ID:** Launch the GDVP application and press `Ctrl` + `L` to open the *Product Activation* panel. Click the `COPY ID` button to copy your unique Machine ID to your clipboard (it will look like `GDVP-XXXXXXXX-XXXXXXXX`).
2. **Issue the License:** Go back to your Dashboard in the web portal and paste the Machine ID into the provided field. Click **Get my license** to generate and download your custom `gdvp.license` file.
3. **Activate:** Drag and drop the downloaded `gdvp.license` file directly onto the GDVP application window. The status will change to LICENSED, and the demo noise will instantly stop.

### Manual Activation Alternative

If drag-and-drop does not work for you, you can manually place the `gdvp.license` file into your GDVP data folder and click `RECHECK` in the activation panel. The folder paths are:

* **Windows:** `%APPDATA%\RealDocFX\GDVP\`
* **macOS:** `~/Library/Application Support/RealDocFX/GDVP/`
* **Linux:** `~/.config/RealDocFX/GDVP/`

*(Note: The same license file will automatically unlock both the standalone application and the VST3 plug-in.)*
