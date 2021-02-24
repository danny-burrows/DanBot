# DanBot 
Just another discord bot.

<img height=100 src="https://i.imgur.com/0QdtDn8.png">

## Requirements & Setup
Python >=3.6, <=3.8 are required. This is due to chatterbot currently not working on anything over Python 3.8.

### 1. Python requirements...
```sh
pip install -r requirements.txt
```

### 2. wkhtmltopdf
Get wkhtmltopdf for generating cards and producing images from templates...
- Ubuntu and Debian
```sh
sudo apt install wkhtmltopdf
```

- Windows...
Install the binaries here http://wkhtmltopdf.org/.

## Useful Links
- [Imgkit](https://github.com/jarrekk/imgkit)
- [Chatterbot](https://github.com/gunthercox/ChatterBot)

## Future Plans
Some features and fixes to come...
- Replacing jinja2 templating with something more lightweight [String Templating](https://www.geeksforgeeks.org/template-class-in-python/)
- Mode for only talking to one person at a time.
- Speed fixes and improvements.
- Handling SSL disconnect errors that can cause crashes.
- ASCII dice rolls.
- Stopping DanBot responding to other bots.
- Fixing the permission mess with server info.
- Maybe finding a better host.
