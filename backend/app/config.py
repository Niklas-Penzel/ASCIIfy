class Config:
    ALLOWED_EXTENSIONS = set(
        ["jpg", "png", "jpeg", "tiff", "bmp", "gif", "ppm", "pgm", "tif", "svg"]
    )
    FONT_FOLDER = "fonts"


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
