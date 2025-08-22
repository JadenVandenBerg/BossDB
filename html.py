import os
import json
import re

def sanitize_filename(name):
    return re.sub(r'[/\\]', '', name)  # Remove slashes from boss names

def sanitize_game_name(name):
    return name.replace(':', ' -')  # Replace colons with hyphens and add space before

def create_folders():
    os.makedirs("HTML/games", exist_ok=True)
    os.makedirs("HTML/bosses", exist_ok=True)

def generate_index_html(games):
    sorted_games = sorted(games)
    content = """
    <html>
    <head>
        <title>Game Bosses</title>
        <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body class="flex">
        <div id="sidebar">
            <h1>Game Bosses</h1>
            <ul>
    """
    for game in sorted_games:
        sanitized_game = sanitize_game_name(game)
        content += f'<li><a href="games/{sanitized_game}.html">{game}</a></li>\n'
    content += """
            </ul>
        </div>
        <div id="main">
            <h2>Welcome to the Game Bosses Database</h2>
            <p>Select a game from the sidebar to see its bosses.</p>
        </div>
    </body>
    </html>
    """
    
    with open("HTML/index.html", "w", encoding="utf-8") as f:
        f.write(content)

def generate_game_pages(game, bosses):
    sanitized_game = sanitize_game_name(game)
    content = f"""
    <html>
    <head>
        <title>{game} Bosses</title>
        <link rel="stylesheet" type="text/css" href="../../style.css">
    </head>
    <body>
        <h1>{game} Bosses</h1>
        <div id="gridContainer">
    """
    for boss, details in bosses.items():
        sanitized_boss = sanitize_filename(boss)
        content += f"""<a class="gridItem" href="../bosses/{sanitized_boss}.html"><div style="background: url('{details['img']}') center center no-repeat; background-size: cover;"><p>{boss}</p></div></a>\n"""
    content += """
        </div>
    </body>
    </html>
    """
    
    with open(f"HTML/games/{sanitized_game}.html", "w", encoding="utf-8") as f:
        f.write(content)

def generate_boss_pages(boss, details):
    sanitized_boss = sanitize_filename(boss)
    content = f"""
    <html>
    <head>
        <title>{details['boss']}</title>
        <link rel="stylesheet" type="text/css" href="../style.css">
    </head>
    <body>
        <div id="main">
            <h1>{details['boss']}</h1>
            <iframe width="560" height="315" src="{details['embedSRC']}" frameborder="0" allowfullscreen></iframe>
        </div>
    </body>
    </html>
    """
    
    with open(f"HTML/bosses/{sanitized_boss}.html", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    create_folders()
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    generate_index_html(data.keys())
    
    for game in sorted(data.keys()):
        generate_game_pages(game, data[game])
        for boss, details in data[game].items():
            generate_boss_pages(boss, details)

if __name__ == "__main__":
    main()
