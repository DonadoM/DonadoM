"""Generate an animated terminal SVG for the GitHub profile README."""
import sys
from xml.sax.saxutils import escape

FONT_SIZE = 15
CHAR_W = FONT_SIZE * 0.62  # generous monospace advance so typed text is never clipped
LINE_H = 22
PAD_X, TOP = 22, 62
WIDTH = 860
BG, FG = "#1a1b26", "#c0caf5"
C = {"green": "#9ece6a", "blue": "#7aa2f7", "magenta": "#bb9af7", "cyan": "#7dcfff",
     "yellow": "#e0af68", "red": "#f7768e", "dim": "#565f89", "fg": FG}
PROMPT = [("mauricio@donadom", "green"), (":", "fg"), ("~", "blue"), ("$ ", "fg")]
TYPE_SPEED = 0.07   # seconds per typed char
PAUSE = 0.6         # pause after a command before its output

TUX = [
    "    .--.     ",
    "   |o_o |    ",
    "   |:_/ |    ",
    "  //   \\ \\   ",
    " (|     | )  ",
    "/'\\_   _/`\\  ",
    "\\___)=(___/  ",
]
INFO = [
    [("mauricio", "green"), ("@", "fg"), ("donadom", "green")],
    [("----------------", "dim")],
    [("Role", "yellow"), (":     Full-Stack Developer", "fg")],
    [("Backend", "yellow"), (":  Python · FastAPI · PostgreSQL", "fg")],
    [("Frontend", "yellow"), (": React · TypeScript · Vite", "fg")],
    [("Mobile", "yellow"), (":   React Native · Expo", "fg")],
    [("Infra", "yellow"), (":    Docker · AWS · GitHub Actions", "fg")],
    [("Arch", "yellow"), (":     Clean · Hexagonal · Screaming", "fg")],
    [("Shell", "yellow"), (":    zsh + tmux + LazyVim", "fg")],
    [("Location", "yellow"), (": Colombia", "fg")],
]

SCRIPT = [
    ("cmd", "whoami"),
    ("out", [[("Mauricio Donado", "cyan"), (" — full-stack developer", "fg")]]),
    ("cmd", "neofetch"),
    ("neofetch", None),
    ("cmd", "cat ~/.focus"),
    ("out", [[("> ", "magenta"), ("clean architecture, testing & real-time systems", "fg")],
             [("> ", "magenta"), ("open to collaborate on interesting projects", "fg")]]),
    ("prompt", None),
]


def tspans(segments):
    return "".join(f'<tspan fill="{C[c]}">{escape(t)}</tspan>' for t, c in segments)


def text_line(x, y, segments, cls="", delay=None):
    style = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
    klass = f' class="{cls}"' if cls else ""
    return f'<text x="{x:.1f}" y="{y}"{klass}{style}>{tspans(segments)}</text>'


def build():
    body, y, t = [], TOP, 0.4
    prompt_w = sum(len(s) for s, _ in PROMPT) * CHAR_W
    for kind, data in SCRIPT:
        if kind in ("cmd", "prompt"):
            body.append(text_line(PAD_X, y, PROMPT, "ln", t))
            if kind == "prompt":
                cx = PAD_X + prompt_w
                body.append(f'<rect class="ln cursor" x="{cx:.1f}" y="{y - FONT_SIZE + 2}" '
                            f'width="{CHAR_W:.1f}" height="{FONT_SIZE + 2}" fill="{FG}" '
                            f'style="animation-delay:{t:.2f}s,{t:.2f}s"/>')
                y += LINE_H
                continue
            n = len(data)
            cx = PAD_X + prompt_w
            body.append(text_line(cx, y, [(data, "fg")], "ln", t))
            # A background-coloured cover slides right in character steps: the "typing" effect.
            dur = n * TYPE_SPEED
            body.append(f'<rect class="ln type" x="{cx:.1f}" y="{y - FONT_SIZE}" '
                        f'width="{(n + 2) * CHAR_W:.1f}" height="{LINE_H}" fill="{BG}" '
                        f'style="--d:{(n + 1) * CHAR_W:.1f}px;animation-delay:{t:.2f}s,{t:.2f}s;'
                        f'animation-duration:0.01s,{dur:.2f}s;animation-timing-function:linear,steps({n + 1},end)"/>')
            t += dur + PAUSE
            y += LINE_H
        elif kind == "out":
            for seg in data:
                body.append(text_line(PAD_X, y, seg, "ln", t))
                y += LINE_H
                t += 0.12
            t += 0.3
        elif kind == "neofetch":
            info_x = PAD_X + len(TUX[0]) * CHAR_W + 10
            for i in range(max(len(TUX), len(INFO)) + 2):
                if i < len(TUX):
                    body.append(text_line(PAD_X, y, [(TUX[i], "cyan")], "ln", t))
                if i < len(INFO):
                    body.append(text_line(info_x, y, INFO[i], "ln", t))
                if i == len(INFO) + 1:
                    palette = ["dim", "red", "green", "yellow", "blue", "magenta", "cyan", "fg"]
                    for j, c in enumerate(palette):
                        body.append(f'<rect class="ln" x="{info_x + j * 3 * CHAR_W:.1f}" y="{y - FONT_SIZE + 1}" '
                                    f'width="{3 * CHAR_W:.1f}" height="{FONT_SIZE + 2}" fill="{C[c]}" '
                                    f'style="animation-delay:{t:.2f}s"/>')
                y += LINE_H
                t += 0.08
            t += 0.4
    height = y + 10
    dots = "".join(f'<circle cx="{24 + i * 20}" cy="20" r="6" fill="{c}"/>'
                   for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Terminal: Mauricio Donado, full-stack developer">
<style>
text {{ font-family: "JetBrains Mono","Fira Code","SF Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace; font-size: {FONT_SIZE}px; white-space: pre; }}
.ln {{ opacity: 0; animation: show 0.01s forwards; }}
.type {{ animation-name: show, type; animation-fill-mode: forwards, forwards; }}
.cursor {{ animation: show 0.01s forwards, blink 1s step-end infinite; }}
@keyframes show {{ to {{ opacity: 1; }} }}
@keyframes type {{ from {{ transform: translateX(0); }} to {{ transform: translateX(var(--d)); }} }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .ln, .type {{ animation: none; opacity: 1; }} .type {{ opacity: 0; }} }}
</style>
<rect width="{WIDTH}" height="{height}" rx="10" fill="{BG}"/>
<rect width="{WIDTH}" height="40" rx="10" fill="#16161e"/><rect y="30" width="{WIDTH}" height="10" fill="#16161e"/>
{dots}
<text x="{WIDTH / 2}" y="25" text-anchor="middle" fill="{C["dim"]}" style="font-size:13px">mauricio@donadom: ~ — zsh</text>
<g xml:space="preserve">
{chr(10).join(body)}
</g>
</svg>
'''


if __name__ == "__main__":
    sys.stdout.write(build())
