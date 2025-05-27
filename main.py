import os
import re
import sys

def find_fortnite_config_path():
    """
    Attempts to find the path to the GameUserSettings.ini file.
    This is typically located in %LOCALAPPDATA%\FortniteGame\Saved\Config\WindowsClient\
    """
    local_app_data = os.getenv('LOCALAPPDATA')
    if not local_app_data:
        print("Error: LOCALAPPDATA environment variable not found.", file=sys.stderr)
        return None

    config_path = os.path.join(
        local_app_data,
        'FortniteGame',
        'Saved',
        'Config',
        'WindowsClient',
        'GameUserSettings.ini'
    )
    return config_path

def change_fortnite_resolution(width, height):
    """
    Changes the resolution settings in the Fortnite GameUserSettings.ini file.

    Args:
        width (int): The desired horizontal resolution.
        height (int): The desired vertical resolution.
    """
    config_file_path = find_fortnite_config_path()

    if not config_file_path:
        print("Could not determine Fortnite config file path. Please check your Fortnite installation.", file=sys.stderr)
        return

    if not os.path.exists(config_file_path):
        print(f"Error: GameUserSettings.ini not found at '{config_file_path}'.", file=sys.stderr)
        print("Please ensure Fortnite has been run at least once to generate this file.", file=sys.stderr)
        return

    try:
        # Read the entire content of the file
        with open(config_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expressions to find and replace resolution settings
        # We need to update ResolutionSizeX, ResolutionSizeY, LastUserConfirmedResolutionSizeX, LastUserConfirmedResolutionSizeY
        # and DesiredScreenWidth, DesiredScreenHeight, LastUserConfirmedDesiredScreenWidth, LastUserConfirmedDesiredScreenHeight
        # and also FullscreenMode and LastConfirmedFullscreenMode (optional, but good practice if resolution changes)

        # Pattern for ResolutionSizeX and Y
        content = re.sub(r'(ResolutionSizeX=)\d+', r'\g<1>' + str(width), content)
        content = re.sub(r'(ResolutionSizeY=)\d+', r'\g<1>' + str(height), content)

        # Pattern for LastUserConfirmedResolutionSizeX and Y
        content = re.sub(r'(LastUserConfirmedResolutionSizeX=)\d+', r'\g<1>' + str(width), content)
        content = re.sub(r'(LastUserConfirmedResolutionSizeY=)\d+', r'\g<1>' + str(height), content)

        # Pattern for DesiredScreenX and Y (these are often the same as ResolutionSize but can differ)
        content = re.sub(r'(DesiredScreenWidth=)\d+', r'\g<1>' + str(width), content)
        content = re.sub(r'(DesiredScreenHeight=)\d+', r'\g<1>' + str(height), content)

        # Pattern for LastUserConfirmedDesiredScreenX and Y
        content = re.sub(r'(LastUserConfirmedDesiredScreenWidth=)\d+', r'\g<1>' + str(width), content)
        content = re.sub(r'(LastUserConfirmedDesiredScreenHeight=)\d+', r'\g<1>' + str(height), content)

        # Ensure FullscreenMode and LastConfirmedFullscreenMode are set to 1 (Fullscreen)
        # This is often necessary when manually changing resolution to ensure it applies correctly.
        content = re.sub(r'(FullscreenMode=)\d+', r'\g<1>1', content)
        content = re.sub(r'(LastConfirmedFullscreenMode=)\d+', r'\g<1>1', content)


        # Write the modified content back to the file
        with open(config_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Successfully updated Fortnite resolution to {width}x{height}.")
        print("Please restart Fortnite for changes to take effect.")

    except PermissionError:
        print(f"Error: Permission denied when trying to write to '{config_file_path}'.", file=sys.stderr)
        print("Please run this script as administrator, or ensure the file is not read-only.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    print("Fortnite Resolution Changer Script")
    print("----------------------------------")
    print("This script will modify your GameUserSettings.ini file.")

    try:
        # Get desired resolution from user input
        while True:
            try:
                res_width = int(input("Enter desired width (e.g., 1920): "))
                if res_width <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid width. Please enter a positive integer.")

        while True:
            try:
                res_height = int(input("Enter desired height (e.g., 1080): "))
                if res_height <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid height. Please enter a positive integer.")

        change_fortnite_resolution(res_width, res_height)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred during input: {e}", file=sys.stderr)

