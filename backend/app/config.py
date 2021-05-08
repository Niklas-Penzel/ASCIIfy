class Config:
    ALLOWED_EXTENSIONS = set(
        ["jpg", "png", "jpeg", "tiff", "bmp", "gif", "ppm", "pgm", "tif", "svg"]
    )
    FONT_FOLDER = "fonts"
    MODEL_FOLDER = "models"
    ARTISTS = [
        "cezanne",
        "monet",
        "el-greco",
        "gauguin",
        "kandinsky",
        "kirchner",
        "morisot",
        "munch",
        "peploe",
        "picasso",
        "pollock",
        "roerich",
        "van-gogh",
    ]


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
