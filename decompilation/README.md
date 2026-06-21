# Decrypting and decompiling game code

The games include .lua files, most of which are encrypted. Luckily, the encryption keys are stored inside the game's executable.

## Automatic key discovery and Lua decryption

`decrypt_lua.py` finds AES keys that the Windows executable constructs byte by byte, tests each candidate against the encrypted Lua files, and only accepts a key when the decrypted data has valid PKCS#7 padding and a 7-Zip signature. It supports the AES-256-CBC/zero-IV format used by the tested Rovio PC releases and also probes AES-ECB.

Run it with `uv`; its dependencies are declared inside the script:

```sh
uv run decompilation/decrypt_lua.py "/path/to/Angry Birds Star Wars II" --output "/path/to/decrypted-lua" --include-plain
```

To inspect a specific executable instead of every `.exe` in the game directory:

```sh
uv run decompilation/decrypt_lua.py "/path/to/game" --exe "/path/to/game/Game.exe" --output "/path/to/decrypted-lua"
```

The output is compiled Lua bytecode. Use a Lua 5.1 decompiler such as `unluac` to produce source-like Lua.
