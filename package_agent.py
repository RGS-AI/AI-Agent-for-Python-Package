import subprocess
import sys
import json
import os
from datetime import datetime

class PackageManagerAI:
    def __init__(self, save_folder="package_memory"):
        self.save_folder = save_folder
        os.makedirs(self.save_folder, exist_ok=True)
        self.current_memory = []
        self.memory_file = self.get_latest_memory_file()

    def get_latest_memory_file(self):
        """Get the most recent saved memory snapshot."""
        files = [f for f in os.listdir(self.save_folder) if f.endswith(".json")]
        if not files:
            return None
        files.sort()
        return os.path.join(self.save_folder, files[-1])

    def save_memory(self, packages):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        memory_path = os.path.join(self.save_folder, f"packages_{timestamp}.json")
        with open(memory_path, "w") as f:
            json.dump(packages, f, indent=4)
        self.memory_file = memory_path
        print(f"[Memory] Saved current packages to {memory_path}")

    def load_memory(self, memory_file=None):
        if not memory_file:
            memory_file = self.memory_file
        if not memory_file or not os.path.exists(memory_file):
            print("[Memory] No saved package memory found.")
            return []
        with open(memory_file, "r") as f:
            packages = json.load(f)
        return packages

    def detect_installed_packages(self):
        print("[Perception] Scanning installed packages...")
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
        packages = result.stdout.strip().split("\n")
        self.current_memory = packages
        self.save_memory(packages)

    def reason_and_plan(self, goal):
        print(f"[Brain] Reasoning for goal: '{goal}'")
        plan = []
        memory_packages = self.load_memory()

        if "install" in goal.lower():
            plan = [("install", pkg) for pkg in memory_packages]
        elif "upgrade" in goal.lower():
            plan = [("upgrade", pkg.split("==")[0]) for pkg in memory_packages]
        elif "delete" in goal.lower():
            plan = [("uninstall", pkg.split("==")[0]) for pkg in memory_packages]
        elif "rollback" in goal.lower():
            # rollback = uninstall all current, install from memory
            current_packages = [pkg.split("==")[0] for pkg in self.current_memory]
            plan = [("uninstall", pkg) for pkg in current_packages]
            plan += [("install", pkg) for pkg in memory_packages]
        else:
            print("[Brain] Unknown goal! No plan generated.")

        print(f"[Brain] Generated plan with {len(plan)} steps.")
        return plan

    def act(self, plan):
        print("[Action] Starting to execute the plan...\n")
        for action, package in plan:
            try:
                if action == "install":
                    print(f"[Action] Installing {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                    print(f"Successfully installed {package}")
                elif action == "upgrade":
                    print(f"[Action] Upgrading {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], check=True)
                    print(f"Successfully upgraded {package}")
                elif action == "uninstall":
                    print(f"[Action] Uninstalling {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package], check=True)
                    print(f"Successfully uninstalled {package}")
            except subprocess.CalledProcessError:
                print(f"[Error] Failed to {action} {package}. Skipping...")

        print("\n[Action] Plan execution completed.")

    def run(self, goal):
        self.detect_installed_packages()
        plan = self.reason_and_plan(goal)
        self.act(plan)


if __name__ == "__main__":
    agent = PackageManagerAI()
    print("\nWelcome to your Package Manager AI Agent!")
    print("You can choose a goal:")
    print("- install → Install packages from memory")
    print("- upgrade → Upgrade all packages from memory")
    print("- delete → Delete all packages from memory")
    print("- rollback → Revert system to saved package state\n")
    user_goal = input("Enter your goal: ")
    agent.run(user_goal)
