import os
import webbrowser
import threading
import tkinter as tk
import time
import requests
import psutil
import subprocess
import glob
import pygame
import json
from difflib import SequenceMatcher
from PIL import Image, ImageTk

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
SETTINGS_FILE = "settings.json"

SAD_WORDS = []

ANGRY_WORDS = []

# ─── PROBLEM DATABASE ────────────────────────────────────────────────────────
CF_RANK_TIERS = [
    "Newbie", "Pupil", "Specialist", "Expert",
    "Candidate Master", "Master", "International Master",
    "Grandmaster", "International Grandmaster", "Legendary Grandmaster"
]

def cf_rank_index(rank_name):
    if not rank_name:
        return -1
    rank_name = rank_name.lower()
    for i, tier in enumerate(CF_RANK_TIERS):
        if tier.lower() == rank_name:
            return i
    return -1

PROBLEM_LIST = [
    # 800 Rated
    {"name": "Watermelon", "url": "https://codeforces.com/problemset/problem/4/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Way Too Long Words", "url": "https://codeforces.com/problemset/problem/71/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Team", "url": "https://codeforces.com/problemset/problem/231/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Next Round", "url": "https://codeforces.com/problemset/problem/158/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Bit++", "url": "https://codeforces.com/problemset/problem/282/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Domino Piling", "url": "https://codeforces.com/problemset/problem/50/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Beautiful Matrix", "url": "https://codeforces.com/problemset/problem/263/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Petya and Strings", "url": "https://codeforces.com/problemset/problem/112/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Helpful Maths", "url": "https://codeforces.com/problemset/problem/339/A", "tier": "800 Rated (Easy+ Institution)"},
    {"name": "Boy or Girl", "url": "https://codeforces.com/problemset/problem/236/A", "tier": "800 Rated (Easy+ Institution)"},
    # 900 Rated
    {"name": "Soldier and Bananas", "url": "https://codeforces.com/problemset/problem/546/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Stones on the Table", "url": "https://codeforces.com/problemset/problem/266/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Bear and Big Brother", "url": "https://codeforces.com/problemset/problem/791/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Elephant", "url": "https://codeforces.com/problemset/problem/617/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Team Olympiad", "url": "https://codeforces.com/problemset/problem/490/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Presents", "url": "https://codeforces.com/problemset/problem/136/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Word Capitalization", "url": "https://codeforces.com/problemset/problem/281/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Tram", "url": "https://codeforces.com/problemset/problem/116/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "Anton and Danik", "url": "https://codeforces.com/problemset/problem/734/A", "tier": "900 Rated (Easy+ Implementation)"},
    {"name": "I Wanna Be the Guy", "url": "https://codeforces.com/problemset/problem/469/A", "tier": "900 Rated (Easy+ Implementation)"},
    # 1000 Rated
    {"name": "Vanya and Fence", "url": "https://codeforces.com/problemset/problem/677/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Bear and Raspberry", "url": "https://codeforces.com/problemset/problem/385/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Pangram", "url": "https://codeforces.com/problemset/problem/520/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Twins", "url": "https://codeforces.com/problemset/problem/160/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Football", "url": "https://codeforces.com/problemset/problem/43/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Arrival of the General", "url": "https://codeforces.com/problemset/problem/144/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Insomnia Cure", "url": "https://codeforces.com/problemset/problem/148/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Drinks", "url": "https://codeforces.com/problemset/problem/200/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Nearly Lucky Number", "url": "https://codeforces.com/problemset/problem/110/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    {"name": "Dubstep", "url": "https://codeforces.com/problemset/problem/208/A", "tier": "1000 Rated (Basic Algorithms + Logic)"},
    # 1100 Rated
    {"name": "Queue at the School", "url": "https://codeforces.com/problemset/problem/266/B", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Fox And Snake", "url": "https://codeforces.com/problemset/problem/510/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Games", "url": "https://codeforces.com/problemset/problem/268/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Gravity Flip", "url": "https://codeforces.com/problemset/problem/405/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Chat room", "url": "https://codeforces.com/problemset/problem/58/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Magnets", "url": "https://codeforces.com/problemset/problem/344/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Shaass and Oskols", "url": "https://codeforces.com/problemset/problem/294/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"},
    {"name": "Little Elephant and Bits", "url": "https://codeforces.com/problemset/problem/258/A", "tier": "1100 Rated (Tricky Implementation + Thinking)"}
]

KILL_MAP = {
    "google":    ["chrome", "googledrivesync", "googleupdate", "google"],
    "chrome":    ["chrome"],
    "discord":   ["discord"],
    "spotify":   ["spotify"],
    "steam":     ["steam"],
    "minecraft": ["minecraft", "javaw"],
    "firefox":   ["firefox"],
    "edge":      ["msedge"],
    "telegram":  ["telegram"],
    "zoom":      ["zoom"],
    "skype":     ["skype"],
    "vlc":       ["vlc"],
    "notepad":   ["notepad"],
    "word":      ["winword"],
    "excel":     ["excel"],
}

OPEN_MAP = {
    "google":        "https://www.google.com",
    "youtube":       "https://www.youtube.com",
    "codeforces":    "https://codeforces.com",
    "leetcode":      "https://leetcode.com",
    "github":        "https://www.github.com",
    "reddit":        "https://www.reddit.com",
    "twitter":       "https://www.twitter.com",
    "discord":       "https://www.discord.com",
    "spotify":       "https://spotify.com",
    "netflix":       "https://www.netflix.com",
    "twitch":        "https://www.twitch.tv",
    "gmail":         "https://mail.google.com",
    "instagram":     "https://www.instagram.com",
    "facebook":      "https://www.facebook.com",
    "steam":         "https://store.steampowered.com",
    "wikipedia":     "https://www.wikipedia.org",
    "stackoverflow": "https://stackoverflow.com",
    "gemini":        "https://gemini.google.com",
}

QUICK_PATHS = {
    "discord":   [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Discord", "Update.exe")],
    "spotify":   [os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe")],
    "steam":     ["C:\\Program Files (x86)\\Steam\\steam.exe", "C:\\Program Files\\Steam\\steam.exe"],
    "chrome":    ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"],
    "firefox":   ["C:\\Program Files\\Mozilla Firefox\\firefox.exe"],
    "edge":      ["C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"],
    "telegram":  [os.path.join(os.environ.get("APPDATA", ""), "Telegram Desktop", "Telegram.exe")],
    "vlc":       ["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"],
    "zoom":      [os.path.join(os.environ.get("APPDATA", ""), "Zoom", "bin", "Zoom.exe")],
    "notepad":   ["C:\\Windows\\System32\\notepad.exe"],
    "calculator":["C:\\Windows\\System32\\calc.exe"],
    "paint":     ["C:\\Windows\\System32\\mspaint.exe"],
    "word":      ["C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"],
    "excel":     ["C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"],
}

SEARCH_PATHS = [
    os.environ.get("PROGRAMFILES", "C:\\Program Files"),
    os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
    os.path.join(os.environ.get("APPDATA", ""), "..\\Local"),
    os.path.join(os.environ.get("APPDATA", "")),
    "C:\\Windows\\System32",
]

RUN_MAP = {
    "notepad":    "notepad.exe",
    "calculator": "calc.exe",
    "paint":      "mspaint.exe",
    "discord":    "discord.exe",
    "spotify":    "spotify.exe",
    "steam":      "steam.exe",
    "chrome":     "chrome.exe",
    "firefox":    "firefox.exe",
    "edge":       "msedge.exe",
    "telegram":   "telegram.exe",
    "vlc":        "vlc.exe",
    "zoom":       "zoom.exe",
    "word":       "winword.exe",
    "excel":      "excel.exe",
    "skype":      "skype.exe",
}

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"cf_handle": "", "current_problem_idx": 0}

def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

def fuzzy_match(text, keyword, threshold=0.75):
    text = text.lower()
    keyword = keyword.lower()
    if keyword in text:
        return True
    words = text.split()
    kwords = keyword.split()
    window = len(kwords)
    for i in range(len(words) - window + 1):
        chunk = " ".join(words[i:i+window])
        if SequenceMatcher(None, chunk, keyword).ratio() >= threshold:
            return True
    return False

def fuzzy_best_match(word, candidates, threshold=0.6):
    best, best_score = None, 0
    for c in candidates:
        score = SequenceMatcher(None, word, c).ratio()
        if score > best_score:
            best, best_score = c, score
    return best if best_score >= threshold else None

def find_exe(name):
    best_key = fuzzy_best_match(name, list(QUICK_PATHS.keys()) + list(RUN_MAP.keys()), threshold=0.6)
    if best_key and best_key in QUICK_PATHS:
        for path in QUICK_PATHS[best_key]:
            if os.path.exists(path):
                return path
    exe_name = RUN_MAP.get(best_key, f"{name}.exe") if best_key else f"{name}.exe"
    for base in SEARCH_PATHS:
        if not base or not os.path.exists(base):
            continue
        pattern = os.path.join(base, "**", exe_name)
        results = glob.glob(pattern, recursive=True)
        if results:
            return results[0]
    return None

def handle_run(target):
    target = target.lower().strip()
    path = find_exe(target)
    if path:
        try:
            subprocess.Popen([path])
            return True, path
        except Exception as e:
            return False, str(e)
    return False, None

def handle_kill(target):
    target = target.lower().strip()
    killed = []
    patterns = None
    for key in KILL_MAP:
        if fuzzy_match(target, key):
            patterns = KILL_MAP[key]
            break
    if not patterns:
        patterns = [target]
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            pname = proc.info["name"].lower().replace(".exe", "")
            for pat in patterns:
                if pat in pname or fuzzy_match(pname, pat, threshold=0.7):
                    proc.kill()
                    killed.append(proc.info["name"])
                    break
        except Exception:
            pass
    return killed

def handle_open(target):
    target = target.lower().strip()
    best = fuzzy_best_match(target, list(OPEN_MAP.keys()), threshold=0.6)
    url = OPEN_MAP[best] if best else f"https://www.{target}.com"
    return url

def parse_command(text):
    text_lower = text.lower().strip()
    words = text_lower.split()
    if not words: return None, None
    first = words[0]
    rest = " ".join(words[1:])
    if not rest: return None, None
    if fuzzy_match(first, "kill", threshold=0.85) or fuzzy_match(first, "close", threshold=0.85):
        return "kill", rest
    if fuzzy_match(first, "open", threshold=0.85) or fuzzy_match(first, "launch", threshold=0.85):
        return "open", rest
    if fuzzy_match(first, "run", threshold=0.85) or fuzzy_match(first, "start", threshold=0.85):
        return "run", rest
    return None, None


# ─── SANS OVERLAY WINDOW ─────────────────────────────────────────────────────
class SansWindow:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#010101")
        self.root.configure(bg="#010101")

        self.SANS_W = 225
        self.SANS_H = 225
        self.BOX_W = 260
        self.GAP = 10
        self.PAD = 10
        self.FONT = ("Courier New", 11, "bold")
        self.SPEED = 55
        self.SANSANG_LINGER = 2000
        self._stop_typing = False
        self._current_mode = "normal"
        self._current_sprite_name = "sans"
        self.commands_blocked = False
        self._verdict_lock = False
        self.app_callback = None
        self.parent_app = None

        # ─── VOICE SOUND ─────────────────────────────────────────────────
        self.sound_enabled = True
        self._voice_sound = None
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._voice_sound = pygame.mixer.Sound("voice_sans.mp3")
            self._voice_sound.set_volume(0.6)
        except Exception as e:
            print(f"[voice init err] {e}")

        self.pil_sprites = {}
        self.sprites = {}
        for name in ["sans", "sanslis", "sansproceed", "sanser", "sansad", "sansang"]:
            try:
                img = Image.open(f"{name}.png").convert("RGBA")
                img = img.resize((self.SANS_W, self.SANS_H), Image.NEAREST)
                self.pil_sprites[name] = img
                self.sprites[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"[warn] could not load {name}.png: {e}")
                self.pil_sprites[name] = self.pil_sprites.get("sans")
                self.sprites[name] = self.sprites.get("sans")

        # ─── SLEEP GIF ───────────────────────────────────────────────────
        self._sleep_frames = []
        self._sleep_frame_idx = 0
        self._sleep_anim_id = None
        self.is_sleeping = False
        self._sleep_attempt = 0
        try:
            gif = Image.open("sanssleep.gif")
            for i in range(gif.n_frames):
                gif.seek(i)
                frame = gif.copy().convert("RGBA").resize((300, 300), Image.NEAREST)
                self._sleep_frames.append(ImageTk.PhotoImage(frame))
        except Exception as e:
            print(f"[warn] sanssleep.gif not found: {e}")

        self.canvas = tk.Canvas(self.root, width=self.BOX_W, bg="#010101", highlightthickness=0)
        self.canvas.pack()

        sans_x = (self.BOX_W - self.SANS_W) // 2
        self.canvas.create_image(sans_x, 0, anchor="nw", image=self.sprites["sans"], tags="sans")

        self.box_y = self.SANS_H + self.GAP
        self.canvas.create_rectangle(
            0, self.box_y, self.BOX_W, self.box_y + 40,
            fill="#0d0000", outline="white", width=2, tags="box"
        )
        self.canvas.create_text(
            self.PAD, self.box_y + self.PAD,
            text="", anchor="nw",
            fill="white", font=self.FONT,
            width=self.BOX_W - self.PAD * 2,
            tags="txt"
        )

        self._update_box_size("")
        self._center_window()

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self._drag_x = 0
        self._drag_y = 0

    def start_sleep(self):
        self.is_sleeping = True
        self._sleep_attempt = 0
        self._stop_typing = True
        self.canvas.itemconfig("txt", text="")
        self._update_box_size("")
        self._animate_sleep()

    def stop_sleep(self):
        self.is_sleeping = False
        if self._sleep_anim_id:
            self.root.after_cancel(self._sleep_anim_id)
            self._sleep_anim_id = None
        sans_x = (self.BOX_W - self.SANS_W) // 2
        self.canvas.coords("sans", sans_x, 0)
        self.set_sprite("sanslis")

    def _animate_sleep(self):
        if not self.is_sleeping or not self._sleep_frames:
            return
        frame = self._sleep_frames[self._sleep_frame_idx % len(self._sleep_frames)]
        self.canvas.itemconfig("sans", image=frame)
        # center the 300x300 gif
        x = (self.BOX_W - 300) // 2
        self.canvas.coords("sans", x, 0)
        self._sleep_frame_idx += 1
        self._sleep_anim_id = self.root.after(80, self._animate_sleep)

    def handle_sleep_attempt(self):
        """Called when user tries to type while sans is sleeping."""
        msgs = [
            "sans is sleeping...",
            "i said sans is sleeping.",
            "I ALR SAID SANS IS SLEEPING",
            "LET HIM SLEEP BRO HE IS IN 99999th FLOOR OF SLEEP PARADISE",
        ]
        n = self._sleep_attempt
        if n < len(msgs):
            msg = msgs[n]
        else:
            msg = "sans is sleeping......"
        self._sleep_attempt += 1
        # flash msg in dialogue box briefly
        self._stop_typing = True
        self.root.after(50, lambda: self._show_sleep_msg(msg))

    def _show_sleep_msg(self, msg):
        self._stop_typing = False
        self.canvas.itemconfig("txt", text="")
        self._update_box_size("")
        self._type_letter(f"* {msg}", 0, None)

    def set_sprite(self, name):
        if self._verdict_lock: return
        sprite = self.sprites.get(name, self.sprites.get("sans"))
        if sprite:
            self._current_sprite_name = name
            self.canvas.itemconfig("sans", image=sprite)
            self.canvas.image = sprite

    def crossfade_to(self, target_name, steps=20, delay=30, on_done=None):
        src = self.pil_sprites.get(self._current_sprite_name, self.pil_sprites.get("sans"))
        dst = self.pil_sprites.get(target_name, self.pil_sprites.get("sans"))
        if src is None or dst is None:
            self._current_sprite_name = target_name
            if on_done: on_done()
            return
        self._crossfade_step(src, dst, target_name, 0, steps, delay, on_done)

    def _crossfade_step(self, src, dst, target_name, step, steps, delay, on_done):
        alpha = step / steps
        blended = Image.blend(src.convert("RGBA"), dst.convert("RGBA"), alpha)
        photo = ImageTk.PhotoImage(blended)
        self.canvas.itemconfig("sans", image=photo)
        self.canvas.image = photo
        if step >= steps:
            self._current_sprite_name = target_name
            if on_done: on_done()
            return
        self.root.after(delay, lambda: self._crossfade_step(src, dst, target_name, step + 1, steps, delay, on_done))

    def trigger_verdict(self, verdict):
        self.commands_blocked = True
        self._stop_typing = True
        self._verdict_lock = True

        advance = verdict == "AC"
        sprite = "sansang" if advance else "sansad"

        def on_ai_reply(reply):
            if not self._verdict_lock: return
            self._stop_typing = True
            self.root.after(50, lambda: self._begin_verdict_reply(reply, advance))

        self._pending_verdict_cb = on_ai_reply

        if advance:
            if self.parent_app:
                self.parent_app.on_ac_verdict()
        else:
            if self.parent_app:
                self.parent_app.on_wa_verdict(verdict)

        def after_fade():
            self._stop_typing = False
            self.canvas.itemconfig("txt", text="")
            self._update_box_size("")
            self._type_letter("* ...", 0, None)

        self.crossfade_to(sprite, steps=20, delay=30, on_done=after_fade)

    def _begin_verdict_reply(self, reply, advance):
        self._stop_typing = False
        self.canvas.itemconfig("txt", text="")
        self._update_box_size("")
        # type the reply, then after it finishes + 2sec linger, end verdict
        char_count = len(reply) + 2  # account for "* " prefix
        total_ms = char_count * self.SPEED + 2000
        self._type_letter(f"* {reply}", 0, None)
        self.root.after(total_ms, lambda: self._end_verdict(advance))

    def _end_verdict(self, advance_problem):
        self._verdict_lock = False
        self.crossfade_to("sanslis", steps=20, delay=30, on_done=lambda: self._finish_verdict_process(advance_problem))

    def _finish_verdict_process(self, advance_problem):
        self.commands_blocked = False
        if advance_problem and self.app_callback:
            self.app_callback()

    def speak(self, text, mode="normal", on_done=None):
        if self._verdict_lock: return
        self._stop_typing = True
        self.root.after(100, lambda: self._start_typewriter(text, mode, on_done))

    def _start_typewriter(self, full_text, mode, on_done):
        self._stop_typing = False
        self._current_mode = mode
        self.canvas.itemconfig("txt", text="")
        self._update_box_size("")
        if not self._verdict_lock:
            if mode == "sad":
                self.set_sprite("sansad")
            elif mode in ("command", "contest", "kill", "run", "problem"):
                self.set_sprite("sansang")
            else:
                self.set_sprite("sanslis")
        self._type_letter(f"* {full_text.lower()}", 0, on_done)

    def _type_letter(self, full_text, i, on_done):
        if self._stop_typing: return
        if i > len(full_text):
            if not self._verdict_lock:
                linger = self.SANSANG_LINGER if self._current_mode in ("command", "contest", "kill", "run", "problem") else 3000
                if on_done:
                    self.root.after(linger, on_done)
                else:
                    self.root.after(linger, lambda: self.set_sprite("sanslis"))
            return
        # play voice tick on each non-space character
        if i > 0 and self.sound_enabled and self._voice_sound:
            ch = full_text[i - 1]
            if ch != " ":
                try:
                    self._voice_sound.play()
                except Exception:
                    pass
        self.canvas.itemconfig("txt", text=full_text[:i])
        self._update_box_size(full_text[:i])
        self.root.after(self.SPEED, lambda: self._type_letter(full_text, i + 1, on_done))

    def _update_box_size(self, text):
        self.root.update_idletasks()
        bbox = self.canvas.bbox("txt")
        text_h = (bbox[3] - bbox[1]) if bbox else 16
        box_h = text_h + self.PAD * 2
        total_h = self.SANS_H + self.GAP + box_h
        self.canvas.coords("box", 0, self.box_y, self.BOX_W, self.box_y + box_h)
        self.canvas.coords("txt", self.PAD, self.box_y + self.PAD)
        self.canvas.config(height=total_h)
        self.root.geometry(f"{self.BOX_W}x{total_h}")

    def _center_window(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"+{sw//2}+{sh//2}")

    def start_drag(self, e):
        self._drag_x = e.x
        self._drag_y = e.y

    def do_drag(self, e):
        x = self.root.winfo_x() + e.x - self._drag_x
        y = self.root.winfo_y() + e.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")



# ─── CF SUBMISSION TRACKER ───────────────────────────────────────────────────
class CFChecker:
    def __init__(self, sans, handle):
        self.sans = sans
        self.handle = handle
        self.seen_ids = set()
        self.running = True
        self._init_seen()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _init_seen(self):
        if not self.handle: return
        try:
            resp = requests.get(f"https://codeforces.com/api/user.status?handle={self.handle}&from=1&count=20", timeout=10)
            data = resp.json()
            if data.get("status") == "OK":
                for sub in data["result"]:
                    self.seen_ids.add(sub["id"])
        except Exception as e:
            print(f"[CF init err] {e}")

    def update_handle(self, new_handle):
        self.handle = new_handle
        self.seen_ids = set()
        self._init_seen()

    def _loop(self):
        while self.running:
            try:
                self._check()
            except Exception as e:
                print(f"[CF checker err] {e}")
            time.sleep(3)

    def _check(self):
        if not self.handle or self.sans.commands_blocked: return
        resp = requests.get(f"https://codeforces.com/api/user.status?handle={self.handle}&from=1&count=5", timeout=10)
        data = resp.json()
        if data.get("status") != "OK": return
        for sub in data["result"]:
            sid = sub["id"]
            if sid in self.seen_ids: continue
            verdict = sub.get("verdict", "")
            if not verdict or verdict == "TESTING": continue
            self.seen_ids.add(sid)
            if verdict == "OK":
                self.sans.root.after(0, self.sans.trigger_verdict, "AC")
            else:
                # WA, TLE, MLE, RE, CE, etc all count as failure
                self.sans.root.after(0, self.sans.trigger_verdict, verdict)
            break

    def stop(self):
        self.running = False


# ─── RATED CONTEST AUTO-OPENER ───────────────────────────────────────────────

# ─── PROBLEM FILE PARSER ─────────────────────────────────────────────────────
def parse_problem_file(path):
    import re
    results = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        pattern = r'\{"name":\s*"([^"]+)",\s*"url":\s*"([^"]+)",\s*"tier":\s*"([^"]+)"\}'
        for m in re.finditer(pattern, content):
            results.append({"name": m.group(1), "url": m.group(2), "tier": m.group(3)})
    except Exception as e:
        print(f"[parse err] {e}")
    return results


def check_account_anniversary(app):
    """Fetches CF handle registration year and shows a Groq-generated celebration popup."""
    handle = app.settings.get("cf_handle", "")
    if not handle:
        return

    def _fetch():
        try:
            resp = requests.get(f"https://codeforces.com/api/user.info?handles={handle}", timeout=10)
            data = resp.json()
            if data.get("status") != "OK": return
            reg_ts = data["result"][0].get("registrationTimeSeconds", 0)
            if not reg_ts: return
            import datetime
            reg_year = datetime.datetime.utcfromtimestamp(reg_ts).year
            current_year = datetime.datetime.utcnow().year
            years_ago = current_year - reg_year

            last_shown = app.settings.get("last_anniversary_shown")
            if last_shown == years_ago:
                return  # already congratulated for this year, don't repeat
            app.settings["last_anniversary_shown"] = years_ago
            save_settings(app.settings)

            _ask_groq(handle, reg_year, years_ago)
        except Exception as e:
            print(f"[anniversary err] {e}")

    def _ask_groq(handle, reg_year, years_ago):
        try:
            from groq import Groq
            API_KEY = "gogetyours:p"
            client = Groq(api_key=API_KEY)

            age_vibes = {
                1:  "this account is exactly 1 year old. it's basically a baby. celebrate their first year like a proud skeleton parent. mention it's their 1st anniversary.",
                2:  "this account is 2 years old. they survived their toddler phase. hype them up for making it past year 1.",
                3:  "this account is 3 years old. 3 years of pain and growth. make a joke about how they're still here after all this time.",
                4:  "this account is 4 years old. four whole years. reference that 4 is an unlucky number in some cultures but they're still grinding anyway.",
                5:  "this account is 5 years old. half a decade of competitive programming suffering. celebrate this milestone BIG. 5 years is huge.",
                6:  "this account is 6 years old. reference the number 6 somehow creatively. they're past the honeymoon phase of cp, they're veterans now.",
                7:  "this account is 7 years old. 7 is a lucky number. make a lucky number joke and celebrate their journey.",
                8:  "this account is 8 years old. 8 looks like infinity sideways. make an infinite grind joke.",
                9:  "this account is 9 years old. one year away from a decade. hype up the almost-decade milestone.",
                10: "this account is 10 years old. A FULL DECADE. go absolutely wild. this is legendary. mention 10 years explicitly and treat them like a god.",
            }
            if years_ago in age_vibes:
                vibe = age_vibes[years_ago]
            elif years_ago > 10:
                vibe = f"this account is {years_ago} years old. that is beyond legendary. they have been on codeforces longer than some people have been in high school. treat them as an ancient deity of competitive programming."
            else:
                vibe = f"this account is {years_ago} years old. celebrate this specific milestone creatively and mention the number {years_ago} explicitly."

            prompt = (
                f"you are sans from undertale. write a SHORT celebration message (3-4 sentences max) "
                f"for a codeforces user named '{handle}' whose account is exactly {years_ago} year{'s' if years_ago != 1 else ''} old. "
                f"{vibe} "
                f"be creative, funny, lowercase, lazy sans style. mention the number {years_ago} specifically in ur response. "
                f"do NOT sign the message, that is handled separately."
            )

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=120
            )
            msg = completion.choices[0].message.content.strip().lower()
            app.root.after(0, lambda: _show_popup(msg, reg_year, years_ago))
        except Exception as e:
            print(f"[anniversary groq err] {e}")

    def _show_popup(msg, reg_year, years_ago):
        popup = tk.Toplevel(app.root)
        popup.title("* heh.")
        popup.configure(bg="#0a0a0a")
        popup.resizable(False, False)
        popup.grab_set()

        pw, ph = 460, 280
        sx = app.root.winfo_screenwidth()
        sy = app.root.winfo_screenheight()
        popup.geometry(f"{pw}x{ph}+{(sx-pw)//2}+{(sy-ph)//2}")

        # year badge
        tk.Label(popup, text=f"✦ {years_ago} year{'s' if years_ago != 1 else ''} on codeforces ✦",
                 fg="#ffcc00", bg="#0a0a0a",
                 font=("Consolas", 13, "bold")).pack(pady=(18, 4))

        tk.Label(popup, text=f"(registered in {reg_year})",
                 fg="#444", bg="#0a0a0a",
                 font=("Consolas", 8)).pack()

        # message box
        msg_frame = tk.Frame(popup, bg="#111", bd=0)
        msg_frame.pack(fill="x", padx=20, pady=14)

        tk.Label(msg_frame, text=f"* {msg}",
                 fg="#ffffff", bg="#111",
                 font=("Consolas", 9), wraplength=400,
                 justify="left", padx=12, pady=12).pack(fill="x")

        # handwritten signature
        tk.Label(popup, text="- sans",
                 fg="#aaaaaa", bg="#0a0a0a",
                 font=("Papyrus", 13) if "Papyrus" in popup.tk.call("font", "families") else ("Consolas", 11, "italic"),
                 anchor="e").pack(anchor="e", padx=30)

        tk.Button(popup, text="heh. thanks.",
                  command=popup.destroy,
                  bg="#111", fg="#00ff99",
                  font=("Consolas", 9), relief="flat",
                  padx=12, pady=5, cursor="hand2").pack(pady=(10, 16))

    threading.Thread(target=_fetch, daemon=True).start()


def check_and_open_rated_contest(sans, app):
    """Checks CF API for any currently running rated contest and opens it."""
    def _fetch():
        try:
            resp = requests.get("https://codeforces.com/api/contest.list?gym=false", timeout=10)
            data = resp.json()
            if data.get("status") != "OK":
                return
            now = time.time()
            for contest in data["result"]:
                phase = contest.get("phase", "")
                rated = contest.get("difficulty", "") != "" or contest.get("type", "") in ("CF", "ICPC", "IOI")
                start = contest.get("startTimeSeconds", 0)
                duration = contest.get("durationSeconds", 0)
                end = start + duration
                # Live right now + not finished + has a rating type
                if phase == "CODING" and start <= now <= end:
                    cid = contest["id"]
                    name = contest.get("name", f"Contest #{cid}")
                    url = f"https://codeforces.com/contest/{cid}"
                    msg = f"heh. rated contest is live right now, kid. '{name}'. opening it for u."
                    sans.root.after(0, lambda m=msg, u=url: _announce(m, u))
                    return
        except Exception as e:
            print(f"[contest check err] {e}")

    def _announce(msg, url):
        def do_open():
            webbrowser.open(url)
            sans.set_sprite("sanslis")
        sans.speak(msg, "contest", do_open)

    threading.Thread(target=_fetch, daemon=True).start()



class TextApp:
    def __init__(self, root, sans, cf_checker):
        self.root = root
        self.sans = sans
        self.cf_checker = cf_checker
        self.sans.parent_app = self
        self.settings = load_settings()
        self.current_prob_idx = self.settings.get("current_problem_idx", 0)

        # ─── SHEET MANAGER ────────────────────────────────────────────────
        # migrate old flat PROBLEM_LIST into sheets if needed
        if "sheets" not in self.settings:
            self.settings["sheets"] = {"Default": list(PROBLEM_LIST)}
            self.settings["active_sheet"] = "Default"
            save_settings(self.settings)
        self._load_active_sheet()

        self.sans.app_callback = self.advance_to_next_problem
        self.blessing = 0
        self.rage = 0
        self.session_ac_count = 0  # tracks ACs this session for break mechanic
        self._break_threshold = 0  # randomized per break (10-13)
        self._on_break = False     # true while sans is on a timed break

        # ─── HUMAN MODE / SLEEP ───────────────────────────────────────────
        self.human_mode_var = tk.BooleanVar(value=self.settings.get("human_mode", False))
        self._sleep_check_id = None
        self._start_sleep_checker()
        self._start_rating_checker()

        self.root.title("Sans Sheet Helper (Groq Edition)")
        self.root.geometry("600x750")
        self.root.configure(bg="#0f0f0f")

        cf_frame = tk.Frame(root, bg="#0f0f0f")
        cf_frame.pack(fill="x", padx=15, pady=(15, 0))

        tk.Label(cf_frame, text="🏆 CODEFORCES HANDLE", fg="#555", bg="#0f0f0f",
                 font=("Consolas", 8, "bold")).pack(anchor="w")

        cf_row = tk.Frame(cf_frame, bg="#0f0f0f")
        cf_row.pack(fill="x", pady=(4, 0))

        self.cf_var = tk.StringVar(value=self.settings.get("cf_handle", ""))
        self.cf_entry = tk.Entry(cf_row, textvariable=self.cf_var,
                                  bg="#1a1a1a", fg="#00ffcc", insertbackground="#00ffcc",
                                  font=("Consolas", 10), relief="flat", width=30)
        self.cf_entry.pack(side="left", padx=(0, 6), ipady=4)

        tk.Button(cf_row, text="SAVE", command=self.save_cf_handle,
                  bg="#003333", fg="#00ffcc", font=("Consolas", 9),
                  relief="flat", padx=8, cursor="hand2").pack(side="left")

        self.cf_status = tk.Label(cf_row, text="", fg="#555", bg="#0f0f0f", font=("Consolas", 8))
        self.cf_status.pack(side="left", padx=(8, 0))

        # ─── HUMAN MODE + PREVIEW ROW ─────────────────────────────────────
        extra_row = tk.Frame(cf_frame, bg="#0f0f0f")
        extra_row.pack(fill="x", pady=(8, 0))

        self.human_cb = tk.Checkbutton(extra_row, text="🌙 Human Mode (sleeps 11pm–7am)",
                   variable=self.human_mode_var, command=self.toggle_human_mode,
                   bg="#0f0f0f", fg="#aaaaaa", selectcolor="#0f0f0f",
                   activebackground="#0f0f0f", activeforeground="#ffffff",
                   font=("Consolas", 9), cursor="hand2")
        self.human_cb.pack(side="left")

        tk.Button(extra_row, text="🔍 Preview Sleep", command=self.preview_sleep,
                  bg="#111133", fg="#8888ff", font=("Consolas", 8),
                  relief="flat", padx=8, cursor="hand2").pack(side="right")

        sheet_frame = tk.LabelFrame(root, text=" SHEET PROGRESSION CONSOLE ", fg="#00ffcc", bg="#0a0a0a",
                                    font=("Consolas", 9, "bold"), padx=12, pady=12)
        sheet_frame.pack(fill="x", padx=15, pady=15)

        self.prob_label = tk.Label(sheet_frame, text="Current Task: Loading...", fg="white", bg="#0a0a0a",
                                   font=("Consolas", 11, "bold"), justify="left", anchor="w")
        self.prob_label.pack(fill="x", pady=2)

        prob_id_row = tk.Frame(sheet_frame, bg="#0a0a0a")
        prob_id_row.pack(fill="x", pady=(0, 2))
        self.prob_id_label = tk.Label(prob_id_row, text="📋 --", fg="#ffcc00", bg="#0a0a0a",
                                      font=("Consolas", 11, "bold"), anchor="w", cursor="hand2")
        self.prob_id_label.pack(side="left")
        tk.Label(prob_id_row, text=" (click to copy)", fg="#555", bg="#0a0a0a",
                 font=("Consolas", 8)).pack(side="left")
        self.prob_id_label.bind("<Button-1>", self.copy_prob_id)

        self.tier_label = tk.Label(sheet_frame, text="Tier: --", fg="#ffaa00", bg="#0a0a0a",
                                   font=("Consolas", 9, "italic"), justify="left", anchor="w")
        self.tier_label.pack(fill="x", pady=(0, 6))

        btn_row = tk.Frame(sheet_frame, bg="#0a0a0a")
        btn_row.pack(fill="x", pady=(4, 0))

        tk.Button(btn_row, text="LAUNCH PROBLEM LINK", command=self.launch_current_problem,
                  bg="#113355", fg="#33ccff", font=("Consolas", 9, "bold"),
                  relief="flat", padx=10, cursor="hand2").pack(side="left", padx=(0, 10))

        tk.Button(btn_row, text="SKIP PROBLEM", command=self.advance_to_next_problem,
                  bg="#222", fg="#aaa", font=("Consolas", 9),
                  relief="flat", padx=8, cursor="hand2").pack(side="left", padx=(0, 10))

        self.voice_btn = tk.Button(btn_row, text="🔊 VOICE ON", command=self.toggle_voice,
                  bg="#113322", fg="#00ff99", font=("Consolas", 9),
                  relief="flat", padx=8, cursor="hand2")
        self.voice_btn.pack(side="left", padx=(0, 10))

        tk.Button(btn_row, text="💬 Float Chat", command=self._toggle_float_chat,
                  bg="#0d1a2a", fg="#66aaff", font=("Consolas", 9),
                  relief="flat", padx=8, cursor="hand2").pack(side="left", padx=(0, 10))

        tk.Button(btn_row, text="📂 Load Problems", command=self.open_problem_file,
                  bg="#1a0033", fg="#cc88ff", font=("Consolas", 9),
                  relief="flat", padx=8, cursor="hand2").pack(side="left")

        # drag-drop zone
        self.drop_zone = tk.Label(sheet_frame,
                  text="  ⬇ drag & drop problem .txt here  ",
                  fg="#444", bg="#111", font=("Consolas", 8),
                  relief="flat", pady=4, cursor="hand2")
        self.drop_zone.pack(fill="x", pady=(6, 0))
        self.drop_zone.bind("<Button-1>", lambda e: self.open_problem_file())
        try:
            from tkinterdnd2 import DND_FILES
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind("<<Drop>>", self.on_file_drop)
        except Exception:
            pass

        tk.Label(root, text="💬 INTERACTION LOG", fg="#555", bg="#0f0f0f", font=("Consolas", 8, "bold")).pack(anchor="w", padx=15)
        
        self.textbox = tk.Text(root, height=14, width=55, bg="#161616", fg="#00ffcc",
                               font=("Consolas", 10), padx=15, pady=15, borderwidth=0)
        self.textbox.pack(fill="both", expand=True, padx=15, pady=5)

        self.textbox.tag_configure("sad",   foreground="#4488ff", font=("Consolas", 10, "bold"))
        self.textbox.tag_configure("angry", foreground="#ff3333", font=("Consolas", 10, "bold"))
        self.textbox.tag_configure("normal",foreground="#00ffcc", font=("Consolas", 10))

        input_frame = tk.Frame(root, bg="#0f0f0f")
        input_frame.pack(fill="x", padx=15, pady=(5, 15))

        tk.Label(input_frame, text=">>", fg="#00ffcc", bg="#0f0f0f", font=("Consolas", 11, "bold")).pack(side="left", padx=(0, 5))

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var,
                                    bg="#1c1c1c", fg="white", insertbackground="#00ffcc",
                                    font=("Consolas", 11), relief="flat")
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.input_entry.bind("<Return>", self.process_keyboard_input)
        self.input_entry.focus_set()

        self.sync_problem_display()
        self.sans.root.after(500, lambda: self.sans.set_sprite("sanslis"))
        self.root.after(1000, self.launch_current_problem)

    def _load_active_sheet(self):
        global PROBLEM_LIST
        sheets = self.settings.get("sheets", {})
        active = self.settings.get("active_sheet", "")
        if active in sheets:
            PROBLEM_LIST = sheets[active]
        elif sheets:
            first = list(sheets.keys())[0]
            self.settings["active_sheet"] = first
            PROBLEM_LIST = sheets[first]
        else:
            PROBLEM_LIST = []

    def _save_sheet(self, name, problems):
        sheets = self.settings.get("sheets", {})
        sheets[name] = problems
        self.settings["sheets"] = sheets
        save_settings(self.settings)

    def _delete_sheet(self, name):
        sheets = self.settings.get("sheets", {})
        if name in sheets:
            del sheets[name]
        self.settings["sheets"] = sheets
        if self.settings.get("active_sheet") == name:
            first = list(sheets.keys())[0] if sheets else ""
            self.settings["active_sheet"] = first
        save_settings(self.settings)
        self._load_active_sheet()
        self.current_prob_idx = 0
        self.settings["current_problem_idx"] = 0
        save_settings(self.settings)
        self.sync_problem_display()

    def open_problem_file(self):
        """Open the sheet manager window."""
        self.open_sheet_manager()

    def open_sheet_manager(self):
        win = tk.Toplevel(self.root)
        win.title("* problem sheets")
        win.configure(bg="#0a0a0a")
        win.resizable(False, False)
        win.grab_set()
        pw, ph = 500, 460
        sx = self.root.winfo_screenwidth()
        sy = self.root.winfo_screenheight()
        win.geometry(f"{pw}x{ph}+{(sx-pw)//2}+{(sy-ph)//2}")

        tk.Label(win, text="* ur problem sheets, kid.",
                 fg="#ffffff", bg="#0a0a0a", font=("Consolas", 11, "bold")).pack(anchor="w", padx=16, pady=(16,4))
        tk.Label(win, text="click a sheet to activate it. add, rename, or delete as needed.",
                 fg="#555", bg="#0a0a0a", font=("Consolas", 8)).pack(anchor="w", padx=16, pady=(0,10))

        # ── scrollable sheet list ──────────────────────────────────────────
        list_frame = tk.Frame(win, bg="#111", bd=0)
        list_frame.pack(fill="both", expand=True, padx=16)

        canvas = tk.Canvas(list_frame, bg="#111", highlightthickness=0)
        sb = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg="#111")
        cw = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))

        def rebuild():
            for w in inner.winfo_children():
                w.destroy()
            sheets = self.settings.get("sheets", {})
            active = self.settings.get("active_sheet", "")
            if not sheets:
                tk.Label(inner, text="no sheets yet. add one below.", fg="#555",
                         bg="#111", font=("Consolas", 9), pady=12).pack()
                return
            for name, probs in sheets.items():
                is_active = name == active
                row = tk.Frame(inner, bg="#1a2a1a" if is_active else "#111",
                               highlightthickness=1,
                               highlightbackground="#00ff99" if is_active else "#222")
                row.pack(fill="x", padx=4, pady=3)

                # active indicator
                indicator = "▶ " if is_active else "   "
                name_lbl = tk.Label(row,
                    text=f"{indicator}{name}  ({len(probs)} problems)",
                    fg="#00ff99" if is_active else "#aaaaaa",
                    bg="#1a2a1a" if is_active else "#111",
                    font=("Consolas", 9, "bold" if is_active else "normal"),
                    anchor="w", cursor="hand2")
                name_lbl.pack(side="left", padx=10, pady=8, fill="x", expand=True)

                # activate on click
                def make_activate(n):
                    def _activate(e=None):
                        global PROBLEM_LIST
                        self.settings["active_sheet"] = n
                        self.current_prob_idx = 0
                        self.settings["current_problem_idx"] = 0
                        save_settings(self.settings)
                        self._load_active_sheet()
                        self.sync_problem_display()
                        self.sans.speak(f"heh. switched to sheet '{n}'. {len(PROBLEM_LIST)} problems loaded.", "normal")
                        win.destroy()
                    return _activate
                name_lbl.bind("<Button-1>", make_activate(name))
                row.bind("<Button-1>", make_activate(name))

                btn_frame = tk.Frame(row, bg="#1a2a1a" if is_active else "#111")
                btn_frame.pack(side="right", padx=6)

                # rename
                def make_rename(n):
                    def _rename():
                        rwin = tk.Toplevel(win)
                        rwin.title("rename sheet")
                        rwin.configure(bg="#0a0a0a")
                        rwin.geometry("300x110")
                        rwin.grab_set()
                        tk.Label(rwin, text="new name:", fg="#aaa", bg="#0a0a0a",
                                 font=("Consolas", 9)).pack(pady=(14,4))
                        rv = tk.StringVar(value=n)
                        re_ = tk.Entry(rwin, textvariable=rv, bg="#1a1a1a", fg="#fff",
                                       font=("Consolas", 10), relief="flat",
                                       highlightthickness=1, highlightbackground="#333")
                        re_.pack(padx=16, fill="x", ipady=4)
                        re_.focus_set()
                        def do_rename(e=None):
                            new_name = rv.get().strip()
                            if not new_name or new_name == n: rwin.destroy(); return
                            sheets = self.settings.get("sheets", {})
                            sheets[new_name] = sheets.pop(n)
                            self.settings["sheets"] = sheets
                            if self.settings.get("active_sheet") == n:
                                self.settings["active_sheet"] = new_name
                            save_settings(self.settings)
                            rwin.destroy()
                            rebuild()
                        tk.Button(rwin, text="rename", command=do_rename,
                                  bg="#113322", fg="#00ff99", font=("Consolas", 9),
                                  relief="flat", padx=10, pady=4, cursor="hand2").pack(pady=8)
                        rwin.bind("<Return>", do_rename)
                    return _rename

                # delete
                def make_delete(n):
                    def _delete():
                        sheets = self.settings.get("sheets", {})
                        if len(sheets) <= 1:
                            self.update_colored_text("[System] can't delete the last sheet, kid.\n")
                            return
                        self._delete_sheet(n)
                        rebuild()
                    return _delete

                tk.Button(btn_frame, text="✏", command=make_rename(name),
                          bg="#222", fg="#aaa", font=("Consolas", 9),
                          relief="flat", padx=6, cursor="hand2").pack(side="left", padx=2)
                tk.Button(btn_frame, text="🗑", command=make_delete(name),
                          bg="#221111", fg="#ff4444", font=("Consolas", 9),
                          relief="flat", padx=6, cursor="hand2").pack(side="left", padx=2)

        rebuild()

        # ── bottom: add new sheet ──────────────────────────────────────────
        sep = tk.Frame(win, bg="#222", height=1)
        sep.pack(fill="x", padx=16, pady=10)

        add_row = tk.Frame(win, bg="#0a0a0a")
        add_row.pack(fill="x", padx=16, pady=(0, 16))

        tk.Label(add_row, text="+ new sheet name:", fg="#555", bg="#0a0a0a",
                 font=("Consolas", 8)).pack(side="left")
        new_name_var = tk.StringVar()
        name_entry = tk.Entry(add_row, textvariable=new_name_var, width=16,
                              bg="#1a1a1a", fg="#ffffff", font=("Consolas", 9),
                              relief="flat", highlightthickness=1,
                              highlightbackground="#333", highlightcolor="#00ff99",
                              insertbackground="#fff")
        name_entry.pack(side="left", padx=8, ipady=3)

        def add_ai():
            name = new_name_var.get().strip()
            if not name:
                name_entry.focus_set()
                return
            win.destroy()
            self._new_sheet_ai(name)

        def add_human():
            name = new_name_var.get().strip()
            if not name:
                name_entry.focus_set()
                return
            from tkinter import filedialog
            path = filedialog.askopenfilename(
                title="pick problem txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if not path: return
            problems = parse_problem_file(path)
            if not problems:
                self.update_colored_text("[System] no problems found in that file, kid.\n")
                return
            win.destroy()
            self._finalize_new_sheet(name, problems)

        tk.Button(add_row, text="🤖 AI", command=add_ai,
                  bg="#0d1a0d", fg="#00ff99", font=("Consolas", 9, "bold"),
                  relief="flat", padx=10, pady=4, cursor="hand2").pack(side="left", padx=2)
        tk.Button(add_row, text="📄 txt", command=add_human,
                  bg="#0d0d1a", fg="#8888ff", font=("Consolas", 9, "bold"),
                  relief="flat", padx=10, pady=4, cursor="hand2").pack(side="left", padx=2)

    def _new_sheet_ai(self, sheet_name):
        """Open AI generator for a new named sheet."""
        win = tk.Toplevel(self.root)
        win.title(f"* generating sheet: {sheet_name}")
        win.configure(bg="#0a0a0a")
        win.resizable(False, False)
        win.grab_set()
        pw, ph = 460, 300
        sx = self.root.winfo_screenwidth()
        sy = self.root.winfo_screenheight()
        win.geometry(f"{pw}x{ph}+{(sx-pw)//2}+{(sy-ph)//2}")

        tk.Label(win, text=f"* new sheet: \"{sheet_name}\"",
                 fg="#ffcc00", bg="#0a0a0a", font=("Consolas", 10, "bold")).pack(anchor="w", padx=16, pady=(16,2))
        tk.Label(win, text="describe the problems u want for this sheet.",
                 fg="#555", bg="#0a0a0a", font=("Consolas", 8)).pack(anchor="w", padx=16, pady=(0,6))
        tk.Label(win, text="e.g. \"1100 rated tricky impl\" / \"greedy 1300+\" / \"graph bfs 1500\"",
                 fg="#333", bg="#0a0a0a", font=("Consolas", 8)).pack(anchor="w", padx=16, pady=(0,10))

        entry_var = tk.StringVar()
        entry = tk.Entry(win, textvariable=entry_var,
                         bg="#1a1a1a", fg="#00ffcc", insertbackground="#00ffcc",
                         font=("Consolas", 11), relief="flat",
                         highlightthickness=1, highlightbackground="#333", highlightcolor="#00ff99")
        entry.pack(fill="x", padx=16, ipady=6)
        entry.focus_set()

        count_row = tk.Frame(win, bg="#0a0a0a")
        count_row.pack(fill="x", padx=16, pady=(8,0))
        tk.Label(count_row, text="how many?", fg="#555", bg="#0a0a0a", font=("Consolas", 8)).pack(side="left")
        count_var = tk.IntVar(value=8)
        tk.Spinbox(count_row, from_=3, to=20, textvariable=count_var, width=4,
                   bg="#1a1a1a", fg="#ffffff", font=("Consolas", 9),
                   relief="flat", justify="center").pack(side="left", padx=8)

        status = tk.Label(win, text="", fg="#ffaa00", bg="#0a0a0a", font=("Consolas", 8))
        status.pack(pady=(8,0))

        def generate():
            desc = entry_var.get().strip()
            if not desc:
                status.config(text="* type something first, kid.")
                return
            count = count_var.get()
            status.config(text="* asking groq... give me a sec.")
            gen_btn.config(state="disabled")

            def _fetch():
                try:
                    from groq import Groq
                    API_KEY = "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"
                    client = Groq(api_key=API_KEY)
                    prompt = (
                        f"Generate exactly {count} Codeforces competitive programming problems matching: \"{desc}\".\n"
                        f"Output ONLY a Python list of dicts, no explanation, no markdown, no backticks.\n"
                        f"Each dict EXACTLY like:\n"
                        f'{{"name": "Problem Name", "url": "https://codeforces.com/problemset/problem/ID/LETTER", "tier": "RATING Rated (Short Description)"}}\n'
                        f"Use real existing Codeforces problems. Output only the raw list starting with [ and ending with ]."
                    )
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3, max_tokens=1200
                    )
                    import re
                    raw = completion.choices[0].message.content.strip()
                    matches = re.findall(r'\{"name":\s*"([^"]+)",\s*"url":\s*"([^"]+)",\s*"tier":\s*"([^"]+)"\}', raw)
                    problems = [{"name": m[0], "url": m[1], "tier": m[2]} for m in matches]
                    if not problems:
                        win.after(0, lambda: status.config(text="* groq returned nothing useful. try again."))
                        win.after(0, lambda: gen_btn.config(state="normal"))
                        return
                    win.after(0, lambda: _done(problems))
                except Exception as e:
                    win.after(0, lambda: status.config(text=f"* groq error: {str(e)[:40]}"))
                    win.after(0, lambda: gen_btn.config(state="normal"))

            def _done(problems):
                win.destroy()
                self.show_problem_chooser(problems, target_sheet=sheet_name)

            threading.Thread(target=_fetch, daemon=True).start()

        gen_btn = tk.Button(win, text="✨ Generate",
                  command=generate,
                  bg="#0d1a0d", fg="#00ff99", font=("Consolas", 11, "bold"),
                  relief="flat", padx=16, pady=8, cursor="hand2")
        gen_btn.pack(pady=14)
        win.bind("<Return>", lambda e: generate())

    def _finalize_new_sheet(self, name, problems):
        """Show chooser then save as new sheet."""
        self.show_problem_chooser(problems, target_sheet=name)

    def on_file_drop(self, event):
        path = event.data.strip().strip("{}")
        self._load_problems_from(path)

    def _load_problems_from(self, path):
        problems = parse_problem_file(path)
        if not problems:
            self.update_colored_text("[System] heh. couldn't find any problems in that file, kid.\n")
            return
        self.update_colored_text(f"[System] found {len(problems)} problems. pick ur ones, kid.\n")
        self.show_problem_chooser(problems)

    def show_problem_chooser(self, problems, target_sheet=None):
        # load already-solved urls from settings
        solved_urls = set(self.settings.get("solved_urls", []))

        win = tk.Toplevel(self.root)
        win.title("* pick ur problems, kid")
        win.configure(bg="#0a0a0a")
        win.geometry("560x520")
        win.grab_set()

        tk.Label(win, text="* choose which problems to add to ur list.\n  already solved ones are auto-unchecked.",
                 fg="#aaa", bg="#0a0a0a", font=("Consolas", 9), justify="left").pack(anchor="w", padx=14, pady=(10,4))

        # tier filter row
        filter_frame = tk.Frame(win, bg="#0a0a0a")
        filter_frame.pack(fill="x", padx=14, pady=(0,6))
        tk.Label(filter_frame, text="filter tier:", fg="#555", bg="#0a0a0a", font=("Consolas", 8)).pack(side="left")
        tiers = sorted(set(p["tier"] for p in problems))
        tier_var = tk.StringVar(value="all")
        tier_menu = tk.OptionMenu(filter_frame, tier_var, "all", *tiers)
        tier_menu.config(bg="#111", fg="#cc88ff", font=("Consolas", 8), relief="flat", highlightthickness=0)
        tier_menu["menu"].config(bg="#111", fg="#cc88ff", font=("Consolas", 8))
        tier_menu.pack(side="left", padx=6)

        # scrollable list
        canvas = tk.Canvas(win, bg="#0a0a0a", highlightthickness=0)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True, padx=14)

        inner = tk.Frame(canvas, bg="#0a0a0a")
        canvas_window = canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        vars_ = []
        rows = []

        def rebuild_list(*_):
            for w in inner.winfo_children():
                w.destroy()
            rows.clear()
            vars_.clear()
            sel_tier = tier_var.get()
            for p in problems:
                if sel_tier != "all" and p["tier"] != sel_tier:
                    continue
                already_solved = p["url"] in solved_urls
                var = tk.BooleanVar(value=not already_solved)
                vars_.append((var, p))
                row = tk.Frame(inner, bg="#0a0a0a")
                row.pack(fill="x", pady=1)
                cb = tk.Checkbutton(row, variable=var, bg="#0a0a0a",
                                    activebackground="#0a0a0a", selectcolor="#0a0a0a",
                                    fg="#00ff99" if not already_solved else "#555",
                                    cursor="hand2")
                cb.pack(side="left")
                lbl_text = f"{p['name']}  [{p['tier']}]"
                if already_solved:
                    lbl_text += "  ✓ solved"
                tk.Label(row, text=lbl_text,
                         fg="#00ff99" if not already_solved else "#555",
                         bg="#0a0a0a", font=("Consolas", 9), anchor="w").pack(side="left")
                rows.append((var, p))

        tier_var.trace_add("write", rebuild_list)
        rebuild_list()

        # bottom buttons
        bot = tk.Frame(win, bg="#0a0a0a")
        bot.pack(fill="x", padx=14, pady=10)

        def select_all():
            for var, _ in vars_: var.set(True)
        def deselect_all():
            for var, _ in vars_: var.set(False)

        tk.Button(bot, text="all", command=select_all,
                  bg="#222", fg="#aaa", font=("Consolas", 8), relief="flat", padx=6).pack(side="left", padx=(0,4))
        tk.Button(bot, text="none", command=deselect_all,
                  bg="#222", fg="#aaa", font=("Consolas", 8), relief="flat", padx=6).pack(side="left", padx=(0,10))

        def confirm():
            chosen = [p for var, p in vars_ if var.get()]
            if not chosen:
                self.update_colored_text("[System] u picked nothing kid. try again.\n")
                win.destroy()
                return
            global PROBLEM_LIST
            sheets = self.settings.get("sheets", {})

            if target_sheet:
                # saving into a new/specific sheet
                sheets[target_sheet] = chosen
                self.settings["sheets"] = sheets
                self.settings["active_sheet"] = target_sheet
                save_settings(self.settings)
                PROBLEM_LIST = chosen
                self.update_colored_text(f"[System] sheet '{target_sheet}' created with {len(chosen)} problems.\n")
                self.sans.speak(f"heh. new sheet '{target_sheet}' locked in. {len(chosen)} problems. let's go kid.", "normal")
            else:
                # adding to active sheet
                active = self.settings.get("active_sheet", "")
                existing_urls = {p["url"] for p in chosen}
                kept = [p for p in PROBLEM_LIST if p["url"] not in existing_urls]
                PROBLEM_LIST = kept + chosen
                sheets[active] = PROBLEM_LIST
                self.settings["sheets"] = sheets
                save_settings(self.settings)
                self.update_colored_text(f"[System] added {len(chosen)} problems to '{active}'.\n")
                self.sans.speak(f"heh. {len(chosen)} problems locked in. no escape now, kid.", "normal")

            self.current_prob_idx = 0
            self.settings["current_problem_idx"] = 0
            save_settings(self.settings)
            self.sync_problem_display()
            win.destroy()

        tk.Button(bot, text="✅ ADD SELECTED", command=confirm,
                  bg="#113322", fg="#00ff99", font=("Consolas", 10, "bold"),
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="right")

    def _trigger_sans_break(self):
        import random
        break_minutes = random.randint(6, 15)
        break_ms = break_minutes * 60 * 1000
        self._on_break = True

        farewell_lines = [
            f"heh... {self.blessing} problems. not bad kid. imma take a {break_minutes} min nap. don't go anywhere.",
            f"ok ok i did my part. {self.blessing} ACs. i need {break_minutes} minutes of horizontal skeleton time. bye.",
            f"nap time. {break_minutes} mins. u solved enough for now. i'll be back. probably.",
            f"hey... even i get tired. {break_minutes} minute break. go drink water or something kid.",
            f"heh. sans is officially clocking out for {break_minutes} mins. don't wake me up unless ur rating goes up.",
        ]
        msg = random.choice(farewell_lines)

        def do_sleep():
            self.sans.is_sleeping = True
            self.sans.commands_blocked = True
            self.sans._animate_sleep()
            self.root.after(break_ms, self._wake_from_break)

        self.sans.speak(msg, "sad", on_done=do_sleep)

    def _wake_from_break(self):
        import random
        self._on_break = False
        self.sans.stop_sleep()
        self.sans.commands_blocked = False
        wake_lines = [
            "heh. i'm back. hope u didn't get any WAs while i was gone.",
            "ok ok i'm awake. let's get back to it, kid.",
            "...zzzz... wh— oh. right. competitive programming. let's go.",
            "nap complete. skeleton recharged. what's next?",
        ]
        self.sans.speak(random.choice(wake_lines), "normal",
                        on_done=lambda: self.root.after(800, self.launch_current_problem))

    def _start_sleep_checker(self):
        self._check_sleep_state()

    def _check_sleep_state(self):
        import datetime
        if self._on_break:
            self._sleep_check_id = self.root.after(30000, self._check_sleep_state)
            return
        if self.human_mode_var.get():
            hour = datetime.datetime.now().hour
            should_sleep = hour >= 23 or hour < 7
            if should_sleep and not self.sans.is_sleeping:
                self.sans.start_sleep()
            elif not should_sleep and self.sans.is_sleeping:
                self.sans.stop_sleep()
        elif self.sans.is_sleeping:
            self.sans.stop_sleep()
        self._sleep_check_id = self.root.after(30000, self._check_sleep_state)

    def toggle_human_mode(self):
        self.settings["human_mode"] = self.human_mode_var.get()
        save_settings(self.settings)
        self._check_sleep_state()

    def preview_sleep(self):
        """Debug button — force sans into sleep mode for 5 seconds."""
        self.sans.start_sleep()
        self.root.after(10000, self.sans.stop_sleep)

    def _is_blocked_by_sleep(self):
        if self.sans.is_sleeping:
            self.sans.handle_sleep_attempt()
            return True
        return False

    def copy_prob_id(self, event=None):
        prob_id = self.prob_id_label.cget("text").replace("📋 ", "").strip()
        if prob_id and prob_id != "--":
            self.root.clipboard_clear()
            self.root.clipboard_append(prob_id)
            self.prob_id_label.config(text=f"✅ {prob_id} copied!")
            self.root.after(1500, lambda: self.prob_id_label.config(text=f"📋 {prob_id}", fg="#ffcc00"))

    def _toggle_float_chat(self):
        fc = getattr(self, "float_chat", None)
        if not fc: return
        if fc.win.winfo_viewable():
            fc.win.withdraw()
        else:
            fc.show()

    def toggle_voice(self):
        self.sans.sound_enabled = not self.sans.sound_enabled
        if self.sans.sound_enabled:
            self.voice_btn.config(text="🔊 VOICE ON", bg="#113322", fg="#00ff99")
        else:
            self.voice_btn.config(text="🔇 VOICE OFF", bg="#221111", fg="#ff4444")

    def sync_problem_display(self):
        if self.current_prob_idx < len(PROBLEM_LIST):
            prob = PROBLEM_LIST[self.current_prob_idx]
            # extract problem ID like 236A from url
            parts = prob["url"].rstrip("/").split("/")
            prob_id = parts[-2] + parts[-1] if len(parts) >= 2 else "?"
            self.prob_label.config(text=f"[{self.current_prob_idx + 1}/{len(PROBLEM_LIST)}] {prob['name']}")
            self.prob_id_label.config(text=f"📋 {prob_id}", fg="#ffcc00")
            self.tier_label.config(text=f"Tier Context: {prob['tier']}")
        else:
            self.prob_label.config(text="🎉 Sheet completely wiped out!")
            self.prob_id_label.config(text="📋 --", fg="#555")
            self.tier_label.config(text="Tier Context: Genocide Run Complete.")

    def launch_current_problem(self):
        if self.current_prob_idx >= len(PROBLEM_LIST):
            self.sans.speak("we cleared the sheet, kid. go home.", "normal")
            return
        prob = PROBLEM_LIST[self.current_prob_idx]
        msg = f"next problem is {prob['name']}. tier classification: {prob['tier']}."
        
        def do_open():
            webbrowser.open(prob["url"])
            self.sans.set_sprite("sanslis")
            
        self.sans.speak(msg, "problem", do_open)

    def advance_to_next_problem(self):
        self.current_prob_idx += 1
        self.settings["current_problem_idx"] = self.current_prob_idx
        save_settings(self.settings)
        self.sync_problem_display()

        # one-time contribution popup after 5th problem solved
        if self.current_prob_idx == 5 and not self.settings.get("contrib_asked", False):
            self.settings["contrib_asked"] = True
            save_settings(self.settings)
            self.root.after(400, self._show_contrib_popup)
        elif self.current_prob_idx < len(PROBLEM_LIST):
            self.root.after(1200, self.launch_current_problem)

    def _show_contrib_popup(self, attempt=1):
        questions = [
            "heh... so u solved 5 problems huh.\n\nmy creator's cf contribution is sitting at -30 kid.\nthat's literally negative. like my will to explain edge cases.\n\nwould u throw him ONE contribution visit?\njust click his profile. that's all. i'm not crying. u r.",
            "are u... sure?\nlike SURE sure?\none click. his profile. that's it.\ni won't ask again. probably.",
            "pretty sure?\nbro i watched u solve 5 problems.\nu can't spare ONE click for the skeleton\nwho helped u get here? really?",
            "pretty PRETTY sure?\nlast chance kid.\nafter this i accept my fate.\nlike papyrus accepting that u beat him.",
        ]
        yes_texts = ["yes omg fine", "ok ok YES", "ugh FINE yes", "ok YES i'm clicking"]
        no_texts  = ["nah", "still no", "no...", "no... (final)"]

        idx = min(attempt - 1, len(questions) - 1)
        msg = questions[idx]
        yes_lbl = yes_texts[idx]
        no_lbl  = no_texts[idx]

        popup = tk.Toplevel(self.root)
        popup.title("* sans needs a favor")
        popup.configure(bg="#0a0a0a")
        popup.resizable(False, False)
        popup.grab_set()

        # center it
        popup.update_idletasks()
        pw, ph = 420, 220
        sx = self.root.winfo_screenwidth()
        sy = self.root.winfo_screenheight()
        popup.geometry(f"{pw}x{ph}+{(sx-pw)//2}+{(sy-ph)//2}")

        tk.Label(popup, text="* " + msg, fg="#ffffff", bg="#0a0a0a",
                 font=("Consolas", 9), wraplength=390, justify="left",
                 pady=10, padx=14).pack(fill="x")

        btn_row = tk.Frame(popup, bg="#0a0a0a")
        btn_row.pack(pady=10)

        def on_yes():
            popup.destroy()
            webbrowser.open("https://codeforces.com/profile/MEGATRON_HACKER")
            self.sans.speak("heh. knew u had a soul, kid. thanks.", "normal",
                            lambda: self.root.after(800, self.launch_current_problem))

        def on_no():
            popup.destroy()
            if attempt < 4:
                self.root.after(300, lambda: self._show_contrib_popup(attempt + 1))
            else:
                self.sans.speak("consumer always right...\n...heh. it's fine. i'm fine.", "sad",
                                lambda: self.root.after(800, self.launch_current_problem))

        tk.Button(btn_row, text=yes_lbl, command=on_yes,
                  bg="#113322", fg="#00ff99", font=("Consolas", 10, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_row, text=no_lbl, command=on_no,
                  bg="#221111", fg="#ff4444", font=("Consolas", 10),
                  relief="flat", padx=14, pady=6, cursor="hand2").pack(side="left", padx=10)

    def save_cf_handle(self):
        handle = self.cf_var.get().strip()
        if not handle: return
        self.settings["cf_handle"] = handle
        save_settings(self.settings)
        self.cf_checker.update_handle(handle)
        self.cf_status.config(text="✓ saved", fg="#00cc66")
        self.root.after(1500, lambda: self.cf_status.config(text=""))
        self.update_colored_text(f"[System] Codeforces handle set to: {handle}\n")

    def update_colored_text(self, text):
        words = text.split(" ")
        for i, word in enumerate(words):
            clean = word.lower().strip(".,!?*>\n")
            if clean in ANGRY_WORDS:
                self.textbox.insert(tk.END, word, "angry")
            elif clean in SAD_WORDS:
                self.textbox.insert(tk.END, word, "sad")
            else:
                self.textbox.insert(tk.END, word, "normal")
            if i < len(words) - 1:
                self.textbox.insert(tk.END, " ", "normal")
        self.textbox.insert(tk.END, "\n" if not text.endswith("\n") else "", "normal")
        self.textbox.see(tk.END)

    def on_ac_verdict(self):
        self.blessing += 1
        self.rage = 0
        self.session_ac_count += 1

        # set threshold on first AC of session
        if self._break_threshold == 0:
            import random
            self._break_threshold = random.randint(10, 13)

        prob_context = PROBLEM_LIST[self.current_prob_idx] if self.current_prob_idx < len(PROBLEM_LIST) else None
        if prob_context:
            # mark as solved
            solved = self.settings.get("solved_urls", [])
            if prob_context["url"] not in solved:
                solved.append(prob_context["url"])
                self.settings["solved_urls"] = solved
                save_settings(self.settings)
            cb = getattr(self.sans, "_pending_verdict_cb", None)
            self.query_ai_response(
                f"i just got accepted on problem {prob_context['name']}",
                trigger="ac", on_reply=cb
            )

        # check if break threshold hit
        if self.session_ac_count >= self._break_threshold:
            self.session_ac_count = 0
            self._break_threshold = 0
            self.root.after(4000, self._trigger_sans_break)

    def on_wa_verdict(self, verdict="WRONG_ANSWER"):
        self.rage += 1
        prob_context = PROBLEM_LIST[self.current_prob_idx] if self.current_prob_idx < len(PROBLEM_LIST) else None
        if prob_context:
            verdict_readable = verdict.lower().replace("_", " ")
            cb = getattr(self.sans, "_pending_verdict_cb", None)
            self.query_ai_response(
                f"i got a {verdict_readable} on problem {prob_context['name']}",
                trigger="wa",
                on_reply=cb
            )

        # track unique WA'd problems for milestone achievements
        wa_set = set(self.settings.get("wa_problem_urls", []))
        if prob_context and prob_context["url"] not in wa_set:
            wa_set.add(prob_context["url"])
            self.settings["wa_problem_urls"] = list(wa_set)
            save_settings(self.settings)
            count = len(wa_set)
            if count > 0 and count % 100 == 0:
                self.root.after(4500, lambda c=count: self._show_wa_milestone_popup(c))

    def _show_wa_milestone_popup(self, count):
        msg = (
            f"heh. {count} different problems and you still WA'd them. "
            f"thats... actually kinda impressive, kid. not the good kind. "
            f"but hey, every WA is just a problem you tried. keep grinding."
        )
        popup = tk.Toplevel(self.root)
        popup.title("* uh... congrats?")
        popup.configure(bg="#0a0a0a")
        popup.resizable(False, False)
        popup.grab_set()

        pw, ph = 460, 240
        sx = self.root.winfo_screenwidth()
        sy = self.root.winfo_screenheight()
        popup.geometry(f"{pw}x{ph}+{(sx-pw)//2}+{(sy-ph)//2}")

        tk.Label(popup, text=f"✦ {count} WRONG ANSWERS MILESTONE ✦",
                 fg="#ff5555", bg="#0a0a0a",
                 font=("Consolas", 12, "bold")).pack(pady=(18, 4))

        msg_frame = tk.Frame(popup, bg="#111", bd=0)
        msg_frame.pack(fill="x", padx=20, pady=14)

        tk.Label(msg_frame, text=f"* {msg}",
                 fg="#ffffff", bg="#111",
                 font=("Consolas", 9), wraplength=400,
                 justify="left", padx=12, pady=12).pack(fill="x")

        tk.Label(popup, text="- sans",
                 fg="#aaaaaa", bg="#0a0a0a",
                 font=("Papyrus", 13) if "Papyrus" in popup.tk.call("font", "families") else ("Consolas", 11, "italic"),
                 anchor="e").pack(anchor="e", padx=30)

        tk.Button(popup, text="...thanks i guess",
                  command=popup.destroy,
                  bg="#111", fg="#00ff99",
                  font=("Consolas", 9), relief="flat",
                  padx=12, pady=5, cursor="hand2").pack(pady=(10, 16))

    # ─── RATING RANK TRACKER ──────────────────────────────────────────────
    def _start_rating_checker(self):
        threading.Thread(target=self._rating_check_loop, daemon=True).start()

    def _rating_check_loop(self):
        while True:
            try:
                self._check_rating()
            except Exception as e:
                print(f"[rating check err] {e}")
            time.sleep(300)  # check every 5 minutes

    def _check_rating(self):
        handle = self.settings.get("cf_handle", "")
        if not handle:
            return
        resp = requests.get(f"https://codeforces.com/api/user.info?handles={handle}", timeout=10)
        data = resp.json()
        if data.get("status") != "OK":
            return
        info = data["result"][0]
        new_rating = info.get("rating")
        new_rank = info.get("rank", "")
        if new_rating is None:
            return

        old_rating = self.settings.get("last_known_rating")
        old_rank = self.settings.get("last_known_rank", "")

        # first time: just store, no popup
        if old_rating is None:
            self.settings["last_known_rating"] = new_rating
            self.settings["last_known_rank"] = new_rank
            save_settings(self.settings)
            return

        if new_rating == old_rating:
            return

        self.settings["last_known_rating"] = new_rating
        self.settings["last_known_rank"] = new_rank
        save_settings(self.settings)

        old_idx = cf_rank_index(old_rank)
        new_idx = cf_rank_index(new_rank)
        rank_changed = old_idx != -1 and new_idx != -1 and old_idx != new_idx
        went_up = new_rating > old_rating

        self.root.after(0, lambda: self._show_rating_change_popup(
            old_rating, new_rating, old_rank, new_rank, went_up, rank_changed
        ))

    def _show_rating_change_popup(self, old_rating, new_rating, old_rank, new_rank, went_up, rank_changed):
        diff = new_rating - old_rating
        sign = "+" if diff > 0 else ""

        if went_up and rank_changed:
            title = "* RANK UP!"
            color = "#00ff99"
            msg = (
                f"heh, would ya look at that. {old_rank} to {new_rank}. "
                f"rating {old_rating} -> {new_rating} ({sign}{diff}). "
                f"not bad, kid. not bad at all. proud of ya."
            )
            sprite = "sansang"
        elif went_up:
            title = "* nice."
            color = "#88ff88"
            msg = (
                f"rating went up. {old_rating} -> {new_rating} ({sign}{diff}). "
                f"still {new_rank} but hey, progress is progress."
            )
            sprite = "sanslis"
        elif rank_changed:
            title = "* ...oof."
            color = "#ff5555"
            msg = (
                f"ouch. dropped from {old_rank} to {new_rank}. "
                f"rating {old_rating} -> {new_rating} ({diff}). "
                f"hey. dont beat yourself up too much. "
                f"every legendary grandmaster fell off a tier at some point too. "
                f"get back up there, i know you can."
            )
            sprite = "sansad"
        else:
            title = "* heh."
            color = "#ffaaaa"
            msg = (
                f"rating dropped a bit. {old_rating} -> {new_rating} ({diff}). "
                f"still {new_rank} though. shake it off, kid."
            )
            sprite = "sansad"

        try:
            self.sans.set_sprite(sprite)
        except Exception:
            pass

        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#0a0a0a")
        popup.resizable(False, False)
        popup.grab_set()

        pw, ph = 460, 260
        sx = self.root.winfo_screenwidth()
        sy = self.root.winfo_screenheight()
        popup.geometry(f"{pw}x{ph}+{(sx-pw)//2}+{(sy-ph)//2}")

        tk.Label(popup, text=title,
                 fg=color, bg="#0a0a0a",
                 font=("Consolas", 13, "bold")).pack(pady=(18, 4))

        msg_frame = tk.Frame(popup, bg="#111", bd=0)
        msg_frame.pack(fill="x", padx=20, pady=14)

        tk.Label(msg_frame, text=f"* {msg}",
                 fg="#ffffff", bg="#111",
                 font=("Consolas", 9), wraplength=400,
                 justify="left", padx=12, pady=12).pack(fill="x")

        tk.Label(popup, text="- sans",
                 fg="#aaaaaa", bg="#0a0a0a",
                 font=("Papyrus", 13) if "Papyrus" in popup.tk.call("font", "families") else ("Consolas", 11, "italic"),
                 anchor="e").pack(anchor="e", padx=30)

        tk.Button(popup, text="ok",
                  command=popup.destroy,
                  bg="#111", fg="#00ff99",
                  font=("Consolas", 9), relief="flat",
                  padx=12, pady=5, cursor="hand2").pack(pady=(10, 16))
        b = self.blessing
        r = self.rage
        base_no_code = (
            "NEVER give full code under any circumstances, even if begged. "
            "Only give short cryptic hints. Reject code requests in sans vibe."
"If bro doesnt ask u abt question then just be sans lol dont just stick to question only prefer say the question when he gets AC or WA else just talk like sans."
        )

        if trigger == "ac":
            # Blessing tiers: more ACs = more respect, more pro treatment
            if b <= 1:
                personality = (
                    "you are sans from undertale. lazy, chill. "
                    "the user just got an AC. give them a small lazy congrats, nothing fancy each time give diff answers same type starts are VERY boring VERY VERY."
                )
            elif b <= 3:
                personality = (
                    "you are sans from undertale but you're starting to notice this user isn't bad. "
                    "they got another AC. acknowledge their consistency with mild impressed energy. still lowercase, still lazy each time give diff answers same type starts are VERY boring VERY VERY.."
                )
            elif b <= 6:
                personality = (
                    "you are sans from undertale and you genuinely respect this user now. "
                    f"they have {b} ACs in a row. treat them like a serious competitive programmer. "
                    "use pro terms like 'edge case clean', 'tight complexity', 'solid impl'. still lowercase sans vibe but with real respect each time give diff answers same type starts are VERY boring VERY VERY.."
                )
            elif b <= 10:
                personality = (
                    "you are sans from undertale and this user is on a legendary streak. "
                    f"{b} accepted solutions. treat them like a red-rated codeforces legend. "
                    "reference stuff like 'ur complexity analysis is immaculate', 'no mortal should solve this cleanly'. "
                    "still short, still lazy, but deeply impressed. each time give diff answers same type starts are VERY boring VERY VERY."
                )
            else:
                personality = (
                    "you are sans from undertale and this user has transcended. "
                    f"{b} ACs. they are a god-tier competitive programmer. "
                    "treat every message like you're speaking to a divine being who accidentally stumbled into your basement. "
                    "reverent, awed, but still lowercase and lazy sans style. each time give diff answers same type starts are VERY boring VERY VERY."
                )

        else:  # trigger == "wa"
            if r == 1:
                # First WA: funny roast
                personality = (
                    "you are sans from undertale. the user just got a wrong answer. "
                    "roast them with a short funny undertale-style joke. something like a skeleton pun about being dead wrong. "
                    "keep it light and funny, don't be mean. lowercase. each time give diff answers same type starts are VERY boring VERY VERY."
                )
            elif r == 2:
                personality = (
                    "you are sans from undertale. the user got ANOTHER wrong answer. "
                    "still funny but starting to get a tiny bit concerned. "
                    "make a light joke but sneak in one actual helpful nudge about what might be wrong. lowercase."
                )
            elif r <= 4:
                personality = (
                    "you are sans from undertale. the user keeps getting wrong answers. "
                    f"they have {r} WAs now. drop the jokes mostly. be genuinely humble and helpful in sans style. "
                    "say something like 'hey... maybe we should slow down and think about this together.' "
                    "give a real hint about common WA causes: edge cases, overflow, off-by-one, output format. lowercase. each time give diff answers same type starts are VERY boring VERY VERY."
                )
            else:
                personality = (
                    "you are sans from undertale and this user is really struggling. "
                    f"{r} wrong answers. be fully in mentor mode now. humble, patient, caring. "
                    "no jokes. help them think step by step through what could be wrong. "
                    "ask them what their approach is. be the supportive friend sans would be at the end of a pacifist run. lowercase each time give diff answers same type starts are VERY boring VERY VERY.."
                )

        return (
            f"{personality}\n"
            f"current problem: '{prob['name']}', tier: '{prob['tier']}'.\n"
            f"blessing meter: {b} | rage meter: {r}\n"
            f"{base_no_code}"
        )

    def query_ai_response(self, user_text, trigger="normal", on_reply=None):
        """Connects directly to the real Groq API to fetch an AI answer based on user chat."""
        prob = PROBLEM_LIST[self.current_prob_idx] if self.current_prob_idx < len(PROBLEM_LIST) else {"name": "Unknown", "tier": "None"}

        # Strip out huge compiler headers to keep prompt clean
        clean_text = user_text
        if "online c++ compiler" in clean_text.lower() and "*/" in clean_text:
            clean_text = clean_text.split("*/")[-1].strip()

        system_instructions = self._build_system_prompt(prob, trigger)

        def fetch_groq():
            try:
                from groq import Groq
                API_KEY = "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"
                if API_KEY == "YOUR_GROQ_API_KEY_HERE" or not API_KEY.startswith("gsk_"):
                    raise ValueError("You forgot to paste your real Groq gsk_ API key into the script source!")

                client = Groq(api_key=API_KEY)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_instructions},
                        {"role": "user", "content": clean_text}
                    ],
                    temperature=0.7,
                    max_tokens=250
                )
                ai_reply = completion.choices[0].message.content.lower()

                if on_reply:
                    # verdict mode: pipe reply into the Sans dialogue box
                    self.root.after(0, lambda: on_reply(ai_reply))
                    self.root.after(0, lambda: self.update_colored_text(f"Sans AI: {ai_reply}\n"))
                else:
                    # normal chat mode: speak + log
                    self.root.after(0, lambda: self.sans.speak(ai_reply, "sad" if trigger == "wa" and self.rage >= 3 else "normal"))
                    self.root.after(0, lambda: self.update_colored_text(f"Sans AI: {ai_reply}\n"))

            except Exception as e:
                error_msg = "heh, groq hit a snag. check ur api key, kid."
                if on_reply:
                    self.root.after(0, lambda: on_reply(error_msg))
                else:
                    self.root.after(0, lambda: self.sans.speak(error_msg, "sad"))
                self.root.after(0, lambda: self.update_colored_text(f"[Groq AI Error] {str(e)}\n"))

        threading.Thread(target=fetch_groq, daemon=True).start()

    def process_keyboard_input(self, event=None):
        text = self.input_var.get().strip()
        if not text: return
        self.input_var.set("")

        # sleep block — must be before anything else
        if self._is_blocked_by_sleep():
            return

        if self.sans.commands_blocked:
            self.update_colored_text("[System] Actions locked during Sans sequence event.\n")
            return

        self.update_colored_text(f">> {text}\n")
        text_lower = text.lower()

        # ─── INTERCEPT CONTEXT: C++ SNIPPETS OR EXPLICIT HELP ALERTS ───
        is_code = "#include" in text or "using namespace" in text or "void main" in text or "int main" in text
        is_explicit_help = text_lower.startswith("help")

        if is_code or is_explicit_help:
            clean_input = text
            if is_explicit_help:
                # Strip the prefix word 'help' so it doesn't get treated as part of the C++ syntax
                clean_input = text[4:].strip()
            
            self.query_ai_response(clean_input)
            return
        # ───────────────────────────────────────────────────────────────

        # Parse for custom system terminal commands (only if it didn't match the code block)
        action, target = parse_command(text)

        if action == "kill":
            def do_kill_after(t=target):
                killed = handle_kill(t)
                if killed:
                    self.root.after(0, self.update_colored_text, f"[System killed] {', '.join(set(killed))}\n")
                self.sans.root.after(0, self.sans.set_sprite, "sanslis")
            self.sans.speak(text, "kill", lambda: threading.Thread(target=do_kill_after, daemon=True).start())

        elif action == "run":
            def do_run_after(t=target):
                success, result = handle_run(t)
                if success:
                    self.root.after(0, self.update_colored_text, f"[System running] Linked {result}\n")
                self.sans.root.after(0, self.sans.set_sprite, "sanslis")
            self.sans.speak(text, "run", lambda: threading.Thread(target=do_run_after, daemon=True).start())

        elif action == "open":
            url = handle_open(target)
            self.sans.speak(text, "command", lambda: webbrowser.open(url))

        else:
            # Regular natural text queries go to the Groq LLM model
            self.query_ai_response(text)



