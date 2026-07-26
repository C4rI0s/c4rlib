# Menu / Prompt / Table — the interactive layer, driven by scripted keystrokes.
# Regenerate:  vhs interactive.tape
output ../assets/interactive.gif

Set Shell      bash
Set FontSize   18
Set Width      1100
Set Height     620
Set Theme      "Catppuccin Mocha"
Set Padding    20
Set TypingSpeed 50ms

Hide
Type "cd .. && python" Enter
Sleep 2s
Show

Type "from c4rlib import Menu, Table, Logger" Enter
Sleep 400ms

Type `choice = Menu.select("Deploy target", options=["staging", "production", "cancel"])` Enter
Sleep 2s
Down
Sleep 800ms
Down
Sleep 800ms
Up
Sleep 800ms
Enter
Sleep 1s

Type `Logger.success("TARGET", choice)` Enter
Sleep 1s

Type `t = Table(headers=["service", "status", "latency"], title="Health")` Enter
Type `t.add_rows([["api", "ok", "12ms"], ["worker", "ok", "31ms"], ["cache", "degraded", "204ms"]])` Enter
Type `t.print()` Enter
Sleep 4s

Hide
Type "exit()" Enter
