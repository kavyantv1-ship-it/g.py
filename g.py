#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                    @@GRW_XD UNLIMITED LUA TOOL                              │
# │                         COMPLETE VERSION                                   │
# │                    DEVELOPER : @GRW_XD                                      │
# │                    OWNER   : SAMEER                                         │
# └─────────────────────────────────────────────────────────────────────────────┘

import os
import sys
import struct
import glob
import shutil
import subprocess
import time
import re
import tempfile
import colorsys
import math
import zlib
import socket
import base64
import itertools as it
import traceback
import random
import hashlib
import platform
import json
import uuid
import threading
from typing import Tuple, List, Optional, Dict, Any
from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePath, Path
from datetime import datetime
from collections import Counter

# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 LICENSE VERIFICATION SYSTEM - ONLINE ONLY
# ═══════════════════════════════════════════════════════════════════════════════

try:
    import requests
except ImportError:
    print("⚠️ requests module not found! Installing...")
    os.system("pip install requests")
    import requests

# ── CONFIGURATION ──
PANEL_URL = "https://enginehost.org/connect"
GAME_NAME = "PUBG"

# Key storage folder - changed to "User"
CONFIG_DIR = Path("/storage/emulated/0/Documents/GRW_LUA_TOOL")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
AUTH_CONFIG_FILE = CONFIG_DIR / ".shadow_auth.json"

# ── Rich UI imports (EARLY) ──────────────────────────────────────────────────

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.markup import escape
    from rich.text import Text
    from rich.box import ROUNDED, HEAVY, DOUBLE
    from rich import box
    from rich.align import Align
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.live import Live
    from rich.console import Group
    RICH_AVAILABLE = True
except ImportError:
    print("⚠️ rich module not found! Installing...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.markup import escape
    from rich.text import Text
    from rich.box import ROUNDED, HEAVY, DOUBLE
    from rich import box
    from rich.align import Align
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.live import Live
    from rich.console import Group
    RICH_AVAILABLE = True

console = Console()

# ── Themes ──────────────────────────────────────────────────────────────────

NEON = "bright_white"
NEON_DIM = "white"
ERR = "red"
WARN = "yellow"
ACCENT = "cyan"
MUTED = "dim white"
SUCCESS = "green"
GOLD = "gold1"
PURPLE = "magenta"
RED = "red"
GREEN = "green"
BLUE = "blue"

# ── ANIMATED BORDER ENGINE (EARLY) ──────────────────────────────────────────

class AnimatedBorder:
    _instance = None
    
    def __init__(self):
        self._start_time = time.time()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_rainbow_color(self, offset=0, speed=1.0):
        hue = (time.time() * speed + offset) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def get_moving_border_style(self, position=0, speed=0.8):
        offset = (position / 8.0) + (time.time() * speed * 0.1)
        return self.get_rainbow_color(offset % 1.0, speed)

def safe_input(prompt: str='') -> str:
    try:
        return input(prompt)
    except (EOFError, RuntimeError):
        try:
            if sys.platform != 'win32':
                with open('/dev/tty', 'r') as tty:
                    sys.stderr.write(prompt); sys.stderr.flush()
                    return tty.readline().rstrip('\n')
            else:
                with open('CON', 'r') as con:
                    sys.stderr.write(prompt); sys.stderr.flush()
                    return con.readline().rstrip('\r\n')
        except Exception:
            return ''
    except Exception:
        return ''

def check_internet() -> bool:
    try:
        requests.head("https://www.google.com", timeout=5)
        return True
    except Exception:
        return False

def get_hwid() -> str:
    try:
        mac = uuid.getnode()
        if mac != 0xffffffffffff:
            return f"MAC_{mac:012x}"
    except:
        pass
    return f"RAND_{uuid.uuid4().hex[:16]}"

def verify_key_with_panel(user_key: str, serial: str = None) -> dict:
    if serial is None:
        serial = get_hwid()
    payload = {
        'game': GAME_NAME,
        'user_key': user_key,
        'serial': serial
    }
    try:
        response = requests.post(PANEL_URL, data=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': False, 'reason': f'HTTP {response.status_code}'}
    except requests.exceptions.Timeout:
        return {'status': False, 'reason': 'Connection timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'reason': 'Check your internet'}
    except Exception as e:
        return {'status': False, 'reason': str(e)}

def save_license(key: str, expiry: str):
    """Save license details to local storage."""
    try:
        data = {
            'key': key,
            'expiry': expiry,
            'hwid': get_hwid(),
            'saved_at': datetime.now().isoformat()
        }
        with open(AUTH_CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def check_license():
    """
    Perform online license verification only.
    Returns (success, license_key, info_dict)
    """
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Check internet
    if not check_internet():
        console.print("[red]No internet connection. Please check your network and try again.[/red]")
        sys.exit(1)

    # Show verification panel
    W = 52
    console.print(Align.center(f"[bold yellow]╔{'═'*W}╗[/]"))
    console.print(Align.center(f"[bold yellow]╠{'═'*W}╣[/]"))
    title_pad = (W - len("[ LICENSE KEY REQUIRED ]")) // 2
    console.print(Align.center(
        f"[bold yellow]║[/]"
        f"{' ' * title_pad}[bold red][ LICENSE KEY REQUIRED ][/bold red]"
        f"{' ' * (W - title_pad - len('[ LICENSE KEY REQUIRED ]'))}"
        f"[bold yellow]║[/]"
    ))
    console.print(Align.center(f"[bold yellow]╠{'═'*W}╣[/]"))
    instr = "Enter your license key below to continue"
    ip = (W - len(instr)) // 2
    console.print(Align.center(
        f"[bold yellow]║[/]"
        f"{' ' * ip}[cyan]{instr}[/cyan]"
        f"{' ' * (W - ip - len(instr))}"
        f"[bold yellow]║[/]"
    ))
    contact_line = "WhatsApp 03704831068 · @GRW_XD"
    cp = (W - len(contact_line)) // 2
    console.print(Align.center(
        f"[bold yellow]║[/]"
        f"{' ' * cp}[dim]{contact_line}[/dim]"
        f"{' ' * (W - cp - len(contact_line))}"
        f"[bold yellow]║[/]"
    ))
    console.print(Align.center(f"[bold yellow]╚{'═'*W}╝[/]"))
    console.print()

    attempts = 0
    while attempts < 3:
        user_key = safe_input("Enter your license key: ").strip()
        if not user_key:
            console.print("[red]Key cannot be empty![/red]")
            attempts += 1
            continue

        with Progress(SpinnerColumn(), TextColumn("[cyan]Verifying license...[/cyan]"), transient=True) as prog:
            prog.add_task("", total=None)
            hwid = get_hwid()
            result = verify_key_with_panel(user_key, serial=hwid)

        if result.get('status') == True:
            data = result.get('data', {})
            mod_status = data.get('mod_status', 'on')
            if mod_status == 'off':
                console.print("[red]Tool disabled by admin![/red]")
                sys.exit(1)
            expiry_str = data.get('EXP', '')
            if expiry_str:
                try:
                    expiry_date = datetime.fromisoformat(expiry_str.replace(' ', 'T'))
                    if expiry_date < datetime.now():
                        console.print("[red]Key Expired! Contact owner to renew.[/red]")
                        attempts += 1
                        continue
                except:
                    pass

            # Save license details
            save_license(user_key, expiry_str)

            console.print(f"[bold green]  [OK]  License verification successful![/bold green]")
            time.sleep(0.5)

            # Build info dict
            info = {
                'key': user_key,
                'expiry': expiry_str,
                'max_devices': 1,
                'current_devices': 1,
                'remaining_seconds': -1
            }
            return True, user_key, info

        reason = result.get('reason', '')
        if any(keyword in reason.lower() for keyword in ["user or game not registered", "invalid", "wrong"]):
            console.print("[red]Invalid key. Contact owner to buy.[/red]")
        elif 'expired' in reason.lower():
            console.print("[red]Key Expired! Contact owner to renew.[/red]")
        elif 'device' in reason.lower() and 'limit' in reason.lower():
            console.print("[red]Your key maximum devices reached.[/red]")
        else:
            console.print(f"[red]{reason}[/red]")
        attempts += 1

    console.print("[red]Access denied (3/3 invalid keys). Contact owner to buy.[/red]")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# END OF LICENSE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

# ── Python version compatibility ──────────────────────────────────────────

if not hasattr(it, 'batched'):
    def batched(iterable, n):
        it_iter = iter(iterable)
        while True:
            chunk = list(it.islice(it_iter, n))
            if not chunk:
                break
            yield chunk
    it.batched = batched

# ── Optional PAK dependencies ─────────────────────────────────────────────

PAK_MODE_AVAILABLE = True
try:
    import gmalg
    try:
        from gmalg.base import BlockCipher
        from gmalg.errors import IncorrectLengthError
        from gmalg.utils import ROL32
    except ImportError:
        class BlockCipher: pass
        class IncorrectLengthError(Exception):
            def __init__(self, name, expected, actual):
                super().__init__(f"Incorrect length for {name}: expected {expected}, got {actual}")
        def ROL32(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))
except ImportError:
    PAK_MODE_AVAILABLE = False
    class BlockCipher: pass
    class IncorrectLengthError(Exception):
        def __init__(self, name, expected, actual):
            super().__init__(f"Incorrect length for {name}: expected {expected}, got {actual}")
    def ROL32(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    PAK_MODE_AVAILABLE = False

try:
    from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict, DICT_TYPE_AUTO
except ImportError:
    PAK_MODE_AVAILABLE = False

# ==============================================================================
# HEXA CORE UI - PROFESSIONAL
# ==============================================================================

def get_rainbow_color(offset=0, speed=1.0):
    return AnimatedBorder.get_instance().get_rainbow_color(offset, speed)

def get_border_style(position=0, speed=0.8):
    return AnimatedBorder.get_instance().get_moving_border_style(position, speed)

def hexa_alert(message: str, kind: str = "info") -> None:
    tags = {
        "success": ("✓", SUCCESS),
        "error": ("✗", ERR),
        "warning": ("⚠", WARN),
        "info": ("▶", ACCENT),
    }
    tag, color = tags.get(kind, tags["info"])
    console.print(f"  {tag}  {message}", style=color)

def hexa_section(title: str) -> None:
    console.print()
    console.print(f"  ═══ {title} ═══", style=f"bold {ACCENT}")
    console.print(f"  {'─' * (len(title) + 8)}", style=MUTED)

def hexa_prompt(label: str) -> str:
    console.print(f"  {label}", style=f"bold {NEON}")
    return safe_input("  └─> ").strip()

def format_time(seconds: int) -> str:
    """Convert seconds to human readable time format"""
    if seconds < 0:
        return "Unlimited"
    if seconds == 0:
        return "Expired"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    else:
        return f"{minutes}m {secs}s"

def print_main_banner(title="", key_info=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 80
    
    BOX_WIDTH = 60
    padding = max(0, (term_width - BOX_WIDTH) // 2)
    pad = " " * padding
    
    ab = AnimatedBorder.get_instance()
    
    top_line = "╔" + "═" * (BOX_WIDTH - 2) + "╗"
    sep_line = "╠" + "═" * (BOX_WIDTH - 2) + "╣"
    sep2_line = "╟" + "─" * (BOX_WIDTH - 2) + "╢"
    bot_line = "╚" + "═" * (BOX_WIDTH - 2) + "╝"
    
    c1 = ab.get_moving_border_style(0, 0.6)
    c2 = ab.get_moving_border_style(4, 0.6)
    c3 = ab.get_moving_border_style(8, 0.6)
    
    def make_center_line(text):
        content_len = len(text)
        total_pad = BOX_WIDTH - 2 - content_len
        left_pad = total_pad // 2
        right_pad = total_pad - left_pad
        return "║" + " " * left_pad + text + " " * right_pad + "║"
    
    title_text = "@GRW_XD UNLIMITED LUA TOOL"
    
    console.print(pad + f"[{c1}]{top_line}[/{c1}]")
    console.print(pad + make_center_line(title_text), style=f"bold {GREEN}")
    console.print(pad + f"[{c2}]{sep_line}[/{c2}]")
    console.print(pad + make_center_line("REAL DEVELOPER @GRW_XD"), style=f"bold {GREEN}")
    
    if key_info:
        console.print(pad + f"[{c3}]{sep2_line}[/{c3}]")
        console.print(pad + make_center_line(f"LICENSE KEY : {key_info.get('key', 'N/A')}"), style=f"bold {ACCENT}")
        
        expiry = key_info.get('expiry', 'N/A')
        if expiry == 'lifetime':
            console.print(pad + make_center_line("EXPIRY   : LIFETIME"), style=f"bold {GREEN}")
            console.print(pad + make_center_line("TIME    : UNLIMITED"), style=f"bold {GREEN}")
        else:
            console.print(pad + make_center_line(f"EXPIRY      : {expiry}"), style=NEON)
            
            rem = key_info.get('remaining_seconds', -1)
            if rem is not None and rem >= 0:
                time_str = format_time(rem)
                if rem < 3600:
                    color = RED
                elif rem < 86400:
                    color = WARN
                else:
                    color = SUCCESS
                console.print(pad + make_center_line(f"TIME LEFT   : {time_str}"), style=f"bold {color}")
            else:
                console.print(pad + make_center_line("TIME LEFT   : N/A"), style=MUTED)
        
        devices = key_info.get('current_devices', 0)
        max_dev = key_info.get('max_devices', 1)
        console.print(pad + make_center_line(f"DEVICES     : {devices} / {max_dev}"), style=NEON)
    
    console.print(pad + f"[{c3}]{bot_line}[/{c3}]")
    console.print()
    
    if title:
        console.print(f"  {title}", style=f"bold {ACCENT}")
        console.print(f"  {'─' * len(title)}", style=MUTED)

def human_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} PB'

# ==============================================================================
# SHARED DIRECTORY CONFIGURATION
# ==============================================================================

def get_lua_pak_root() -> Path:
    docs_path = Path("/storage/emulated/0/Documents/GRW_LUA_TOOL")
    if not docs_path.exists():
        docs_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[{SUCCESS}]✓ Created GRW_LUA_TOOL folder at {docs_path}[/{SUCCESS}]")
    return docs_path

LUA_PAK_ROOT = get_lua_pak_root()
SOURCE_DIR = LUA_PAK_ROOT / "SOURCE"
REAL_DIR   = LUA_PAK_ROOT / "LUA_ORIGINAL"
UNPACK_DIR = LUA_PAK_ROOT / "LUA_EDIT"
EDIT_DIR   = LUA_PAK_ROOT / "COMPILED"
PAK_DIR    = LUA_PAK_ROOT / "PAK_ORIGINAL"
PAK_UNPACK_DIR = LUA_PAK_ROOT / "PAK_UNPACK"
RESULT_DIR = LUA_PAK_ROOT / "PAK_RESULT"
CONFIG_FILE_PATH = LUA_PAK_ROOT / "config.json"

FORCE_COMPILE = True
SKIP_ALL_FIXES = True
SKIP_AUTO_FIX = True

def load_config():
    config = {}
    if CONFIG_FILE_PATH.exists():
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                config = json.load(f)
        except Exception:
            pass
    return config

def save_config(config):
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass

def hexa_prompt_with_default(label: str, default: str = "") -> str:
    console.print(f"  {label}", style=f"bold {NEON}")
    if default:
        console.print(f"  └─> [bold green]{default}[/bold green]", style=f"bold")
        console.print(f"  [dim](Press Enter to use default, or type new path)[/dim]")
        result = safe_input("  └─> ").strip()
        return result if result else default
    else:
        return safe_input("  └─> ").strip()

def setup_directories():
    for d in [REAL_DIR, UNPACK_DIR, EDIT_DIR, PAK_DIR, PAK_UNPACK_DIR, RESULT_DIR, SOURCE_DIR]:
        try: d.mkdir(parents=True, exist_ok=True)
        except OSError as e: console.print(f"Error creating {d}: {e}")

def get_real_files():   
    return [f for f in os.listdir(REAL_DIR) if f.lower().endswith((".lua",".luac",".slua"))] if REAL_DIR.exists() else []

def get_unpack_files(): 
    return [f for f in os.listdir(UNPACK_DIR) if f.endswith(".lua")] if UNPACK_DIR.exists() else []

# ==============================================================================
# TOOLCHAIN — LUA CORE (FULL)
# ==============================================================================

def _load_xor_key() -> bytes:
    env_key = os.environ.get('BGMI_XOR_KEY')
    if env_key:
        try:
            key_bytes = bytes.fromhex(env_key.replace(' ', '').replace(':', '').replace('-', ''))
            if len(key_bytes) == 32: return key_bytes
        except ValueError: pass
    return bytes([0x11, 0x21, 0x36, 0x47, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0x35, 0x26, 0x1A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x15, 0x07, 0xD0, 0x2C, 0x1E, 0x8F, 0xF6, 0xC8])

STRING_XOR_KEY = _load_xor_key()

_BGMI_TO_STD = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,0,1,2,3,4,5,6,7,8,9,10,11,12,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]
BGMI_TO_STD = _BGMI_TO_STD + [i for i in range(len(_BGMI_TO_STD), 64)]
STD_TO_BGMI = {v: k for k, v in enumerate(BGMI_TO_STD) if k < len(BGMI_TO_STD)}
STD_FMT = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,2,0,2,0,1,0,3]
iABC, iABx, iAsBx, iAx = 0, 1, 2, 3
HEADER_SIZE = 33

class BinaryReader:
    def __init__(self, data: bytes, sizet: int = 4):
        self.data = bytearray(data); self.pos = 0; self.sizet = sizet
    def byte(self) -> int:
        if self.pos >= len(self.data): raise EOFError()
        v = self.data[self.pos]; self.pos += 1; return v
    def int32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<i', self.data, self.pos)[0]; self.pos += 4; return v
    def uint32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<I', self.data, self.pos)[0]; self.pos += 4; return v
    def double(self) -> float:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<d', self.data, self.pos)[0]; self.pos += 8; return v
    def int64(self) -> int:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<q', self.data, self.pos)[0]; self.pos += 8; return v
    def bytes(self, n: int) -> bytes:
        if self.pos + n > len(self.data): raise EOFError()
        v = self.data[self.pos:self.pos+n]; self.pos += n; return bytes(v)
    def pubg_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        enc = self.bytes(sz)
        dec = bytes(enc[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(enc)))
        try: return dec.decode('utf-8', errors='replace')
        except Exception: return dec.decode('latin-1')
    def std_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF:
            if self.sizet == 8:
                if self.pos + 8 > len(self.data): raise EOFError()
                sz = struct.unpack_from('<Q', self.data, self.pos)[0]; self.pos += 8
            else: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        raw = self.bytes(sz)
        try: return raw.decode('utf-8', errors='replace')
        except Exception: return raw.decode('latin-1')

class BinaryWriter:
    def __init__(self): self.buf = bytearray()
    def byte(self, v): self.buf.append(v & 0xFF)
    def int32(self, v): self.buf.extend(struct.pack('<i', v))
    def uint32(self, v): self.buf.extend(struct.pack('<I', v))
    def int64(self, v): self.buf.extend(struct.pack('<q', v))
    def double(self, v): self.buf.extend(struct.pack('<d', v))
    def raw(self, data): self.buf.extend(data)
    def lua_string(self, s: Optional[str], is_pubg: bool = False):
        if s is None: self.byte(0); return
        e = s.encode('utf-8') if isinstance(s, str) else s
        sz = len(e) + 1
        if sz < 0xFF: self.byte(sz)
        else: self.byte(0xFF); self.uint32(sz)
        if is_pubg:
            enc = bytes(e[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(e)))
            self.raw(enc)
        else: self.raw(e)
    def lua_inst(self, op, A, B, C, Bx, sBx, Ax, fmt):
        op &= 0x3F
        if   fmt == iABC:  r = op | ((A & 0xFF)<<6) | ((C & 0x1FF)<<14) | ((B & 0x1FF)<<23)
        elif fmt == iABx:  r = op | ((A & 0xFF)<<6) | ((Bx & 0x3FFFF)<<14)
        elif fmt == iAsBx: r = op | ((A & 0xFF)<<6) | (((sBx+131071) & 0x3FFFF)<<14)
        elif fmt == iAx:   r = op | ((Ax & 0x3FFFFFF)<<6)
        else: r = 0
        self.uint32(r)
    def get_data(self) -> bytes: return bytes(self.buf)

def _convert_function(reader: BinaryReader, writer: BinaryWriter, to_std: bool = True):
    src = reader.pubg_string() if to_std else reader.std_string()
    writer.lua_string(src, is_pubg=(not to_std))
    linedefined = reader.int32(); writer.int32(linedefined)
    writer.int32(reader.int32())
    writer.byte(reader.byte()); writer.byte(reader.byte()); writer.byte(reader.byte())
    csz = reader.uint32(); writer.uint32(csz)
    opmap = BGMI_TO_STD if to_std else STD_TO_BGMI
    for _ in range(csz):
        raw = reader.uint32()
        bop = raw & 0x3F; A = (raw >> 6) & 0xFF; B = (raw >> 23) & 0x1FF; C = (raw >> 14) & 0x1FF
        Bx = (raw >> 14) & 0x3FFFF; sBx = Bx - 131071; Ax = (raw >> 6) & 0x3FFFFFF
        sop = opmap[bop] if bop < len(opmap) else bop
        fmt = STD_FMT[sop] if sop < len(STD_FMT) else iABC
        writer.lua_inst(sop, A, B, C, Bx, sBx, Ax, fmt)
    nk = reader.uint32(); writer.uint32(nk)
    for _ in range(nk):
        t = reader.byte(); writer.byte(t)
        if t == 0: pass
        elif t == 1: writer.byte(reader.byte())
        elif t == 3: writer.double(reader.double())
        elif t == 19: writer.int64(reader.int64())
        elif t in (4, 20):
            s = reader.pubg_string() if to_std else reader.std_string()
            writer.lua_string(s, is_pubg=(not to_std))
        else: raise ValueError(f"Unknown constant type 0x{t:02X}")
    nups = reader.uint32(); writer.uint32(nups)
    for _ in range(nups): writer.byte(reader.byte()); writer.byte(reader.byte())
    npts = reader.uint32(); writer.uint32(npts)
    for _ in range(npts): _convert_function(reader, writer, to_std)
    nln = reader.uint32()
    if to_std:
        lines = []; cur = linedefined
        for _ in range(nln):
            d = reader.byte()
            cur += d if d <= 127 else d - 256
            lines.append(cur)
        writer.uint32(len(lines))
        for ln in lines: writer.int32(ln)
        nab = reader.uint32()
        for _ in range(nab): reader.uint32(); reader.uint32()
    else:
        lines = [reader.int32() for _ in range(nln)]
        writer.uint32(len(lines))
        prev = linedefined
        for ln in lines:
            delta = ln - prev
            if -128 <= delta <= 127: writer.byte(delta & 0xFF)
            else: writer.byte(0x00); writer.int32(delta)
            prev = ln
        writer.uint32(0)
    nloc = reader.uint32(); writer.uint32(nloc)
    for _ in range(nloc):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))
        writer.int32(reader.int32()); writer.int32(reader.int32())
    nupn = reader.uint32(); writer.uint32(nupn)
    for _ in range(nupn):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))

def bgmi_to_std(data: bytes) -> bytes:
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    reader = BinaryReader(data, sizet=4); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=True)
    return writer.get_data()

def std_to_bgmi(data: bytes) -> bytes:
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    sizet = data[13] if data[13] in (4, 8) else 4
    reader = BinaryReader(data, sizet=sizet); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=False)
    return writer.get_data()

def convert_file(inp: str, outp: str = None) -> Tuple[bool, str]:
    if not outp: outp = os.path.splitext(inp)[0] + '.std.luac'
    try:
        with open(inp, 'rb') as f: data = f.read()
    except Exception as e: return False, f"Cannot read input file: {e}"
    if len(data) < 34 or data[:4] != b'\x1bLua':
        try: shutil.copy2(inp, outp); return True, outp
        except: return False, "Failed to copy non-Lua file"
    nibble_flag = data[33]
    if nibble_flag > 2: nibble_flag = 0; data = bytearray(data); data[33] = 0; data = bytes(data)
    if nibble_flag > 1:
        fixed = bytearray(data[:34])
        for i in range(34, len(data)):
            b = data[i]; fixed.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
        data = bytes(fixed)
    try:
        std_data = bgmi_to_std(data)
        with open(outp, 'wb') as f: f.write(std_data)
        return True, outp
    except Exception:
        try: shutil.copy2(inp, outp); return True, outp
        except: return False, "Conversion failed"

def repack_to_pubg(std_luac_path: str, original_pubg_path: str, outp: str = None, pad_to_size: int = None) -> Tuple[bool, str]:
    if not outp: outp = os.path.splitext(std_luac_path)[0] + '.pubg.luac'
    try:
        with open(original_pubg_path, 'rb') as f: orig_data = f.read()
    except Exception as e: return False, f"Cannot read original: {e}"
    if len(orig_data) < 34 or orig_data[:4] != b'\x1bLua': return False, "Original not valid Lua bytecode"
    header = orig_data[:33]; nibble_flag = orig_data[33]
    if nibble_flag > 2: nibble_flag = 0
    try:
        with open(std_luac_path, 'rb') as f: std_data = f.read()
    except Exception as e: return False, f"Cannot read std luac: {e}"
    try:
        bgmi_data = std_to_bgmi(std_data)
        bgmi_data = header + bytes([nibble_flag]) + bgmi_data[34:]
        if nibble_flag > 1:
            data_list = bytearray(bgmi_data[:34])
            for i in range(34, len(bgmi_data)):
                b = bgmi_data[i]; data_list.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
            bgmi_data = bytes(data_list)
        if pad_to_size is not None and len(bgmi_data) < pad_to_size:
            bgmi_data += b'\x00' * (pad_to_size - len(bgmi_data))
        with open(outp, 'wb') as f: f.write(bgmi_data)
        return True, outp
    except Exception as e: return False, f"Repack failed: {e}"

UNLUAC_JAR_PATH = SOURCE_DIR / "unluac_patched.jar"
UNLUAC_JAR = str(UNLUAC_JAR_PATH)
JAVA_CMD = "java"
BUNDLED_JDK_CANDIDATES = list(SOURCE_DIR.glob("jdk*/bin/java.exe")) + list(SOURCE_DIR.glob("jdk*/bin/java"))
if BUNDLED_JDK_CANDIDATES: JAVA_CMD = str(BUNDLED_JDK_CANDIDATES[0])

def get_luac_cmd() -> str:
    for name in ["luac5.3", "luac53", "luac5.3.exe", "luac53.exe"]:
        p = SOURCE_DIR / name
        if p.exists(): return str(p)
    for name in ["luac5.3", "luac53.exe"]:
        w = shutil.which(name)
        if w: return w
    return "luac5.3"

LUAC_PATH = get_luac_cmd()
STRIP_DEBUG = True

def decrypt_decompile_file(file_path: str, output_dir: str, progress_callback=None) -> bool:
    try:
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        if base_name.lower().endswith('.lua'): base_name = os.path.splitext(base_name)[0]
        output_file = os.path.join(output_dir, base_name + ".lua")
        temp_std = file_path + ".temp.std.luac"
        if progress_callback: progress_callback(f"Converting {filename}...")
        success, msg = convert_file(file_path, temp_std)
        if not success:
            if progress_callback: progress_callback(f"Conversion failed: {msg}")
            shutil.copy2(file_path, os.path.join(output_dir, base_name + ".luac"))
            return False
        if not os.path.exists(UNLUAC_JAR):
            if progress_callback: progress_callback("unluac.jar missing, saving raw bytecode")
            shutil.copy2(temp_std, os.path.join(output_dir, base_name + ".luac"))
            os.remove(temp_std); return False
        try:
            cmd = [JAVA_CMD, "-jar", UNLUAC_JAR, temp_std]
            with open(output_file, "w", encoding="utf-8") as out:
                subprocess.check_call(cmd, stdout=out, stderr=subprocess.PIPE, timeout=30)
            if progress_callback: progress_callback(f"Decompiled {filename}")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            if progress_callback: progress_callback(f"Decompilation failed: {e}")
            shutil.copy2(temp_std, os.path.join(output_dir, base_name + ".luac"))
            return False
        finally:
            if os.path.exists(temp_std): os.remove(temp_std)
        return True
    except Exception as e:
        if progress_callback: progress_callback(f"Exception: {e}")
        return False

def robust_decompile(encrypted_path: str, output_dir: str, tmp_dir: str) -> Tuple[bool, str, List[str]]:
    name = os.path.basename(encrypted_path); base = os.path.splitext(name)[0]
    out_path = os.path.join(output_dir, base + ".lua")
    temp_std = os.path.join(tmp_dir, base + ".std.luac")
    ok, msg = convert_file(encrypted_path, temp_std)
    if not ok: return False, msg, []
    if not os.path.exists(UNLUAC_JAR): return False, "unluac_patched.jar not found", []
    try:
        cmd = [JAVA_CMD, "-jar", UNLUAC_JAR, temp_std]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout:
            with open(out_path, 'w', encoding='utf-8') as f: f.write(result.stdout)
            return True, out_path, []
        else: return False, f"Decompilation failed: {(result.stderr or 'unknown error').strip()[:200]}", []
    except subprocess.TimeoutExpired: return False, "Decompilation timed out", []
    except Exception as e: return False, str(e), []

