import time
import c4rlib
from c4rlib import (
    Logger, ColorUtils, Gradient, GradientPresets,
    Box, Banner, TextStyle, Utils,
    Spinner, ProgressBar, Table, Console,
    Http, Crypto, Files, Discord
)

Console.clear()

print(Banner.gradient_title("  c4rlib 2.0.0 — FULL DEMO  ", start=(0,200,255), end=(200,0,255)))
print()
Console.typewriter("  Bienvenido al demo completo de c4rlib 2.0.0", delay=0.02, color="#00ccff")
print()
Console.pause()
Console.clear()


print(Banner.section("COLORS & GRADIENTS", color="#00ccff"))
print()

print("  " + ColorUtils.paint("paint() con hex color", "#FF4444"))
print("  " + ColorUtils.paint("bold + color", "#29bf12"))
print("  " + ColorUtils.bold(ColorUtils.paint("bold text", "#ffd60a")))
print("  " + ColorUtils.italic(ColorUtils.paint("italic text", "#9b5de5")))
print("  " + ColorUtils.underline(ColorUtils.paint("underline text", "#00ccff")))
print("  " + ColorUtils.strike(ColorUtils.paint("strikethrough text", "#ff7b00")))
print("  " + ColorUtils.bg_paint("bg + fg color", "#000000", "#00ccff"))
print()

print("  " + Gradient.fire("fire gradient"))
print("  " + Gradient.ice("ice gradient"))
print("  " + Gradient.toxic("toxic gradient"))
print("  " + Gradient.sunset("sunset gradient"))
print("  " + Gradient.ocean("ocean gradient"))
print("  " + Gradient.galaxy("galaxy gradient"))
print("  " + Gradient.neon("neon gradient"))
print("  " + Gradient.matrix("matrix gradient"))
print("  " + Gradient.lava("lava gradient"))
print("  " + Gradient.candy("candy gradient"))
print("  " + Gradient.aurora("aurora gradient"))
print("  " + Gradient.electric("electric gradient"))
print("  " + Gradient.rose("rose gradient"))
print("  " + Gradient.random_gradient("random gradient — diferente cada vez!"))
print()

print("  " + Gradient.multicolor("multi-stop: rojo → amarillo → verde → azul → purpura", [
    (255,0,0),(255,255,0),(0,255,0),(0,100,255),(150,0,255)
]))
print()

print("  " + ColorUtils.rainbow("rainbow text caracter por caracter"))
print()

blended = ColorUtils.blend("#FF0000", "#0000FF", 0.5)
print(f"  blend(#FF0000, #0000FF, 0.5) = {ColorUtils.paint(blended, blended)}")
print(f"  lighten(#FF0000, 0.3) = ", end="")
lightened = ColorUtils.lighten("#FF0000", 0.3)
print(ColorUtils.paint(lightened, lightened))
print(f"  palette(#00ccff, 5) = ", end="")
for c in ColorUtils.palette("#00ccff", 5):
    print(ColorUtils.paint("██", c), end="")
print()
print()

Console.pause()
Console.clear()


print(Banner.section("LOGGER — TODOS LOS NIVELES", color="#00ccff"))
print()

