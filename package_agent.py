import subprocess
import sys
import json
import os

class PackageManagerAI:
    def __init__(self, save_file="package_memory.json"):
        self.save_file = save_file
        self.packages = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                return json.load(f)
        return []

    def save_memory(self, packages):
        with open(self.save_file, "w") as f:
            json.dump(packages, f, indent=4)

    def detect_installed_packages(self):
        print("[Perception] Detecting installed packages...")
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
        packages = result.stdout.strip().split("\n")
        self.packages = packages
        self.save_memory(packages)
        print(f"[Memory] Saved {len(packages)} installed packages.")

    def reason_and_plan(self, goal):
        print(f"[Brain] Reasoning based on goal: {goal}")
        plan = []
        if "install" in goal.lower():
            plan = [("install", pkg) for pkg in self.packages]
        elif "upgrade" in goal.lower():
            plan = [("upgrade", pkg.split("==")[0]) for pkg in self.packages]
        else:
            print("[Brain] Goal not recognized. Doing nothing.")
        return plan

    def act(self, plan):
        print("[Action] Executing the plan...")
        for action, package in plan:
            try:
                if action == "install":
                    print(f"Installing {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                elif action == "upgrade":
                    print(f"Upgrading {package}...")
                    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package], check=True)
            except subprocess.CalledProcessError:
                print(f"[Error] Failed to {action} {package}, skipping.")

    def run(self, goal):
        self.detect_installed_packages()
        plan = self.reason_and_plan(goal)
        self.act(plan)

# --- Usage ---

if __name__ == "__main__":
    agent = PackageManagerAI()
    user_goal = input("What is your goal for the packages? (install / upgrade): ")
    agent.run(user_goal)