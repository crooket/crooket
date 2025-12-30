import PyInstaller.__main__

PyInstaller.__main__.run([
    "crinst.py",
    "--name=Crinst",
    "--clean",
    "--noconfirm",
    "--contents-directory=."
])
