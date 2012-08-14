__version__ = 1
__labels__ = [
    {"language": "it", "name": "Novità"},
    {"language": "en", "name": "News"}
]
__all__ = ["latest"]

def latest(request, limit=20):
    return [
        {
            "name": "first"
        },
        {
            "name": "second"
        }
    ]