Logger.success("Login",    "usuario autenticado",         "200 OK")
Logger.error  ("Request",  "timeout de conexion",         "408")
Logger.warning ("RateLimit","demasiadas peticiones",       "429")
Logger.info   ("Server",   "escuchando en puerto",        "8080")
Logger.debug  ("Memory",   "uso actual de RAM",           "312 MB")
Logger.critical("Crash",   "error fatal detectado",       "SIGKILL")
Logger.network ("HTTP",    "GET /api/v1/users",           "200 OK")
Logger.captcha ("Solver",  "resolviendo hcaptcha",        "token_abc")
Logger.input  ("User",     "nuevo input recibido",        "stdin")
Logger.output ("Result",   "respuesta lista",             "stdout")
Logger.proxy  ("Proxy",    "conectado via proxy",         "127.0.0.1:8080")
Logger.token  ("Token",    "token generado",              "Bearer xyz...")
Logger.upload ("Upload",   "archivo subido",              "file.zip 4.2MB")
Logger.download("Download","archivo descargado",          "data.json 1.1MB")
Logger.database("DB",      "query ejecutada",             "SELECT * FROM users")
Logger.file   ("File",     "archivo leido",               "config.json")
Logger.crypto ("Crypto",   "hash calculado",              "sha256")
Logger.wait   ("Wait",     "esperando respuesta",         "timeout 30s")
Logger.done   ("Done",     "tarea completada",            "100%")
Logger.send   ("Send",     "mensaje enviado",             "channel #general")
Logger.receive("Receive",  "mensaje recibido",            "channel #logs")
Logger.locked ("Lock",     "recurso bloqueado",           "mutex_1")
Logger.unlocked("Unlock",  "recurso liberado",            "mutex_1")
Logger.custom ("#FF69B4",  "♥", "LVL", "custom log", "cualquier color", "cualquier simbolo")
print()
Logger.gradient_log("Gradient log — aplica gradiente automatico al mensaje completo")
Logger.banner_log("BANNER LOG — MUY DESTACADO", hex_color="#ffd60a")
print()
Logger.fire   ("Fire log   — gradiente de fuego aplicado automaticamente")
Logger.galaxy ("Galaxy log — gradiente galactico aplicado automaticamente")
Logger.neon   ("Neon log   — gradiente neon aplicado automaticamente")
print()

Console.pause()
Console.clear()


print(Banner.section("BOXES & BANNERS", color="#00ccff"))
print()

print(Box.rounded      ("rounded box",      color="#00ccff"))
print(Box.double       ("double box",        color="#9b5de5"))
print(Box.heavy        ("heavy box",         color="#29bf12"))
print(Box.simple       ("simple box",        color="#ffd60a"))
print(Box.dots         ("dots box",          color="#ff7b00"))
print(Box.stars        ("stars box",         color="#FF69B4"))
print(Box.ascii        ("ascii box",         color="#adb5bd"))
print(Box.diamond      ("diamond box",       color="#00bbf9"))
print(Box.arrows       ("arrows box",        color="#f72585"))
print(Box.classic_round("classic round box", color="#06d6a0"))
print(Box.neon         ("neon box",          color="#00ccff"))
print(Box.gradient_box ("gradient box",      start=(0,200,255), end=(200,0,255)))
print()

print(Box.multiline(
    ["Linea 1 del multiline box", "Linea 2 del multiline box", "Linea 3 del multiline box"],
    style="rounded", color="#00ccff"
))
print()

print(Box.titled(
    "INFO DEL SISTEMA",
    [f"Version:   {c4rlib.__version__}", f"Author:    {c4rlib.__author__}", f"License:   {c4rlib.__license__}"],
    style="double", title_color="#ffd60a", border_color="#6c757d"
))
print()

print(Banner.line         ("banner line",         color="#00ccff"))
print(Banner.double_line  ("banner double line",  color="#9b5de5"))
print(Banner.arrow_line   ("banner arrow line",   color="#ffd60a"))
print(Banner.heart_line   ("banner heart line",   color="#FF69B4"))
print(Banner.wave_line    ("banner wave line",    color="#29bf12"))
print(Banner.star_line    ("banner star line",    color="#ffd60a"))
print(Banner.dot_line     ("banner dot line",     color="#adb5bd"))
print(Banner.slash_line   ("banner slash line",   color="#ff7b00"))
print(Banner.diamond_line ("banner diamond line", color="#00bbf9"))
print(Banner.lightning_line("banner lightning",   color="#ffd60a"))
print(Banner.fire_line    ("banner fire line",    color="#ff4500"))
print(Banner.gradient_banner("gradient banner",   start=(0,200,255), end=(200,0,255)))
print()

Console.pause()
Console.clear()


print(Banner.section("TEXT STYLES", color="#00ccff"))
print()

