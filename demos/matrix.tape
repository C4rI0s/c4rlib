# Animations.matrix_rain — the full-screen effect people screenshot.
# Regenerate:  vhs matrix.tape
output ../assets/matrix.gif

Set Shell      bash
Set FontSize   18
Set Width      1200
Set Height     640
Set Theme      "Catppuccin Mocha"
Set Padding    10
Set TypingSpeed 60ms

Hide
Type "cd .. && python" Enter
Sleep 2s
Show

Type "from c4rlib import Animations" Enter
Sleep 500ms
Type `Animations.matrix_rain(duration=6.0, color="#00ff41")` Enter
Sleep 8s

Hide
Type "exit()" Enter
