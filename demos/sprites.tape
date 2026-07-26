# Sprite — animated ASCII characters moving across the terminal.
# Regenerate:  vhs sprites.tape
output ../assets/sprites.gif

Set Shell      bash
Set FontSize   18
Set Width      1200
Set Height     500
Set Theme      "Catppuccin Mocha"
Set Padding    20
Set TypingSpeed 50ms

Hide
Type "cd .. && python" Enter
Sleep 2s
Show

Type "from c4rlib import Sprite" Enter
Sleep 400ms

Type `Sprite.preset("ghost", color="#a78bfa").move(from_x=2, to_x=70, duration=2.5, bob=True)` Enter
Sleep 4s

Type `Sprite.parade(["rocket", "ufo", "dragon", "pacman"], speed=25)` Enter
Sleep 5s

Hide
Type "exit()" Enter