base = "c4rlib text"
styles = [
    ("original",        base),
    ("fancy",           TextStyle.fancy(base)),
    ("double_struck",   TextStyle.double_struck(base)),
    ("cursive",         TextStyle.cursive(base)),
    ("fraktur",         TextStyle.fraktur(base)),
    ("bold_serif",      TextStyle.bold_serif(base)),
    ("sans_bold",       TextStyle.sans_bold(base)),
    ("monospace",       TextStyle.monospace(base)),
    ("syllabic",        TextStyle.syllabic(base)),
    ("small_caps",      TextStyle.small_caps(base)),
    ("wide",            TextStyle.wide("c4rlib")),
    ("bubble",          TextStyle.bubble(base)),
    ("negative_square", TextStyle.negative_square(base)),
    ("leet",            TextStyle.leet(base)),
    ("alternate_case",  TextStyle.alternate_case(base)),
    ("reverse",         TextStyle.reverse(base)),
    ("strikethrough",   TextStyle.strikethrough(base)),
    ("underline_text",  TextStyle.underline_text(base)),
    ("overline_text",   TextStyle.overline_text(base)),
    ("superscript",     TextStyle.superscript("c4rlib")),
    ("subscript",       TextStyle.subscript("c4rlib")),
    ("space_out",       TextStyle.space_out("c4rlib", 2)),
    ("rot13",           TextStyle.rot13(base)),
    ("caesar(3)",       TextStyle.caesar(base, 3)),
    ("clap",            TextStyle.clap("c4r lib text")),
    ("uwuify",          TextStyle.uwuify("hello world")),
    ("zalgo",           TextStyle.zalgo("zalgo", intensity=2)),
]
for name, result in styles:
    label = ColorUtils.paint(f"  {name:<20}", "#6c757d")
    print(f"{label}{result}")

print()
print(f"  {ColorUtils.paint('morse:', '#6c757d')}  {TextStyle.morse('sos')}")
print(f"  {ColorUtils.paint('nato:', '#6c757d')}   {TextStyle.nato('sos')}")
print(f"  {ColorUtils.paint('binary:', '#6c757d')} {TextStyle.binary('hi')}")
print(f"  {ColorUtils.paint('hex:', '#6c757d')}    {TextStyle.hex_encode('hi')}")
print()

Console.pause()
Console.clear()


print(Banner.section("UTILITIES", color="#00ccff"))
print()

print(ColorUtils.paint("  ── Identity ──────────────────────", "#6c757d"))
print(f"  uuid v4:          {Utils.generate_uuid()}")
print(f"  uuid hex:         {Utils.generate_uuid_hex()}")
print(f"  token 32:         {Utils.generate_token(32)}")
print(f"  hex token:        {Utils.generate_hex_token(16)}")
print(f"  pin 6:            {Utils.generate_pin(6)}")
print(f"  password:         {Utils.generate_password(20, symbols=True)}")
print()

print(ColorUtils.paint("  ── Fake Data ───────────────────────", "#6c757d"))
print(f"  name:             {Utils.random_name()}")
print(f"  first name:       {Utils.random_first_name()}")
print(f"  last name:        {Utils.random_last_name()}")
print(f"  email:            {Utils.random_email()}")
print(f"  username:         {Utils.random_username()}")
print(f"  birthdate:        {Utils.random_birthdate()}")
print(f"  phone:            {Utils.random_phone('+34')}")
print(f"  address:          {Utils.random_address()}")
print(f"  zip US:           {Utils.random_zip('US')}")
print(f"  zip UK:           {Utils.random_zip('UK')}")
card = Utils.random_credit_card("visa")
print(f"  card:             {card['number']}  {card['expiry']}  CVV:{card['cvv']}  ({card['brand']})")
print(f"  user agent:       {Utils.random_user_agent()[:60]}...")
print(f"  color hex:        {Utils.random_color_hex()}")
print()

print(ColorUtils.paint("  ── Network ─────────────────────────", "#6c757d"))
print(f"  ipv4:             {Utils.generate_ipv4()}")
print(f"  ipv6:             {Utils.generate_ipv6()}")
print(f"  mac:              {Utils.generate_mac()}")
print(f"  port:             {Utils.generate_port()}")
print()

