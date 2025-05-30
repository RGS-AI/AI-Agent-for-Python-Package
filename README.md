# Python AI Agent Package Manager v1.0

**Python AI Package Manager Agent**

A lightweight AI-driven agent to manage Python environments automatically.<br>
It can detect installed packages, save snapshots, and act based on user goals — such as install, upgrade, delete, or rollback packages.

***

### Features

• Detects and saves current installed packages as JSON snapshots<br>
• Acts intelligently based on user goals:<br>
• Install saved packages<br>
• Upgrade packages<br>
• Delete packages<br>
• Rollback to a saved environment state<br>
• Explains every step it takes (installing, upgrading, uninstalling)<br>
• Handles errors gracefully and skips failed installations<br>
• Fully local, no external API calls required

***

### How It Works

1.	The agent scans the environment and saves the installed packages with a timestamp.
2.	Based on your command (install, upgrade, delete, or rollback), it reasons a plan of action.
3.	It executes the plan, providing clear feedback at every step.

***

### Usage

python package_agent.py

You’ll be prompted to enter a goal like:

• install<br>
• upgrade<br>
• delete<br>
• rollback

The agent will take it from there!

***

### Memory System

Snapshots are saved automatically in the package_memory/ directory, allowing full or partial restoration whenever needed.

***

### Future Ideas

• Support selecting specific snapshots<br>
• Add smarter dependency resolution<br>
• Integrate lightweight LLMs for advanced reasoning

***

**License**: Credit my work if you share!
