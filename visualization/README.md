# Explore the threshold join

Extract the ZIP and open index.html in any modern browser. It runs offline and uses no external resources. Toggle either diagonal, then use the slider or drag the graph to see all eight cross edges. Expand the calculation to see every independent set of the join.

With neither diagonal the input has seven independent sets, with one it has six, and with both it has five. The two-vertex padding edge contributes two new nonempty sets and shares the empty set with the input. The corresponding joined counts are nine, eight and seven. The visual shows the middle case. The equality test accepts it.

The GIF is rendered by rotating the graph's 3D coordinates through 72 frames. With Python and Pillow already available, run python3 visualization/render.py from the repository root. The renderer uses Arial when available and Pillow's bundled font otherwise. Font differences may change GIF bytes.
