# Gradients, boxes and FIGlet — the static visual surface, in one screen.
# Regenerate:  vhs gradients.tape
output ../assets/gradients.gif

Set Shell      bash
Set FontSize   18
Set Width      1200
Set Height     700
Set Theme      "Catppuccin Mocha"
Set Padding    20
Set TypingSpeed 50ms

Hide
Type "cd .. && python" Enter
Sleep 2s
Show

Type "from c4rlib import Gradient, Box, Figlet, Banner" Enter
Sleep 400ms

Type `Figlet.print_gradient("c4rlib", font="slant", start=(0,200,255), end=(200,0,255))` Enter
Sleep 2s

Type `print(Gradient.fire("fire") + " " + Gradient.ice("ice") + " " + Gradient.toxic("toxic") + " " + Gradient.galaxy("galaxy"))` Enter
Sleep 2s

Type `print(Box.neon("64 gradient presets, 12 box styles"))` Enter
Sleep 2s

Type `print(Banner.gradient_title("SHOWTIME"))` Enter
Sleep 3s

Hide
Type "exit()" Enter