def select_files_interactive(files: List[str], source_dir: str, action_name: str) -> List[str]:
    if not files: return []
    if len(files) == 1:
        console.print(f"Only 1 file found: {files[0]}")
        confirm = hexa_prompt("Process this file? (Y/n): ").strip().lower()
        return files if confirm != 'n' else []
    console.print(f"\nSelect files to {action_name}:")
    for idx, f in enumerate(files, 1):
        sz = os.path.getsize(os.path.join(source_dir, f))
        console.print(f"  [{idx}] {f} ({sz:,} bytes)")
    console.print("  [A] ALL FILES")
    console.print("  [0] Cancel")
    while True:
        choice = hexa_prompt("Your choice: ").strip().upper()
        if choice == 'A': return files
        if choice == '0': return []
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(files): return [files[idx-1]]
        console.print("Invalid selection!")

def action_unpack():
    files = get_real_files()
    if not files: hexa_alert("LUA_ORIGINAL folder is empty!", "error"); safe_input('\nPress Enter...'); return
    selected = select_files_interactive(files, str(REAL_DIR), "UNPACK")
    if not selected: return
    success = 0
    with tempfile.TemporaryDirectory(prefix='bgmi_dec_') as tmp_dir:
        for idx, f in enumerate(selected, 1):
            console.print(f"[{idx}/{len(selected)}] {f}")
            inp = REAL_DIR / f
            ok, result, _ = robust_decompile(str(inp), str(UNPACK_DIR), tmp_dir)
            if ok:
                console.print(f"Decompiled: {os.path.basename(result)}"); success += 1
            else:
                console.print(f"Failed: {result}")
                fallback_path = UNPACK_DIR / (os.path.splitext(f)[0] + ".luac")
                ok2, _ = convert_file(str(inp), str(fallback_path))
                if ok2: console.print(f"Saved raw bytecode as {fallback_path}")
    hexa_alert(f"Unpack Complete! {success}/{len(selected)} files decompiled.", "success")
    safe_input('\nPress Enter...')

def recompile_lua_files(selected: List[str], quiet: bool = False) -> Tuple[int, List[str]]:
    success = 0; failed = []
    for idx, f in enumerate(selected, 1):
        name = os.path.splitext(f)[0]
        inp = UNPACK_DIR / f
        out = EDIT_DIR / (name + ".lua")
        console.print(f"[{idx}/{len(selected)}] {f}")
        
        if FORCE_COMPILE:
            console.print(f"[bold yellow]FORCE COMPILE GRW POWER FULL TOOL[/bold yellow]")
        
        temp_std = str(LUA_PAK_ROOT / f"{name}_temp_std.luac")
        cmd = [LUAC_PATH, "-s", "-o", temp_std, str(inp)] if STRIP_DEBUG else [LUAC_PATH, "-o", temp_std, str(inp)]
        try: 
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            console.print("Compilation timed out")
            failed.append(f)
            continue
        
        if res.returncode == 0 and os.path.exists(temp_std):
            orig = None
            for ext in ['.luac', '.slua', '.lua']:
                p = REAL_DIR / (name + ext)
                if p.exists():
                    orig = str(p)
                    break
            if not orig:
                console.print("Original file not found in LUA_ORIGINAL")
                failed.append(f)
            else:
                ok2, msg = repack_to_pubg(temp_std, orig, str(out), pad_to_size=os.path.getsize(orig))
                if ok2:
                    console.print(f"Recompiled: {out.name} ({out.stat().st_size:,} bytes)")
                    success += 1
                else:
                    console.print(f"Recompile failed: {msg}")
                    failed.append(f)
            if os.path.exists(temp_std):
                os.remove(temp_std)
        else:
            console.print(f"Compilation failed: {res.stderr.strip() if res.stderr else 'Unknown error'}")
            failed.append(f)
    return success, failed

def action_repack_unpack():
    files = get_unpack_files()
    if not files: hexa_alert("LUA_EDIT folder is empty!", "error"); safe_input('\nPress Enter...'); return
    selected = select_files_interactive(files, str(UNPACK_DIR), "REPACK")
    if not selected: return
    
    if FORCE_COMPILE and SKIP_ALL_FIXES:
        console.print("[bold cyan] 🚀 FAST COMPILE MODE — Raw Build Execution[/bold cyan]")
        console.print("[bold cyan]Launching high-speed compilation...[/bold cyan]")
    
    success, failed = recompile_lua_files(selected)
    hexa_alert(f"Repack Complete! {success}/{len(selected)} successful.", "success")
    if failed: hexa_alert(f"Failed files: {', '.join(failed)}", "error")
    safe_input('\nPress Enter...')

# ==============================================================================
# TOOLCHAIN — PAK CORE (COMPLETE)
# ==============================================================================

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')
SIMPLE1_DECRYPT_KEY = 0x79
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16
SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = ['xG2qW5lP7lV2iN5fN5pG','xT1cJ6dL5wC0kK1rB4dK','qC4jS5bZ6fL5xE6nD4zA','gD4jQ2aL3bS3lC3xT0iW','xU1yQ8wE9zY3gZ3bT5aE','uQ3cO2dX7xY4xU7gH7iS','gW1fR0jK6wQ4oN0oK1kZ','aJ4pV7iZ7pU4wP2aC2cZ','cX6jT3cM2oT3vK0kJ1qN','iT2vS0cS6yT6cZ1sE1lO','hM1pH9iY8wM9hT4lN5uJ','kG6bC8jK0fL0dE4sH4mL','dB6lB3vE0eZ8wM8rI0aC','tP7sP7nI9rA2vQ4cV5yQ','aT0cL1yN4pT3sZ7eM2vY','uV6fU8fC9zN3mP5dH8mN']
EM_SIMPLE1 = 1; EM_SIMPLE2 = 16; EM_UNKNOWN_17 = 17; EM_SM4_2 = 2; EM_SM4_4 = 4; EM_SM4_NEW_BASE = 31; EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
CM_NONE = 0; CM_ZLIB = 1; CM_ZSTD = 6; CM_ZSTD_DICT = 8; CM_MASK = 15