print(ColorUtils.paint("  ── Hashes ──────────────────────────", "#6c757d"))
print(f"  md5:              {Utils.hash_md5('c4rlib')}")
print(f"  sha1:             {Utils.hash_sha1('c4rlib')}")
print(f"  sha256:           {Utils.hash_sha256('c4rlib')}")
print(f"  sha512:           {Utils.hash_sha512('c4rlib')[:64]}...")
print()

print(ColorUtils.paint("  ── Helpers ─────────────────────────", "#6c757d"))
print(f"  chunk([1-9],3):   {Utils.chunk([1,2,3,4,5,6,7,8,9], 3)}")
print(f"  flatten:          {Utils.flatten([[1,2],[3,[4,5]],6])}")
print(f"  unique:           {Utils.unique([1,2,2,3,3,3,4])}")
print(f"  clamp(150,0,100): {Utils.clamp(150, 0, 100)}")
print(f"  lerp(0,100,0.3):  {Utils.lerp(0, 100, 0.3)}")
print(f"  percentage(7,10): {Utils.percentage(7, 10)}%")
print(f"  format_bytes:     {Utils.format_bytes(1536000)}")
print(f"  format_number:    {Utils.format_number(1000000)}")
print()

Console.pause()
Console.clear()


print(Banner.section("CRYPTO", color="#00ccff"))
print()

print(ColorUtils.paint("  ── Hashes ──────────────────────────", "#6c757d"))
print(f"  md5:              {Crypto.md5('c4rlib')}")
print(f"  sha1:             {Crypto.sha1('c4rlib')}")
print(f"  sha256:           {Crypto.sha256('c4rlib')}")
print(f"  sha3_256:         {Crypto.sha3_256('c4rlib')}")
print(f"  blake2b:          {Crypto.blake2b('c4rlib')[:48]}...")
print(f"  hmac_sha256:      {Crypto.hmac_sha256('secret_key', 'message')}")
print()

print(ColorUtils.paint("  ── Base64 ──────────────────────────", "#6c757d"))
encoded = Crypto.b64_encode("hello c4rlib!")
decoded = Crypto.b64_decode(encoded)
print(f"  encode:           {encoded}")
print(f"  decode:           {decoded}")
url_enc = Crypto.b64_urlsafe_encode("hello c4rlib!")
url_dec = Crypto.b64_urlsafe_decode(url_enc)
print(f"  urlsafe encode:   {url_enc}")
print(f"  urlsafe decode:   {url_dec}")
print()

print(ColorUtils.paint("  ── Encoding ────────────────────────", "#6c757d"))
print(f"  hex encode:       {Crypto.hex_encode('c4rlib')}")
print(f"  hex decode:       {Crypto.hex_decode(Crypto.hex_encode('c4rlib'))}")
print(f"  url encode:       {Crypto.url_encode('hello world & more')}")
print(f"  html encode:      {Crypto.html_encode('<script>alert(1)</script>')}")
print(f"  rot13:            {Crypto.rot13('c4rlib rocks')}")
print(f"  caesar(5):        {Crypto.caesar('c4rlib rocks', 5)}")
print()

print(ColorUtils.paint("  ── XOR / Vigenere ──────────────────", "#6c757d"))
xor_enc = Crypto.xor_encrypt("hello world", "secretkey")
xor_dec = Crypto.xor_decrypt(xor_enc, "secretkey")
print(f"  xor encrypt:      {xor_enc}")
print(f"  xor decrypt:      {xor_dec}")
vig_enc = Crypto.vigenere_encrypt("hello world", "key")
vig_dec = Crypto.vigenere_decrypt(vig_enc, "key")
print(f"  vigenere encrypt: {vig_enc}")
print(f"  vigenere decrypt: {vig_dec}")
print()

