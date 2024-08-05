### World of Goo 2 Disable Camera Panning On Mouse Drag Mod

This mod disables the camera panning when dragging the mouse in the game. This is useful for players who accidentally pan the camera while trying to grab gooballs, and is especially useful for thwacking.

### Installation

This mod uses PyInstaller to create a standalone executable. You can download the latest version of the mod from the [releases page](https://github.com/zakaryan2004/wog2_disabledragview/releases).

Alternatively, you can run the Python script directly if you have Python installed.

There are no dependencies required for this mod.

### Usage

Run the executable file with the input file as the argument. 

On Windows, the input file is the WorldOfGoo2.exe located in the root of the game installation directory.

On macOS, the input file is the WorldOfGoo2 binary, located in WorldOfGoo2.app/Contents/MacOS.

On Linux, the input file is the WorldOfGoo2 binary, located in the root of the game installation directory.

An optional second argument can be provided to specify the platform of the input file. This is useful when patching the game executable on a different platform. If the platform is not provided, the script will use the host machine's platform.

PyInstaller binary (command line):
```bash
wog2_disableDragView WorldOfGoo2
```

```bash
wog2_disableDragView WorldOfGoo2.exe win32
```

```bash
wog2_disableDragView.exe WorldOfGoo2.exe
```

**On Windows, you can also drag and drop the game executable onto the mod executable.**

The mod will copy the original executable to a backup file and patch the backup executable with the mod, preserving the original game executable. The new file will have the same name as the original but `_patched` or `_patched.exe` at the end, depending on the platform.


For any other issues, contact me (@zakaryan2004) on the [GooFans Discord server](https://discord.gg/6BEecnD) or open an issue here.