class SM4:
    _S_BOX = bytes([0x34,0x66,0x25,0x74,0x89,0x78,0xE4,0xA9,0x5A,0x41,0xBC,0x7A,0xD6,0x16,0x21,0x23,0x4D,0x61,0xDA,0x94,0x9B,0xDF,0x13,0x3C,0x69,0x3A,0x31,0x0A,0x5F,0xD7,0x99,0x95,0xF1,0xAE,0x72,0x3D,0x07,0x60,0x24,0xB6,0x98,0xEE,0xC4,0xA2,0x2D,0x88,0xDD,0x8D,0x04,0xEA,0xBB,0x11,0xCA,0x3E,0x5D,0xA1,0xF6,0x3F,0xB0,0x97,0x80,0x47,0x2B,0xA6,0xE6,0xF7,0xD9,0xB1,0x59,0xC0,0x7C,0xBE,0x54,0x28,0xB7,0x7E,0x4F,0xF8,0x43,0x6E,0xA0,0x50,0x0E,0xF5,0x90,0xB8,0xFB,0xA3,0x7B,0x62,0x19,0x46,0x03,0x2A,0xB9,0x8F,0x9F,0x77,0xB4,0x5B,0x83,0x87,0x08,0xEB,0xE2,0x1E,0x42,0xF0,0x0F,0xE8,0x71,0x6A,0x75,0xAD,0x55,0x1F,0xB5,0xAB,0x33,0xFA,0x7F,0x15,0xBD,0x85,0xD8,0x06,0x68,0xB3,0x52,0x30,0x48,0x0B,0x00,0xED,0xEF,0xB2,0x57,0x8E,0xE7,0x6C,0xD5,0xE5,0x2E,0x53,0x82,0x05,0xF9,0x81,0xF4,0x56,0xBF,0x8C,0x4B,0xE3,0xDB,0x4A,0x91,0x4C,0x2C,0xD3,0x40,0x29,0x4E,0x20,0x14,0x36,0x79,0x09,0x6F,0xD1,0x37,0xE0,0x39,0x0C,0x8A,0x92,0x38,0x12,0x35,0x6D,0xE1,0xFD,0x93,0x9A,0x17,0xD4,0xC9,0x9C,0x6B,0x84,0x26,0x9D,0xAF,0x76,0xC1,0x9E,0xD0,0x96,0xC5,0xCB,0xE9,0x73,0x49,0xD2,0xCD,0x64,0xC3,0xC7,0x01,0x7D,0xF3,0xAC,0xFC,0xDE,0xA4,0x44,0x32,0x1B,0xC2,0xBA,0x1C,0x02,0xC6,0x27,0x45,0x8B,0xF2,0x18,0xA7,0x10,0x51,0x1D,0xC8,0xCF,0x63,0xFF,0x2F,0x0D,0x58,0xCE,0x65,0xA5,0xDC,0x1A,0x3B,0x86,0xFE,0x22,0x5C,0xA8,0x5E,0x67,0xAA,0xEC,0x70,0xCC])
    _FK = [0x46970E9C,0x4BC0685E,0x59056186,0xBCA2491E]
    _CK = [0x000EB92B,0x3A0AE783,0x9E3B5C67,0xADDBDABF,0x7B7484CB,0x49156C63,0xC79AB5E7,0x79EC9CFF,0x1725BEAB,0x2FB89CA3,0x24808AD7,0xDDD28B1F,0x4740DA4B,0xBBC3EA73,0x247B30E7,0x91BE385F,0x0401248B,0x45FCD3A3,0x530B4CE7,0xC68DD35F,0xE3D16C2B,0x4F698C13,0x6B92C747,0x769EFB1F,0x4C73BE9B,0xC942B193,0xAD80D827,0x372FB33F,0x13CB6AAB,0x2BDC0AA3,0x17A4A247,0xD5E96CAF]
    @staticmethod
    def ROL32(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))
    @staticmethod
    def _BS(X): return ((SM4._S_BOX[(X>>24)&0xff]<<24)|(SM4._S_BOX[(X>>16)&0xff]<<16)|(SM4._S_BOX[(X>>8)&0xff]<<8)|SM4._S_BOX[X&0xff])
    @staticmethod
    def _T0(X): X = SM4._BS(X); return X ^ SM4.ROL32(X,2) ^ SM4.ROL32(X,10) ^ SM4.ROL32(X,18) ^ SM4.ROL32(X,24)
    @staticmethod
    def _T1(X): X = SM4._BS(X); return X ^ SM4.ROL32(X,13) ^ SM4.ROL32(X,23)
    @classmethod
    def key_length(cls): return 16
    @classmethod
    def block_length(cls): return 16
    def __init__(self, key: bytes):
        if len(key) != 16: raise IncorrectLengthError("Key","16 bytes",f"{len(key)} bytes")
        self._key = key; self._rkey = [0]*32
        K0 = int.from_bytes(key[0:4],'big') ^ self._FK[0]; K1 = int.from_bytes(key[4:8],'big') ^ self._FK[1]
        K2 = int.from_bytes(key[8:12],'big') ^ self._FK[2]; K3 = int.from_bytes(key[12:16],'big') ^ self._FK[3]
        for i in range(0,32,4):
            K0 = K0 ^ self._T1(K1^K2^K3^self._CK[i]); self._rkey[i] = K0
            K1 = K1 ^ self._T1(K2^K3^K0^self._CK[i+1]); self._rkey[i+1] = K1
            K2 = K2 ^ self._T1(K3^K0^K1^self._CK[i+2]); self._rkey[i+2] = K2
            K3 = K3 ^ self._T1(K0^K1^K2^self._CK[i+3]); self._rkey[i+3] = K3
        self._block_buffer = bytearray()
    def encrypt(self, block: bytes) -> bytes:
        if len(block) != 16: raise IncorrectLengthError("Block","16 bytes",f"{len(block)} bytes")
        RK = self._rkey; X0 = int.from_bytes(block[0:4],'big'); X1 = int.from_bytes(block[4:8],'big')
        X2 = int.from_bytes(block[8:12],'big'); X3 = int.from_bytes(block[12:16],'big')
        for i in range(0,32,4):
            X0 = X0 ^ self._T0(X1^X2^X3^RK[i]); X1 = X1 ^ self._T0(X2^X3^X0^RK[i+1])
            X2 = X2 ^ self._T0(X3^X0^X1^RK[i+2]); X3 = X3 ^ self._T0(X0^X1^X2^RK[i+3])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4,'big')); buf.extend(X2.to_bytes(4,'big'))
        buf.extend(X1.to_bytes(4,'big')); buf.extend(X0.to_bytes(4,'big'))
        return bytes(buf)
    def decrypt(self, block: bytes) -> bytes:
        if len(block) != 16: raise IncorrectLengthError("Block","16 bytes",f"{len(block)} bytes")
        RK = self._rkey; X0 = int.from_bytes(block[0:4],'big'); X1 = int.from_bytes(block[4:8],'big')
        X2 = int.from_bytes(block[8:12],'big'); X3 = int.from_bytes(block[12:16],'big')
        for i in range(0,32,4):
            X0 = X0 ^ self._T0(X1^X2^X3^RK[31-i]); X1 = X1 ^ self._T0(X2^X3^X0^RK[30-i])
            X2 = X2 ^ self._T0(X3^X0^X1^RK[29-i]); X3 = X3 ^ self._T0(X0^X1^X2^RK[28-i])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4,'big')); buf.extend(X2.to_bytes(4,'big'))
        buf.extend(X1.to_bytes(4,'big')); buf.extend(X0.to_bytes(4,'big'))
        return bytes(buf)

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        padding = n - (len(data) % n)
        return data if padding == n else data + b'\x00' * padding
    @staticmethod
    def align_up(x: int, n: int) -> int: return ((x + n - 1) // n) * n

class Reader:
    def __init__(self, buffer, cursor=0): self._buffer = buffer; self._cursor = cursor
    def u1(self, move_cursor=True): return self.unpack('B', move_cursor=move_cursor)[0]
    def u4(self, move_cursor=True): return self.unpack('<I', move_cursor=move_cursor)[0]
    def u8(self, move_cursor=True): return self.unpack('<Q', move_cursor=move_cursor)[0]
    def i1(self, move_cursor=True): return self.unpack('b', move_cursor=move_cursor)[0]
    def i4(self, move_cursor=True): return self.unpack('<i', move_cursor=move_cursor)[0]
    def i8(self, move_cursor=True): return self.unpack('<q', move_cursor=move_cursor)[0]
    def s(self, n: int, move_cursor=True): return self.unpack(f'{n}s', move_cursor=move_cursor)[0]
    def unpack(self, f, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor: self._cursor += struct.calcsize(f)
        return x
    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0: return str()
        offset = 0 if move_cursor else 4
        return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()

class PakInfo:
    def __init__(self, buffer, keystream: list):
        def dec_enc(x): return (x ^ keystream[3]) & 0xFF
        def dec_magic(x): return x ^ keystream[2]
        def dec_ihash(x): key = struct.pack('<5I', *keystream[4:][:5]); return bytes(a^b for a,b in zip(x,key))
        def dec_isz(x): return x ^ ((keystream[10]<<32)|keystream[11])
        def dec_ioff(x): return x ^ ((keystream[0]<<32)|keystream[1])
        reader = Reader(buffer[-PakInfo._mem_size(-1):])
        self.index_encrypted = dec_enc(reader.u1()) == 1
        self.magic = dec_magic(reader.u4())
        self.version = reader.u4()
        self.index_hash = dec_ihash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size = dec_isz(reader.u8())
        self.index_offset = dec_ioff(reader.u8())
        if self.version <= 3: self.index_encrypted = False
    @staticmethod
    def _mem_size(_): return 1+4+4+20+8+8

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: list):
        def dec_unk(x): key = struct.pack('<8I', *keystream[7:][:8]); return bytes(a^b for a,b in zip(x,key))
        def dec_stem(x): return x ^ keystream[8]
        def dec_uhash(x): return x ^ keystream[9]
        super().__init__(buffer, keystream)
        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1 = dec_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash = dec_stem(reader.u4()) if self.version >= 9 else 0
        self.unk2 = dec_uhash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash = reader.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(version):
        return PakInfo._mem_size(version) + (32 if version>=7 else 0) + (768 if version>=8 else 0) + (8 if version>=9 else 0) + (20 if version>=12 else 0)

class PakCompressedBlock:
    def __init__(self, reader: Reader = None, start: int = 0, end: int = 0):
        if reader is not None: self.start = reader.u8(); self.end = reader.u8()
        else: self.start = start; self.end = end

class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash = reader.s(20)
        if version <= 1: _ = reader.u8()
        self.offset = reader.u8()
        self.uncompressed_size = reader.u8()
        self.compression_method = reader.u4() & CM_MASK
        self.size = reader.u8()
        self.unk1 = reader.u1() if version >= 5 else 0
        self.unk2 = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks = [PakCompressedBlock(reader) for _ in range(reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size = reader.u4() if version >= 4 else 0
        self.encrypted = reader.u1() == 1 if version >= 4 else False
        self.encryption_method = reader.u4() if version >= 12 else 0
        self.index_new_sep = reader.u4() if version >= 12 else 0

class PakCrypto:
    class _LCG:
        def __init__(self, seed): self.state = seed
        def next(self):
            MASK_32 = 0xFFFFFFFF; MSB_1 = 1<<31
            def wrap(x):
                x &= MASK_32
                return x if not x&MSB_1 else ((x+MSB_1)&MASK_32)-MSB_1
            x1 = wrap(0x41C64E6D * self.state); self.state = wrap(x1+12345)
            x2 = wrap(x1+0x13038) if self.state < 0 else self.state
            return ((x2>>16) & MASK_32) % 0x7FFF

    @staticmethod
    def zuc_keystream() -> list:
        if not PAK_MODE_AVAILABLE or not hasattr(gmalg, 'ZUC'): return [0]*16
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]

    @staticmethod
    def _xorxor(buffer, x) -> bytes: return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))
    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        if not PAK_MODE_AVAILABLE: return b'\x00'*n
        block = SHA1.new(buffer).digest()
        result = block * math.ceil(n / SHA1.digest_size)
        return result[:n] if len(result) >= n else result + b'\x00' * (n - len(result))

    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]
        if len(buffer) < 43: return bytes()
        x1 = buffer[1:][:SHA1.digest_size]; x2 = buffer[SHA1.digest_size+1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = x2[:SHA1.digest_size], x2[SHA1.digest_size:]
        if part1 != SHA1.new(b'\x00'*SHA1.digest_size).digest(): return bytes()
        return unpad(m)

    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature,'little'); n = int.from_bytes(modulus,'little')
        m = pow(c, 0x10001, n).to_bytes(256,'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))

    @staticmethod
    def _encrypt_simple1(pt) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in pt)
    @staticmethod
    def _decrypt_simple1(ct) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ct)

    @staticmethod
    def _encrypt_simple2(pt) -> bytes:
        class RK:
            def __init__(self, v): self._v = v
            def update(self, x): ov = self._v; self._v = x; return ov ^ x
        assert len(pt) % SIMPLE2_BLOCK_SIZE == 0
        iv, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rk = RK(iv)
        return bytes(it.chain.from_iterable(struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(pt)//4}I', pt)))

    @staticmethod
    def _decrypt_simple2(ct) -> bytes:
        class RK:
            def __init__(self, v): self._v = v
            def update(self, x): self._v ^= x; return self._v
        assert len(ct) % SIMPLE2_BLOCK_SIZE == 0
        iv, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rk = RK(iv)
        return bytes(it.chain.from_iterable(struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(ct)//4}I', ct)))

    @staticmethod
    @lru_cache(maxsize=33)
    def _derive_sm4_key(file_path: PurePath, em: int) -> bytes:
        part1 = file_path.stem.lower()
        if em == EM_SM4_2: secret = SM4_SECRET_2
        elif em == EM_SM4_4: secret = SM4_SECRET_4
        else: secret = f'{SM4_SECRET_NEW[(em-EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)]}{em}'
        return SHA1.new(str(part1+secret).encode()).digest()[:SM4.key_length()]

    @staticmethod
    @lru_cache(maxsize=33)
    def _sm4_ctx(key: bytes) -> SM4: return SM4(key)

    @staticmethod
    def _encrypt_sm4(pt, fp: PurePath, em: int) -> bytes:
        padded = pad(pt, SM4.block_length())
        sm4 = PakCrypto._sm4_ctx(PakCrypto._derive_sm4_key(fp, em))
        return bytes(it.chain.from_iterable(sm4.encrypt(bytes(x)) for x in it.batched(padded, SM4.block_length())))

    @staticmethod
    def _decrypt_sm4(ct, fp: PurePath, em: int) -> bytes:
        assert len(ct) % SM4.block_length() == 0
        sm4 = PakCrypto._sm4_ctx(PakCrypto._derive_sm4_key(fp, em))
        return bytes(it.chain.from_iterable(sm4.decrypt(bytes(x)) for x in it.batched(ct, SM4.block_length())))

    @staticmethod
    def decrypt_index(ct, pak_info: TencentPakInfo) -> bytes:
        if pak_info.version > 7:
            key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            aes = AES.new(key, MODE_CBC, iv[:16])
            return unpad(aes.decrypt(ct), AES.block_size)
        return bytes(PakCrypto._decrypt_simple1(ct))

    @staticmethod
    def _is_simple1(em): return em == EM_SIMPLE1
    @staticmethod
    def _is_simple2(em): return em == EM_SIMPLE2 or em == 17
    @staticmethod
    def _is_sm4(em): return em in (EM_SM4_2, EM_SM4_4) or em & EM_SM4_NEW_MASK != 0

    @staticmethod
    def align_encrypted_content_size(n: int, em: int) -> int:
        if PakCrypto._is_simple2(em): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        if PakCrypto._is_sm4(em): return Misc.align_up(n, SM4.block_length())
        return n

    @staticmethod
    def encrypt_block(pt, file: PurePath, em: int) -> bytes:
        if PakCrypto._is_simple1(em): return PakCrypto._encrypt_simple1(pt)
        if PakCrypto._is_simple2(em): return PakCrypto._encrypt_simple2(pad(pt, SIMPLE2_BLOCK_SIZE))
        if PakCrypto._is_sm4(em): return PakCrypto._encrypt_sm4(pt, file, em)
        assert False, f"Unknown encryption method: {em}"

    @staticmethod
    def decrypt_block(ct, file: PurePath, em: int) -> bytes:
        if PakCrypto._is_simple1(em): return PakCrypto._decrypt_simple1(ct)
        if PakCrypto._is_simple2(em): return PakCrypto._decrypt_simple2(ct)
        if PakCrypto._is_sm4(em): return PakCrypto._decrypt_sm4(ct, file, em)
        assert False, f"Unknown encryption method: {em}"

    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, em: int) -> list:
        if not PakCrypto._is_sm4(em): return list(range(n))
        perm = list(range(n))
        rng = random.Random(n)
        rng.shuffle(perm)
        inv = [0]*n
        for i, x in enumerate(perm): inv[x] = i
        return inv

class PakCompression:
    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_dec(dict_data):
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdDecompressor(dict_obj)

    @staticmethod
    @lru_cache(maxsize=128)
    def _zstd_enc(dict_data, level):
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdCompressor(level=level, dict_data=dict_obj, write_checksum=False, write_content_size=False, write_dict_id=False)

    @staticmethod
    def decompress_block(block, dict_data, cm: int) -> bytes:
        if cm == CM_ZLIB:
            try: return zlib.decompress(block)
            except: return block
        elif cm in (CM_ZSTD, CM_ZSTD_DICT):
            dd = dict_data if cm == CM_ZSTD_DICT else None
            try: return PakCompression._zstd_dec(dd).decompress(block)
            except: return block
        assert False, f"Unknown decompression method: {cm}"

    @staticmethod
    def compress_block(block, dict_data, cm: int, level=None) -> bytes:
        if cm == CM_ZLIB:
            return zlib.compress(block, level=level if level is not None else 9)
        elif cm in (CM_ZSTD, CM_ZSTD_DICT):
            dd = dict_data if cm == CM_ZSTD_DICT else None
            return PakCompression._zstd_enc(dd, level if level is not None else 22).compress(block)
        assert False, f"Unknown compression method: {cm}"

class TencentPakFile:
    def __init__(self, file_path: PurePath, is_od=False):
        self._file_path = file_path
        with open(file_path, 'rb') as f: self._file_content = memoryview(f.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files: list = []
        self._index: dict = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._verify_stem_hash()
        self._tencent_load_index()
        self._path_to_entry = None

    def _verify_stem_hash(self):
        if not self._is_od and self._pak_info.version >= 9:
            assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))

    def _tencent_load_index(self):
        index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        if self._pak_info.index_encrypted: index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
        self._verify_index_hash(index_data)
        self._load_index(index_data)

    def _verify_index_hash(self, index_data):
        expected = self._pak_info.index_hash
        if not self._is_od and self._pak_info.version >= 8:
            assert expected == PakCrypto.rsa_extract(self._pak_info.packed_index_hash, RSA_MOD_2)
        assert expected == SHA1.new(index_data).digest()

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        result = PurePath()
        for part in PurePath(mount_point).parts:
            if part != '..': result /= part
        return result

    def _peek_content(self, offset, size, em):
        size = PakCrypto.align_encrypted_content_size(size, em)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, em):
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, em)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry):
        assert not self._zstd_dict and not dict_entry.encrypted and dict_entry.compression_method == CM_NONE
        console.print("[bold cyan]► LOADING ZSTD DICTIONARY...[/bold cyan]")
        reader = Reader(self._peek_content(dict_entry.offset, dict_entry.size, 0))
        dict_size = reader.u8(); _ = reader.u4(); real_size = reader.u4()
        assert dict_size == real_size
        self._zstd_dict = reader.s(dict_size)
        console.print("[bold green]► DICTIONARY LOADED SUCCESSFULLY![/bold green]")
        time.sleep(2)

    def _load_index(self, index_data):
        if self._pak_info.version <= 10:
            console.print("[bold yellow]Warning: Pak version is too old, may not be fully supported[/bold yellow]")
        reader = Reader(index_data)
        self._original_mount_point = reader.string()
        self._mount_point = self._construct_mount_point(self._original_mount_point)
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(reader.u4())]
        self._dir_path_strings = {}
        try:
            num_dirs = reader.u8()
            for _ in range(num_dirs):
                dir_str = reader.string()
                dir_path = PurePath(dir_str); num_files = reader.u8()
                self._dir_path_strings[dir_path] = dir_str
                e = {reader.string(): self._files[~reader.i4()] for _ in range(num_files)}
                if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                    assert len(e) == 1
                    self._construct_zstd_dict(list(e.values())[0])
                    self._zstddic_info = (dir_str, e)
                    continue
                self._index.update({PurePath(dir_path): e})
        except struct.error:
            console.print("[dim]Note: Finished reading index (older pak format).[/dim]")
        self._path_to_entry = None

    def _build_path_map(self) -> Dict[str, TencentPakEntry]:
        if self._path_to_entry is None:
            self._path_to_entry = {}
            for dir_path, dir_content in self._index.items():
                for fname, entry in dir_content.items():
                    full_path = self._mount_point / dir_path / fname
                    full = str(full_path).replace('\\', '/')
                    self._path_to_entry[full] = entry
        return self._path_to_entry

    def _get_method_str(self, m, is_enc):
        if is_enc:
            if PakCrypto._is_simple1(m): return "SIMPLE1"
            if PakCrypto._is_simple2(m): return "SIMPLE2"
            if PakCrypto._is_sm4(m): return f"SM4 (Type {m})"
            return "NONE" if m == 0 else "UNKNOWN"
        else:
            return {CM_NONE:"NONE",CM_ZLIB:"ZLIB",CM_ZSTD:"ZSTD",CM_ZSTD_DICT:"ZSTD_DICT"}.get(m,"UNKNOWN")

    def _write_to_disk(self, file_path: PurePath, entry: TencentPakEntry):
        em = entry.encryption_method; cm = entry.compression_method
        enc_str = self._get_method_str(em,True); comp_str = self._get_method_str(cm,False)
        console.print(f"[bold cyan]->[/bold cyan] Unpack: [bold green]{file_path.name}[/bold green] [[bold yellow]{comp_str}[/bold yellow]/[bold magenta]{enc_str}[/bold magenta]]")
        with open(file_path, 'wb') as f:
            if cm == CM_NONE:
                data = self._peek_content(entry.offset, entry.size, em)
                if entry.encrypted: data = PakCrypto.decrypt_block(bytes(data), file_path, em)
                f.write(data[:entry.size]); return
            buf = bytearray()
            for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), em):
                data = self._peek_block_content(entry.compressed_blocks[x], em)
                if entry.encrypted: data = PakCrypto.decrypt_block(bytes(data), file_path, em)
                if not data: continue
                data = data[:entry.compressed_blocks[x].end - entry.compressed_blocks[x].start]
                buf.extend(PakCompression.decompress_block(bytes(data), self._zstd_dict, cm))
            f.write(bytes(buf)[:entry.uncompressed_size])

    def dump(self, out_path: PurePath):
        dest_dir = Path(out_path)
        dest_dir.mkdir(parents=True, exist_ok=True)
        total_files = sum(len(d) for d in self._index.values())
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan][UNPACK][/] {task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Extracting files...", total=total_files)
            for dir_path, dir_content in self._index.items():
                current_out_path = dest_dir / dir_path
                current_out_path.mkdir(parents=True, exist_ok=True)
                for file_name, entry in dir_content.items():
                    self._write_to_disk(current_out_path / file_name, entry)
                    progress.update(task, advance=1)

    def dump_lua_only(self, out_path: PurePath):
        dest_dir = Path(out_path)
        dest_dir.mkdir(parents=True, exist_ok=True)
        for dir_path, dir_content in self._index.items():
            for file_name, entry in dir_content.items():
                if file_name.lower().endswith(('.lua', '.luac', '.slua')):
                    self._write_to_disk(dest_dir / file_name, entry)

    def _pack_string(self, s: str) -> bytes:
        if not s: return struct.pack('<i', 0)
        encoded = s.encode('utf-8') + b'\x00'
        return struct.pack('<i', len(encoded)) + encoded

    def _pack_entry(self, entry, version: int) -> bytes:
        buf = bytearray()
        buf.extend(struct.pack('<20s', entry.content_hash))
        if version <= 1: buf.append(0)
        buf.extend(struct.pack('<Q', entry.offset))
        buf.extend(struct.pack('<Q', entry.uncompressed_size))
        buf.extend(struct.pack('<I', entry.compression_method))
        buf.extend(struct.pack('<Q', entry.size))
        if version >= 5:
            buf.append(entry.unk1)
            buf.extend(struct.pack('<20s', entry.unk2))
        if entry.compression_method != 0 and version >= 3:
            buf.extend(struct.pack('<I', len(entry.compressed_blocks)))
            for block in entry.compressed_blocks:
                buf.extend(struct.pack('<QQ', block.start, block.end))
        if version >= 4:
            buf.extend(struct.pack('<I', entry.compression_block_size))
            buf.append(1 if entry.encrypted else 0)
        if version >= 12:
            buf.extend(struct.pack('<I', entry.encryption_method))
            buf.extend(struct.pack('<I', entry.index_new_sep))
        return bytes(buf)

    def _pack_index(self) -> bytes:
        buf = bytearray()
        mount_point_str = getattr(self, '_original_mount_point', str(self._mount_point))
        buf.extend(self._pack_string(mount_point_str))
        buf.extend(struct.pack('<I', len(self._files)))
        for entry in self._files:
            buf.extend(self._pack_entry(entry, self._pak_info.version))
        entry_to_idx = {id(entry): idx for idx, entry in enumerate(self._files)}
        dirs_to_pack = []
        for dir_path, dir_content in self._index.items():
            valid_files = []
            for file_name, entry in dir_content.items():
                if id(entry) in entry_to_idx:
                    valid_files.append((file_name, entry))
            if valid_files:
                dirs_to_pack.append((dir_path, valid_files))
        if hasattr(self, '_zstddic_info') and self._zstddic_info:
            dir_str, e = self._zstddic_info
            valid_files = []
            for file_name, entry in e.items():
                if id(entry) in entry_to_idx:
                    valid_files.append((file_name, entry))
            dirs_to_pack.append((PurePath(dir_str), valid_files))
        buf.extend(struct.pack('<Q', len(dirs_to_pack)))
        for dir_path, valid_files in dirs_to_pack:
            dir_str = self._dir_path_strings.get(dir_path, dir_path.as_posix())
            buf.extend(self._pack_string(dir_str))
            buf.extend(struct.pack('<Q', len(valid_files)))
            for file_name, entry in valid_files:
                buf.extend(self._pack_string(file_name))
                buf.extend(struct.pack('<i', ~entry_to_idx[id(entry)]))
        return bytes(buf)

    def _pack_footer(self) -> bytes:
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        enc_flag = ((1 if self._pak_info.index_encrypted else 0) ^ keystream[3]) & 0xFF
        enc_magic = (self._pak_info.magic ^ keystream[2]) & 0xFFFFFFFF
        key_ihash = struct.pack('<5I', *keystream[4:][:5])
        enc_index_hash = bytes(a^b for a,b in zip(self._pak_info.index_hash, key_ihash)) if version >= 6 else bytes()
        enc_index_size = (self._pak_info.index_size ^ ((keystream[10]<<32)|keystream[11])) & 0xFFFFFFFFFFFFFFFF
        enc_index_offset = (self._pak_info.index_offset ^ ((keystream[0]<<32)|keystream[1])) & 0xFFFFFFFFFFFFFFFF
        base_buf = bytearray()
        base_buf.append(enc_flag)
        base_buf.extend(struct.pack('<II', enc_magic, version))
        if version >= 6: base_buf.extend(enc_index_hash)
        base_buf.extend(struct.pack('<QQ', enc_index_size, enc_index_offset))
        t_buf = bytearray()
        if version >= 7:
            key_unk = struct.pack('<8I', *keystream[7:][:8])
            enc_unk1 = bytes(a^b for a,b in zip(self._pak_info.unk1, key_unk))
            t_buf.extend(enc_unk1)
        if version >= 8:
            t_buf.extend(self._pak_info.packed_key)
            t_buf.extend(self._pak_info.packed_iv)
            t_buf.extend(self._pak_info.packed_index_hash)
        if version >= 9:
            enc_stem = (self._pak_info.stem_hash ^ keystream[8]) & 0xFFFFFFFF
            enc_unk2 = (self._pak_info.unk2 ^ keystream[9]) & 0xFFFFFFFF
            t_buf.extend(struct.pack('<II', enc_stem, enc_unk2))
        if version >= 12:
            t_buf.extend(self._pak_info.content_org_hash)
        return bytes(t_buf + base_buf)

    def _encrypt_plaintext(self, plaintext: bytes, pak_relative_path: PurePath, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1(encryption_method):
            return bytes((b ^ SIMPLE1_DECRYPT_KEY for b in plaintext))
        elif PakCrypto._is_simple2(encryption_method):
            pad_len = -len(plaintext) % SIMPLE2_BLOCK_SIZE
            plaintext += b'\x00' * pad_len
            key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
            rolling = key
            out = []
            for x, in struct.iter_unpack('<I', plaintext):
                c = rolling ^ x
                out.append(c)
                rolling ^= c
            return struct.pack(f'<{len(out)}I', *out)
        elif PakCrypto._is_sm4(encryption_method):
            key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
            sm4 = PakCrypto._sm4_ctx(key)
            pad_len = -len(plaintext) % 16
            if pad_len > 0: plaintext = plaintext + b'\x00' * pad_len
            out = bytearray()
            for i in range(0, len(plaintext), 16):
                block = plaintext[i:i + 16]
                if len(block) < 16: block = block.ljust(16, b'\x00')
                out.extend(sm4.encrypt(block))
            return bytes(out)
        return plaintext

    def _best_compress(self, chunk, cm, zstd_dict=None):
        if cm == CM_ZLIB: return zlib.compress(chunk, 9)
        if cm in (CM_ZSTD, CM_ZSTD_DICT):
            zd = zstd_dict if cm == CM_ZSTD_DICT else None
            for lvl in [22, 19, 16, 13, 10, 7, 4, 1]:
                try: return ZstdCompressor(level=lvl, dict_data=zd, threads=1).compress(chunk)
                except Exception: continue
        return chunk

    def detect_dominant_style(self) -> dict:
        """Detect dominant compression/encryption style from PAK entries"""
        comp_counter = Counter()
        enc_counter = Counter()
        blk_counter = Counter()
        enc_flag_counter = Counter()
        total = len(self._files)
        if total == 0:
            return {'comp_method': CM_ZSTD, 'enc_method': 0, 'encrypted': False, 'block_size': 0x10000}
        for entry in self._files:
            comp_counter[entry.compression_method] += 1
            if entry.encrypted:
                enc_counter[entry.encryption_method] += 1
                enc_flag_counter['encrypted'] += 1
            else:
                enc_flag_counter['plain'] += 1
            if entry.compression_block_size:
                blk_counter[entry.compression_block_size] += 1
        non_none = [(m,c) for m,c in comp_counter.items() if m != CM_NONE]
        comp_method = max(non_none, key=lambda x: x[1])[0] if non_none else CM_NONE
        encrypted = enc_flag_counter.get('encrypted', 0) > enc_flag_counter.get('plain', 0)
        enc_method = enc_counter.most_common(1)[0][0] if encrypted and enc_counter else 0
        block_size = blk_counter.most_common(1)[0][0] if blk_counter else 0x10000
        return {'comp_method': comp_method, 'enc_method': enc_method, 'encrypted': encrypted, 'block_size': block_size}

    def repack_pak_file_full(self, edited_root, output_path, target_path=None, force_add=False):
        import copy as _cp
        console.print("[bold cyan]Full PAK Rebuild mode[/bold cyan]")
        if target_path: console.print(f"[bold cyan]Target path: {target_path}[/bold cyan]")
        edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file()]
        if not edit_files:
            console.print("[bold red]No files found in COMPILED folder![/bold red]")
            return 0
        console.print(f"[bold cyan]Found {len(edit_files)} files in COMPILED folder[/bold cyan]")

        version = self._pak_info.version
        keystream = PakCrypto.zuc_keystream()
        orig_fc = self._file_content
        mp_str, all_dirs = self._get_all_dirs_and_mp()

        if target_path and force_add:
            target_path = target_path.replace('\\', '/')
            matched_dir = None
            for existing_dir in all_dirs.keys():
                if existing_dir.strip('/').lower() == target_path.strip('/').lower():
                    matched_dir = existing_dir; break
            if matched_dir: target_path = matched_dir
            else: target_path = target_path.strip('/') + '/'

        pak_name_map = {}
        for dir_path, files in self._index.items():
            for name, entry in files.items():
                full_path = str(PurePath(dir_path)/name).replace('\\', '/')
                pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

        edited = {}
        for p in edit_files:
            fl = p.name.lower()
            found_match = False
            if fl in pak_name_map:
                cands = pak_name_map[fl]
                if target_path:
                    target_candidates = [(fp, e) for fp, e in cands if target_path.strip('/') in fp]
                    if target_candidates:
                        sz = p.stat().st_size
                        sm = [(fp, e) for fp, e in target_candidates if e.uncompressed_size == sz]
                        fp, ent = sm[0] if sm else target_candidates[0]
                        edited[fp] = (p, ent)
                        found_match = True
                if not found_match:
                    sz = p.stat().st_size
                    sm = [(fp, e) for fp, e in cands if e.uncompressed_size == sz]
                    fp, ent = sm[0] if sm else cands[0]
                    if target_path:
                        new_fp = f"{target_path.rstrip('/')}/{p.name}"
                        edited[new_fp] = (p, ent)
                    else:
                        edited[fp] = (p, ent)
                    found_match = True
            if not found_match:
                stem = p.stem.lower()
                ext = p.suffix.lower()
                for dir_path, files in self._index.items():
                    for name, entry in files.items():
                        if Path(name).stem.lower() == stem and Path(name).suffix.lower() == ext:
                            full_path = str(PurePath(dir_path)/name).replace('\\', '/')
                            if target_path:
                                new_fp = f"{target_path.rstrip('/')}/{p.name}"
                                edited[new_fp] = (p, entry)
                            else:
                                edited[full_path] = (p, entry)
                            found_match = True; break
                    if found_match: break
            if not found_match and force_add and target_path:
                template_entry = None
                for dir_path, files in self._index.items():
                    for name, entry in files.items():
                        if Path(name).suffix.lower() == p.suffix.lower():
                            template_entry = entry; break
                    if template_entry: break
                if not template_entry:
                    for dir_path, files in self._index.items():
                        for name, entry in files.items():
                            template_entry = entry; break
                        if template_entry: break
                if template_entry:
                    new_fp = f"{target_path.rstrip('/')}/{p.name}"
                    edited[new_fp] = (p, template_entry)

        if not edited:
            console.print("[bold red]No files to repack![/bold red]")
            return 0
        console.print(f"  [bold bright_cyan]Files to repack: {len(edited)}[/bold bright_cyan]")

        new_files = []
        for e in self._files:
            ne = _cp.copy(e)
            ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
            new_files.append(ne)
        old_to_new = {id(self._files[i]): new_files[i] for i in range(len(self._files))}
        edited_paths = {fp: p for fp, (p, _) in edited.items()}
        out_buf = bytearray()

        for dp_str, dir_files in list(all_dirs.items()):
            for name, old_entry in list(dir_files.items()):
                full_path = str(PurePath(dp_str)/name).replace('\\', '/')
                ne = old_to_new.get(id(old_entry), None)
                if ne is None:
                    ne = _cp.copy(old_entry)
                    ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                    new_files.append(ne)
                    old_to_new[id(old_entry)] = ne
                em = old_entry.encryption_method
                cm = old_entry.compression_method
                if full_path in edited_paths:
                    p, template = edited[full_path]
                    new_raw = p.read_bytes()
                    pak_rel = PurePath(full_path)
                    ne.content_hash = SHA1.new(new_raw).digest()
                    ne.uncompressed_size = len(new_raw)
                    ne.compression_method = template.compression_method if template else cm
                    ne.encryption_method = template.encryption_method if template else em
                    ne.encrypted = template.encrypted if template else old_entry.encrypted
                    ne.unk1 = template.unk1 if template else old_entry.unk1
                    if template and target_path:
                        full_path_str = mp_str + full_path
                        ne.unk2 = SHA1.new(full_path_str.lower().encode('utf-8')).digest()
                    else:
                        ne.unk2 = template.unk2 if template else old_entry.unk2
                    ne.index_new_sep = template.index_new_sep if template else old_entry.index_new_sep
                    
                    if ne.compression_method == CM_NONE:
                        cipher = self._encrypt_plaintext(new_raw, pak_rel, ne.encryption_method) if ne.encrypted else new_raw
                        ne.offset = len(out_buf)
                        ne.size = len(new_raw)
                        ne.uncompressed_size = len(new_raw)
                        out_buf += cipher
                    else:
                        cs = (template.compression_block_size if template and template.compression_block_size > 0 
                              else old_entry.compression_block_size if old_entry.compression_block_size > 0 
                              else 65536)
                        chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                        new_blks = []
                        for chunk in chunks:
                            compressed = self._best_compress(chunk, ne.compression_method, self._zstd_dict)
                            cipher = self._encrypt_plaintext(compressed, pak_rel, ne.encryption_method) if ne.encrypted else compressed
                            blk = PakCompressedBlock(start=len(out_buf), end=len(out_buf)+len(cipher))
                            out_buf += cipher
                            new_blks.append(blk)
                        ne.compressed_blocks = new_blks
                        ne.offset = new_blks[0].start if new_blks else len(out_buf)
                        ne.size = sum(b.end - b.start for b in new_blks)
                        ne.uncompressed_size = len(new_raw)
                    console.print(f"[green]Processed: {full_path}[/green]")
                else:
                    if cm == CM_NONE:
                        read_sz = PakCrypto.align_encrypted_content_size(old_entry.size, em) if old_entry.encrypted else old_entry.size
                        ne.offset = len(out_buf)
                        out_buf += bytes(orig_fc[old_entry.offset: old_entry.offset + read_sz])
                    elif old_entry.compressed_blocks:
                        new_blks = []
                        for ob in old_entry.compressed_blocks:
                            unc = ob.end - ob.start
                            enc = PakCrypto.align_encrypted_content_size(unc, em) if old_entry.encrypted else unc
                            nb = PakCompressedBlock(start=len(out_buf), end=len(out_buf)+unc)
                            out_buf += bytes(orig_fc[ob.start: ob.start + enc])
                            new_blks.append(nb)
                        ne.compressed_blocks = new_blks
                        ne.offset = new_blks[0].start

        if target_path and force_add:
            for fp, (p, template) in edited.items():
                already_processed = False
                for dp_str, dir_files in all_dirs.items():
                    for name, entry in dir_files.items():
                        if str(PurePath(dp_str)/name).replace('\\', '/') == fp:
                            already_processed = True; break
                    if already_processed: break
                if not already_processed:
                    ne = _cp.copy(template)
                    new_raw = p.read_bytes()
                    pak_rel = PurePath(fp)
                    ne.content_hash = SHA1.new(new_raw).digest()
                    ne.uncompressed_size = len(new_raw)
                    ne.compression_method = template.compression_method
                    ne.encryption_method = template.encryption_method
                    ne.encrypted = template.encrypted
                    ne.unk1 = template.unk1
                    full_path_str = mp_str + fp
                    ne.unk2 = SHA1.new(full_path_str.lower().encode('utf-8')).digest()
                    ne.index_new_sep = template.index_new_sep
                    if ne.compression_method == CM_NONE:
                        cipher = self._encrypt_plaintext(new_raw, pak_rel, ne.encryption_method) if ne.encrypted else new_raw
                        ne.offset = len(out_buf)
                        ne.size = len(new_raw)
                        ne.uncompressed_size = len(new_raw)
                        out_buf += cipher
                    else:
                        cs = template.compression_block_size if template.compression_block_size > 0 else 65536
                        chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                        new_blks = []
                        for chunk in chunks:
                            compressed = self._best_compress(chunk, ne.compression_method, self._zstd_dict)
                            cipher = self._encrypt_plaintext(compressed, pak_rel, ne.encryption_method) if ne.encrypted else compressed
                            blk = PakCompressedBlock(start=len(out_buf), end=len(out_buf)+len(cipher))
                            out_buf += cipher
                            new_blks.append(blk)
                        ne.compressed_blocks = new_blks
                        ne.offset = new_blks[0].start if new_blks else len(out_buf)
                        ne.size = sum(b.end - b.start for b in new_blks)
                        ne.uncompressed_size = len(new_raw)
                    new_files.append(ne)
                    if target_path not in all_dirs: all_dirs[target_path] = {}
                    all_dirs[target_path][p.name] = ne
                    console.print(f"[green]Added new: {fp}[/green]")

        eidx = {id(new_files[i]): i for i in range(len(new_files))}
        idx = bytearray(self._pack_string(mp_str))
        idx += struct.pack('<I', len(new_files))
        for ne in new_files:
            idx += self._pack_entry(ne, version)
        idx += struct.pack('<Q', len(all_dirs))
        for dp_str, dir_files in all_dirs.items():
            idx += self._pack_string(dp_str)
            idx += struct.pack('<Q', len(dir_files))
            for name, old_e in dir_files.items():
                idx += self._pack_string(name)
                found_idx = None
                for i, e in enumerate(new_files):
                    if id(e) == id(old_e):
                        found_idx = i; break
                if found_idx is None:
                    for i, e in enumerate(new_files):
                        if e.offset == old_e.offset and e.size == old_e.size:
                            found_idx = i; break
                idx += struct.pack('<i', ~found_idx if found_idx is not None else -1)

        index_plain = bytes(idx)
        new_sha1 = SHA1.new(index_plain).digest()
        if self._pak_info.index_encrypted:
            key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
            aes = AES.new(key, MODE_CBC, iv[:16])
            pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
            index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
        else:
            index_bytes = index_plain

        new_idx_offset = len(out_buf)
        new_idx_size = len(index_bytes)
        out_buf += index_bytes

        footer_sz = TencentPakInfo._mem_size(version)
        new_footer = bytearray(orig_fc[-footer_sz:])
        h_key = struct.pack('<5I', *keystream[4:9])
        new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
        new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
        new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))
        out_buf += new_footer

        with open(output_path, 'wb') as f: f.write(out_buf)
        return len(edited)

    def _get_all_dirs_and_mp(self):
        raw = bytes(self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size])
        if self._pak_info.index_encrypted: raw = PakCrypto.decrypt_index(raw, self._pak_info)
        r = Reader(raw)
        mp = r.string()
        num_files = r.u4()
        for _ in range(num_files): TencentPakEntry(r, self._pak_info.version)
        dirs = {}
        for _ in range(r.u8()):
            dp = r.string()
            cnt = r.u8()
            dirs[dp] = {r.string(): self._files[~r.i4()] for _ in range(cnt)}
        return mp, dirs

    def inject_files(self, inject_plan: list, output_pak: Path, add_signature_marker: bool = True) -> None:
        """Inject new files into this PAK, producing a new PAK at output_pak."""
        if not inject_plan:
            raise ValueError('inject_plan is empty — nothing to inject')

        console.print(Panel(
            f'[bold magenta]💉 CUSTOM INJECT[/bold magenta]\n'
            f'[white]Source PAK:[/] [yellow]{self._file_path.name}[/yellow]\n'
            f'[white]Output    :[/] [cyan]{output_pak.name}[/cyan]\n'
            f'[white]Injecting :[/] [green]{len(inject_plan)} new file(s)[/green]',
            title='INJECT MODE', border_style='magenta', padding=(0, 2)
        ))

        console.print('\n[bold magenta]━━ STEP 1/5 : LOADING INJECT FILES ━━[/bold magenta]')
        work_items = []
        for i, item in enumerate(inject_plan):
            if item.get('plain_bytes') is not None:
                plain = item['plain_bytes']
            elif item.get('src_path') is not None:
                try:
                    plain = Path(item['src_path']).read_bytes()
                except Exception as e:
                    console.print(f'   [red]✗ Cannot read {item["src_path"]}: {e} — skipping[/red]')
                    continue
            else:
                console.print(f'   [red]✗ Inject item {i} has no src_path or plain_bytes — skipping[/red]')
                continue

            internal = item['internal_path'].replace('\\', '/').lstrip('/')
            if not internal:
                console.print(f'   [red]✗ Empty internal_path for item {i} — skipping[/red]')
                continue

            parts = internal.rsplit('/', 1)
            if len(parts) == 2:
                dir_str, file_name = parts[0], parts[1]
            else:
                dir_str, file_name = '', parts[0]

            work_items.append({
                'dir_str':       dir_str,
                'file_name':     file_name,
                'internal_path': internal,
                'plain':         plain,
                'comp_method':   item['comp_method'],
                'enc_method':    item['enc_method'],
                'encrypted':     bool(item['encrypted']),
                'block_size':    item['block_size'],
                'comp_level':    item.get('comp_level', 19),
            })
            console.print(f'   [blue]✨[/] {internal} [dim]({len(plain):,} bytes)[/dim]')

        if not work_items:
            raise RuntimeError('No valid inject items after loading')
        console.print(f'[green]✔ Loaded {len(work_items)} file(s)[/green]')

        console.print('\n[bold magenta]━━ STEP 2/5 : ENCODING INJECT FILES ━━[/bold magenta]')
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        header_size = TencentPakInfo._mem_size(version)
        PAK_MAGIC = self._pak_info.magic

        orig_index_offset = self._pak_info.index_offset
        current_new_offset = orig_index_offset
        new_data_region = bytearray()
        new_injected_entries = []

        # Helper function for encryption
        def _encrypt_plaintext(plaintext, pak_relative_path, encryption_method):
            if PakCrypto._is_simple1(encryption_method):
                return bytes(b ^ SIMPLE1_DECRYPT_KEY for b in plaintext)
            elif PakCrypto._is_simple2(encryption_method):
                pad = (-len(plaintext)) % SIMPLE2_BLOCK_SIZE
                plaintext += b"\x00" * pad
                key, = struct.unpack("<I", SIMPLE2_DECRYPT_KEY)
                rolling = key
                out = []
                for x, in struct.iter_unpack("<I", plaintext):
                    c = rolling ^ x
                    out.append(c)
                    rolling ^= c
                return struct.pack(f"<{len(out)}I", *out)
            elif PakCrypto._is_sm4(encryption_method):
                key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
                sm4 = PakCrypto._sm4_ctx(key)
                pad_len = (-len(plaintext)) % 16
                if pad_len > 0:
                    plaintext = plaintext + b'\x00' * pad_len
                out = bytearray()
                for i in range(0, len(plaintext), 16):
                    block = plaintext[i:i+16]
                    if len(block) < 16:
                        block = block.ljust(16, b'\x00')
                    out.extend(sm4.encrypt(block))
                return bytes(out)
            return plaintext

        for item in work_items:
            plain = item['plain']
            comp_method = item['comp_method']
            enc_method = item['enc_method']
            encrypted = item['encrypted']
            block_size_val = item['block_size']
            file_path_for_crypto = PurePath(item['file_name'])

            if len(plain) == 0:
                new_injected_entries.append({
                    'content_hash': SHA1.new(b'').digest(),
                    'offset': current_new_offset,
                    'uncompressed_size': 0, 'size': 0,
                    'comp_method': CM_NONE, 'enc_method': 0, 'encrypted': False,
                    'block_size_val': 0, 'compressed_blocks': [],
                    'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0,
                    '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(),
                    '_file_name': item['file_name'],
                })
                continue

            if comp_method == CM_NONE:
                if encrypted:
                    aligned_size = PakCrypto.align_encrypted_content_size(len(plain), enc_method)
                    padded = plain + b'\x00' * (aligned_size - len(plain))
                    stored_data = _encrypt_plaintext(padded, file_path_for_crypto, enc_method)
                else:
                    stored_data = plain
                new_size = len(stored_data)
                new_compressed_blocks = []
            else:
                chunks = [plain[i:i+block_size_val] for i in range(0, len(plain), block_size_val)]
                if not chunks: chunks = [b'']
                compressed_chunks = []
                for chunk in chunks:
                    comp = None
                    if comp_method in (CM_ZSTD, CM_ZSTD_DICT):
                        zstd_dict = self._zstd_dict if comp_method == CM_ZSTD_DICT else None
                        for lvl in range(22, 0, -1):
                            try:
                                c = ZstdCompressor(level=lvl, dict_data=zstd_dict, threads=1)
                                comp = c.compress(chunk)
                                break
                            except: continue
                    elif comp_method == CM_ZLIB:
                        comp = zlib.compress(chunk, level=9)
                    if comp is None: comp = chunk
                    compressed_chunks.append(comp)

                encrypted_chunks = []
                for comp_data in compressed_chunks:
                    if encrypted:
                        comp_data = _encrypt_plaintext(comp_data, file_path_for_crypto, enc_method)
                    encrypted_chunks.append(comp_data)

                n_blocks = len(encrypted_chunks)
                indices = PakCrypto.generate_block_indices(n_blocks, enc_method)
                physical_blocks = [None] * n_blocks
                for j, chunk_data in enumerate(encrypted_chunks):
                    physical_blocks[indices[j]] = chunk_data

                physical_offsets = []
                block_cursor = current_new_offset
                for phys_block in physical_blocks:
                    physical_offsets.append((block_cursor, block_cursor + len(phys_block)))
                    block_cursor += len(phys_block)
                new_compressed_blocks = physical_offsets
                stored_data = b''.join(physical_blocks)
                new_size = len(stored_data)
                if encrypted:
                    aligned_total = PakCrypto.align_encrypted_content_size(new_size, enc_method)
                    if aligned_total > new_size:
                        stored_data = stored_data + b'\x00' * (aligned_total - new_size)
                        new_size = aligned_total

            new_content_hash = SHA1.new(stored_data).digest()
            new_data_region.extend(stored_data)

            new_injected_entries.append({
                'content_hash': new_content_hash,
                'offset': current_new_offset,
                'uncompressed_size': len(plain),
                'size': new_size,
                'comp_method': comp_method,
                'enc_method': enc_method if encrypted else 0,
                'encrypted': encrypted,
                'block_size_val': block_size_val,
                'compressed_blocks': new_compressed_blocks,
                'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0,
                '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(),
                '_file_name': item['file_name'],
            })
            current_new_offset += new_size

        console.print(f'[green]✔ Encoded {len(new_injected_entries)} file(s)[/green]')

        # Build final entries
        new_entries = []
        entry_to_path = {}
        for dir_path, files in self._index.items():
            for fname, entry in files.items():
                entry_to_path[id(entry)] = (dir_path, fname)
        for i, entry in enumerate(self._files):
            dir_path, fname = entry_to_path.get(id(entry), (PurePath(), f'unknown_{i}'))
            new_entries.append({
                'content_hash': entry.content_hash,
                'offset': entry.offset,
                'uncompressed_size': entry.uncompressed_size,
                'size': entry.size,
                'comp_method': entry.compression_method,
                'enc_method': entry.encryption_method if entry.encrypted else 0,
                'encrypted': entry.encrypted,
                'block_size_val': entry.compression_block_size,
                'compressed_blocks': [(b.start, b.end) for b in entry.compressed_blocks],
                'unk1': entry.unk1, 'unk2': entry.unk2,
                'index_new_sep': entry.index_new_sep,
            })
        new_entries.extend(new_injected_entries)

        if add_signature_marker:
            marker_already_present = False
            for dp, files_dict in self._index.items():
                if dp.name == 'HR_DHAMA' and 'PATCHED.txt' in files_dict:
                    marker_already_present = True
                    break
            if not marker_already_present:
                # Create marker entry
                empty_hash = SHA1.new(b'').digest()
                new_entries.append({
                    'content_hash': empty_hash,
                    'offset': current_new_offset,
                    'uncompressed_size': 0,
                    'size': 0,
                    'comp_method': CM_NONE,
                    'enc_method': 0,
                    'encrypted': False,
                    'block_size_val': 0,
                    'compressed_blocks': [],
                    'unk1': 0,
                    'unk2': b'\x00' * 20,
                    'index_new_sep': 0,
                    '_dir_path': PurePath('SAMEERxPUBG'),
                    '_file_name': 'PATCHED.txt',
                })

        # Build Index
        index_data = bytearray()
        raw_orig_index = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        orig_index_decoded = PakCrypto.decrypt_index(bytes(raw_orig_index), self._pak_info)
        orig_reader = Reader(orig_index_decoded)
        orig_mount_len = orig_reader.i4()
        orig_mount_bytes = bytes(orig_reader.s(orig_mount_len))
        index_data.extend(struct.pack('<I', orig_mount_len))
        index_data.extend(orig_mount_bytes)
        index_data.extend(struct.pack('<I', len(new_entries)))

        for item in new_entries:
            index_data.extend(item['content_hash'])
            if version <= 1: index_data.extend(struct.pack('<Q', 0))
            index_data.extend(struct.pack('<Q', item['offset']))
            index_data.extend(struct.pack('<Q', item['uncompressed_size']))
            index_data.extend(struct.pack('<I', item['comp_method'] & CM_MASK))
            index_data.extend(struct.pack('<Q', item['size']))
            if version >= 5:
                index_data.extend(struct.pack('<B', item['unk1']))
                index_data.extend(item['unk2'] if item['unk2'] else b'\x00' * 20)
            if item['comp_method'] != CM_NONE and version >= 3:
                index_data.extend(struct.pack('<I', len(item['compressed_blocks'])))
                for (start, end) in item['compressed_blocks']:
                    index_data.extend(struct.pack('<Q', start))
                    index_data.extend(struct.pack('<Q', end))
            if version >= 4:
                index_data.extend(struct.pack('<I', item['block_size_val']))
                index_data.extend(struct.pack('<B', 1 if item['encrypted'] else 0))
            if version >= 12:
                index_data.extend(struct.pack('<I', item['enc_method']))
                index_data.extend(struct.pack('<I', item['index_new_sep']))

        file_to_dirname = {}
        for dir_path, files_dict in self._index.items():
            dir_str = dir_path.as_posix()
            for fname, entry in files_dict.items():
                for i, fe in enumerate(self._files):
                    if id(fe) == id(entry):
                        file_to_dirname[i] = (dir_str, fname)
                        break
        for i, item in enumerate(new_entries):
            if i not in file_to_dirname:
                if '_dir_path' in item:
                    file_to_dirname[i] = (item['_dir_path'].as_posix(), item['_file_name'])
                else:
                    file_to_dirname[i] = ('', f'file_{i}')

        all_dirs = []
        dir_to_files = {}
        for dir_path in self._index.keys():
            ds = dir_path.as_posix()
            all_dirs.append(ds)
            dir_to_files[ds] = []
        for i, item in enumerate(new_entries):
            ds, fn = file_to_dirname[i]
            if ds not in dir_to_files:
                dir_to_files[ds] = []
                all_dirs.append(ds)
            dir_to_files[ds].append((fn, i))

        index_data.extend(struct.pack('<Q', len(all_dirs)))
        for dir_str in all_dirs:
            files_list = dir_to_files[dir_str]
            if not dir_str or dir_str == '.':
                index_data.extend(struct.pack('<I', 0))
            else:
                if not dir_str.endswith('/'): dir_str_with_slash = dir_str + '/'
                else: dir_str_with_slash = dir_str
                dir_bytes = dir_str_with_slash.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(dir_bytes)))
                index_data.extend(dir_bytes)
            index_data.extend(struct.pack('<Q', len(files_list)))
            for file_name, fi in files_list:
                name_bytes = file_name.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(name_bytes)))
                index_data.extend(name_bytes)
                index_data.extend(struct.pack('<i', -fi - 1))
        index_data.extend(b'\x1d\x00\x00\x00\x2e\x2e')

        index_hash = SHA1.new(bytes(index_data)).digest()

        if version > 7 and self._pak_info.index_encrypted:
            key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            padded = pad(bytes(index_data), AES.block_size)
            aes = AES.new(key, MODE_CBC, iv[:16])
            encrypted_index = aes.encrypt(padded)
        elif self._pak_info.index_encrypted:
            encrypted_index = bytes(b ^ SIMPLE1_DECRYPT_KEY for b in bytes(index_data))
        else:
            encrypted_index = bytes(index_data)

        index_size = len(encrypted_index)
        new_index_offset = orig_index_offset + len(new_data_region)

        encrypted_magic = PAK_MAGIC ^ keystream[2]
        key_stream_hash = struct.pack('<5I', *keystream[4:][:5])
        encrypted_index_hash = bytes(a ^ b for a, b in zip(index_hash, key_stream_hash))
        encrypted_index_size = index_size ^ ((keystream[10] << 32) | keystream[11])
        encrypted_index_offset = new_index_offset ^ ((keystream[0] << 32) | keystream[1])
        encrypted_flag_byte = (1 if self._pak_info.index_encrypted else 0) ^ (keystream[3] & 0xFF)

        orig_data_region = bytearray(self._file_content[0:orig_index_offset])
        output_pak.parent.mkdir(parents=True, exist_ok=True)
        with open(output_pak, 'wb') as f:
            f.write(bytes(orig_data_region))
            f.write(bytes(new_data_region))
            f.write(encrypted_index)
            if version >= 7:
                key_unk1 = struct.pack('<8I', *keystream[7:][:8])
                unk1_plain = self._pak_info.unk1 if self._pak_info.unk1 else b'\x00' * 32
                encrypted_unk1 = bytes(a ^ b for a, b in zip(unk1_plain, key_unk1))
                f.write(encrypted_unk1)
            if version >= 8:
                f.write(self._pak_info.packed_key if self._pak_info.packed_key else b'\x00' * 256)
                f.write(self._pak_info.packed_iv if self._pak_info.packed_iv else b'\x00' * 256)
                f.write(self._pak_info.packed_index_hash if self._pak_info.packed_index_hash else b'\x00' * 256)
            if version >= 9:
                f.write(struct.pack('<I', (self._pak_info.stem_hash or 0) ^ keystream[8]))
                f.write(struct.pack('<I', (self._pak_info.unk2 or 0) ^ keystream[9]))
            if version >= 12:
                f.write(self._pak_info.content_org_hash if self._pak_info.content_org_hash else b'\x00' * 20)
            f.write(struct.pack('<B', encrypted_flag_byte))
            f.write(struct.pack('<I', encrypted_magic))
            f.write(struct.pack('<I', version))
            if version >= 6:
                f.write(encrypted_index_hash)
            else:
                f.write(b'\x00' * 20)
            f.write(struct.pack('<Q', encrypted_index_size))
            f.write(struct.pack('<Q', encrypted_index_offset))

        console.print(Panel(
            f'[bold green]🎉 INJECT COMPLETE![/bold green]\n\n'
            f'[white]Output  :[/] [cyan]{output_pak.name}[/cyan]',
            title='✅ SUCCESS', border_style='green', padding=(1, 2)
        ))

