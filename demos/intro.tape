# FX.intro — the headline demo.
# Regenerate:  vhs intro.tape
output ../assets/intro.gif

Set Shell      bash
Set FontSize   20
Set Width      1200
Set Height     600
Set Theme       "Catppuccin Mocha"
Set Padding    20
Set TypingSpeed 60ms

Hide
Type "cd .. && python" Enter
Sleep 2s
Show

Type "from c4rlib import FX" Enter
Sleep 500ms
Type `FX.intro("C4RLIB", subtitle="showtime CLI toolkit", style="fireworks", sound=False)` Enter
Sleep 8s

Hide
Type "exit()" Enter
