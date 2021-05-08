import numpy as np
import tensorflow as tf
from PIL import Image

def wrap_frozen_graph(graph_def, inputs, outputs, print_graph=False):
    def _imports_graph_def():
        tf.compat.v1.import_graph_def(graph_def, name="")

    wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
    import_graph = wrapped_import.graph

    layers = [op.name for op in import_graph.get_operations()]
    if print_graph == True:
        for layer in layers:
            print(layer)
    return wrapped_import.prune(
        tf.nest.map_structure(import_graph.as_graph_element, inputs),
        tf.nest.map_structure(import_graph.as_graph_element, outputs))

def load_artist_graph(artist, model_path):
    print(f"Loading model for {artist}.")
    try: 
        with tf.io.gfile.GFile(model_path / artist / "frozen_model.pb", "rb") as f:
            graph_def = tf.compat.v1.GraphDef()
            loaded = graph_def.ParseFromString(f.read())
        frozen_func = wrap_frozen_graph(graph_def, ["placeholder/photo:0"], ["decoder/sub:0"])
    except FileNotFoundError:
        def frozen_func(x):
            return x
    return frozen_func

def artify(image, model):
    image = image.convert("RGB")
    np_image = np.asarray(image)
    input_image = (
        tf.expand_dims(tf.constant(np_image, dtype=tf.float32), 0) / 127.5 - 1.0
    )
    artified = (model(input_image)[0] + 1) * 127.5
    artified = Image.fromarray(tf.squeeze(artified, 0).numpy().astype(np.uint8))
    return artified