# ==============================================================================
# OPTION 5: INJECT ANY LUA - COMPLETE FUNCTIONALITY FROM c.py
# ==============================================================================

# ==============================================================================
# OPTION 5: INJECT ANY LUA - COMPLETE FUNCTIONALITY WITH PER-FILE LOCATIONS
# ==============================================================================

def handle_lua_inject():
    """Complete INJECT ANY LUA functionality with per-file location selection"""
    console.print("\n[bold #00AAFF]📦 INJECT ANY LUA (PER-FILE LOCATIONS)[/bold #00AAFF]")
    console.print("[white]Inject Lua files into PAK with custom paths per file[/white]")
    
    edit_dir = EDIT_DIR
    out_path = RESULT_DIR
    pak_dir = PAK_DIR
    
    if not edit_dir.exists():
        edit_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]⚠ Created empty folder: {edit_dir}[/yellow]")
        console.print("[yellow]Please add your LUA files there first![/yellow]")
        safe_input("\nPress Enter to continue...")
        return
    
    files_in_edit = [f for f in edit_dir.rglob("*") if f.is_file() and f.name not in ['pak_manifest.json','.DS_Store']]
    if not files_in_edit:
        console.print("[bold red]❌ COMPILED folder is empty![/bold red]")
        console.print(f"[red]📁 Please put LUA files in: {edit_dir}[/red]")
        safe_input("\nPress Enter to continue...")
        return
    
    console.print("[cyan]🔍 Searching for PAK files in PAK_ORIGINAL...[/cyan]")
    pak_files = []
    for file in pak_dir.iterdir():
        if file.name.lower().endswith('.pak'):
            pak_files.append(file)
    
    if not pak_files:
        console.print("[bold red]❌ No PAK file found in PAK_ORIGINAL folder![/bold red]")
        console.print(f"[red]📁 Please put PAK file in: {pak_dir}[/red]")
        safe_input("\nPress Enter to continue...")
        return
    
    if len(pak_files) == 1:
        pak_path = pak_files[0]
        console.print(f"[green]✅ Found PAK: {pak_path.name}[/green]")
    else:
        console.print(f"[yellow]⚠️ Multiple PAK files found:[/yellow]")
        for i, pak in enumerate(pak_files, 1):
            console.print(f"  [{i}] {pak.name}")
        console.print("\n[bold yellow]Enter number to select:[/bold yellow]")
        try:
            choice_pak = int(safe_input("> ").strip())
            if 1 <= choice_pak <= len(pak_files):
                pak_path = pak_files[choice_pak - 1]
                console.print(f"[green]✅ Selected: {pak_path.name}[/green]")
            else:
                console.print("[bold red]❌ Invalid choice![/bold red]")
                safe_input("\nPress Enter to continue...")
                return
        except:
            console.print("[bold red]❌ Invalid input![/bold red]")
            safe_input("\nPress Enter to continue...")
            return
    
    # Get all files with their relative paths
    console.print("\n[bold cyan]📂 Files found in COMPILED folder:[/bold cyan]")
    files = []
    for f in files_in_edit:
        rel_path = str(f.relative_to(edit_dir)).replace("\\", "/")
        files.append((f, rel_path))
        console.print(f"  [dim]•[/dim] {rel_path}")
    
    console.print("\n[bold yellow]Choose mode:[/bold yellow]")
    console.print("  [1] Use same target path for ALL files")
    console.print("  [2] Set custom path for EACH file individually")
    
    mode_choice = safe_input("Select mode (1 or 2): ").strip()
    
    # Dictionary to store file -> target path mapping
    file_locations = {}
    
    if mode_choice == '1':
        # Same path for all files
        console.print("\n[bold yellow]Enter Target Repacking Path (common for all files):[/bold yellow]")
        console.print("[dim](Press Enter for default: Content/Lua/)[/dim]")
        console.print("[dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]")
        target_path = safe_input("> ").strip()
        if not target_path:
            target_path = "Content/Lua/"
            console.print(f"[cyan]🎯 Using default: {target_path}[/cyan]")
        else:
            if not target_path.endswith('/'):
                target_path += '/'
            console.print(f"[cyan]🎯 Target path: {target_path}[/cyan]")
        
        # Same path for all files
        for f, rel_path in files:
            full_path = target_path + rel_path
            file_locations[str(f)] = full_path
            
    else:
        # Custom path for each file
        console.print("\n[bold cyan]Set custom path for each file:[/bold cyan]")
        console.print("[dim]Press Enter to use default: Content/Lua/ + filename[/dim]")
        console.print("[dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]\n")
        
        for idx, (f, rel_path) in enumerate(files, 1):
            console.print(f"[{idx}/{len(files)}] [bold green]{rel_path}[/bold green]")
            console.print(f"  [dim]Current file: {f.name}[/dim]")
            console.print(f"  [dim]Suggested: Content/Lua/{rel_path}[/dim]")
            
            custom_path = safe_input("  Enter path (or press Enter for default): ").strip()
            
            if not custom_path:
                # Default path: Content/Lua/ + relative path
                full_path = "Content/Lua/" + rel_path
            else:
                if not custom_path.endswith('/'):
                    custom_path += '/'
                # If user just types folder name, prepend Content/Lua/
                if not custom_path.startswith('Content/'):
                    full_path = "Content/Lua/" + custom_path + f.name
                else:
                    full_path = custom_path + f.name
            
            file_locations[str(f)] = full_path
            console.print(f"  [green]✓ Location set: {full_path}[/green]\n")
    
    # Show summary
    console.print("\n[bold cyan]📋 Summary of file locations:[/bold cyan]")
    for f, loc in file_locations.items():
        console.print(f"  [dim]•[/dim] {Path(f).name} → [yellow]{loc}[/yellow]")
    
    confirm = safe_input("\n[bold yellow]Proceed with repack? (y/n): [/bold yellow]").strip().lower()
    if confirm != 'y':
        console.print("[red]Cancelled.[/red]")
        safe_input("\nPress Enter to continue...")
        return
    
    # Backup
    BACKUP_FOLDER = PAK_DIR.parent / "BACKUP"
    BACKUP_FOLDER.mkdir(exist_ok=True)
    backup_name = f"{pak_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pak"
    backup_path = BACKUP_FOLDER / backup_name
    shutil.copy2(pak_path, backup_path)
    console.print(f"[bold green]✅ Backup created: {backup_path}[/bold green]")
    
    try:
        console.print("[cyan]📦 Loading PAK file...[/cyan]")
        pak = TencentPakFile(PurePath(pak_path))
        output_name = f"{pak_path.stem}_MODIFIED.pak"
        output_pak = out_path / output_name
        
        console.print("[cyan]🔄 Repacking PAK...[/cyan]")
        
        dominant = pak.detect_dominant_style()
        console.print(f"[cyan]Dominant style: comp={dominant['comp_method']}, enc={dominant['enc_method']}, encrypted={dominant['encrypted']}, block={dominant['block_size']}[/cyan]")
        
        inject_plan = []
        for f, rel_path in files:
            internal_path = file_locations.get(str(f), "Content/Lua/" + rel_path)
            # Ensure path doesn't start with /
            if internal_path.startswith('/'):
                internal_path = internal_path[1:]
            
            inject_plan.append({
                'src_path': f,
                'internal_path': internal_path,
                'comp_method': dominant['comp_method'],
                'enc_method': dominant['enc_method'],
                'encrypted': dominant['encrypted'],
                'block_size': dominant['block_size'],
            })
        
        console.print(f"[green]Plan: {len(inject_plan)} files with custom locations.[/green]")
        
        # Show final plan
        console.print("\n[bold cyan]📦 Final inject plan:[/bold cyan]")
        for item in inject_plan:
            console.print(f"  [dim]•[/dim] {Path(item['src_path']).name} → [yellow]{item['internal_path']}[/yellow]")
        
        pak.inject_files(inject_plan, Path(output_pak))
        console.print(f"[bold green]✅ Repack complete! Output: {output_pak}[/bold green]")
        console.print(f"[green]Processed {len(inject_plan)} files with custom locations.[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
    
    safe_input("\nPress Enter to continue...")

# ==============================================================================
# UI & MENU FUNCTIONS
# ==============================================================================

def display_file_selector(title, folder_path, file_pattern="*.pak"):
    files = list(folder_path.glob(file_pattern))
    if not files:
        hexa_alert(f"No {file_pattern} files found in {folder_path}", "error")
        return None, None
    
    table = Table(box=ROUNDED, show_header=True, expand=True, padding=(0, 1), border_style=ACCENT)
    table.add_column("#", justify="right", style=f"bold {GOLD}", width=4)
    table.add_column("File", style=f"bold {NEON}")
    table.add_column("Size", justify="right", style=MUTED)
    
    for i, f in enumerate(files, 1):
        size_mb = f.stat().st_size / (1024 * 1024)
        table.add_row(f"[{i}]", f.name, f"{size_mb:.2f} MB")
    
    console.print()
    console.print(Panel(table, title=f"[bold {ACCENT}] {title} [/bold {ACCENT}]", 
                        border_style=GOLD, box=HEAVY, padding=(1, 2)))
    
    try:
        idx = int(hexa_prompt(f"Select file (1-{len(files)})")) - 1
        if idx < 0 or idx >= len(files):
            hexa_alert("Invalid selection", "error")
            return None, None
        return files[idx], files
    except ValueError:
        hexa_alert("Please enter a valid number", "error")
        return None, None

def delete_folder(data_path: Path) -> None:
    folders = []
    for item in data_path.iterdir():
        if item.is_dir() and item.name not in ['PAK', 'UNPACK', 'REPACK', 'RESULT', 'PAK TOOL', 'SOURCE', 'LUA_ORIGINAL', 'LUA_UNPACK', 'LUA_EDIT', 'PAK_ORIGINAL', 'PAK_UNPACK', 'PAK_RESULT', 'COMPILED']:
            folders.append(item)
    
    if not folders:
        hexa_alert("No folders found to delete", "warning")
        return
    
    table = Table(box=ROUNDED, show_header=True, expand=True, padding=(0, 1), border_style=ACCENT)
    table.add_column("#", justify="right", style=f"bold {GOLD}", width=4)
    table.add_column("Folder", style=f"bold {NEON}")
    table.add_column("Size", justify="right", style=MUTED)
    
    for i, folder in enumerate(folders, 1):
        folder_size = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path): folder_size += os.path.getsize(file_path)
        table.add_row(f"[{i}]", folder.name, human_size(folder_size))
    
    console.print()
    console.print(Panel(table, title=f"[bold {ACCENT}] AVAILABLE FOLDERS [/bold {ACCENT}]", 
                        border_style=GOLD, box=HEAVY, padding=(1, 2)))
    
    try:
        choice = int(hexa_prompt(f"Select folder number (1-{len(folders)})"))
        if 1 <= choice <= len(folders):
            selected_folder = folders[choice - 1]
            confirm = hexa_prompt(f"Delete {selected_folder.name}? (yes/no)").strip().lower()
            if confirm == 'yes':
                shutil.rmtree(selected_folder)
                hexa_alert(f"Deleted: {selected_folder.name}", "success")
            else: hexa_alert("Cancelled", "warning")
        else: hexa_alert("Invalid selection", "error")
    except ValueError: hexa_alert("Invalid input", "error")

# ==============================================================================
# MAIN MENU
# ==============================================================================

def main_menu():
    # 🔐 CHECK LICENSE FIRST
    valid, license_key, key_info = check_license()
    if not valid:
        console.print("[red]License verification failed. Exiting...[/red]")
        time.sleep(2)
        return
    
    setup_directories()
    ab = AnimatedBorder.get_instance()
    
    while True:
        print_main_banner(key_info=key_info)
        
        menu_table = Table(box=ROUNDED, show_header=False, padding=(0, 2), border_style=RED)
        menu_table.add_column(justify="right", style=f"bold {GREEN}", width=4)
        menu_table.add_column(justify="left", style=f"bold {NEON}", min_width=18)
        menu_table.add_column(justify="left", style=MUTED)
        
        menu_table.add_row("1.", "UNPACK_PAK", "extract every entry from a .pak")
        menu_table.add_row("2.", "LUA_MAKE", "Decompile & Recompile .luac")
        menu_table.add_row("3.", "REPACK_LUA_PAK", "add new files a target path")
        menu_table.add_row("4.", "CLEAN_ALL", "remove a SAMEER directory")
        menu_table.add_row("5.", "INJECT LUA", "Inject Lua files Without Firewall")
        menu_table.add_row("6.", "CLOSE_TERMUX", "close the tool")
        
        border_color = ab.get_moving_border_style(2, 0.5)
        console.print(Panel(menu_table, title="[bold white]═══ MAIN MENU ═══[/bold white]", 
                            border_style=border_color, box=HEAVY, padding=(1, 2)))
        console.print()
        
        choice = hexa_prompt("Enter your choice")

        if choice == '1':
            pak_dir = PAK_DIR
            if not pak_dir.exists(): 
                hexa_alert(f"PAK folder not found at {pak_dir}", "error")
                safe_input('\nPress Enter...')
                continue
            pak_file, _ = display_file_selector("Available .pak files to UNPACK", pak_dir)
            if not pak_file: 
                safe_input('\nPress Enter...')
                continue
            try:
                hexa_section(f"Unpacking {pak_file.name}")
                pak = TencentPakFile(pak_file)
                unpack_path = PAK_UNPACK_DIR / pak_file.stem
                pak.dump(unpack_path)
                hexa_alert(f"Extracted to {unpack_path}", "success")
            except Exception as e:
                hexa_alert(f"{escape(str(e))}", "error")
            safe_input('\nPress Enter to continue...')

        elif choice == '2':
            lua_mode_menu()

        elif choice == '3':
            pak_dir = PAK_DIR
            edit_dir = EDIT_DIR
            result_dir = RESULT_DIR
            
            if not pak_dir.exists(): 
                hexa_alert(f"PAK folder not found at {pak_dir}", "error")
                safe_input('\nPress Enter...')
                continue
                
            pak_file, _ = display_file_selector("Available .pak files to REPACK TO PATH", pak_dir)
            if not pak_file: 
                safe_input('\nPress Enter...')
                continue
                
            if not edit_dir.exists() or not any(edit_dir.iterdir()):
                hexa_alert("No files in COMPILED folder. Place files to add in COMPILED first.", "error")
                safe_input('\nPress Enter...')
                continue
                
            console.print()
            console.print(Panel(f"Target path inside the PAK where files should be added.\n[{MUTED}]e.g. Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/{MUTED}]",
                                border_style=ACCENT, box=ROUNDED, padding=(0, 2)))
            
            config = load_config()
            last_path = config.get('last_repack_path', '')
            
            if last_path:
                console.print(f"[bold green]▶ Last used path: {last_path}[/bold green]")
                console.print(f"[dim]  (Press Enter to use same path)[/dim]")
            else:
                console.print(f"[dim]  (No previous path found, type a new one)[/dim]")
            
            target_path = hexa_prompt_with_default("Path", last_path)
            
            if not target_path: 
                hexa_alert("No path provided", "error")
                safe_input('\nPress Enter...')
                continue
                
            config['last_repack_path'] = target_path
            save_config(config)
            console.print(f"[dim]  ✓ Saved path for next session[/dim]")
            
            target_path = target_path.replace('\\', '/').strip('/')
            if not target_path: 
                hexa_alert("Invalid target path", "error")
                safe_input('\nPress Enter...')
                continue
                
            try:
                hexa_section(f"Adding files to {target_path} · {pak_file.name}")
                pak = TencentPakFile(pak_file)
                output_pak = result_dir / pak_file.name
                count = pak.repack_pak_file_full(edit_dir, output_pak, target_path, force_add=True)
                if count > 0:
                    hexa_alert(f"Processed {count} files to {target_path} -> {output_pak}\nPAK is game ready", "success")
                else:
                    hexa_alert("No files were processed", "error")
            except Exception as e:
                hexa_alert(f"Repack failed: {e}", "error")
                traceback.print_exc()
            safe_input('\nPress Enter to continue...')

        elif choice == '4':
            delete_folder(LUA_PAK_ROOT)
            safe_input('\nPress Enter to continue...')

        elif choice == '5':
            # INJECT ANY LUA - Complete functionality from c.py
            handle_lua_inject()

        elif choice == '6':
            console.print()
            border_color = ab.get_moving_border_style(6, 0.7)
            console.print(Panel(
                "[bold white]═══ @GRW_XD UNLIMITED LUA TOOL ═══[/bold white]\n\n"
                "[bold white]Thank you for using![/bold white]\n\n"
                "[bold green]DEVELOPER[/bold green]  :   @GRW_XD\n"
                "[bold green]OWNER[/bold green]   :   SAMEER\n",
                border_style=border_color, box=HEAVY, padding=(1, 2)))
            time.sleep(2)
            os.system('pkill -f termux 2>/dev/null')
            os._exit(0)
            break

        else:
            hexa_alert("Invalid choice", "error")
            time.sleep(2)

def lua_mode_menu():
    ab = AnimatedBorder.get_instance()
    
    while True:
        print_main_banner("LUA_MAKE")
        
        menu_table = Table(box=ROUNDED, show_header=False, padding=(0, 2), border_style=RED)
        menu_table.add_column(justify="right", style=f"bold {GREEN}", width=4)
        menu_table.add_column(justify="left", style=f"bold {NEON}", min_width=18)
        menu_table.add_column(justify="left", style=MUTED)
        
        menu_table.add_row("1.", "RECOMPILE", "LUA_EDIT → COMPILED")
        menu_table.add_row("2.", "DECOMPILE", "LUA_ORIGINAL → LUA_EDIT")
        menu_table.add_row("3.", "BACK", "return to main menu")
        
        border_color = ab.get_moving_border_style(4, 0.5)
        console.print(Panel(menu_table, title="[bold white]═══ LUA_MAKE ═══[/bold white]", 
                            border_style=border_color, box=HEAVY, padding=(1, 2)))
        console.print()
        
        choice = hexa_prompt("Select option: ").strip()
        if choice == '1':
            action_repack_unpack()
        elif choice == '2':
            action_unpack()
        elif choice == '3':
            return
        else:
            hexa_alert("Invalid option", "error")
            time.sleep(1)

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print(f"\n[bold {WARN}]Interrupted. Exiting...[/bold {WARN}]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold {ERR}]FATAL: {escape(str(e))}[/bold {ERR}]")
        traceback.print_exc()
        safe_input('\nPress Enter to exit...')
        sys.exit(1)
# ═══════════════════════════════════════════════════════════════════════════════
# 🔐 LICENSE VERIFICATION SYSTEM - COMPLETE FIX
# ═══════════════════════════════════════════════════════════════════════════════

try:
    import requests
except ImportError:
    print("⚠️ requests module not found! Installing...")
    os.system("pip install requests")
    import requests

# ── CONFIGURATION ──
SERVER_URL = 'https://Sameerfga.pythonanywhere.com'
LICENSE_SERVER = SERVER_URL

CONFIG_DIR = Path("/storage/emulated/0/Documents/GRW_LUA_TOOL")
CONFIG_FILE = CONFIG_DIR / "license_config.json"
DEVICE_ID_FILE = CONFIG_DIR / ".device_id"

# ── Rich UI imports (EARLY) ──────────────────────────────────────────────────

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.markup import escape
    from rich.text import Text
    from rich.box import ROUNDED, HEAVY, DOUBLE
    from rich import box
    from rich.align import Align
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.live import Live
    from rich.console import Group
    RICH_AVAILABLE = True
