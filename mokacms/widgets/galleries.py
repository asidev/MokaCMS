__version__ = 1
__labels__ = [
    {"language": "it", "name": "Galleria Immagini"},
    {"language": "en", "name": "Image Gallery"}
]
__all__ = ['latest',]


def latest(request, limit=20):
    return [
        {
            "name": "gallery"
        },
        {
            "name": "gallery2"
        }
    ]
