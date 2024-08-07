import subprocess

class AndroidControl:
    def __init__(self):
        self.check_adb()

    def check_adb(self):
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if "Android Debug Bridge" not in result.stdout:
            raise EnvironmentError("adb is not installed or not found in PATH")

    def adb_command(self, command):
        result = subprocess.run(["adb"] + command.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr.strip()}")
        return result.stdout.strip()

    def open_google_maps(self):
        return self.adb_command("shell monkey -p com.google.android.apps.maps -c android.intent.category.LAUNCHER 1")

if __name__ == "__main__":
    android = AndroidControl()
    print("Opening Google Maps...")
    android.open_google_maps()