except ImportError:
    print("⚠️ rich module not found! Installing...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.markup import escape
    from rich.text import Text
    from rich.box import ROUNDED, HEAVY, DOUBLE
    from rich import box
    from rich.align import Align
    from rich.layout import Layout
    from rich.columns import Columns
    from rich.live import Live
    from rich.console import Group
    RICH_AVAILABLE = True

console = Console()

# ── Themes ──────────────────────────────────────────────────────────────────

NEON = "bright_white"
NEON_DIM = "white"
ERR = "red"
WARN = "yellow"
ACCENT = "cyan"
MUTED = "dim white"
SUCCESS = "green"
GOLD = "gold1"
PURPLE = "magenta"
RED = "red"
GREEN = "green"
BLUE = "blue"

# ── ANIMATED BORDER ENGINE (EARLY) ──────────────────────────────────────────

class AnimatedBorder:
    _instance = None
    
    def __init__(self):
        self._start_time = time.time()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_rainbow_color(self, offset=0, speed=1.0):
        hue = (time.time() * speed + offset) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def get_moving_border_style(self, position=0, speed=0.8):
        offset = (position / 8.0) + (time.time() * speed * 0.1)
        return self.get_rainbow_color(offset % 1.0, speed)

def safe_input(prompt: str='') -> str:
    try:
        return input(prompt)
    except (EOFError, RuntimeError):
        try:
            if sys.platform != 'win32':
                with open('/dev/tty', 'r') as tty:
                    sys.stderr.write(prompt); sys.stderr.flush()
                    return tty.readline().rstrip('\n')
            else:
                with open('CON', 'r') as con:
                    sys.stderr.write(prompt); sys.stderr.flush()
                    return con.readline().rstrip('\r\n')
        except Exception:
            return ''
    except Exception:
        return ''

# ── STABLE DEVICE ID ──────────────────────────────────────────────────────

def get_stable_device_id():
    """
    Generate a STABLE unique device ID that persists across runs.
    This is the KEY FIX - device ID will NEVER change.
    """
    
    # ── METHOD 1: Use stored ID file (PERSISTENT) ──
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if DEVICE_ID_FILE.exists():
            stored_id = DEVICE_ID_FILE.read_text().strip()
            if stored_id and len(stored_id) == 64:
                console.print(f"[dim]✓ Using stored device ID[/dim]")
                return stored_id
    except:
        pass
    
    # ── METHOD 2: Android ANDROID_ID ──
    try:
        result = subprocess.run(
            ['settings', 'get', 'secure', 'android_id'],
            capture_output=True, text=True, timeout=2
        )
        android_id = result.stdout.strip()
        if android_id and android_id != 'null' and len(android_id) > 5:
            device_id = hashlib.sha256(f"android_{android_id}".encode()).hexdigest()
            try:
                DEVICE_ID_FILE.write_text(device_id)
            except:
                pass
            return device_id
    except:
        pass
    
    # ── METHOD 3: Build fingerprint ──
    try:
        with open('/system/build.prop', 'r') as f:
            for line in f:
                if 'ro.build.fingerprint' in line:
                    fingerprint = line.strip().split('=', 1)[1]
                    if fingerprint:
                        device_id = hashlib.sha256(f"fp_{fingerprint}".encode()).hexdigest()
                        try:
                            DEVICE_ID_FILE.write_text(device_id)
                        except:
                            pass
                        return device_id
    except:
        pass
    
    # ── METHOD 4: Hardware Serial ──
    try:
        result = subprocess.run(['getprop', 'ro.serialno'], capture_output=True, text=True, timeout=2)
        serial = result.stdout.strip()
        if serial and serial != 'unknown' and len(serial) > 3:
            device_id = hashlib.sha256(f"serial_{serial}".encode()).hexdigest()
            try:
                DEVICE_ID_FILE.write_text(device_id)
            except:
                pass
            return device_id
    except:
        pass
    
    # ── METHOD 5: Generate NEW persistent ID ──
    try:
        # Use multiple stable factors
        factors = [
            platform.node(),
            platform.machine(),
            platform.system(),
            str(uuid.getnode()),
            socket.gethostname()
        ]
        raw = ''.join(str(x) for x in factors).encode('utf-8')
        device_id = hashlib.sha256(raw).hexdigest()
        
        # Save permanently
        try:
            DEVICE_ID_FILE.write_text(device_id)
        except:
            pass
        return device_id
    except:
        pass
    
    # ── FINAL FALLBACK ──
    device_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
    try:
        DEVICE_ID_FILE.write_text(device_id)
    except:
        pass
    return device_id

# ── LICENSE FUNCTIONS ──────────────────────────────────────────────────────

def get_device_id():
    """Alias for stable device ID - maintains compatibility"""
    return get_stable_device_id()

def verify_key(key, device_id):
    try:
        resp = requests.get(
            f'{LICENSE_SERVER}/verify',
            params={'key': key, 'device_id': device_id},
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
        return {'status': 'error', 'message': 'Server error'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def save_license(key, expiry):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        device_id = get_stable_device_id()  # Stable ID
        data = {
            'key': key,
            'expiry': expiry,
            'device_id': device_id,
            'saved_at': datetime.now().isoformat()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        console.print(f"[dim]✓ License saved to {CONFIG_FILE}[/dim]")
        return True
    except Exception as e:
        console.print(f"[dim]⚠️ Could not save license: {e}[/dim]")
        return False

def load_saved_license():
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def delete_saved_license():
    try:
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        if DEVICE_ID_FILE.exists():
            DEVICE_ID_FILE.unlink()
        return True
    except:
        return False

# ── GLOBAL KEY_INFO FOR THREAD SAFETY ─────────────────────────────────────

_key_info_lock = threading.Lock()
_global_key_info = {
    'key': 'N/A',
    'expiry': 'N/A',
    'max_devices': 1,
    'current_devices': 0,
    'remaining_seconds': -1
}

def update_key_info(data):
    """Thread-safe update of global key_info"""
    global _global_key_info
    with _key_info_lock:
        _global_key_info.update(data)

def get_key_info():
    """Thread-safe read of global key_info"""
    global _global_key_info
    with _key_info_lock:
        return _global_key_info.copy()

def start_background_verification(key, device_id):
    def verify_loop():
        while True:
            time.sleep(10)
            try:
                resp = requests.get(
                    f'{LICENSE_SERVER}/verify',
                    params={'key': key, 'device_id': device_id},
                    timeout=10
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('status') != 'valid':
                        console.print("\n" + "="*50)
                        console.print(f"⚠️ LICENSE {data.get('status', 'INVALID').upper()}!")
                        console.print(f"Reason: {data.get('message', 'Unknown')}")
                        console.print("Tool will exit in 10 seconds...")
                        console.print("="*50)
                        time.sleep(10)
                        os._exit(1)
                    else:
                        update_key_info({
                            'remaining_seconds': data.get('remaining_seconds', -1),
                            'current_devices': data.get('current_devices', 0),
                            'expiry': data.get('expiry', 'N/A')
                        })
            except Exception:
                pass
    threading.Thread(target=verify_loop, daemon=True).start()

def check_license():
    """Main license check - AUTO-LOGIN with saved license"""
    global _global_key_info
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 80
    
    BOX_WIDTH = 75
    padding = max(0, (term_width - BOX_WIDTH) // 2)
    pad = " " * padding
    
    ab = AnimatedBorder.get_instance()
    
    top_line = "╔" + "═" * (BOX_WIDTH - 2) + "╗"
    sep_line = "╠" + "═" * (BOX_WIDTH - 2) + "╣"
    sep2_line = "╟" + "─" * (BOX_WIDTH - 2) + "╢"
    bot_line = "╚" + "═" * (BOX_WIDTH - 2) + "╝"
    
    c1 = ab.get_moving_border_style(0, 0.6)
    c2 = ab.get_moving_border_style(4, 0.6)
    c3 = ab.get_moving_border_style(8, 0.6)
    
    def make_center_line(text):
        content_len = len(text)
        total_pad = BOX_WIDTH - 2 - content_len
        left_pad = total_pad // 2
        right_pad = total_pad - left_pad
        return "║" + " " * left_pad + text + " " * right_pad + "║"
    
    title_text = "@GRW_XD UNLIMITED LUA TOOL"
    
    console.print(pad + f"[{c1}]{top_line}[/{c1}]")
    console.print(pad + make_center_line(title_text), style=f"bold {GREEN}")
    console.print(pad + f"[{c2}]{sep_line}[/{c2}]")
    console.print(pad + make_center_line("DEVELOPER  : SAMEER"), style=f"bold {GREEN}")
    console.print(pad + make_center_line("OWNER     : @GRW_XD"), style=f"bold {GREEN}")
    console.print(pad + f"[{c3}]{sep2_line}[/{c3}]")
    console.print(pad + make_center_line("LICENSE VERIFICATION"), style=f"bold {ACCENT}")
    console.print(pad + f"[{c3}]{bot_line}[/{c3}]")
    console.print()
    
    # ── Get STABLE device ID ──
    device_id = get_stable_device_id()
    console.print(f"[dim]  Device ID: {device_id[:16]}...[/dim]")
    console.print()
    
    saved = load_saved_license()
    
    # ── CHECK SAVED LICENSE ──
    if saved:
        console.print(pad + make_center_line("Found saved license, checking..."))
        
        # Check if device_id matches
        saved_device_id = saved.get('device_id', '')
        if saved_device_id != device_id:
            console.print(pad + make_center_line("⚠️ Device mismatch - re-verifying..."), style=f"bold {WARN}")
            # BUT don't delete - maybe server has correct info
        else:
            console.print(pad + make_center_line("Device ID matches"), style=f"bold {SUCCESS}")
        
        # Try to verify with server
        try:
            result = verify_key(saved['key'], device_id)
            if result.get('status') == 'valid':
                console.print(pad + make_center_line(f"✅ License Valid!"), style=f"bold {SUCCESS}")
                console.print(pad + make_center_line(f"Expiry: {result.get('expiry', 'N/A')}"))
                console.print(pad + make_center_line(f"Devices: {result.get('current_devices', 0)}/{result.get('max_devices', 1)}"))
                console.print()
                
                # Update global key_info
                with _key_info_lock:
                    _global_key_info.update({
                        'key': saved['key'],
                        'expiry': result.get('expiry', 'N/A'),
                        'max_devices': result.get('max_devices', 1),
                        'current_devices': result.get('current_devices', 0),
                        'remaining_seconds': result.get('remaining_seconds', -1)
                    })
                
                # Save updated expiry
                save_license(saved['key'], result.get('expiry', 'N/A'))
                
                start_background_verification(saved['key'], device_id)
                console.print(pad + f"[{c3}]{bot_line}[/{c3}]")
                console.print()
                return True, saved['key'], get_key_info()
            else:
                console.print(pad + make_center_line(f"✗ Saved license invalid"), style=f"bold {ERR}")
                console.print(pad + make_center_line(f"Reason: {result.get('message', 'Unknown')}"))
                delete_saved_license()
                console.print()
        except Exception as e:
            # Network error - use cached license if device matches
            if saved_device_id == device_id:
                console.print(pad + make_center_line(f"⚠️ Server unreachable, using cached license"), style=f"bold {WARN}")
                console.print(pad + make_center_line(f"✅ License Valid (Cached)"), style=f"bold {SUCCESS}")
                console.print(pad + make_center_line(f"Expiry: {saved.get('expiry', 'N/A')}"))
                console.print()
                
                with _key_info_lock:
                    _global_key_info.update({
                        'key': saved['key'],
                        'expiry': saved.get('expiry', 'N/A'),
                        'max_devices': 1,
                        'current_devices': 1,
                        'remaining_seconds': -1
                    })
                
                start_background_verification(saved['key'], device_id)
                console.print(pad + f"[{c3}]{bot_line}[/{c3}]")
                console.print()
                return True, saved['key'], get_key_info()
            else:
                console.print(pad + make_center_line(f"⚠️ Device mismatch, re-enter key"), style=f"bold {WARN}")
                delete_saved_license()
                console.print()
    
    # ── ASK FOR KEY ──
    while True:
        console.print(pad + make_center_line("Enter your license key:"), style=f"bold {ACCENT}")
        try:
            key = safe_input(pad + "       ╚══════> ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            console.print(pad + make_center_line("✗ Input cancelled."), style=f"bold {ERR}")
            sys.exit(1)
            
        if not key:
            console.print(pad + make_center_line("✗ Key cannot be empty!"), style=f"bold {ERR}")
            continue
        
        console.print(pad + make_center_line("Verifying..."))
        result = verify_key(key, device_id)
        
        if result.get('status') == 'valid':
            console.print(pad + f"[{c3}]{sep2_line}[/{c3}]")
            console.print(pad + make_center_line(f"✅ License Valid!"), style=f"bold {SUCCESS}")
            console.print(pad + make_center_line(f"Expiry: {result.get('expiry', 'N/A')}"))
            console.print(pad + make_center_line(f"Devices: {result.get('current_devices', 0)}/{result.get('max_devices', 1)}"))
            
            save_license(key, result.get('expiry', 'N/A'))
            
            with _key_info_lock:
                _global_key_info.update({
                    'key': key,
                    'expiry': result.get('expiry', 'N/A'),
                    'max_devices': result.get('max_devices', 1),
                    'current_devices': result.get('current_devices', 0),
                    'remaining_seconds': result.get('remaining_seconds', -1)
                })
            
            start_background_verification(key, device_id)
            console.print(pad + f"[{c3}]{bot_line}[/{c3}]")
            console.print()
            return True, key, get_key_info()
        else:
            console.print(pad + f"[{c3}]{sep2_line}[/{c3}]")
            console.print(pad + make_center_line(f"✗ Verification failed"), style=f"bold {ERR}")
            console.print(pad + make_center_line("Please check your key and try again."))
            console.print()

# ═══════════════════════════════════════════════════════════════════════════════
# END OF LICENSE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

# ── Python version compatibility ──────────────────────────────────────────

if not hasattr(it, 'batched'):
    def batched(iterable, n):
        it_iter = iter(iterable)
        while True:
            chunk = list(it.islice(it_iter, n))
            if not chunk:
                break
            yield chunk
    it.batched = batched

# ── Optional PAK dependencies ─────────────────────────────────────────────

PAK_MODE_AVAILABLE = True
try:
    import gmalg
    try:
        from gmalg.base import BlockCipher
        from gmalg.errors import IncorrectLengthError
        from gmalg.utils import ROL32
    except ImportError:
        class BlockCipher: pass
        class IncorrectLengthError(Exception):
            def __init__(self, name, expected, actual):
                super().__init__(f"Incorrect length for {name}: expected {expected}, got {actual}")
        def ROL32(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))
except ImportError:
    PAK_MODE_AVAILABLE = False
    class BlockCipher: pass
    class IncorrectLengthError(Exception):
        def __init__(self, name, expected, actual):
            super().__init__(f"Incorrect length for {name}: expected {expected}, got {actual}")
    def ROL32(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    PAK_MODE_AVAILABLE = False

try:
    from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict, DICT_TYPE_AUTO
except ImportError:
    PAK_MODE_AVAILABLE = False

# ==============================================================================
# HEXA CORE UI - PROFESSIONAL
# ==============================================================================

def get_rainbow_color(offset=0, speed=1.0):
    return AnimatedBorder.get_instance().get_rainbow_color(offset, speed)

def get_border_style(position=0, speed=0.8):
    return AnimatedBorder.get_instance().get_moving_border_style(position, speed)

def hexa_alert(message: str, kind: str = "info") -> None:
    tags = {
        "success": ("✓", SUCCESS),
        "error": ("✗", ERR),
        "warning": ("⚠", WARN),
        "info": ("▶", ACCENT),
    }
    tag, color = tags.get(kind, tags["info"])
    console.print(f"  {tag}  {message}", style=color)

def hexa_section(title: str) -> None:
    console.print()
    console.print(f"  ═══ {title} ═══", style=f"bold {ACCENT}")
    console.print(f"  {'─' * (len(title) + 8)}", style=MUTED)

def hexa_prompt(label: str) -> str:
    console.print(f"  {label}", style=f"bold {NEON}")
    return safe_input("  └─> ").strip()

def format_time(seconds: int) -> str:
    """Convert seconds to human readable time format"""
    if seconds < 0:
        return "Unlimited"
    if seconds == 0:
        return "Expired"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    else:
        return f"{minutes}m {secs}s"

def print_main_banner(title="", key_info=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        term_width = shutil.get_terminal_size().columns
    except:
        term_width = 80
    
    BOX_WIDTH = 60
    padding = max(0, (term_width - BOX_WIDTH) // 2)
    pad = " " * padding
    
    ab = AnimatedBorder.get_instance()
    
    top_line = "╔" + "═" * (BOX_WIDTH - 2) + "╗"
    sep_line = "╠" + "═" * (BOX_WIDTH - 2) + "╣"
    sep2_line = "╟" + "─" * (BOX_WIDTH - 2) + "╢"
    bot_line = "╚" + "═" * (BOX_WIDTH - 2) + "╝"
    
    c1 = ab.get_moving_border_style(0, 0.6)
    c2 = ab.get_moving_border_style(4, 0.6)
    c3 = ab.get_moving_border_style(8, 0.6)
    
    def make_center_line(text):
        content_len = len(text)
        total_pad = BOX_WIDTH - 2 - content_len
        left_pad = total_pad // 2
        right_pad = total_pad - left_pad
        return "║" + " " * left_pad + text + " " * right_pad + "║"
    
    title_text = "@GRW_XD UNLIMITED LUA TOOL"
    
    console.print(pad + f"[{c1}]{top_line}[/{c1}]")
    console.print(pad + make_center_line(title_text), style=f"bold {GREEN}")
    console.print(pad + f"[{c2}]{sep_line}[/{c2}]")
    console.print(pad + make_center_line("REAL DEVELOPER @GRW_XD"), style=f"bold {GREEN}")
    
    if key_info:
        console.print(pad + f"[{c3}]{sep2_line}[/{c3}]")
        console.print(pad + make_center_line(f"LICENSE KEY : {key_info.get('key', 'N/A')}"), style=f"bold {ACCENT}")
        
        expiry = key_info.get('expiry', 'N/A')
        if expiry == 'lifetime':
            console.print(pad + make_center_line("EXPIRY   : LIFETIME"), style=f"bold {GREEN}")
            console.print(pad + make_center_line("TIME    : UNLIMITED"), style=f"bold {GREEN}")
        else:
            console.print(pad + make_center_line(f"EXPIRY      : {expiry}"), style=NEON)
            
            rem = key_info.get('remaining_seconds', -1)
            if rem is not None and rem >= 0:
                time_str = format_time(rem)
                if rem < 3600:
                    color = RED
                elif rem < 86400:
                    color = WARN
                else:
                    color = SUCCESS
                console.print(pad + make_center_line(f"TIME LEFT   : {time_str}"), style=f"bold {color}")
            else:
                console.print(pad + make_center_line("TIME LEFT   : N/A"), style=MUTED)
        
        devices = key_info.get('current_devices', 0)
        max_dev = key_info.get('max_devices', 1)
        console.print(pad + make_center_line(f"DEVICES     : {devices} / {max_dev}"), style=NEON)
    
    console.print(pad + f"[{c3}]{bot_line}[/{c3}]")
    console.print()
    
    if title:
        console.print(f"  {title}", style=f"bold {ACCENT}")
        console.print(f"  {'─' * len(title)}", style=MUTED)

def human_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.2f} {unit}'
        size /= 1024.0
    return f'{size:.2f} PB'

# ==============================================================================
# SHARED DIRECTORY CONFIGURATION
# ==============================================================================

def get_lua_pak_root() -> Path:
    docs_path = Path("/storage/emulated/0/Documents/GRW_LUA_TOOL")
    if not docs_path.exists():
        docs_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[{SUCCESS}]✓ Created GRW_LUA_TOOL folder at {docs_path}[/{SUCCESS}]")
    return docs_path

LUA_PAK_ROOT = get_lua_pak_root()
SOURCE_DIR = LUA_PAK_ROOT / "SOURCE"
REAL_DIR   = LUA_PAK_ROOT / "LUA_ORIGINAL"
UNPACK_DIR = LUA_PAK_ROOT / "LUA_EDIT"
EDIT_DIR   = LUA_PAK_ROOT / "COMPILED"
PAK_DIR    = LUA_PAK_ROOT / "PAK_ORIGINAL"
PAK_UNPACK_DIR = LUA_PAK_ROOT / "PAK_UNPACK"
RESULT_DIR = LUA_PAK_ROOT / "PAK_RESULT"
CONFIG_FILE_PATH = LUA_PAK_ROOT / "config.json"

FORCE_COMPILE = True
SKIP_ALL_FIXES = True
SKIP_AUTO_FIX = True

def load_config():
    config = {}
    if CONFIG_FILE_PATH.exists():
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                config = json.load(f)
        except Exception:
            pass
    return config

def save_config(config):
    try:
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass

def hexa_prompt_with_default(label: str, default: str = "") -> str:
    console.print(f"  {label}", style=f"bold {NEON}")
    if default:
        console.print(f"  └─> [bold green]{default}[/bold green]", style=f"bold")
        console.print(f"  [dim](Press Enter to use default, or type new path)[/dim]")
        result = safe_input("  └─> ").strip()
        return result if result else default
    else:
        return safe_input("  └─> ").strip()

def setup_directories():
    for d in [REAL_DIR, UNPACK_DIR, EDIT_DIR, PAK_DIR, PAK_UNPACK_DIR, RESULT_DIR, SOURCE_DIR]:
        try: d.mkdir(parents=True, exist_ok=True)
        except OSError as e: console.print(f"Error creating {d}: {e}")

def get_real_files():   
    return [f for f in os.listdir(REAL_DIR) if f.lower().endswith((".lua",".luac",".slua"))] if REAL_DIR.exists() else []

def get_unpack_files(): 
    return [f for f in os.listdir(UNPACK_DIR) if f.endswith(".lua")] if UNPACK_DIR.exists() else []

# ==============================================================================
# TOOLCHAIN — LUA CORE (FULL)
# ==============================================================================

def _load_xor_key() -> bytes:
    env_key = os.environ.get('BGMI_XOR_KEY')
    if env_key:
        try:
            key_bytes = bytes.fromhex(env_key.replace(' ', '').replace(':', '').replace('-', ''))
            if len(key_bytes) == 32: return key_bytes
        except ValueError: pass
    return bytes([0x11, 0x21, 0x36, 0x47, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0x35, 0x26, 0x1A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x15, 0x07, 0xD0, 0x2C, 0x1E, 0x8F, 0xF6, 0xC8])

STRING_XOR_KEY = _load_xor_key()

_BGMI_TO_STD = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,0,1,2,3,4,5,6,7,8,9,10,11,12,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]
BGMI_TO_STD = _BGMI_TO_STD + [i for i in range(len(_BGMI_TO_STD), 64)]
STD_TO_BGMI = {v: k for k, v in enumerate(BGMI_TO_STD) if k < len(BGMI_TO_STD)}
STD_FMT = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,2,0,2,0,1,0,3]
iABC, iABx, iAsBx, iAx = 0, 1, 2, 3
HEADER_SIZE = 33

class BinaryReader:
    def __init__(self, data: bytes, sizet: int = 4):
        self.data = bytearray(data); self.pos = 0; self.sizet = sizet
    def byte(self) -> int:
        if self.pos >= len(self.data): raise EOFError()
        v = self.data[self.pos]; self.pos += 1; return v
    def int32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<i', self.data, self.pos)[0]; self.pos += 4; return v
    def uint32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<I', self.data, self.pos)[0]; self.pos += 4; return v
    def double(self) -> float:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<d', self.data, self.pos)[0]; self.pos += 8; return v
    def int64(self) -> int:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<q', self.data, self.pos)[0]; self.pos += 8; return v
    def bytes(self, n: int) -> bytes:
        if self.pos + n > len(self.data): raise EOFError()
        v = self.data[self.pos:self.pos+n]; self.pos += n; return bytes(v)
    def pubg_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        enc = self.bytes(sz)
        dec = bytes(enc[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(enc)))
        try: return dec.decode('utf-8', errors='replace')
        except Exception: return dec.decode('latin-1')
    def std_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF:
            if self.sizet == 8:
                if self.pos + 8 > len(self.data): raise EOFError()
                sz = struct.unpack_from('<Q', self.data, self.pos)[0]; self.pos += 8
            else: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        raw = self.bytes(sz)
        try: return raw.decode('utf-8', errors='replace')
        except Exception: return raw.decode('latin-1')

class BinaryWriter:
    def __init__(self): self.buf = bytearray()
    def byte(self, v): self.buf.append(v & 0xFF)
    def int32(self, v): self.buf.extend(struct.pack('<i', v))
    def uint32(self, v): self.buf.extend(struct.pack('<I', v))
    def int64(self, v): self.buf.extend(struct.pack('<q', v))
    def double(self, v): self.buf.extend(struct.pack('<d', v))
    def raw(self, data): self.buf.extend(data)
    def lua_string(self, s: Optional[str], is_pubg: bool = False):
        if s is None: self.byte(0); return
        e = s.encode('utf-8') if isinstance(s, str) else s
        sz = len(e) + 1
        if sz < 0xFF: self.byte(sz)
        else: self.byte(0xFF); self.uint32(sz)
        if is_pubg:
            enc = bytes(e[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(e)))
            self.raw(enc)
        else: self.raw(e)
    def lua_inst(self, op, A, B, C, Bx, sBx, Ax, fmt):
        op &= 0x3F
        if   fmt == iABC:  r = op | ((A & 0xFF)<<6) | ((C & 0x1FF)<<14) | ((B & 0x1FF)<<23)
        elif fmt == iABx:  r = op | ((A & 0xFF)<<6) | ((Bx & 0x3FFFF)<<14)
        elif fmt == iAsBx: r = op | ((A & 0xFF)<<6) | (((sBx+131071) & 0x3FFFF)<<14)
        elif fmt == iAx:   r = op | ((Ax & 0x3FFFFFF)<<6)
        else: r = 0
        self.uint32(r)
    def get_data(self) -> bytes: return bytes(self.buf)

def _convert_function(reader: BinaryReader, writer: BinaryWriter, to_std: bool = True):
    src = reader.pubg_string() if to_std else reader.std_string()
    writer.lua_string(src, is_pubg=(not to_std))
    linedefined = reader.int32(); writer.int32(linedefined)
    writer.int32(reader.int32())
    writer.byte(reader.byte()); writer.byte(reader.byte()); writer.byte(reader.byte())
    csz = reader.uint32(); writer.uint32(csz)
    opmap = BGMI_TO_STD if to_std else STD_TO_BGMI
    for _ in range(csz):
        raw = reader.uint32()
        bop = raw & 0x3F; A = (raw >> 6) & 0xFF; B = (raw >> 23) & 0x1FF; C = (raw >> 14) & 0x1FF
        Bx = (raw >> 14) & 0x3FFFF; sBx = Bx - 131071; Ax = (raw >> 6) & 0x3FFFFFF
        sop = opmap[bop] if bop < len(opmap) else bop
        fmt = STD_FMT[sop] if sop < len(STD_FMT) else iABC
        writer.lua_inst(sop, A, B, C, Bx, sBx, Ax, fmt)
    nk = reader.uint32(); writer.uint32(nk)
    for _ in range(nk):
        t = reader.byte(); writer.byte(t)
        if t == 0: pass
        elif t == 1: writer.byte(reader.byte())
        elif t == 3: writer.double(reader.double())
        elif t == 19: writer.int64(reader.int64())
        elif t in (4, 20):
            s = reader.pubg_string() if to_std else reader.std_string()
            writer.lua_string(s, is_pubg=(not to_std))
        else: raise ValueError(f"Unknown constant type 0x{t:02X}")
    nups = reader.uint32(); writer.uint32(nups)
    for _ in range(nups): writer.byte(reader.byte()); writer.byte(reader.byte())
    npts = reader.uint32(); writer.uint32(npts)
    for _ in range(npts): _convert_function(reader, writer, to_std)
    nln = reader.uint32()
    if to_std:
        lines = []; cur = linedefined
        for _ in range(nln):
            d = reader.byte()
            cur += d if d <= 127 else d - 256
            lines.append(cur)
        writer.uint32(len(lines))
        for ln in lines: writer.int32(ln)
        nab = reader.uint32()
        for _ in range(nab): reader.uint32(); reader.uint32()
    else:
        lines = [reader.int32() for _ in range(nln)]
        writer.uint32(len(lines))
        prev = linedefined
        for ln in lines:
            delta = ln - prev
            if -128 <= delta <= 127: writer.byte(delta & 0xFF)
            else: writer.byte(0x00); writer.int32(delta)
            prev = ln
        writer.uint32(0)
    nloc = reader.uint32(); writer.uint32(nloc)
    for _ in range(nloc):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))
        writer.int32(reader.int32()); writer.int32(reader.int32())
    nupn = reader.uint32(); writer.uint32(nupn)
    for _ in range(nupn):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))

def bgmi_to_std(data: bytes) -> bytes:
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    reader = BinaryReader(data, sizet=4); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=True)
    return writer.get_data()

def std_to_bgmi(data: bytes) -> bytes:
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    sizet = data[13] if data[13] in (4, 8) else 4
    reader = BinaryReader(data, sizet=sizet); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=False)
    return writer.get_data()

def convert_file(inp: str, outp: str = None) -> Tuple[bool, str]:
    if not outp: outp = os.path.splitext(inp)[0] + '.std.luac'
    try:
        with open(inp, 'rb') as f: data = f.read()
    except Exception as e: return False, f"Cannot read input file: {e}"
    if len(data) < 34 or data[:4] != b'\x1bLua':
        try: shutil.copy2(inp, outp); return True, outp
        except: return False, "Failed to copy non-Lua file"
    nibble_flag = data[33]
    if nibble_flag > 2: nibble_flag = 0; data = bytearray(data); data[33] = 0; data = bytes(data)
    if nibble_flag > 1:
        fixed = bytearray(data[:34])
        for i in range(34, len(data)):
            b = data[i]; fixed.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
        data = bytes(fixed)
    try:
        std_data = bgmi_to_std(data)
        with open(outp, 'wb') as f: f.write(std_data)
        return True, outp
    except Exception:
        try: shutil.copy2(inp, outp); return True, outp
        except: return False, "Conversion failed"

def repack_to_pubg(std_luac_path: str, original_pubg_path: str, outp: str = None, pad_to_size: int = None) -> Tuple[bool, str]:
    if not outp: outp = os.path.splitext(std_luac_path)[0] + '.pubg.luac'
    try:
        with open(original_pubg_path, 'rb') as f: orig_data = f.read()
    except Exception as e: return False, f"Cannot read original: {e}"
    if len(orig_data) < 34 or orig_data[:4] != b'\x1bLua': return False, "Original not valid Lua bytecode"
    header = orig_data[:33]; nibble_flag = orig_data[33]
    if nibble_flag > 2: nibble_flag = 0
    try:
        with open(std_luac_path, 'rb') as f: std_data = f.read()
    except Exception as e: return False, f"Cannot read std luac: {e}"
    try:
        bgmi_data = std_to_bgmi(std_data)
        bgmi_data = header + bytes([nibble_flag]) + bgmi_data[34:]
        if nibble_flag > 1:
            data_list = bytearray(bgmi_data[:34])
            for i in range(34, len(bgmi_data)):
                b = bgmi_data[i]; data_list.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
            bgmi_data = bytes(data_list)
        if pad_to_size is not None and len(bgmi_data) < pad_to_size:
            bgmi_data += b'\x00' * (pad_to_size - len(bgmi_data))
        with open(outp, 'wb') as f: f.write(bgmi_data)
        return True, outp
    except Exception as e: return False, f"Repack failed: {e}"

