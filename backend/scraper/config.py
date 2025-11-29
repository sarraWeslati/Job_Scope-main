import random

# Liste d'exemples d'user-agents. Vous pouvez étendre cette liste ou la charger depuis un fichier.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
]

# Liste de proxies au format 'http://user:pass@host:port' ou 'http://host:port'.
# Laisser vide si pas de proxy disponible.
PROXIES = []
# Exemple de proxies (décommentez et remplacez par vos proxies réels si disponibles) :
# PROXIES = [
#     'http://user:pass@12.34.56.78:8000',
#     'http://23.45.67.89:3128',
# ]


def random_ua():
    return random.choice(USER_AGENTS)


def random_proxy():
    if not PROXIES:
        return None
    return random.choice(PROXIES)
