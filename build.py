import PyInstaller.__main__

PyInstaller.__main__.run([
    "crooket.py",
    "--name=Crooket",
    "--icon=crooketicon.png",
    "--clean",
    "--noconfirm",
    "--contents-directory=."
])
