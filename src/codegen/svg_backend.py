# codegen/svg_backend.py
# Backend SVG: genera un diagrama del workflow (grafo dirigido de estados con
# guardias en las aristas) directamente desde la IR, sin dependencias
# externas. Cumple dos requisitos del curso: las imagenes de los entregables
# deben estar en SVG, y el profesor pidio "un diagrama del flujo completo con
# este lenguaje".
#
# Layout: por capas (estilo Sugiyama simplificado)
#   1. Cada estado recibe una capa = longitud del camino mas largo desde
#      `start` (calculada sobre el DAG que resulta de ignorar aristas de
#      retroceso), de modo que las aristas normales siempre bajan.
#   2. `end` se fuerza a la ultima capa.
#   3. Dentro de una capa los nodos se ordenan por el promedio de la posicion
#      de sus predecesores (reduccion simple de cruces) y se centran.
#   4. Aristas hacia abajo: curvas Bezier; aristas de retroceso: rodean por
#      el lateral. La guardia se dibuja como etiqueta sobre la arista.
import html

from model import START, END

# --- estetica -------------------------------------------------------------
FONT = "Segoe UI, Helvetica, Arial, sans-serif"
FONT_SIZE = 13
CHAR_W = 7.3          # ancho estimado por caracter
NODE_H = 36
PAD_X = 16
LAYER_GAP = 84
NODE_GAP = 46
MARGIN = 36

COLORS = {
    "start": {"fill": "#e8f5e9", "stroke": "#2e7d32", "text": "#1b5e20"},
    "end":   {"fill": "#ffebee", "stroke": "#c62828", "text": "#b71c1c"},
    "state": {"fill": "#e3f2fd", "stroke": "#1565c0", "text": "#0d47a1"},
}
EDGE_COLOR = "#546e7a"
LABEL_COLOR = "#37474f"
LABEL_BG = "#ffffff"


def _node_width(name):
    return max(72, int(len(name) * CHAR_W) + 2 * PAD_X)


def _layers(wf):
    """Asigna capa a cada estado: camino mas largo desde start sobre el DAG
    (las aristas que cierran ciclos se ignoran para el layout)."""
    estados = wf.orden_estados()
    idx = {s: i for i, s in enumerate(estados)}
    succ = {s: [] for s in estados}
    for t in wf.transiciones:
        succ[t.origen].append(t.destino)

    # deteccion de aristas de retroceso con DFS
    back = set()
    color = {s: 0 for s in estados}  # 0 blanco, 1 gris, 2 negro

    def dfs(u):
        color[u] = 1
        for v in succ[u]:
            if color[v] == 1:
                back.add((u, v))
            elif color[v] == 0:
                dfs(v)
        color[u] = 2

    if START in color:
        dfs(START)
    for s in estados:
        if color[s] == 0:
            dfs(s)

    # capas por camino mas largo (orden topologico por relajaciones)
    layer = {s: 0 for s in estados}
    for _ in range(len(estados)):
        changed = False
        for t in wf.transiciones:
            if (t.origen, t.destino) in back:
                continue
            if layer[t.destino] < layer[t.origen] + 1:
                layer[t.destino] = layer[t.origen] + 1
                changed = True
        if not changed:
            break

    if END in layer:
        layer[END] = max(layer.values()) + (0 if layer[END] == max(layer.values()) else 0)
        layer[END] = max(layer.values())

    # agrupar por capa, orden estable por baricentro de predecesores
    by_layer = {}
    for s in estados:
        by_layer.setdefault(layer[s], []).append(s)
    pos_prev = {}
    for lv in sorted(by_layer):
        nodes = by_layer[lv]

        def key(s):
            preds = [pos_prev[t.origen] for t in wf.transiciones
                     if t.destino == s and t.origen in pos_prev]
            return (sum(preds) / len(preds) if preds else idx[s], idx[s])

        nodes.sort(key=key)
        for i, s in enumerate(nodes):
            pos_prev[s] = i
    return by_layer, back


def _esc(s):
    return html.escape(str(s), quote=True)