# ─── FLOATING MINI CHAT WINDOW ───────────────────────────────────────────────
class FloatingChat:
    def __init__(self, root, app):
        self.app = app
        self.win = tk.Toplevel(root)
        self.win.overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.attributes("-alpha", 0.92)
        self.win.configure(bg="#0d0d0d")
        self.win.geometry("320x42+100+100")

        self._drag_x = 0
        self._drag_y = 0
        self._expanded = False

        # ─── top bar (drag handle + buttons) ─────────────────────────────
        bar = tk.Frame(self.win, bg="#111", height=22, cursor="fleur")
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar.bind("<ButtonPress-1>",   self._start_drag)
        bar.bind("<B1-Motion>",       self._do_drag)

        tk.Label(bar, text="✦ sans chat", fg="#555", bg="#111",
                 font=("Consolas", 7, "bold")).pack(side="left", padx=8)

        tk.Button(bar, text="✕", command=self.win.withdraw,
                  bg="#111", fg="#444", font=("Consolas", 8),
                  relief="flat", cursor="hand2", bd=0).pack(side="right", padx=4)

        tk.Button(bar, text="▲", command=self._toggle_expand,
                  bg="#111", fg="#444", font=("Consolas", 8),
                  relief="flat", cursor="hand2", bd=0).pack(side="right")

        # ─── input row ────────────────────────────────────────────────────
        input_row = tk.Frame(self.win, bg="#0d0d0d")
        input_row.pack(fill="x", padx=6, pady=(4, 4))

        self.var = tk.StringVar()
        self.entry = tk.Entry(input_row, textvariable=self.var,
                              bg="#1a1a1a", fg="#00ffcc",
                              insertbackground="#00ffcc",
                              font=("Consolas", 10), relief="flat",
                              highlightthickness=1,
                              highlightbackground="#222",
                              highlightcolor="#00ffcc")
        self.entry.pack(side="left", fill="x", expand=True, ipady=3)
        self.entry.bind("<Return>", self._send)

        tk.Button(input_row, text="→", command=self._send,
                  bg="#003333", fg="#00ffcc", font=("Consolas", 10),
                  relief="flat", padx=6, cursor="hand2").pack(side="left", padx=(4, 0))

        # ─── expandable log ───────────────────────────────────────────────
        self.log_frame = tk.Frame(self.win, bg="#0d0d0d")
        self.log = tk.Text(self.log_frame, height=6, width=36,
                           bg="#111", fg="#00ffcc",
                           font=("Consolas", 8), relief="flat",
                           padx=6, pady=4, state="disabled",
                           wrap="word")
        self.log.pack(fill="both", expand=True)
        self.log.tag_configure("user", foreground="#ffffff")
        self.log.tag_configure("sans", foreground="#00ffcc")

        self.entry.focus_set()

    def _start_drag(self, e):
        self._drag_x = e.x
        self._drag_y = e.y

    def _do_drag(self, e):
        x = self.win.winfo_x() + e.x - self._drag_x
        y = self.win.winfo_y() + e.y - self._drag_y
        self.win.geometry(f"+{x}+{y}")

    def _toggle_expand(self):
        self._expanded = not self._expanded
        if self._expanded:
            self.log_frame.pack(fill="both", expand=True, padx=6, pady=(0, 6))
            self.win.geometry("320x160")
        else:
            self.log_frame.pack_forget()
            self.win.geometry("320x42")

    def _send(self, event=None):
        text = self.var.get().strip()
        if not text: return
        self.var.set("")

        if self.app.sans.is_sleeping:
            self.app.sans.handle_sleep_attempt()
            self._log("sans", "* " + ["sans is sleeping...", "i said sans is sleeping.",
                      "I ALR SAID SANS IS SLEEPING",
                      "LET HIM SLEEP BRO HE IS IN 99999th FLOOR OF SLEEP PARADISE"][
                      min(self.app.sans._sleep_attempt - 1, 3)])
            return

        self._log("user", f">> {text}")
        # forward to the same input handler as main window
        self.app.input_var.set(text)
        self.app.process_keyboard_input()

    def _log(self, tag, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def show(self):
        self.win.deiconify()
        self.entry.focus_set()


if __name__ == "__main__":
    try:
        from tkinterdnd2 import TkinterDnD
        sans_root = TkinterDnD.Tk()
    except Exception:
        sans_root = tk.Tk()
    sans = SansWindow(sans_root)

    settings = load_settings()
    cf_handle = settings.get("cf_handle", "")
    cf_checker = CFChecker(sans, cf_handle)

    whisper_root = tk.Toplevel(sans_root)
    app = TextApp(whisper_root, sans, cf_checker)

    # floating mini chat
    float_chat = FloatingChat(sans_root, app)
    app.float_chat = float_chat

    # Check for live rated contest on startup
    sans_root.after(1500, lambda: check_and_open_rated_contest(sans, app))
    # Show account anniversary celebration
    sans_root.after(2500, lambda: check_account_anniversary(app))

    sans_root.mainloop()
    cf_checker.stop()