UNLUAC_JAR_PATH = SOURCE_DIR / "unluac_patched.jar"
UNLUAC_JAR = str(UNLUAC_JAR_PATH)
JAVA_CMD = "java"
BUNDLED_JDK_CANDIDATES = list(SOURCE_DIR.glob("jdk*/bin/java.exe")) + list(SOURCE_DIR.glob("jdk*/bin/java"))
if BUNDLED_JDK_CANDIDATES: JAVA_CMD = str(BUNDLED_JDK_CANDIDATES[0])

def get_luac_cmd() -> str:
    for name in ["luac5.3", "luac53", "luac5.3.exe", "luac53.exe"]:
        p = SOURCE_DIR / name
        if p.exists(): return str(p)
    for name in ["luac5.3", "luac53.exe"]:
        w = shutil.which(name)
        if w: return w
    return "luac5.3"

LUAC_PATH = get_luac_cmd()
STRIP_DEBUG = True

def decrypt_decompile_file(file_path: str, output_dir: str, progress_callback=None) -> bool:
    try:
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        if base_name.lower().endswith('.lua'): base_name = os.path.splitext(base_name)[0]
        output_file = os.path.join(output_dir, base_name + ".lua")
        temp_std = file_path + ".temp.std.luac"
        if progress_callback: progress_callback(f"Converting {filename}...")
        success, msg = convert_file(file_path, temp_std)
        if not success:
            if progress_callback: progress_callback(f"Conversion failed: {msg}")
            shutil.copy2(file_path, os.path.join(output_dir, base_name + ".luac"))
            return False
        if not os.path.exists(UNLUAC_JAR):
            if progress_callback: progress_callback("unluac.jar missing, saving raw bytecode")
            shutil.copy2(temp_std, os.path.join(output_dir, base_name + ".luac"))
            os.remove(temp_std); return False
        try:
            cmd = [JAVA_CMD, "-jar", UNLUAC_JAR, temp_std]
            with open(output_file, "w", encoding="utf-8") as out:
                subprocess.check_call(cmd, stdout=out, stderr=subprocess.PIPE, timeout=30)
            if progress_callback: progress_callback(f"Decompiled {filename}")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            if progress_callback: progress_callback(f"Decompilation failed: {e}")
            shutil.copy2(temp_std, os.path.join(output_dir, base_name + ".luac"))
            return False
        finally:
            if os.path.exists(temp_std): os.remove(temp_std)
        return True
    except Exception as e:
        if progress_callback: progress_callback(f"Exception: {e}")
        return False

def robust_decompile(encrypted_path: str, output_dir: str, tmp_dir: str) -> Tuple[bool, str, List[str]]:
    name = os.path.basename(encrypted_path); base = os.path.splitext(name)[0]
    out_path = os.path.join(output_dir, base + ".lua")
    temp_std = os.path.join(tmp_dir, base + ".std.luac")
    ok, msg = convert_file(encrypted_path, temp_std)
    if not ok: return False, msg, []
    if not os.path.exists(UNLUAC_JAR): return False, "unluac_patched.jar not found", []
    try:
        cmd = [JAVA_CMD, "-jar", UNLUAC_JAR, temp_std]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout:
            with open(out_path, 'w', encoding='utf-8') as f: f.write(result.stdout)
            return True, out_path, []
        else: return False, f"Decompilation failed: {(result.stderr or 'unknown error').strip()[:200]}", []
    except subprocess.TimeoutExpired: return False, "Decompilation timed out", []
    except Exception as e: return False, str(e), []

def select_files_interactive(files: List[str], source_dir: str, action_name: str) -> List[str]:
    if not files: return []
    if len(files) == 1:
        console.print(f"Only 1 file found: {files[0]}")
        confirm = hexa_prompt("Process this file? (Y/n): ").strip().lower()
        return files if confirm != 'n' else []
    console.print(f"\nSelect files to {action_name}:")
    for idx, f in enumerate(files, 1):
        sz = os.path.getsize(os.path.join(source_dir, f))
        console.print(f"  [{idx}] {f} ({sz:,} bytes)")
    console.print("  [A] ALL FILES")
    console.print("  [0] Cancel")
    while True:
        choice = hexa_prompt("Your choice: ").strip().upper()
        if choice == 'A': return files
        if choice == '0': return []
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(files): return [files[idx-1]]
        console.print("Invalid selection!")

def action_unpack():
    files = get_real_files()
    if not files: hexa_alert("LUA_ORIGINAL folder is empty!", "error"); safe_input('\nPress Enter...'); return
    selected = select_files_interactive(files, str(REAL_DIR), "UNPACK")
    if not selected: return
    success = 0
    with tempfile.TemporaryDirectory(prefix='bgmi_dec_') as tmp_dir:
        for idx, f in enumerate(selected, 1):
            console.print(f"[{idx}/{len(selected)}] {f}")
            inp = REAL_DIR / f
            ok, result, _ = robust_decompile(str(inp), str(UNPACK_DIR), tmp_dir)
            if ok:
                console.print(f"Decompiled: {os.path.basename(result)}"); success += 1
            else:
                console.print(f"Failed: {result}")
                fallback_path = UNPACK_DIR / (os.path.splitext(f)[0] + ".luac")
                ok2, _ = convert_file(str(inp), str(fallback_path))
                if ok2: console.print(f"Saved raw bytecode as {fallback_path}")
    hexa_alert(f"Unpack Complete! {success}/{len(selected)} files decompiled.", "success")
    safe_input('\nPress Enter...')

def recompile_lua_files(selected: List[str], quiet: bool = False) -> Tuple[int, List[str]]:
    success = 0; failed = []
    for idx, f in enumerate(selected, 1):
        name = os.path.splitext(f)[0]
        inp = UNPACK_DIR / f
        out = EDIT_DIR / (name + ".lua")
        console.print(f"[{idx}/{len(selected)}] {f}")
        
        if FORCE_COMPILE:
            console.print(f"[bold yellow]FORCE COMPILE GRW POWER FULL TOOL[/bold yellow]")
        
        temp_std = str(LUA_PAK_ROOT / f"{name}_temp_std.luac")
        cmd = [LUAC_PATH, "-s", "-o", temp_std, str(inp)] if STRIP_DEBUG else [LUAC_PATH, "-o", temp_std, str(inp)]
        try: 
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            console.print("Compilation timed out")
            failed.append(f)
            continue
        
        if res.returncode == 0 and os.path.exists(temp_std):
            orig = None
            for ext in ['.luac', '.slua', '.lua']:
                p = REAL_DIR / (name + ext)
                if p.exists():
                    orig = str(p)
                    break
            if not orig:
                console.print("Original file not found in LUA_ORIGINAL")
                failed.append(f)
            else:
                ok2, msg = repack_to_pubg(temp_std, orig, str(out), pad_to_size=os.path.getsize(orig))
                if ok2:
                    console.print(f"Recompiled: {out.name} ({out.stat().st_size:,} bytes)")
                    success += 1
                else:
                    console.print(f"Recompile failed: {msg}")
                    failed.append(f)
            if os.path.exists(temp_std):
                os.remove(temp_std)
        else:
            console.print(f"Compilation failed: {res.stderr.strip() if res.stderr else 'Unknown error'}")
            failed.append(f)
    return success, failed

def action_repack_unpack():
    files = get_unpack_files()
    if not files: hexa_alert("LUA_EDIT folder is empty!", "error"); safe_input('\nPress Enter...'); return
    selected = select_files_interactive(files, str(UNPACK_DIR), "REPACK")
    if not selected: return
    
    if FORCE_COMPILE and SKIP_ALL_FIXES:
        console.print("[bold cyan] 🚀 FAST COMPILE MODE — Raw Build Execution[/bold cyan]")
        console.print("[bold cyan]Launching high-speed compilation...[/bold cyan]")
    
    success, failed = recompile_lua_files(selected)
    hexa_alert(f"Repack Complete! {success}/{len(selected)} successful.", "success")
    if failed: hexa_alert(f"Failed files: {', '.join(failed)}", "error")
    safe_input('\nPress Enter...')

# ==============================================================================
# TOOLCHAIN — PAK CORE (COMPLETE)
# ==============================================================================

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')
SIMPLE1_DECRYPT_KEY = 0x79
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16
SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = ['xG2qW5lP7lV2iN5fN5pG','xT1cJ6dL5wC0kK1rB4dK','qC4jS5bZ6fL5xE6nD4zA','gD4jQ2aL3bS3lC3xT0iW','xU1yQ8wE9zY3gZ3bT5aE','uQ3cO2dX7xY4xU7gH7iS','gW1fR0jK6wQ4oN0oK1kZ','aJ4pV7iZ7pU4wP2aC2cZ','cX6jT3cM2oT3vK0kJ1qN','iT2vS0cS6yT6cZ1sE1lO','hM1pH9iY8wM9hT4lN5uJ','kG6bC8jK0fL0dE4sH4mL','dB6lB3vE0eZ8wM8rI0aC','tP7sP7nI9rA2vQ4cV5yQ','aT0cL1yN4pT3sZ7eM2vY','uV6fU8fC9zN3mP5dH8mN']
EM_SIMPLE1 = 1; EM_SIMPLE2 = 16; EM_UNKNOWN_17 = 17; EM_SM4_2 = 2; EM_SM4_4 = 4; EM_SM4_NEW_BASE = 31; EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
CM_NONE = 0; CM_ZLIB = 1; CM_ZSTD = 6; CM_ZSTD_DICT = 8; CM_MASK = 15

