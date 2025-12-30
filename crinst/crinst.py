import sys
import os
import subprocess
import shutil
import tempfile
import urllib.request
import zipfile

CRINST_REPO = "https://github.com/crooket/crinst-pkgs/archive/refs/heads/main.zip"

def download_repo_zip():
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "repo.zip")

    print("Downloading Crooket package index...")
    urllib.request.urlretrieve(CRINST_REPO, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    return os.path.join(temp_dir, "crinst-pkgs-main")


def install_crooket_package(pkg_name):
    cwd = os.getcwd()
    repo_path = download_repo_zip()
    pkg_path = os.path.join(repo_path, pkg_name)

    if not os.path.exists(pkg_path):
        return False  # <-- IMPORTANT CHANGE

    target_path = os.path.join(cwd, pkg_name)

    if os.path.exists(target_path):
        print(f":| | Paritally has ran, Package '{pkg_name}' already exists")
        return True

    shutil.copytree(pkg_path, target_path)
    print(f":) | Installed Crooket package '{pkg_name}'")
    return True


def install_pip_package(pkg_name):
    print(f"Trying pip install for '{pkg_name}'...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--target", os.getcwd(),
            pkg_name
        ])
        print(f":) | Installed pip package '{pkg_name}'")
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  crinst install <package>")
        sys.exit(1)

    command = sys.argv[1]
    package = sys.argv[2]

    if command != "install":
        print(":( | Couldnt run: Unknown command")
        sys.exit(1)

    
    if install_crooket_package(package):
        return

    
    if install_pip_package(package):
        return

    print(f":( | Couldnt run: Package '{package}' not found in crinst repo or pip")


if __name__ == "__main__":
    main()