print(ColorUtils.paint("  ── JWT ─────────────────────────────", "#6c757d"))
payload = {"user": "c4r", "role": "admin", "exp": 9999999999}
token   = Crypto.make_jwt(payload, "my_secret")
decoded_jwt = Crypto.decode_jwt(token)
valid   = Crypto.verify_jwt(token, "my_secret")
print(f"  jwt:              {token[:60]}...")
print(f"  decoded:          {decoded_jwt}")
print(f"  valid:            {valid}")
print()

print(ColorUtils.paint("  ── Random Secure ───────────────────", "#6c757d"))
print(f"  random hex:       {Crypto.random_hex(16)}")
print(f"  random urlsafe:   {Crypto.random_urlsafe(16)}")
print()

Console.pause()
Console.clear()


print(Banner.section("FILES", color="#00ccff"))
print()

print(ColorUtils.paint("  ── Write & Read ────────────────────", "#6c757d"))
Files.write("c4rlib_test.txt", "hello from c4rlib!\nline 2\nline 3")
content = Files.read("c4rlib_test.txt")
lines   = Files.read_lines("c4rlib_test.txt")
print(f"  write + read:     OK — {Files.size_human('c4rlib_test.txt')}")
print(f"  lines:            {lines}")
print()

print(ColorUtils.paint("  ── JSON ────────────────────────────", "#6c757d"))
Files.write_json("c4rlib_test.json", {"name": "c4rlib", "version": "2.0.0", "author": "c4r"})
data = Files.read_json("c4rlib_test.json")
print(f"  write_json:       OK")
print(f"  read_json:        {data}")
print()

print(ColorUtils.paint("  ── Info ────────────────────────────", "#6c757d"))
print(f"  exists:           {Files.exists('c4rlib_test.txt')}")
print(f"  is_file:          {Files.is_file('c4rlib_test.txt')}")
print(f"  size:             {Files.size_human('c4rlib_test.txt')}")
print(f"  extension:        {Files.extension('c4rlib_test.txt')}")
print(f"  basename:         {Files.basename('c4rlib_test.txt')}")
print(f"  stem:             {Files.stem('c4rlib_test.txt')}")
print(f"  hash sha256:      {Files.hash('c4rlib_test.txt')}")
print(f"  modified:         {Files.modified_time('c4rlib_test.txt')}")
print(f"  cwd:              {Files.cwd()}")
print(f"  home:             {Files.home()}")
print()

print(ColorUtils.paint("  ── Utils ───────────────────────────", "#6c757d"))
print(f"  safe_filename:    {Files.safe_filename('my file: *bad* name?.txt')}")
print(f"  list_files:       {Files.list_files('.', '*.txt')[:3]}")
print()

Files.delete("c4rlib_test.txt")
Files.delete("c4rlib_test.json")

Console.pause()
Console.clear()


print(Banner.section("HTTP", color="#00ccff"))
print()

sp = Spinner("Testing HTTP GET...", style="dots", color="#00ccff")
sp.start()
try:
    r = Http.get("https://httpbin.org/get", params={"c4rlib": "2.0.0"}, timeout=8)
    sp.stop(f"GET httpbin.org — status {r.status}")
    data = r.json()
    print(f"  url:              {data.get('url','')}")
    print(f"  origin:           {data.get('origin','')}")
    print(f"  args:             {data.get('args','')}")
except Exception as e:
    sp.stop(f"Request failed: {e}", success=False)
print()

sp2 = Spinner("Testing HTTP POST...", style="dots2", color="#9b5de5")
sp2.start()
try:
    r2 = Http.post("https://httpbin.org/post", json_data={"tool": "c4rlib", "version": "2.0.0"}, timeout=8)
    sp2.stop(f"POST httpbin.org — status {r2.status}")
    data2 = r2.json()
    print(f"  json sent:        {data2.get('json','')}")
except Exception as e:
    sp2.stop(f"Request failed: {e}", success=False)
print()