class SM4:
    _S_BOX = bytes([0x34,0x66,0x25,0x74,0x89,0x78,0xE4,0xA9,0x5A,0x41,0xBC,0x7A,0xD6,0x16,0x21,0x23,0x4D,0x61,0xDA,0x94,0x9B,0xDF,0x13,0x3C,0x69,0x3A,0x31,0x0A,0x5F,0xD7,0x99,0x95,0xF1,0xAE,0x72,0x3D,0x07,0x60,0x24,0xB6,0x98,0xEE,0xC4,0xA2,0x2D,0x88,0xDD,0x8D,0x04,0xEA,0xBB,0x11,0xCA,0x3E,0x5D,0xA1,0xF6,0x3F,0xB0,0x97,0x80,0x47,0x2B,0xA6,0xE6,0xF7,0xD9,0xB1,0x59,0xC0,0x7C,0xBE,0x54,0x28,0xB7,0x7E,0x4F,0xF8,0x43,0x6E,0xA0,0x50,0x0E,0xF5,0x90,0xB8,0xFB,0xA3,0x7B,0x62,0x19,0x46,0x03,0x2A,0xB9,0x8F,0x9F,0x77,0xB4,0x5B,0x83,0x87,0x08,0xEB,0xE2,0x1E,0x42,0xF0,0x0F,0xE8,0x71,0x6A,0x75,0xAD,0x55,0x1F,0xB5,0xAB,0x33,0xFA,0x7F,0x15,0xBD,0x85,0xD8,0x06,0x68,0xB3,0x52,0x30,0x48,0x0B,0x00,0xED,0xEF,0xB2,0x57,0x8E,0xE7,0x6C,0xD5,0xE5,0x2E,0x53,0x82,0x05,0xF9,0x81,0xF4,0x56,0xBF,0x8C,0x4B,0xE3,0xDB,0x4A,0x91,0x4C,0x2C,0xD3,0x40,0x29,0x4E,0x20,0x14,0x36,0x79,0x09,0x6F,0xD1,0x37,0xE0,0x39,0x0C,0x8A,0x92,0x38,0x12,0x35,0x6D,0xE1,0xFD,0x93,0x9A,0x17,0xD4,0xC9,0x9C,0x6B,0x84,0x26,0x9D,0xAF,0x76,0xC1,0x9E,0xD0,0x96,0xC5,0xCB,0xE9,0x73,0x49,0xD2,0xCD,0x64,0xC3,0xC7,0x01,0x7D,0xF3,0xAC,0xFC,0xDE,0xA4,0x44,0x32,0x1B,0xC2,0xBA,0x1C,0x02,0xC6,0x27,0x45,0x8B,0xF2,0x18,0xA7,0x10,0x51,0x1D,0xC8,0xCF,0x63,0xFF,0x2F,0x0D,0x58,0xCE,0x65,0xA5,0xDC,0x1A,0x3B,0x86,0xFE,0x22,0x5C,0xA8,0x5E,0x67,0xAA,0xEC,0x70,0xCC])
    _FK = [0x46970E9C,0x4BC0685E,0x59056186,0xBCA2491E]
    _CK = [0x000EB92B,0x3A0AE783,0x9E3B5C67,0xADDBDABF,0x7B7484CB,0x49156C63,0xC79AB5E7,0x79EC9CFF,0x1725BEAB,0x2FB89CA3,0x24808AD7,0xDDD28B1F,0x4740DA4B,0xBBC3EA73,0x247B30E7,0x91BE385F,0x0401248B,0x45FCD3A3,0x530B4CE7,0xC68DD35F,0xE3D16C2B,0x4F698C13,0x6B92C747,0x769EFB1F,0x4C73BE9B,0xC942B193,0xAD80D827,0x372FB33F,0x13CB6AAB,0x2BDC0AA3,0x17A4A247,0xD5E96CAF]
    @staticmethod
    def ROL32(x, n): return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))
    @staticmethod
    def _BS(X): return ((SM4._S_BOX[(X>>24)&0xff]<<24)|(SM4._S_BOX[(X>>16)&0xff]<<16)|(SM4._S_BOX[(X>>8)&0xff]<<8)|SM4._S_BOX[X&0xff])
    @staticmethod
    def _T0(X): X = SM4._BS(X); return X ^ SM4.ROL32(X,2) ^ SM4.ROL32(X,10) ^ SM4.ROL32(X,18) ^ SM4.ROL32(X,24)
    @staticmethod
    def _T1(X): X = SM4._BS(X); return X ^ SM4.ROL32(X,13) ^ SM4.ROL32(X,23)
    @classmethod
    def key_length(cls): return 16
    @classmethod
    def block_length(cls): return 16
    def __init__(self, key: bytes):
        if len(key) != 16: raise IncorrectLengthError("Key","16 bytes",f"{len(key)} bytes")
        self._key = key; self._rkey = [0]*32
        K0 = int.from_bytes(key[0:4],'big') ^ self._FK[0]; K1 = int.from_bytes(key[4:8],'big') ^ self._FK[1]
        K2 = int.from_bytes(key[8:12],'big') ^ self._FK[2]; K3 = int.from_bytes(key[12:16],'big') ^ self._FK[3]
        for i in range(0,32,4):
            K0 = K0 ^ self._T1(K1^K2^K3^self._CK[i]); self._rkey[i] = K0
            K1 = K1 ^ self._T1(K2^K3^K0^self._CK[i+1]); self._rkey[i+1] = K1
            K2 = K2 ^ self._T1(K3^K0^K1^self._CK[i+2]); self._rkey[i+2] = K2
            K3 = K3 ^ self._T1(K0^K1^K2^self._CK[i+3]); self._rkey[i+3] = K3
        self._block_buffer = bytearray()
    def encrypt(self, block: bytes) -> bytes:
        if len(block) != 16: raise IncorrectLengthError("Block","16 bytes",f"{len(block)} bytes")
        RK = self._rkey; X0 = int.from_bytes(block[0:4],'big'); X1 = int.from_bytes(block[4:8],'big')
        X2 = int.from_bytes(block[8:12],'big'); X3 = int.from_bytes(block[12:16],'big')
        for i in range(0,32,4):
            X0 = X0 ^ self._T0(X1^X2^X3^RK[i]); X1 = X1 ^ self._T0(X2^X3^X0^RK[i+1])
            X2 = X2 ^ self._T0(X3^X0^X1^RK[i+2]); X3 = X3 ^ self._T0(X0^X1^X2^RK[i+3])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4,'big')); buf.extend(X2.to_bytes(4,'big'))
        buf.extend(X1.to_bytes(4,'big')); buf.extend(X0.to_bytes(4,'big'))
        return bytes(buf)
    def decrypt(self, block: bytes) -> bytes:
        if len(block) != 16: raise IncorrectLengthError("Block","16 bytes",f"{len(block)} bytes")
        RK = self._rkey; X0 = int.from_bytes(block[0:4],'big'); X1 = int.from_bytes(block[4:8],'big')
        X2 = int.from_bytes(block[8:12],'big'); X3 = int.from_bytes(block[12:16],'big')
        for i in range(0,32,4):
            X0 = X0 ^ self._T0(X1^X2^X3^RK[31-i]); X1 = X1 ^ self._T0(X2^X3^X0^RK[30-i])
            X2 = X2 ^ self._T0(X3^X0^X1^RK[29-i]); X3 = X3 ^ self._T0(X0^X1^X2^RK[28-i])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4,'big')); buf.extend(X2.to_bytes(4,'big'))
        buf.extend(X1.to_bytes(4,'big')); buf.extend(X0.to_bytes(4,'big'))
        return bytes(buf)

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        padding = n - (len(data) % n)
        return data if padding == n else data + b'\x00' * padding
    @staticmethod
    def align_up(x: int, n: int) -> int: return ((x + n - 1) // n) * n

class Reader:
    def __init__(self, buffer, cursor=0): self._buffer = buffer; self._cursor = cursor
    def u1(self, move_cursor=True): return self.unpack('B', move_cursor=move_cursor)[0]
    def u4(self, move_cursor=True): return self.unpack('<I', move_cursor=move_cursor)[0]
    def u8(self, move_cursor=True): return self.unpack('<Q', move_cursor=move_cursor)[0]
    def i1(self, move_cursor=True): return self.unpack('b', move_cursor=move_cursor)[0]
    def i4(self, move_cursor=True): return self.unpack('<i', move_cursor=move_cursor)[0]
    def i8(self, move_cursor=True): return self.unpack('<q', move_cursor=move_cursor)[0]
    def s(self, n: int, move_cursor=True): return self.unpack(f'{n}s', move_cursor=move_cursor)[0]
    def unpack(self, f, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor: self._cursor += struct.calcsize(f)
        return x
    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0: return str()
        offset = 0 if move_cursor else 4
        return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()

class PakInfo:
    def __init__(self, buffer, keystream: list):
        def dec_enc(x): return (x ^ keystream[3]) & 0xFF
        def dec_magic(x): return x ^ keystream[2]
        def dec_ihash(x): key = struct.pack('<5I', *keystream[4:][:5]); return bytes(a^b for a,b in zip(x,key))
        def dec_isz(x): return x ^ ((keystream[10]<<32)|keystream[11])
        def dec_ioff(x): return x ^ ((keystream[0]<<32)|keystream[1])
        reader = Reader(buffer[-PakInfo._mem_size(-1):])
        self.index_encrypted = dec_enc(reader.u1()) == 1
        self.magic = dec_magic(reader.u4())
        self.version = reader.u4()
        self.index_hash = dec_ihash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size = dec_isz(reader.u8())
        self.index_offset = dec_ioff(reader.u8())
        if self.version <= 3: self.index_encrypted = False
    @staticmethod
    def _mem_size(_): return 1+4+4+20+8+8

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: list):
        def dec_unk(x): key = struct.pack('<8I', *keystream[7:][:8]); return bytes(a^b for a,b in zip(x,key))
        def dec_stem(x): return x ^ keystream[8]
        def dec_uhash(x): return x ^ keystream[9]
        super().__init__(buffer, keystream)
        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1 = dec_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash = dec_stem(reader.u4()) if self.version >= 9 else 0
        self.unk2 = dec_uhash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash = reader.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(version):
        return PakInfo._mem_size(version) + (32 if version>=7 else 0) + (768 if version>=8 else 0) + (8 if version>=9 else 0) + (20 if version>=12 else 0)

class PakCompressedBlock:
    def __init__(self, reader: Reader = None, start: int = 0, end: int = 0):
        if reader is not None: self.start = reader.u8(); self.end = reader.u8()
        else: self.start = start; self.end = end

class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash = reader.s(20)
        if version <= 1: _ = reader.u8()
        self.offset = reader.u8()
        self.uncompressed_size = reader.u8()
        self.compression_method = reader.u4() & CM_MASK
        self.size = reader.u8()
        self.unk1 = reader.u1() if version >= 5 else 0
        self.unk2 = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks = [PakCompressedBlock(reader) for _ in range(reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size = reader.u4() if version >= 4 else 0
        self.encrypted = reader.u1() == 1 if version >= 4 else False
        self.encryption_method = reader.u4() if version >= 12 else 0
        self.index_new_sep = reader.u4() if version >= 12 else 0

class PakCrypto:
    class _LCG:
        def __init__(self, seed): self.state = seed
        def next(self):
            MASK_32 = 0xFFFFFFFF; MSB_1 = 1<<31
            def wrap(x):
                x &= MASK_32
                return x if not x&MSB_1 else ((x+MSB_1)&MASK_32)-MSB_1
            x1 = wrap(0x41C64E6D * self.state); self.state = wrap(x1+12345)
            x2 = wrap(x1+0x13038) if self.state < 0 else self.state
            return ((x2>>16) & MASK_32) % 0x7FFF

    @staticmethod
    def zuc_keystream() -> list:
        if not PAK_MODE_AVAILABLE or not hasattr(gmalg, 'ZUC'): return [0]*16
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]

    @staticmethod
    def _xorxor(buffer, x) -> bytes: return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))
    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        if not PAK_MODE_AVAILABLE: return b'\x00'*n
        block = SHA1.new(buffer).digest()
        result = block * math.ceil(n / SHA1.digest_size)
        return result[:n] if len(result) >= n else result + b'\x00' * (n - len(result))

    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]
        if len(buffer) < 43: return bytes()
        x1 = buffer[1:][:SHA1.digest_size]; x2 = buffer[SHA1.digest_size+1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = x2[:SHA1.digest_size], x2[SHA1.digest_size:]
        if part1 != SHA1.new(b'\x00'*SHA1.digest_size).digest(): return bytes()
        return unpad(m)

    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature,'little'); n = int.from_bytes(modulus,'little')
        m = pow(c, 0x10001, n).to_bytes(256,'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))

    @staticmethod
    def _encrypt_simple1(pt) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in pt)
    @staticmethod
    def _decrypt_simple1(ct) -> bytes: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ct)

    @staticmethod
    def _encrypt_simple2(pt) -> bytes:
        class RK:
            def __init__(self, v): self._v = v
            def update(self, x): ov = self._v; self._v = x; return ov ^ x
        assert len(pt) % SIMPLE2_BLOCK_SIZE == 0
        iv, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rk = RK(iv)
        return bytes(it.chain.from_iterable(struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(pt)//4}I', pt)))

    @staticmethod
    def _decrypt_simple2(ct) -> bytes:
        class RK:
            def __init__(self, v): self._v = v
            def update(self, x): self._v ^= x; return self._v
        assert len(ct) % SIMPLE2_BLOCK_SIZE == 0
        iv, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rk = RK(iv)
        return bytes(it.chain.from_iterable(struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(ct)//4}I', ct)))

    @staticmethod
    @lru_cache(maxsize=33)
    def _derive_sm4_key(file_path: PurePath, em: int) -> bytes:
        part1 = file_path.stem.lower()
        if em == EM_SM4_2: secret = SM4_SECRET_2
        elif em == EM_SM4_4: secret = SM4_SECRET_4
        else: secret = f'{SM4_SECRET_NEW[(em-EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)]}{em}'
        return SHA1.new(str(part1+secret).encode()).digest()[:SM4.key_length()]

    @staticmethod
    @lru_cache(maxsize=33)
    def _sm4_ctx(key: bytes) -> SM4: return SM4(key)

    @staticmethod
    def _encrypt_sm4(pt, fp: PurePath, em: int) -> bytes:
        padded = pad(pt, SM4.block_length())
        sm4 = PakCrypto._sm4_ctx(PakCrypto._derive_sm4_key(fp, em))
        return bytes(it.chain.from_iterable(sm4.encrypt(bytes(x)) for x in it.batched(padded, SM4.block_length())))

    @staticmethod
    def _decrypt_sm4(ct, fp: PurePath, em: int) -> bytes:
        assert len(ct) % SM4.block_length() == 0
        sm4 = PakCrypto._sm4_ctx(PakCrypto._derive_sm4_key(fp, em))
        return bytes(it.chain.from_iterable(sm4.decrypt(bytes(x)) for x in it.batched(ct, SM4.block_length())))

    @staticmethod
    def decrypt_index(ct, pak_info: TencentPakInfo) -> bytes:
        if pak_info.version > 7:
            key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            aes = AES.new(key, MODE_CBC, iv[:16])
            return unpad(aes.decrypt(ct), AES.block_size)
        return bytes(PakCrypto._decrypt_simple1(ct))

    @staticmethod
    def _is_simple1(em): return em == EM_SIMPLE1
    @staticmethod
    def _is_simple2(em): return em == EM_SIMPLE2 or em == 17
    @staticmethod
    def _is_sm4(em): return em in (EM_SM4_2, EM_SM4_4) or em & EM_SM4_NEW_MASK != 0

    @staticmethod
    def align_encrypted_content_size(n: int, em: int) -> int:
        if PakCrypto._is_simple2(em): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        if PakCrypto._is_sm4(em): return Misc.align_up(n, SM4.block_length())
        return n

    @staticmethod
    def encrypt_block(pt, file: PurePath, em: int) -> bytes:
        if PakCrypto._is_simple1(em): return PakCrypto._encrypt_simple1(pt)
        if PakCrypto._is_simple2(em): return PakCrypto._encrypt_simple2(pad(pt, SIMPLE2_BLOCK_SIZE))
        if PakCrypto._is_sm4(em): return PakCrypto._encrypt_sm4(pt, file, em)
        assert False, f"Unknown encryption method: {em}"

    @staticmethod
    def decrypt_block(ct, file: PurePath, em: int) -> bytes:
        if PakCrypto._is_simple1(em): return PakCrypto._decrypt_simple1(ct)
        if PakCrypto._is_simple2(em): return PakCrypto._decrypt_simple2(ct)
        if PakCrypto._is_sm4(em): return PakCrypto._decrypt_sm4(ct, file, em)
        assert False, f"Unknown encryption method: {em}"

    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, em: int) -> list:
        if not PakCrypto._is_sm4(em): return list(range(n))
        perm = list(range(n))
        rng = random.Random(n)
        rng.shuffle(perm)
        inv = [0]*n
        for i, x in enumerate(perm): inv[x] = i
        return inv

class PakCompression:
    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_dec(dict_data):
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdDecompressor(dict_obj)

    @staticmethod
    @lru_cache(maxsize=128)
    def _zstd_enc(dict_data, level):
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdCompressor(level=level, dict_data=dict_obj, write_checksum=False, write_content_size=False, write_dict_id=False)

    @staticmethod
    def decompress_block(block, dict_data, cm: int) -> bytes:
        if cm == CM_ZLIB:
            try: return zlib.decompress(block)
            except: return block
        elif cm in (CM_ZSTD, CM_ZSTD_DICT):
            dd = dict_data if cm == CM_ZSTD_DICT else None
            try: return PakCompression._zstd_dec(dd).decompress(block)
            except: return block
        assert False, f"Unknown decompression method: {cm}"

    @staticmethod
    def compress_block(block, dict_data, cm: int, level=None) -> bytes:
        if cm == CM_ZLIB:
            return zlib.compress(block, level=level if level is not None else 9)
        elif cm in (CM_ZSTD, CM_ZSTD_DICT):
            dd = dict_data if cm == CM_ZSTD_DICT else None
            return PakCompression._zstd_enc(dd, level if level is not None else 22).compress(block)
        assert False, f"Unknown compression method: {cm}"

class TencentPakFile:
    def __init__(self, file_path: PurePath, is_od=False):
        self._file_path = file_path
        with open(file_path, 'rb') as f: self._file_content = memoryview(f.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files: list = []
        self._index: dict = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._verify_stem_hash()
        self._tencent_load_index()
        self._path_to_entry = None

    def _verify_stem_hash(self):
        if not self._is_od and self._pak_info.version >= 9:
            assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))

    def _tencent_load_index(self):
        index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        if self._pak_info.index_encrypted: index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
        self._verify_index_hash(index_data)
        self._load_index(index_data)

    def _verify_index_hash(self, index_data):
        expected = self._pak_info.index_hash
        if not self._is_od and self._pak_info.version >= 8:
            assert expected == PakCrypto.rsa_extract(self._pak_info.packed_index_hash, RSA_MOD_2)
        assert expected == SHA1.new(index_data).digest()

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        result = PurePath()
        for part in PurePath(mount_point).parts:
            if part != '..': result /= part
        return result

    def _peek_content(self, offset, size, em):
        size = PakCrypto.align_encrypted_content_size(size, em)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, em):
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, em)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry):
        assert not self._zstd_dict and not dict_entry.encrypted and dict_entry.compression_method == CM_NONE
        console.print("[bold cyan]► LOADING ZSTD DICTIONARY...[/bold cyan]")
        reader = Reader(self._peek_content(dict_entry.offset, dict_entry.size, 0))
        dict_size = reader.u8(); _ = reader.u4(); real_size = reader.u4()
        assert dict_size == real_size
        self._zstd_dict = reader.s(dict_size)
        console.print("[bold green]► DICTIONARY LOADED SUCCESSFULLY![/bold green]")
        time.sleep(2)

    def _load_index(self, index_data):
        if self._pak_info.version <= 10:
            console.print("[bold yellow]Warning: Pak version is too old, may not be fully supported[/bold yellow]")
        reader = Reader(index_data)
        self._original_mount_point = reader.string()
        self._mount_point = self._construct_mount_point(self._original_mount_point)
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(reader.u4())]
        self._dir_path_strings = {}
        try:
            num_dirs = reader.u8()
            for _ in range(num_dirs):
                dir_str = reader.string()
                dir_path = PurePath(dir_str); num_files = reader.u8()
                self._dir_path_strings[dir_path] = dir_str
                e = {reader.string(): self._files[~reader.i4()] for _ in range(num_files)}
                if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                    assert len(e) == 1
                    self._construct_zstd_dict(list(e.values())[0])
                    self._zstddic_info = (dir_str, e)
                    continue
                self._index.update({PurePath(dir_path): e})
        except struct.error:
            console.print("[dim]Note: Finished reading index (older pak format).[/dim]")
        self._path_to_entry = None

    def _build_path_map(self) -> Dict[str, TencentPakEntry]:
        if self._path_to_entry is None:
            self._path_to_entry = {}
            for dir_path, dir_content in self._index.items():
                for fname, entry in dir_content.items():
                    full_path = self._mount_point / dir_path / fname
                    full = str(full_path).replace('\\', '/')
                    self._path_to_entry[full] = entry
        return self._path_to_entry

    def _get_method_str(self, m, is_enc):
        if is_enc:
            if PakCrypto._is_simple1(m): return "SIMPLE1"
            if PakCrypto._is_simple2(m): return "SIMPLE2"
            if PakCrypto._is_sm4(m): return f"SM4 (Type {m})"
            return "NONE" if m == 0 else "UNKNOWN"
        else:
            return {CM_NONE:"NONE",CM_ZLIB:"ZLIB",CM_ZSTD:"ZSTD",CM_ZSTD_DICT:"ZSTD_DICT"}.get(m,"UNKNOWN")

    def _write_to_disk(self, file_path: PurePath, entry: TencentPakEntry):
        em = entry.encryption_method; cm = entry.compression_method
        enc_str = self._get_method_str(em,True); comp_str = self._get_method_str(cm,False)
        console.print(f"[bold cyan]->[/bold cyan] Unpack: [bold green]{file_path.name}[/bold green] [[bold yellow]{comp_str}[/bold yellow]/[bold magenta]{enc_str}[/bold magenta]]")
        with open(file_path, 'wb') as f:
            if cm == CM_NONE:
                data = self._peek_content(entry.offset, entry.size, em)
                if entry.encrypted: data = PakCrypto.decrypt_block(bytes(data), file_path, em)
                f.write(data[:entry.size]); return
            buf = bytearray()
            for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), em):
                data = self._peek_block_content(entry.compressed_blocks[x], em)
                if entry.encrypted: data = PakCrypto.decrypt_block(bytes(data), file_path, em)
                if not data: continue
                data = data[:entry.compressed_blocks[x].end - entry.compressed_blocks[x].start]
                buf.extend(PakCompression.decompress_block(bytes(data), self._zstd_dict, cm))
            f.write(bytes(buf)[:entry.uncompressed_size])

    def dump(self, out_path: PurePath):
        dest_dir = Path(out_path)
        dest_dir.mkdir(parents=True, exist_ok=True)
        total_files = sum(len(d) for d in self._index.values())
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan][UNPACK][/] {task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Extracting files...", total=total_files)
            for dir_path, dir_content in self._index.items():
                current_out_path = dest_dir / dir_path
                current_out_path.mkdir(parents=True, exist_ok=True)
                for file_name, entry in dir_content.items():
                    self._write_to_disk(current_out_path / file_name, entry)
                    progress.update(task, advance=1)

    def dump_lua_only(self, out_path: PurePath):
        dest_dir = Path(out_path)
        dest_dir.mkdir(parents=True, exist_ok=True)
        for dir_path, dir_content in self._index.items():
            for file_name, entry in dir_content.items():
                if file_name.lower().endswith(('.lua', '.luac', '.slua')):
                    self._write_to_disk(dest_dir / file_name, entry)

    def _pack_string(self, s: str) -> bytes:
        if not s: return struct.pack('<i', 0)
        encoded = s.encode('utf-8') + b'\x00'
        return struct.pack('<i', len(encoded)) + encoded

    def _pack_entry(self, entry, version: int) -> bytes:
        buf = bytearray()
        buf.extend(struct.pack('<20s', entry.content_hash))
        if version <= 1: buf.append(0)
        buf.extend(struct.pack('<Q', entry.offset))
        buf.extend(struct.pack('<Q', entry.uncompressed_size))
        buf.extend(struct.pack('<I', entry.compression_method))
        buf.extend(struct.pack('<Q', entry.size))
        if version >= 5:
            buf.append(entry.unk1)
            buf.extend(struct.pack('<20s', entry.unk2))
        if entry.compression_method != 0 and version >= 3:
            buf.extend(struct.pack('<I', len(entry.compressed_blocks)))
            for block in entry.compressed_blocks:
                buf.extend(struct.pack('<QQ', block.start, block.end))
        if version >= 4:
            buf.extend(struct.pack('<I', entry.compression_block_size))
            buf.append(1 if entry.encrypted else 0)
        if version >= 12:
            buf.extend(struct.pack('<I', entry.encryption_method))
            buf.extend(struct.pack('<I', entry.index_new_sep))
        return bytes(buf)

    def _pack_index(self) -> bytes:
        buf = bytearray()
        mount_point_str = getattr(self, '_original_mount_point', str(self._mount_point))
        buf.extend(self._pack_string(mount_point_str))
        buf.extend(struct.pack('<I', len(self._files)))
        for entry in self._files:
            buf.extend(self._pack_entry(entry, self._pak_info.version))
        entry_to_idx = {id(entry): idx for idx, entry in enumerate(self._files)}
        dirs_to_pack = []
        for dir_path, dir_content in self._index.items():
            valid_files = []
            for file_name, entry in dir_content.items():
                if id(entry) in entry_to_idx:
                    valid_files.append((file_name, entry))
            if valid_files:
                dirs_to_pack.append((dir_path, valid_files))
        if hasattr(self, '_zstddic_info') and self._zstddic_info:
            dir_str, e = self._zstddic_info
            valid_files = []
            for file_name, entry in e.items():
                if id(entry) in entry_to_idx:
                    valid_files.append((file_name, entry))
            dirs_to_pack.append((PurePath(dir_str), valid_files))
        buf.extend(struct.pack('<Q', len(dirs_to_pack)))
        for dir_path, valid_files in dirs_to_pack:
            dir_str = self._dir_path_strings.get(dir_path, dir_path.as_posix())
            buf.extend(self._pack_string(dir_str))
            buf.extend(struct.pack('<Q', len(valid_files)))
            for file_name, entry in valid_files:
                buf.extend(self._pack_string(file_name))
                buf.extend(struct.pack('<i', ~entry_to_idx[id(entry)]))
        return bytes(buf)

    def _pack_footer(self) -> bytes:
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        enc_flag = ((1 if self._pak_info.index_encrypted else 0) ^ keystream[3]) & 0xFF
        enc_magic = (self._pak_info.magic ^ keystream[2]) & 0xFFFFFFFF
        key_ihash = struct.pack('<5I', *keystream[4:][:5])
        enc_index_hash = bytes(a^b for a,b in zip(self._pak_info.index_hash, key_ihash)) if version >= 6 else bytes()
        enc_index_size = (self._pak_info.index_size ^ ((keystream[10]<<32)|keystream[11])) & 0xFFFFFFFFFFFFFFFF
        enc_index_offset = (self._pak_info.index_offset ^ ((keystream[0]<<32)|keystream[1])) & 0xFFFFFFFFFFFFFFFF
        base_buf = bytearray()
        base_buf.append(enc_flag)
        base_buf.extend(struct.pack('<II', enc_magic, version))
        if version >= 6: base_buf.extend(enc_index_hash)
        base_buf.extend(struct.pack('<QQ', enc_index_size, enc_index_offset))
        t_buf = bytearray()
        if version >= 7:
            key_unk = struct.pack('<8I', *keystream[7:][:8])
            enc_unk1 = bytes(a^b for a,b in zip(self._pak_info.unk1, key_unk))
            t_buf.extend(enc_unk1)
        if version >= 8:
            t_buf.extend(self._pak_info.packed_key)
            t_buf.extend(self._pak_info.packed_iv)
            t_buf.extend(self._pak_info.packed_index_hash)
        if version >= 9:
            enc_stem = (self._pak_info.stem_hash ^ keystream[8]) & 0xFFFFFFFF
            enc_unk2 = (self._pak_info.unk2 ^ keystream[9]) & 0xFFFFFFFF
            t_buf.extend(struct.pack('<II', enc_stem, enc_unk2))
        if version >= 12:
            t_buf.extend(self._pak_info.content_org_hash)
        return bytes(t_buf + base_buf)

    def _encrypt_plaintext(self, plaintext: bytes, pak_relative_path: PurePath, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1(encryption_method):
            return bytes((b ^ SIMPLE1_DECRYPT_KEY for b in plaintext))
        elif PakCrypto._is_simple2(encryption_method):
            pad_len = -len(plaintext) % SIMPLE2_BLOCK_SIZE
            plaintext += b'\x00' * pad_len
            key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
            rolling = key
            out = []
            for x, in struct.iter_unpack('<I', plaintext):
                c = rolling ^ x
                out.append(c)
                rolling ^= c
            return struct.pack(f'<{len(out)}I', *out)
        elif PakCrypto._is_sm4(encryption_method):
            key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
            sm4 = PakCrypto._sm4_ctx(key)
            pad_len = -len(plaintext) % 16
            if pad_len > 0: plaintext = plaintext + b'\x00' * pad_len
            out = bytearray()
            for i in range(0, len(plaintext), 16):
                block = plaintext[i:i + 16]
                if len(block) < 16: block = block.ljust(16, b'\x00')
                out.extend(sm4.encrypt(block))
            return bytes(out)
        return plaintext

    def _best_compress(self, chunk, cm, zstd_dict=None):
        if cm == CM_ZLIB: return zlib.compress(chunk, 9)
        if cm in (CM_ZSTD, CM_ZSTD_DICT):
            zd = zstd_dict if cm == CM_ZSTD_DICT else None
            for lvl in [22, 19, 16, 13, 10, 7, 4, 1]:
                try: return ZstdCompressor(level=lvl, dict_data=zd, threads=1).compress(chunk)
                except Exception: continue
        return chunk

    def detect_dominant_style(self) -> dict:
        """Detect dominant compression/encryption style from PAK entries"""
        comp_counter = Counter()
        enc_counter = Counter()
        blk_counter = Counter()
        enc_flag_counter = Counter()
        total = len(self._files)
        if total == 0:
            return {'comp_method': CM_ZSTD, 'enc_method': 0, 'encrypted': False, 'block_size': 0x10000}
        for entry in self._files:
            comp_counter[entry.compression_method] += 1
            if entry.encrypted:
                enc_counter[entry.encryption_method] += 1
                enc_flag_counter['encrypted'] += 1
            else:
                enc_flag_counter['plain'] += 1
            if entry.compression_block_size:
                blk_counter[entry.compression_block_size] += 1
        non_none = [(m,c) for m,c in comp_counter.items() if m != CM_NONE]
        comp_method = max(non_none, key=lambda x: x[1])[0] if non_none else CM_NONE
        encrypted = enc_flag_counter.get('encrypted', 0) > enc_flag_counter.get('plain', 0)
        enc_method = enc_counter.most_common(1)[0][0] if encrypted and enc_counter else 0
        block_size = blk_counter.most_common(1)[0][0] if blk_counter else 0x10000
        return {'comp_method': comp_method, 'enc_method': enc_method, 'encrypted': encrypted, 'block_size': block_size}

    def repack_pak_file_full(self, edited_root, output_path, target_path=None, force_add=False):
        import copy as _cp
        console.print("[bold cyan]Full PAK Rebuild mode[/bold cyan]")
        if target_path: console.print(f"[bold cyan]Target path: {target_path}[/bold cyan]")
        edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file()]
        if not edit_files:
            console.print("[bold red]No files found in COMPILED folder![/bold red]")
            return 0
        console.print(f"[bold cyan]Found {len(edit_files)} files in COMPILED folder[/bold cyan]")

        version = self._pak_info.version
        keystream = PakCrypto.zuc_keystream()
        orig_fc = self._file_content
        mp_str, all_dirs = self._get_all_dirs_and_mp()

        if target_path and force_add:
            target_path = target_path.replace('\\', '/')
            matched_dir = None
            for existing_dir in all_dirs.keys():
                if existing_dir.strip('/').lower() == target_path.strip('/').lower():
                    matched_dir = existing_dir; break
            if matched_dir: target_path = matched_dir
            else: target_path = target_path.strip('/') + '/'

        pak_name_map = {}
        for dir_path, files in self._index.items():
            for name, entry in files.items():
                full_path = str(PurePath(dir_path)/name).replace('\\', '/')
                pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

        edited = {}
        for p in edit_files:
            fl = p.name.lower()
            found_match = False
            if fl in pak_name_map:
                cands = pak_name_map[fl]
                if target_path:
                    target_candidates = [(fp, e) for fp, e in cands if target_path.strip('/') in fp]
                    if target_candidates:
                        sz = p.stat().st_size
                        sm = [(fp, e) for fp, e in target_candidates if e.uncompressed_size == sz]
                        fp, ent = sm[0] if sm else target_candidates[0]
                        edited[fp] = (p, ent)
                        found_match = True
                if not found_match:
                    sz = p.stat().st_size
                    sm = [(fp, e) for fp, e in cands if e.uncompressed_size == sz]
                    fp, ent = sm[0] if sm else cands[0]
                    if target_path:
                        new_fp = f"{target_path.rstrip('/')}/{p.name}"
                        edited[new_fp] = (p, ent)
                    else:
                        edited[fp] = (p, ent)
                    found_match = True
            if not found_match:
                stem = p.stem.lower()
                ext = p.suffix.lower()
                for dir_path, files in self._index.items():
                    for name, entry in files.items():
                        if Path(name).stem.lower() == stem and Path(name).suffix.lower() == ext:
                            full_path = str(PurePath(dir_path)/name).replace('\\', '/')
                            if target_path:
                                new_fp = f"{target_path.rstrip('/')}/{p.name}"
                                edited[new_fp] = (p, entry)
                            else:
                                edited[full_path] = (p, entry)
                            found_match = True; break
                    if found_match: break
            if not found_match and force_add and target_path:
                template_entry = None
                for dir_path, files in self._index.items():
                    for name, entry in files.items():
                        if Path(name).suffix.lower() == p.suffix.lower():
                            template_entry = entry; break
                    if template_entry: break
                if not template_entry:
                    for dir_path, files in self._index.items():
                        for name, entry in files.items():
                            template_entry = entry; break
                        if template_entry: break
                if template_entry:
                    new_fp = f"{target_path.rstrip('/')}/{p.name}"
                    edited[new_fp] = (p, template_entry)

        if not edited:
            console.print("[bold red]No files to repack![/bold red]")
            return 0
        console.print(f"  [bold bright_cyan]Files to repack: {len(edited)}[/bold bright_cyan]")

        new_files = []
        for e in self._files:
            ne = _cp.copy(e)
            ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
            new_files.append(ne)
        old_to_new = {id(self._files[i]): new_files[i] for i in range(len(self._files))}
        edited_paths = {fp: p for fp, (p, _) in edited.items()}
        out_buf = bytearray()

        for dp_str, dir_files in list(all_dirs.items()):
            for name, old_entry in list(dir_files.items()):
                full_path = str(PurePath(dp_str)/name).replace('\\', '/')
                ne = old_to_new.get(id(old_entry), None)
                if ne is None:
                    ne = _cp.copy(old_entry)
                    ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                    new_files.append(ne)
                    old_to_new[id(old_entry)] = ne
                em = old_entry.encryption_method
                cm = old_entry.compression_method
                if full_path in edited_paths:
                    p, template = edited[full_path]
                    new_raw = p.read_bytes()
                    pak_rel = PurePath(full_path)
                    ne.content_hash = SHA1.new(new_raw).digest()
                    ne.uncompressed_size = len(new_raw)
                    ne.compression_method = template.compression_method if template else cm
                    ne.encryption_method = template.encryption_method if template else em
                    ne.encrypted = template.encrypted if template else old_entry.encrypted
                    ne.unk1 = template.unk1 if template else old_entry.unk1
                    if template and target_path:
                        full_path_str = mp_str + full_path
                        ne.unk2 = SHA1.new(full_path_str.lower().encode('utf-8')).digest()
                    else:
                        ne.unk2 = template.unk2 if template else old_entry.unk2
                    ne.index_new_sep = template.index_new_sep if template else old_entry.index_new_sep
                    
                    if ne.compression_method == CM_NONE:
                        cipher = self._encrypt_plaintext(new_raw, pak_rel, ne.encryption_method) if ne.encrypted else new_raw
                        ne.offset = len(out_buf)
                        ne.size = len(new_raw)
                        ne.uncompressed_size = len(new_raw)
                        out_buf += cipher
                    else:
                        cs = (template.compression_block_size if template and template.compression_block_size > 0 
                              else old_entry.compression_block_size if old_entry.compression_block_size > 0 
                              else 65536)
                        chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                        new_blks = []
                        for chunk in chunks:
                            compressed = self._best_compress(chunk, ne.compression_method, self._zstd_dict)
                            cipher = self._encrypt_plaintext(compressed, pak_rel, ne.encryption_method) if ne.encrypted else compressed
                            blk = PakCompressedBlock(start=len(out_buf), end=len(out_buf)+len(cipher))
                            out_buf += cipher
                            new_blks.append(blk)
                        ne.compressed_blocks = new_blks
                        ne.offset = new_blks[0].start if new_blks else len(out_buf)
                        ne.size = sum(b.end - b.start for b in new_blks)
                        ne.uncompressed_size = len(new_raw)
                    console.print(f"[green]Processed: {full_path}[/green]")
                else:
                    if cm == CM_NONE:
                        read_sz = PakCrypto.align_encrypted_content_size(old_entry.size, em) if old_entry.encrypted else old_entry.size
                        ne.offset = len(out_buf)
                        out_buf += bytes(orig_fc[old_entry.offset: old_entry.offset + read_sz])
                    elif old_entry.compressed_blocks:
                        new_blks = []
                        for ob in old_entry.compressed_blocks:
                            unc = ob.end - ob.start
                            enc = PakCrypto.align_encrypted_content_size(unc, em) if old_entry.encrypted else unc
                            nb = PakCompressedBlock(start=len(out_buf), end=len(out_buf)+unc)
                            out_buf += bytes(orig_fc[ob.start: ob.start + enc])
                            new_blks.append(nb)
                        ne.compressed_blocks = new_blks
                        ne.offset = new_blks[0].start

        if target_path and force_add:
            for fp, (p, template) in edited.items():
                already_processed = False
                for dp_str, dir_files in all_dirs.items():
                    for name, entry in dir_files.items():
                        if str(PurePath(dp_str)/name).replace('\\', '/') == fp:
                            already_processed = True; break
                    if already_processed: break
                if not already_processed:
                    ne = _cp.copy(template)
                    new_raw = p.read_bytes()
                    pak_rel = PurePath(fp)
                    ne.content_hash = SHA1.new(new_raw).digest()
                    ne.uncompressed_size = len(new_raw)
                    ne.compression_method = template.compression_method
                    ne.encryption_method = template.encryption_method
                    ne.encrypted = template.encrypted
                    ne.unk1 = template.unk1
                    full_path_str = mp_str + fp
                    ne.unk2 = SHA1.new(full_path_str.lower().encode('utf-8')).digest()
                    ne.index_new_sep = template.index_new_sep
                    if ne.compression_method == CM_NONE:
                        cipher = self._encrypt_plaintext(new_raw, pak_rel, ne.encryption_method) if ne.encrypted else new_raw
                        ne.offset = len(out_buf)
                        ne.size = len(new_raw)
                        ne.uncompressed_size = len(new_raw)
                        out_buf += cipher
                    else:
                        cs = template.compression_block_size if template.compression_block_size > 0 else 65536
                        chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                        new_blks = []
                        for chunk in chunks:
                            compressed = self._best_compress(chunk, ne.compression_method, self._zstd_dict)
                            cipher = self._encrypt_plaintext(compressed, pak_rel, ne.encryption_method) if ne.encrypted else compressed
                            blk = PakCompressedBlock(start=len(out_buf), end=len(out_buf)+len(cipher))
                            out_buf += cipher
                            new_blks.append(blk)
                        ne.compressed_blocks = new_blks
                        ne.offset = new_blks[0].start if new_blks else len(out_buf)
                        ne.size = sum(b.end - b.start for b in new_blks)
                        ne.uncompressed_size = len(new_raw)
                    new_files.append(ne)
                    if target_path not in all_dirs: all_dirs[target_path] = {}
                    all_dirs[target_path][p.name] = ne
                    console.print(f"[green]Added new: {fp}[/green]")

        eidx = {id(new_files[i]): i for i in range(len(new_files))}
        idx = bytearray(self._pack_string(mp_str))
        idx += struct.pack('<I', len(new_files))
        for ne in new_files:
            idx += self._pack_entry(ne, version)
        idx += struct.pack('<Q', len(all_dirs))
        for dp_str, dir_files in all_dirs.items():
            idx += self._pack_string(dp_str)
            idx += struct.pack('<Q', len(dir_files))
            for name, old_e in dir_files.items():
                idx += self._pack_string(name)
                found_idx = None
                for i, e in enumerate(new_files):
                    if id(e) == id(old_e):
                        found_idx = i; break
                if found_idx is None:
                    for i, e in enumerate(new_files):
                        if e.offset == old_e.offset and e.size == old_e.size:
                            found_idx = i; break
                idx += struct.pack('<i', ~found_idx if found_idx is not None else -1)

        index_plain = bytes(idx)
        new_sha1 = SHA1.new(index_plain).digest()
        if self._pak_info.index_encrypted:
            key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
            aes = AES.new(key, MODE_CBC, iv[:16])
            pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
            index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
        else:
            index_bytes = index_plain

        new_idx_offset = len(out_buf)
        new_idx_size = len(index_bytes)
        out_buf += index_bytes

        footer_sz = TencentPakInfo._mem_size(version)
        new_footer = bytearray(orig_fc[-footer_sz:])
        h_key = struct.pack('<5I', *keystream[4:9])
        new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
        new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
        new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))
        out_buf += new_footer

        with open(output_path, 'wb') as f: f.write(out_buf)
        return len(edited)

    def _get_all_dirs_and_mp(self):
        raw = bytes(self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size])
        if self._pak_info.index_encrypted: raw = PakCrypto.decrypt_index(raw, self._pak_info)
        r = Reader(raw)
        mp = r.string()
        num_files = r.u4()
        for _ in range(num_files): TencentPakEntry(r, self._pak_info.version)
        dirs = {}
        for _ in range(r.u8()):
            dp = r.string()
            cnt = r.u8()
            dirs[dp] = {r.string(): self._files[~r.i4()] for _ in range(cnt)}
        return mp, dirs

    def inject_files(self, inject_plan: list, output_pak: Path, add_signature_marker: bool = True) -> None:
        """Inject new files into this PAK, producing a new PAK at output_pak."""
        if not inject_plan:
            raise ValueError('inject_plan is empty — nothing to inject')

        console.print(Panel(
            f'[bold magenta]💉 CUSTOM INJECT[/bold magenta]\n'
            f'[white]Source PAK:[/] [yellow]{self._file_path.name}[/yellow]\n'
            f'[white]Output    :[/] [cyan]{output_pak.name}[/cyan]\n'
            f'[white]Injecting :[/] [green]{len(inject_plan)} new file(s)[/green]',
            title='INJECT MODE', border_style='magenta', padding=(0, 2)
        ))

        console.print('\n[bold magenta]━━ STEP 1/5 : LOADING INJECT FILES ━━[/bold magenta]')
        work_items = []
        for i, item in enumerate(inject_plan):
            if item.get('plain_bytes') is not None:
                plain = item['plain_bytes']
            elif item.get('src_path') is not None:
                try:
                    plain = Path(item['src_path']).read_bytes()
                except Exception as e:
                    console.print(f'   [red]✗ Cannot read {item["src_path"]}: {e} — skipping[/red]')
                    continue
            else:
                console.print(f'   [red]✗ Inject item {i} has no src_path or plain_bytes — skipping[/red]')
                continue

            internal = item['internal_path'].replace('\\', '/').lstrip('/')
            if not internal:
                console.print(f'   [red]✗ Empty internal_path for item {i} — skipping[/red]')
                continue

            parts = internal.rsplit('/', 1)
            if len(parts) == 2:
                dir_str, file_name = parts[0], parts[1]
            else:
                dir_str, file_name = '', parts[0]

            work_items.append({
                'dir_str':       dir_str,
                'file_name':     file_name,
                'internal_path': internal,
                'plain':         plain,
                'comp_method':   item['comp_method'],
                'enc_method':    item['enc_method'],
                'encrypted':     bool(item['encrypted']),
                'block_size':    item['block_size'],
                'comp_level':    item.get('comp_level', 19),
            })
            console.print(f'   [blue]✨[/] {internal} [dim]({len(plain):,} bytes)[/dim]')

        if not work_items:
            raise RuntimeError('No valid inject items after loading')
        console.print(f'[green]✔ Loaded {len(work_items)} file(s)[/green]')

        console.print('\n[bold magenta]━━ STEP 2/5 : ENCODING INJECT FILES ━━[/bold magenta]')
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        header_size = TencentPakInfo._mem_size(version)
        PAK_MAGIC = self._pak_info.magic

        orig_index_offset = self._pak_info.index_offset
        current_new_offset = orig_index_offset
        new_data_region = bytearray()
        new_injected_entries = []

        # Helper function for encryption
        def _encrypt_plaintext(plaintext, pak_relative_path, encryption_method):
            if PakCrypto._is_simple1(encryption_method):
                return bytes(b ^ SIMPLE1_DECRYPT_KEY for b in plaintext)
            elif PakCrypto._is_simple2(encryption_method):
                pad = (-len(plaintext)) % SIMPLE2_BLOCK_SIZE
                plaintext += b"\x00" * pad
                key, = struct.unpack("<I", SIMPLE2_DECRYPT_KEY)
                rolling = key
                out = []
                for x, in struct.iter_unpack("<I", plaintext):
                    c = rolling ^ x
                    out.append(c)
                    rolling ^= c
                return struct.pack(f"<{len(out)}I", *out)
            elif PakCrypto._is_sm4(encryption_method):
                key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
                sm4 = PakCrypto._sm4_ctx(key)
                pad_len = (-len(plaintext)) % 16
                if pad_len > 0:
                    plaintext = plaintext + b'\x00' * pad_len
                out = bytearray()
                for i in range(0, len(plaintext), 16):
                    block = plaintext[i:i+16]
                    if len(block) < 16:
                        block = block.ljust(16, b'\x00')
                    out.extend(sm4.encrypt(block))
                return bytes(out)
            return plaintext

        for item in work_items:
            plain = item['plain']
            comp_method = item['comp_method']
            enc_method = item['enc_method']
            encrypted = item['encrypted']
            block_size_val = item['block_size']
            file_path_for_crypto = PurePath(item['file_name'])

            if len(plain) == 0:
                new_injected_entries.append({
                    'content_hash': SHA1.new(b'').digest(),
                    'offset': current_new_offset,
                    'uncompressed_size': 0, 'size': 0,
                    'comp_method': CM_NONE, 'enc_method': 0, 'encrypted': False,
                    'block_size_val': 0, 'compressed_blocks': [],
                    'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0,
                    '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(),
                    '_file_name': item['file_name'],
                })
                continue

            if comp_method == CM_NONE:
                if encrypted:
                    aligned_size = PakCrypto.align_encrypted_content_size(len(plain), enc_method)
                    padded = plain + b'\x00' * (aligned_size - len(plain))
                    stored_data = _encrypt_plaintext(padded, file_path_for_crypto, enc_method)
                else:
                    stored_data = plain
                new_size = len(stored_data)
                new_compressed_blocks = []
            else:
                chunks = [plain[i:i+block_size_val] for i in range(0, len(plain), block_size_val)]
                if not chunks: chunks = [b'']
                compressed_chunks = []
                for chunk in chunks:
                    comp = None
                    if comp_method in (CM_ZSTD, CM_ZSTD_DICT):
                        zstd_dict = self._zstd_dict if comp_method == CM_ZSTD_DICT else None
                        for lvl in range(22, 0, -1):
                            try:
                                c = ZstdCompressor(level=lvl, dict_data=zstd_dict, threads=1)
                                comp = c.compress(chunk)
                                break
                            except: continue
                    elif comp_method == CM_ZLIB:
                        comp = zlib.compress(chunk, level=9)
                    if comp is None: comp = chunk
                    compressed_chunks.append(comp)

                encrypted_chunks = []
                for comp_data in compressed_chunks:
                    if encrypted:
                        comp_data = _encrypt_plaintext(comp_data, file_path_for_crypto, enc_method)
                    encrypted_chunks.append(comp_data)

                n_blocks = len(encrypted_chunks)
                indices = PakCrypto.generate_block_indices(n_blocks, enc_method)
                physical_blocks = [None] * n_blocks
                for j, chunk_data in enumerate(encrypted_chunks):
                    physical_blocks[indices[j]] = chunk_data

                physical_offsets = []
                block_cursor = current_new_offset
                for phys_block in physical_blocks:
                    physical_offsets.append((block_cursor, block_cursor + len(phys_block)))
                    block_cursor += len(phys_block)
                new_compressed_blocks = physical_offsets
                stored_data = b''.join(physical_blocks)
                new_size = len(stored_data)
                if encrypted:
                    aligned_total = PakCrypto.align_encrypted_content_size(new_size, enc_method)
                    if aligned_total > new_size:
                        stored_data = stored_data + b'\x00' * (aligned_total - new_size)
                        new_size = aligned_total

            new_content_hash = SHA1.new(stored_data).digest()
            new_data_region.extend(stored_data)

            new_injected_entries.append({
                'content_hash': new_content_hash,
                'offset': current_new_offset,
                'uncompressed_size': len(plain),
                'size': new_size,
                'comp_method': comp_method,
                'enc_method': enc_method if encrypted else 0,
                'encrypted': encrypted,
                'block_size_val': block_size_val,
                'compressed_blocks': new_compressed_blocks,
                'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0,
                '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(),
                '_file_name': item['file_name'],
            })
            current_new_offset += new_size

        console.print(f'[green]✔ Encoded {len(new_injected_entries)} file(s)[/green]')

        # Build final entries
        new_entries = []
        entry_to_path = {}
        for dir_path, files in self._index.items():
            for fname, entry in files.items():
                entry_to_path[id(entry)] = (dir_path, fname)
        for i, entry in enumerate(self._files):
            dir_path, fname = entry_to_path.get(id(entry), (PurePath(), f'unknown_{i}'))
            new_entries.append({
                'content_hash': entry.content_hash,
                'offset': entry.offset,
                'uncompressed_size': entry.uncompressed_size,
                'size': entry.size,
                'comp_method': entry.compression_method,
                'enc_method': entry.encryption_method if entry.encrypted else 0,
                'encrypted': entry.encrypted,
                'block_size_val': entry.compression_block_size,
                'compressed_blocks': [(b.start, b.end) for b in entry.compressed_blocks],
                'unk1': entry.unk1, 'unk2': entry.unk2,
                'index_new_sep': entry.index_new_sep,
            })
        new_entries.extend(new_injected_entries)

        if add_signature_marker:
            marker_already_present = False
            for dp, files_dict in self._index.items():
                if dp.name == 'HR_DHAMA' and 'PATCHED.txt' in files_dict:
                    marker_already_present = True
                    break
            if not marker_already_present:
                # Create marker entry
                empty_hash = SHA1.new(b'').digest()
                new_entries.append({
                    'content_hash': empty_hash,
                    'offset': current_new_offset,
                    'uncompressed_size': 0,
                    'size': 0,
                    'comp_method': CM_NONE,
                    'enc_method': 0,
                    'encrypted': False,
                    'block_size_val': 0,
                    'compressed_blocks': [],
                    'unk1': 0,
                    'unk2': b'\x00' * 20,
                    'index_new_sep': 0,
                    '_dir_path': PurePath('SAMEERxPUBG'),
                    '_file_name': 'PATCHED.txt',
                })

        # Build Index
        index_data = bytearray()
        raw_orig_index = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        orig_index_decoded = PakCrypto.decrypt_index(bytes(raw_orig_index), self._pak_info)
        orig_reader = Reader(orig_index_decoded)
        orig_mount_len = orig_reader.i4()
        orig_mount_bytes = bytes(orig_reader.s(orig_mount_len))
        index_data.extend(struct.pack('<I', orig_mount_len))
        index_data.extend(orig_mount_bytes)
        index_data.extend(struct.pack('<I', len(new_entries)))

        for item in new_entries:
            index_data.extend(item['content_hash'])
            if version <= 1: index_data.extend(struct.pack('<Q', 0))
            index_data.extend(struct.pack('<Q', item['offset']))
            index_data.extend(struct.pack('<Q', item['uncompressed_size']))
            index_data.extend(struct.pack('<I', item['comp_method'] & CM_MASK))
            index_data.extend(struct.pack('<Q', item['size']))
            if version >= 5:
                index_data.extend(struct.pack('<B', item['unk1']))
                index_data.extend(item['unk2'] if item['unk2'] else b'\x00' * 20)
            if item['comp_method'] != CM_NONE and version >= 3:
                index_data.extend(struct.pack('<I', len(item['compressed_blocks'])))
                for (start, end) in item['compressed_blocks']:
                    index_data.extend(struct.pack('<Q', start))
                    index_data.extend(struct.pack('<Q', end))
            if version >= 4:
                index_data.extend(struct.pack('<I', item['block_size_val']))
                index_data.extend(struct.pack('<B', 1 if item['encrypted'] else 0))
            if version >= 12:
                index_data.extend(struct.pack('<I', item['enc_method']))
                index_data.extend(struct.pack('<I', item['index_new_sep']))

        file_to_dirname = {}
        for dir_path, files_dict in self._index.items():
            dir_str = dir_path.as_posix()
            for fname, entry in files_dict.items():
                for i, fe in enumerate(self._files):
                    if id(fe) == id(entry):
                        file_to_dirname[i] = (dir_str, fname)
                        break
        for i, item in enumerate(new_entries):
            if i not in file_to_dirname:
                if '_dir_path' in item:
                    file_to_dirname[i] = (item['_dir_path'].as_posix(), item['_file_name'])
                else:
                    file_to_dirname[i] = ('', f'file_{i}')

        all_dirs = []
        dir_to_files = {}
        for dir_path in self._index.keys():
            ds = dir_path.as_posix()
            all_dirs.append(ds)
            dir_to_files[ds] = []
        for i, item in enumerate(new_entries):
            ds, fn = file_to_dirname[i]
            if ds not in dir_to_files:
                dir_to_files[ds] = []
                all_dirs.append(ds)
            dir_to_files[ds].append((fn, i))

        index_data.extend(struct.pack('<Q', len(all_dirs)))
        for dir_str in all_dirs:
            files_list = dir_to_files[dir_str]
            if not dir_str or dir_str == '.':
                index_data.extend(struct.pack('<I', 0))
            else:
                if not dir_str.endswith('/'): dir_str_with_slash = dir_str + '/'
                else: dir_str_with_slash = dir_str
                dir_bytes = dir_str_with_slash.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(dir_bytes)))
                index_data.extend(dir_bytes)
            index_data.extend(struct.pack('<Q', len(files_list)))
            for file_name, fi in files_list:
                name_bytes = file_name.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(name_bytes)))
                index_data.extend(name_bytes)
                index_data.extend(struct.pack('<i', -fi - 1))
        index_data.extend(b'\x1d\x00\x00\x00\x2e\x2e')

        index_hash = SHA1.new(bytes(index_data)).digest()

        if version > 7 and self._pak_info.index_encrypted:
            key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            padded = pad(bytes(index_data), AES.block_size)
            aes = AES.new(key, MODE_CBC, iv[:16])
            encrypted_index = aes.encrypt(padded)
        elif self._pak_info.index_encrypted:
            encrypted_index = bytes(b ^ SIMPLE1_DECRYPT_KEY for b in bytes(index_data))
        else:
            encrypted_index = bytes(index_data)

        index_size = len(encrypted_index)
        new_index_offset = orig_index_offset + len(new_data_region)

        encrypted_magic = PAK_MAGIC ^ keystream[2]
        key_stream_hash = struct.pack('<5I', *keystream[4:][:5])
        encrypted_index_hash = bytes(a ^ b for a, b in zip(index_hash, key_stream_hash))
        encrypted_index_size = index_size ^ ((keystream[10] << 32) | keystream[11])
        encrypted_index_offset = new_index_offset ^ ((keystream[0] << 32) | keystream[1])
        encrypted_flag_byte = (1 if self._pak_info.index_encrypted else 0) ^ (keystream[3] & 0xFF)

        orig_data_region = bytearray(self._file_content[0:orig_index_offset])
        output_pak.parent.mkdir(parents=True, exist_ok=True)
        with open(output_pak, 'wb') as f:
            f.write(bytes(orig_data_region))
            f.write(bytes(new_data_region))
            f.write(encrypted_index)
            if version >= 7:
                key_unk1 = struct.pack('<8I', *keystream[7:][:8])
                unk1_plain = self._pak_info.unk1 if self._pak_info.unk1 else b'\x00' * 32
                encrypted_unk1 = bytes(a ^ b for a, b in zip(unk1_plain, key_unk1))
                f.write(encrypted_unk1)
            if version >= 8:
                f.write(self._pak_info.packed_key if self._pak_info.packed_key else b'\x00' * 256)
                f.write(self._pak_info.packed_iv if self._pak_info.packed_iv else b'\x00' * 256)
                f.write(self._pak_info.packed_index_hash if self._pak_info.packed_index_hash else b'\x00' * 256)
            if version >= 9:
                f.write(struct.pack('<I', (self._pak_info.stem_hash or 0) ^ keystream[8]))
                f.write(struct.pack('<I', (self._pak_info.unk2 or 0) ^ keystream[9]))
            if version >= 12:
                f.write(self._pak_info.content_org_hash if self._pak_info.content_org_hash else b'\x00' * 20)
            f.write(struct.pack('<B', encrypted_flag_byte))
            f.write(struct.pack('<I', encrypted_magic))
            f.write(struct.pack('<I', version))
            if version >= 6:
                f.write(encrypted_index_hash)
            else:
                f.write(b'\x00' * 20)
            f.write(struct.pack('<Q', encrypted_index_size))
            f.write(struct.pack('<Q', encrypted_index_offset))

        console.print(Panel(
            f'[bold green]🎉 INJECT COMPLETE![/bold green]\n\n'
            f'[white]Output  :[/] [cyan]{output_pak.name}[/cyan]',
            title='✅ SUCCESS', border_style='green', padding=(1, 2)
        ))

