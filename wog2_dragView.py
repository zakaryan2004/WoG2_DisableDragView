# Copyright (C) 2024 Gegham Zakaryan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import subprocess
import shutil
import sys
import os


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Ask for the input file
        print("Usage: wog2_disableDragView <input_file> [<platform>]")
        print("Platforms: win32, darwin, linux")
        print("Example: wog2_disableDragView WorldOfGoo2")
        print("Example: wog2_disableDragView WorldOfGoo2.exe win32")
        print("Make sure to run as administrator on Windows, or move the file to a writable location.")

        input_file = input("Input file path (drag the game executable to this window or copy as path): ")
        platform = input(f"Platform (win32, darwin, linux), current: {sys.platform}: ") or sys.platform
    else:
        input_file = sys.argv[1]
        platform = sys.argv[2] if len(sys.argv) > 2 else sys.platform

    if platform in ["cygwin", "msys", "win32"]:
        platform = "win32"

    if platform not in ["win32", "darwin", "linux"]:
        print("Error: Invalid platform. Choose from win32, darwin, linux.")
        sys.exit(1)

    output_file = input_file + "_patched"
    if platform == "win32":
        output_file += ".exe"
    
    shutil.copyfile(input_file, output_file)

    with open(output_file, 'r+b') as f:
        # Windows
        if platform == "win32":
            f.seek(0x0268b40)
            f.write(bytes([0xc3, 0x90]))

        # macOS
        elif platform == "darwin":
            # Use lipo to extract both architectures
            subprocess.run(["lipo", output_file, "-thin", "arm64", "-output", output_file + "_arm64"])
            subprocess.run(["lipo", output_file, "-thin", "x86_64", "-output", output_file + "_x86_64"])

            # Patch the x86_64 binary
            with open(output_file + "_x86_64", 'r+b') as f:
                f.seek(0x024c2d0)
                f.write(bytes([0xC3]))

            # Patch the arm64 binary
            with open(output_file + "_arm64", 'r+b') as f:
                f.seek(0x01e81c4)
                f.write(bytes([0xC0, 0x03, 0x5F, 0xD6]))

            # Use lipo to replace the thin binaries inside output_file
            subprocess.run(["lipo", output_file, "-replace", "x86_64", output_file + "_x86_64", "-replace", "arm64", output_file + "_arm64", "-output", output_file])

            # Use codesign to re-sign the binary
            subprocess.run(["codesign", "-f", "-s", "-", output_file])

            # chmod the file
            os.chmod(output_file, 0o755)

            # Delete the temporary files
            os.remove(output_file + "_arm64")
            os.remove(output_file + "_x86_64")
        
        # Linux
        elif platform == "linux":
            print("Error: Linux not yet supported.")
            sys.exit(1)

    print(f"Patch applied successfully! Written to {output_file}.")

