from cx_Freeze import setup, Executable
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","wx","sys"]}

# GUI applications require a different base on Windows (the default is for a
# console application).

setup(  name = "Random Sampler",
        version = "0.1",
        description = "Randomly samples files according to a confidence measure",
        options = {"build_exe": build_exe_options},
        executables = [Executable("random_sampler_gui.py")])