# ==============================================================================
# OPTION 5: INJECT ANY LUA - COMPLETE FUNCTIONALITY FROM c.py
# ==============================================================================

# ==============================================================================
# OPTION 5: INJECT ANY LUA - COMPLETE FUNCTIONALITY WITH PER-FILE LOCATIONS
# ==============================================================================

def handle_lua_inject():
    """Complete INJECT ANY LUA functionality with per-file location selection"""
    console.print("\n[bold #00AAFF]📦 INJECT ANY LUA (PER-FILE LOCATIONS)[/bold #00AAFF]")
    console.print("[white]Inject Lua files into PAK with custom paths per file[/white]")
    
    edit_dir = EDIT_DIR
    out_path = RESULT_DIR
    pak_dir = PAK_DIR
    
    if not edit_dir.exists():
        edit_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]⚠ Created empty folder: {edit_dir}[/yellow]")
        console.print("[yellow]Please add your LUA files there first![/yellow]")
        safe_input("\nPress Enter to continue...")
        return
    
    files_in_edit = [f for f in edit_dir.rglob("*") if f.is_file() and f.name not in ['pak_manifest.json','.DS_Store']]
    if not files_in_edit:
        console.print("[bold red]❌ COMPILED folder is empty![/bold red]")
        console.print(f"[red]📁 Please put LUA files in: {edit_dir}[/red]")
        safe_input("\nPress Enter to continue...")
        return
    
    console.print("[cyan]🔍 Searching for PAK files in PAK_ORIGINAL...[/cyan]")
    pak_files = []
    for file in pak_dir.iterdir():
        if file.name.lower().endswith('.pak'):
            pak_files.append(file)
    
    if not pak_files:
        console.print("[bold red]❌ No PAK file found in PAK_ORIGINAL folder![/bold red]")
        console.print(f"[red]📁 Please put PAK file in: {pak_dir}[/red]")
        safe_input("\nPress Enter to continue...")
        return
    
    if len(pak_files) == 1:
        pak_path = pak_files[0]
        console.print(f"[green]✅ Found PAK: {pak_path.name}[/green]")
    else:
        console.print(f"[yellow]⚠️ Multiple PAK files found:[/yellow]")
        for i, pak in enumerate(pak_files, 1):
            console.print(f"  [{i}] {pak.name}")
        console.print("\n[bold yellow]Enter number to select:[/bold yellow]")
        try:
            choice_pak = int(safe_input("> ").strip())
            if 1 <= choice_pak <= len(pak_files):
                pak_path = pak_files[choice_pak - 1]
                console.print(f"[green]✅ Selected: {pak_path.name}[/green]")
            else:
                console.print("[bold red]❌ Invalid choice![/bold red]")
                safe_input("\nPress Enter to continue...")
                return
        except:
            console.print("[bold red]❌ Invalid input![/bold red]")
            safe_input("\nPress Enter to continue...")
            return
    
    # Get all files with their relative paths
    console.print("\n[bold cyan]📂 Files found in COMPILED folder:[/bold cyan]")
    files = []
    for f in files_in_edit:
        rel_path = str(f.relative_to(edit_dir)).replace("\\", "/")
        files.append((f, rel_path))
        console.print(f"  [dim]•[/dim] {rel_path}")
    
    console.print("\n[bold yellow]Choose mode:[/bold yellow]")
    console.print("  [1] Use same target path for ALL files")
    console.print("  [2] Set custom path for EACH file individually")
    
    mode_choice = safe_input("Select mode (1 or 2): ").strip()
    
    # Dictionary to store file -> target path mapping
    file_locations = {}
    
    if mode_choice == '1':
        # Same path for all files
        console.print("\n[bold yellow]Enter Target Repacking Path (common for all files):[/bold yellow]")
        console.print("[dim](Press Enter for default: Content/Lua/)[/dim]")
        console.print("[dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]")
        target_path = safe_input("> ").strip()
        if not target_path:
            target_path = "Content/Lua/"
            console.print(f"[cyan]🎯 Using default: {target_path}[/cyan]")
        else:
            if not target_path.endswith('/'):
                target_path += '/'
            console.print(f"[cyan]🎯 Target path: {target_path}[/cyan]")
        
        # Same path for all files
        for f, rel_path in files:
            full_path = target_path + rel_path
            file_locations[str(f)] = full_path
            
    else:
        # Custom path for each file
        console.print("\n[bold cyan]Set custom path for each file:[/bold cyan]")
        console.print("[dim]Press Enter to use default: Content/Lua/ + filename[/dim]")
        console.print("[dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]\n")
        
        for idx, (f, rel_path) in enumerate(files, 1):
            console.print(f"[{idx}/{len(files)}] [bold green]{rel_path}[/bold green]")
            console.print(f"  [dim]Current file: {f.name}[/dim]")
            console.print(f"  [dim]Suggested: Content/Lua/{rel_path}[/dim]")
            
            custom_path = safe_input("  Enter path (or press Enter for default): ").strip()
            
            if not custom_path:
                # Default path: Content/Lua/ + relative path
                full_path = "Content/Lua/" + rel_path
            else:
                if not custom_path.endswith('/'):
                    custom_path += '/'
                # If user just types folder name, prepend Content/Lua/
                if not custom_path.startswith('Content/'):
                    full_path = "Content/Lua/" + custom_path + f.name
                else:
                    full_path = custom_path + f.name
            
            file_locations[str(f)] = full_path
            console.print(f"  [green]✓ Location set: {full_path}[/green]\n")
    
    # Show summary
    console.print("\n[bold cyan]📋 Summary of file locations:[/bold cyan]")
    for f, loc in file_locations.items():
        console.print(f"  [dim]•[/dim] {Path(f).name} → [yellow]{loc}[/yellow]")
    
    confirm = safe_input("\n[bold yellow]Proceed with repack? (y/n): [/bold yellow]").strip().lower()
    if confirm != 'y':
        console.print("[red]Cancelled.[/red]")
        safe_input("\nPress Enter to continue...")
        return
    
    # Backup
    BACKUP_FOLDER = PAK_DIR.parent / "BACKUP"
    BACKUP_FOLDER.mkdir(exist_ok=True)
    backup_name = f"{pak_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pak"
    backup_path = BACKUP_FOLDER / backup_name
    shutil.copy2(pak_path, backup_path)
    console.print(f"[bold green]✅ Backup created: {backup_path}[/bold green]")
    
    try:
        console.print("[cyan]📦 Loading PAK file...[/cyan]")
        pak = TencentPakFile(PurePath(pak_path))
        output_name = f"{pak_path.stem}_MODIFIED.pak"
        output_pak = out_path / output_name
        
        console.print("[cyan]🔄 Repacking PAK...[/cyan]")
        
        dominant = pak.detect_dominant_style()
        console.print(f"[cyan]Dominant style: comp={dominant['comp_method']}, enc={dominant['enc_method']}, encrypted={dominant['encrypted']}, block={dominant['block_size']}[/cyan]")
        
        inject_plan = []
        for f, rel_path in files:
            internal_path = file_locations.get(str(f), "Content/Lua/" + rel_path)
            # Ensure path doesn't start with /
            if internal_path.startswith('/'):
                internal_path = internal_path[1:]
            
            inject_plan.append({
                'src_path': f,
                'internal_path': internal_path,
                'comp_method': dominant['comp_method'],
                'enc_method': dominant['enc_method'],
                'encrypted': dominant['encrypted'],
                'block_size': dominant['block_size'],
            })
        
        console.print(f"[green]Plan: {len(inject_plan)} files with custom locations.[/green]")
        
        # Show final plan
        console.print("\n[bold cyan]📦 Final inject plan:[/bold cyan]")
        for item in inject_plan:
            console.print(f"  [dim]•[/dim] {Path(item['src_path']).name} → [yellow]{item['internal_path']}[/yellow]")
        
        pak.inject_files(inject_plan, Path(output_pak))
        console.print(f"[bold green]✅ Repack complete! Output: {output_pak}[/bold green]")
        console.print(f"[green]Processed {len(inject_plan)} files with custom locations.[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
    
    safe_input("\nPress Enter to continue...")

# ==============================================================================
# UI & MENU FUNCTIONS
# ==============================================================================

def display_file_selector(title, folder_path, file_pattern="*.pak"):
    files = list(folder_path.glob(file_pattern))
    if not files:
        hexa_alert(f"No {file_pattern} files found in {folder_path}", "error")
        return None, None
    
    table = Table(box=ROUNDED, show_header=True, expand=True, padding=(0, 1), border_style=ACCENT)
    table.add_column("#", justify="right", style=f"bold {GOLD}", width=4)
    table.add_column("File", style=f"bold {NEON}")
    table.add_column("Size", justify="right", style=MUTED)
    
    for i, f in enumerate(files, 1):
        size_mb = f.stat().st_size / (1024 * 1024)
        table.add_row(f"[{i}]", f.name, f"{size_mb:.2f} MB")
    
    console.print()
    console.print(Panel(table, title=f"[bold {ACCENT}] {title} [/bold {ACCENT}]", 
                        border_style=GOLD, box=HEAVY, padding=(1, 2)))
    
    try:
        idx = int(hexa_prompt(f"Select file (1-{len(files)})")) - 1
        if idx < 0 or idx >= len(files):
            hexa_alert("Invalid selection", "error")
            return None, None
        return files[idx], files
    except ValueError:
        hexa_alert("Please enter a valid number", "error")
        return None, None

def delete_folder(data_path: Path) -> None:
    folders = []
    for item in data_path.iterdir():
        if item.is_dir() and item.name not in ['PAK', 'UNPACK', 'REPACK', 'RESULT', 'PAK TOOL', 'SOURCE', 'LUA_ORIGINAL', 'LUA_UNPACK', 'LUA_EDIT', 'PAK_ORIGINAL', 'PAK_UNPACK', 'PAK_RESULT', 'COMPILED']:
            folders.append(item)
    
    if not folders:
        hexa_alert("No folders found to delete", "warning")
        return
    
    table = Table(box=ROUNDED, show_header=True, expand=True, padding=(0, 1), border_style=ACCENT)
    table.add_column("#", justify="right", style=f"bold {GOLD}", width=4)
    table.add_column("Folder", style=f"bold {NEON}")
    table.add_column("Size", justify="right", style=MUTED)
    
    for i, folder in enumerate(folders, 1):
        folder_size = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path): folder_size += os.path.getsize(file_path)
        table.add_row(f"[{i}]", folder.name, human_size(folder_size))
    
    console.print()
    console.print(Panel(table, title=f"[bold {ACCENT}] AVAILABLE FOLDERS [/bold {ACCENT}]", 
                        border_style=GOLD, box=HEAVY, padding=(1, 2)))
    
    try:
        choice = int(hexa_prompt(f"Select folder number (1-{len(folders)})"))
        if 1 <= choice <= len(folders):
            selected_folder = folders[choice - 1]
            confirm = hexa_prompt(f"Delete {selected_folder.name}? (yes/no)").strip().lower()
            if confirm == 'yes':
                shutil.rmtree(selected_folder)
                hexa_alert(f"Deleted: {selected_folder.name}", "success")
            else: hexa_alert("Cancelled", "warning")
        else: hexa_alert("Invalid selection", "error")
    except ValueError: hexa_alert("Invalid input", "error")

# ==============================================================================
# MAIN MENU
# ==============================================================================

def main_menu():
    # 🔐 CHECK LICENSE FIRST
    valid, license_key, key_info = check_license()
    if not valid:
        console.print("[red]License verification failed. Exiting...[/red]")
        time.sleep(2)
        return
    
    setup_directories()
    ab = AnimatedBorder.get_instance()
    
    while True:
        print_main_banner(key_info=key_info)
        
        menu_table = Table(box=ROUNDED, show_header=False, padding=(0, 2), border_style=RED)
        menu_table.add_column(justify="right", style=f"bold {GREEN}", width=4)
        menu_table.add_column(justify="left", style=f"bold {NEON}", min_width=18)
        menu_table.add_column(justify="left", style=MUTED)
        
        menu_table.add_row("1.", "UNPACK_PAK", "extract every entry from a .pak")
        menu_table.add_row("2.", "LUA_MAKE", "Decompile & Recompile .luac")
        menu_table.add_row("3.", "REPACK_LUA_PAK", "add new files a target path")
        menu_table.add_row("4.", "CLEAN_ALL", "remove a SAMEER directory")
        menu_table.add_row("5.", "INJECT LUA", "Inject Lua files Without Firewall")
        menu_table.add_row("6.", "CLOSE_TERMUX", "close the tool")
        
        border_color = ab.get_moving_border_style(2, 0.5)
        console.print(Panel(menu_table, title="[bold white]═══ MAIN MENU ═══[/bold white]", 
                            border_style=border_color, box=HEAVY, padding=(1, 2)))
        console.print()
        
        choice = hexa_prompt("Enter your choice")

        if choice == '1':
            pak_dir = PAK_DIR
            if not pak_dir.exists(): 
                hexa_alert(f"PAK folder not found at {pak_dir}", "error")
                safe_input('\nPress Enter...')
                continue
            pak_file, _ = display_file_selector("Available .pak files to UNPACK", pak_dir)
            if not pak_file: 
                safe_input('\nPress Enter...')
                continue
            try:
                hexa_section(f"Unpacking {pak_file.name}")
                pak = TencentPakFile(pak_file)
                unpack_path = PAK_UNPACK_DIR / pak_file.stem
                pak.dump(unpack_path)
                hexa_alert(f"Extracted to {unpack_path}", "success")
            except Exception as e:
                hexa_alert(f"{escape(str(e))}", "error")
            safe_input('\nPress Enter to continue...')

        elif choice == '2':
            lua_mode_menu()

        elif choice == '3':
            pak_dir = PAK_DIR
            edit_dir = EDIT_DIR
            result_dir = RESULT_DIR
            
            if not pak_dir.exists(): 
                hexa_alert(f"PAK folder not found at {pak_dir}", "error")
                safe_input('\nPress Enter...')
                continue
                
            pak_file, _ = display_file_selector("Available .pak files to REPACK TO PATH", pak_dir)
            if not pak_file: 
                safe_input('\nPress Enter...')
                continue
                
            if not edit_dir.exists() or not any(edit_dir.iterdir()):
                hexa_alert("No files in COMPILED folder. Place files to add in COMPILED first.", "error")
                safe_input('\nPress Enter...')
                continue
                
            console.print()
            console.print(Panel(f"Target path inside the PAK where files should be added.\n[{MUTED}]e.g. Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/{MUTED}]",
                                border_style=ACCENT, box=ROUNDED, padding=(0, 2)))
            
            config = load_config()
            last_path = config.get('last_repack_path', '')
            
            if last_path:
                console.print(f"[bold green]▶ Last used path: {last_path}[/bold green]")
                console.print(f"[dim]  (Press Enter to use same path)[/dim]")
            else:
                console.print(f"[dim]  (No previous path found, type a new one)[/dim]")
            
            target_path = hexa_prompt_with_default("Path", last_path)
            
            if not target_path: 
                hexa_alert("No path provided", "error")
                safe_input('\nPress Enter...')
                continue
                
            config['last_repack_path'] = target_path
            save_config(config)
            console.print(f"[dim]  ✓ Saved path for next session[/dim]")
            
            target_path = target_path.replace('\\', '/').strip('/')
            if not target_path: 
                hexa_alert("Invalid target path", "error")
                safe_input('\nPress Enter...')
                continue
                
            try:
                hexa_section(f"Adding files to {target_path} · {pak_file.name}")
                pak = TencentPakFile(pak_file)
                output_pak = result_dir / pak_file.name
                count = pak.repack_pak_file_full(edit_dir, output_pak, target_path, force_add=True)
                if count > 0:
                    hexa_alert(f"Processed {count} files to {target_path} -> {output_pak}\nPAK is game ready", "success")
                else:
                    hexa_alert("No files were processed", "error")
            except Exception as e:
                hexa_alert(f"Repack failed: {e}", "error")
                traceback.print_exc()
            safe_input('\nPress Enter to continue...')

        elif choice == '4':
            delete_folder(LUA_PAK_ROOT)
            safe_input('\nPress Enter to continue...')

        elif choice == '5':
            # INJECT ANY LUA - Complete functionality from c.py
            handle_lua_inject()

        elif choice == '6':
            console.print()
            border_color = ab.get_moving_border_style(6, 0.7)
            console.print(Panel(
                "[bold white]═══ @GRW_XD UNLIMITED LUA TOOL ═══[/bold white]\n\n"
                "[bold white]Thank you for using![/bold white]\n\n"
                "[bold green]DEVELOPER[/bold green]  :   @GRW_XD\n"
                "[bold green]OWNER[/bold green]   :   SAMEER\n",
                border_style=border_color, box=HEAVY, padding=(1, 2)))
            time.sleep(2)
            os.system('pkill -f termux 2>/dev/null')
            os._exit(0)
            break

        else:
            hexa_alert("Invalid choice", "error")
            time.sleep(2)

def lua_mode_menu():
    ab = AnimatedBorder.get_instance()
    
    while True:
        print_main_banner("LUA_MAKE")
        
        menu_table = Table(box=ROUNDED, show_header=False, padding=(0, 2), border_style=RED)
        menu_table.add_column(justify="right", style=f"bold {GREEN}", width=4)
        menu_table.add_column(justify="left", style=f"bold {NEON}", min_width=18)
        menu_table.add_column(justify="left", style=MUTED)
        
        menu_table.add_row("1.", "RECOMPILE", "LUA_EDIT → COMPILED")
        menu_table.add_row("2.", "DECOMPILE", "LUA_ORIGINAL → LUA_EDIT")
        menu_table.add_row("3.", "BACK", "return to main menu")
        
        border_color = ab.get_moving_border_style(4, 0.5)
        console.print(Panel(menu_table, title="[bold white]═══ LUA_MAKE ═══[/bold white]", 
                            border_style=border_color, box=HEAVY, padding=(1, 2)))
        console.print()
        
        choice = hexa_prompt("Select option: ").strip()
        if choice == '1':
            action_repack_unpack()
        elif choice == '2':
            action_unpack()
        elif choice == '3':
            return
        else:
            hexa_alert("Invalid option", "error")
            time.sleep(1)

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print(f"\n[bold {WARN}]Interrupted. Exiting...[/bold {WARN}]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold {ERR}]FATAL: {escape(str(e))}[/bold {ERR}]")
        traceback.print_exc()
        safe_input('\nPress Enter to exit...')
        sys.exit(1)