print(ColorUtils.paint("  ── Utilities ───────────────────────", "#6c757d"))
parsed = Http.parse_url("https://discord.com/api/v9/users/@me?locale=en&with_analytics=true")
print(f"  parse_url scheme: {parsed['scheme']}")
print(f"  parse_url host:   {parsed['host']}")
print(f"  parse_url path:   {parsed['path']}")
print(f"  parse_url query:  {parsed['query']}")
print(f"  build_url:        {Http.build_url('https://api.example.com', 'users', {'page': 1})}")
print(f"  encode_params:    {Http.encode_params({'key': 'value', 'foo': 'bar'})}")
print()
headers = Http.random_headers(token="Bearer my_token_here")
print(f"  random_headers:   {list(headers.keys())}")
print()

Console.pause()
Console.clear()


print(Banner.section("DISCORD UTILS", color="#5865F2"))
print()

print(ColorUtils.paint("  ── Token ───────────────────────────", "#6c757d"))
fake_token = "MTE3MzAwODgzODY5Mw.GYtest.fake_hmac_here_for_demo_purposes"
print(f"  is_valid:         {Discord.is_valid_token(fake_token)}")
print()

print(ColorUtils.paint("  ── Snowflake ───────────────────────", "#6c757d"))
snowflake = 1173008838693
print(f"  snowflake ts:     {Discord.snowflake_to_timestamp(snowflake)}")
print(f"  generate nonce:   {Discord.generate_nonce()}")
print(f"  session id:       {Discord.generate_session_id()}")
print(f"  device id:        {Discord.generate_device_id()}")
print()

print(ColorUtils.paint("  ── Headers ─────────────────────────", "#6c757d"))
xsuper = Discord.make_xsuper(client_version="1.0.9038", build_number=9038)
print(f"  x-super-props:    {xsuper[:60]}...")
headers = Discord.make_headers(token="Bot my_bot_token", xsuper=xsuper)
print(f"  headers keys:     {list(headers.keys())}")
print()

print(ColorUtils.paint("  ── Generation ──────────────────────", "#6c757d"))
print(f"  username:         {Discord.generate_username()}")
print(f"  birthdate:        {Discord.generate_birthdate()}")
print(f"  invite code:      {Discord.random_invite_code()}")
print(f"  invite link:      {Discord.invite_link('abc123xyz')}")
print(f"  message link:     {Discord.message_link(123456789, 987654321, 111222333)}")
print()

print(ColorUtils.paint("  ── Formatting ──────────────────────", "#6c757d"))
print(f"  bold:             {Discord.format_bold('texto en negrita')}")
print(f"  italic:           {Discord.format_italic('texto en italica')}")
print(f"  underline:        {Discord.format_underline('texto subrayado')}")
print(f"  strikethrough:    {Discord.format_strikethrough('texto tachado')}")
print(f"  spoiler:          {Discord.format_spoiler('texto spoiler')}")
print(f"  inline code:      {Discord.format_inline_code('print(hello)')}")
print(f"  code block:       {repr(Discord.format_code('x = 1 + 1', 'python'))}")
print(f"  mention user:     {Discord.format_mention_user(123456789)}")
print(f"  mention role:     {Discord.format_mention_role(987654321)}")
print(f"  mention channel:  {Discord.format_mention_channel(111222333)}")
print(f"  quote:            {repr(Discord.format_quote('linea 1\\nlinea 2'))}")
import datetime
print(f"  timestamp:        {Discord.format_timestamp(datetime.datetime.now(), 'f')}")
print()

print(ColorUtils.paint("  ── Embed Builder ───────────────────", "#6c757d"))
embed = Discord.make_embed(
    title="c4rlib 2.0.0",
    description="Un modulo Python muy completo",
    color="#5865F2",
    fields=[
        Discord.make_field("Version", "2.0.0", inline=True),
        Discord.make_field("Author",  "c4r",   inline=True),
    ],
    footer="c4rlib — pip install c4rlib",
    timestamp=True
)
print(f"  embed keys:       {list(embed.keys())}")
print(f"  embed color:      {embed['color']} (int de #5865F2)")
print(f"  embed fields:     {embed['fields']}")
print()

Console.pause()
Console.clear()


print(Banner.section("SPINNERS — 25 ESTILOS", color="#00ccff"))
print()

