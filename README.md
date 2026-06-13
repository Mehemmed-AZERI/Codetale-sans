💀 Sans Overlay & Codeforces Assistant
A custom interactive system overlay featuring a responsive desktop assistant, audio synthesis pipelines, a built-in conversational inference loop, and a live Codeforces solution tracker.

🚀 Complete Installation Guide
Follow these steps from scratch to get the application running on Windows.

🛠️ Step 0: Install Python (If Not Already Installed)
If you don't have Python 3 installed on your system, you can download and configure it directly through your terminal using the Windows Package Manager (winget):

Press Windows + R on your keyboard to open the Run dialog box.

Type cmd and press Enter to open the Command Prompt.

Paste the following command and hit Enter:

Bash
winget install Python.Python.3.11
⚠️ CRITICAL: Once the installation finishes, you must close your current Command Prompt window and open a new one (by pressing Windows + R and typing cmd again). This refreshes your environment variables so Windows recognizes the pip and python executables.

📦 Step 1: Install Project Dependencies
With a fresh Command Prompt window open, execute the following command to download and install all the non-standard Python frameworks required by the codebase:

Bash
pip install requests psutil pygame pillow groq tkinterdnd2
What's being downloaded:
requests – Queries the Codeforces API endpoints to monitor user profiles and track solution submissions.

psutil – Facilitates system process checks and background script control utilities.

pygame – Coordinates the audio mixer and sound tracking loops for localized sound synthesis.

pillow – Powers frame manipulation and layer rendering for custom window animations.

groq – Manages contextual prompt routing to the Groq inference engine.

tkinterdnd2 – Adds native operating system drag-and-drop registrations onto the UI window canvas.

📂 Step 2: Set Up the File Structure
The main script reads textures and audio directly from its current working path. To prevent FileNotFoundError runtime crashes, organize your local project folder exactly like this:

Markdown
📂 your-project-folder/
 ├── 📄 sans.py                # Main script executable
 ├── 🎵 voice_sans.mp3         # Character voice asset
 ├── 🎞️ sanssleep.gif          # Idle animation state asset
 ├── 🖼️ sans.png               # Default state UI texture
 ├── 🖼️ sanslis.png            # Listening state UI texture
 ├── 🖼️ sansproceed.png        # Execution state UI texture
 ├── 🖼️ sanser.png             # Error state UI texture
 ├── 🖼️ sansad.png             # Warning state UI texture
 └── 🖼️ sansang.png            # Angry state UI texture