def generate(wf, title=None):
    """Genera el documento SVG del diagrama de `wf`."""
    by_layer, back = _layers(wf)

    # coordenadas de nodos
    widths = {s: _node_width(s) for s in wf.estados}
    layer_widths = {
        lv: sum(widths[s] for s in nodes) + NODE_GAP * (len(nodes) - 1)
        for lv, nodes in by_layer.items()
    }
    canvas_w = max(layer_widths.values()) + 2 * MARGIN + 60  # espacio lateral p/ retrocesos
    pos = {}
    for lv, nodes in sorted(by_layer.items()):
        x = (canvas_w - layer_widths[lv]) / 2
        y = MARGIN + 30 + lv * (NODE_H + LAYER_GAP)
        for s in nodes:
            pos[s] = (x, y, widths[s])
            x += widths[s] + NODE_GAP
    canvas_h = MARGIN + 30 + (max(by_layer) + 1) * (NODE_H + LAYER_GAP) - LAYER_GAP + MARGIN

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w:.0f}" '
        f'height="{canvas_h:.0f}" viewBox="0 0 {canvas_w:.0f} {canvas_h:.0f}" '
        f'font-family="{FONT}" font-size="{FONT_SIZE}">')
    out.append(
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{EDGE_COLOR}"/></marker></defs>')
    out.append(f'<rect width="100%" height="100%" fill="#fafafa"/>')

    if title:
        out.append(
            f'<text x="{canvas_w / 2:.0f}" y="{MARGIN - 8}" text-anchor="middle" '
            f'font-size="16" font-weight="bold" fill="#263238">{_esc(title)}</text>')

    # --- aristas ---
    label_slots = {}
    for t in wf.transiciones:
        x1, y1, w1 = pos[t.origen]
        x2, y2, w2 = pos[t.destino]
        sx, sy = x1 + w1 / 2, y1 + NODE_H
        tx, ty = x2 + w2 / 2, y2

        if (t.origen, t.destino) in back or y2 <= y1:
            # arista de retroceso o lateral: rodear por la derecha
            side = canvas_w - MARGIN / 2
            sx2, sy2 = x1 + w1, y1 + NODE_H / 2
            tx2, ty2 = x2 + w2, y2 + NODE_H / 2
            path = (f"M {sx2:.0f} {sy2:.0f} C {side:.0f} {sy2:.0f}, "
                    f"{side:.0f} {ty2:.0f}, {tx2 + 4:.0f} {ty2:.0f}")
            lx, ly = side - 6, (sy2 + ty2) / 2
            anchor = "end"
        else:
            bend = (ty - sy) * 0.4
            path = (f"M {sx:.0f} {sy:.0f} C {sx:.0f} {sy + bend:.0f}, "
                    f"{tx:.0f} {ty - bend:.0f}, {tx:.0f} {ty - 3:.0f}")
            lx, ly = (sx + tx) / 2, (sy + ty) / 2
            anchor = "middle"

        out.append(
            f'<path d="{path}" fill="none" stroke="{EDGE_COLOR}" '
            f'stroke-width="1.6" marker-end="url(#arrow)"/>')

        if t.condicion is not None:
            label = f"if {t.condicion}"
            # evitar solapamiento de etiquetas en el mismo punto medio
            slot = label_slots.get((round(lx), round(ly)), 0)
            label_slots[(round(lx), round(ly))] = slot + 1
            ly += slot * (FONT_SIZE + 4)
            tw = len(label) * (CHAR_W - 1.1) + 8
            bx = lx - (tw if anchor == "end" else tw / 2)
            out.append(
                f'<rect x="{bx:.0f}" y="{ly - FONT_SIZE + 2:.0f}" width="{tw:.0f}" '
                f'height="{FONT_SIZE + 5}" rx="4" fill="{LABEL_BG}" '
                f'stroke="{EDGE_COLOR}" stroke-width="0.6" opacity="0.95"/>')
            out.append(
                f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" '
                f'font-size="{FONT_SIZE - 1}" font-style="italic" '
                f'fill="{LABEL_COLOR}">{_esc(label)}</text>')

    # --- nodos ---
    for s, (x, y, w) in pos.items():
        kind = "start" if s == START else "end" if s == END else "state"
        c = COLORS[kind]
        rx = NODE_H / 2 if kind in ("start", "end") else 8
        out.append(
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{NODE_H}" '
            f'rx="{rx}" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.8"/>')
        out.append(
            f'<text x="{x + w / 2:.0f}" y="{y + NODE_H / 2 + 4.5:.0f}" '
            f'text-anchor="middle" font-weight="600" '
            f'fill="{c["text"]}">{_esc(s)}</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"