todos = list(Spinner.STYLES.keys())
for estilo in todos:
    sp = Spinner(f"  estilo: {estilo}", style=estilo, color="#00ccff", interval=0.08)
    sp.start()
    time.sleep(1.0)
    sp.stop(f"  {Gradient.aurora(estilo)} — OK")

print()
Console.pause()
Console.clear()


print(Banner.section("PROGRESS BARS — 14 ESTILOS", color="#00ccff"))
print()

todos_bar = list(ProgressBar.STYLES.keys())
for estilo in todos_bar:
    bar = ProgressBar(total=50, label=f"  [{estilo:<10}]", style=estilo, color="#00ccff", width=35)
    for _ in range(50):
        time.sleep(0.01)
        bar.update(1)
    bar.finish(f"{estilo} completado")
    time.sleep(0.2)

print()
Console.pause()
Console.clear()


print(Banner.section("TABLES", color="#00ccff"))
print()

t1 = Table(
    headers=["Modulo", "Clases", "Metodos", "Status"],
    title="c4rlib 2.0.0 — MODULOS",
    header_color="#ffd60a",
    border_color="#6c757d"
)
t1.add_rows([
    ["colors",  "ColorUtils, Gradient, GradientPresets", "30+",  "✔ OK"],
    ["logger",  "Logger",                                "25+",  "✔ OK"],
    ["banners", "Box, Banner",                           "25+",  "✔ OK"],
    ["text",    "TextStyle",                             "30+",  "✔ OK"],
    ["utils",   "Utils",                                 "35+",  "✔ OK"],
    ["console", "Spinner, ProgressBar, Table, Console",  "40+",  "✔ OK"],
    ["http",    "Http, Response",                        "15+",  "✔ OK"],
    ["crypto",  "Crypto",                                "30+",  "✔ OK"],
    ["files",   "Files",                                 "35+",  "✔ OK"],
    ["discord", "Discord",                               "40+",  "✔ OK"],
])
t1.print()
print()

t2 = Table(
    headers=["Name", "Score", "Level", "Status"],
    title="LEADERBOARD",
    header_color="#9b5de5",
    border_color="#00ccff",
    align="center"
)
t2.add_rows([
    ["c4r",     "99999", "MAX", "👑 Winner"],
    ["Alice",   "8420",  "S+",  "✔ Pass"],
    ["Bob",     "7310",  "A",   "✔ Pass"],
    ["Charlie", "4120",  "B",   "✔ Pass"],
    ["Dave",    "1050",  "D",   "✘ Fail"],
])
t2.print()
print()

Console.pause()
Console.clear()


print(Banner.section("CONSOLE EXTRAS", color="#00ccff"))
print()

w, h = Console.size()
print(f"  terminal size:    {ColorUtils.paint(str(w), '#00ccff')} x {ColorUtils.paint(str(h), '#00ccff')} chars")
print(f"  width:            {Console.width()}")
print(f"  height:           {Console.height()}")
print()

Console.rule(char="─", color="#6c757d")
Console.rule(char="═", color="#9b5de5")
Console.rule(char="━", color="#00ccff")
Console.gradient_rule(start=(0,200,255), end=(200,0,255))
print()

print(ColorUtils.paint("  typewriter effect:", "#ffd60a"))
Console.typewriter("  Escribiendo letra por letra con efecto maquina de escribir...", delay=0.025, color="#00ccff")
print()

print(ColorUtils.paint("  countdown:", "#ffd60a"))
Console.countdown(3, text="  Demo terminando en", color="#FF4444")
print()


Console.gradient_rule(start=(0,200,255), end=(200,0,255))
print()
print(Banner.gradient_title("  GRACIAS POR USAR c4rlib 2.0.0  ", start=(0,200,255), end=(200,0,255)))
print()
print("  " + Gradient.aurora("pip install c4rlib"))
print("  " + ColorUtils.paint("github.com/c4r/c4rlib", "#6c757d"))
print()
Console.gradient_rule(start=(200,0,255), end=(0,200,255))