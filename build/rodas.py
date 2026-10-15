"""Rodas completas para a tela de carregamento (o logo corta as rodas na linha do texto)."""
import math
CY, R = 432, 165
def roda(cx, cor):
    raios = ''.join(
        f'<path d="M{cx+30*math.cos(a):.1f},{CY+30*math.sin(a):.1f} L{cx+122*math.cos(a-.09):.1f},{CY+122*math.sin(a-.09):.1f} L{cx+122*math.cos(a+.09):.1f},{CY+122*math.sin(a+.09):.1f} Z"/>'
        for a in (math.radians(k * 72 - 90) for k in range(5)))
    return (f'<circle cx="{cx}" cy="{CY}" r="{R-20}" fill="none" stroke="{cor}" stroke-width="40"/>'
            f'<g class="sl-spin" fill="{cor}"><circle cx="{cx}" cy="{CY}" r="125" fill="none"/>'
            f'<circle cx="{cx}" cy="{CY}" r="84" fill="none" stroke="{cor}" stroke-width="9"/>{raios}'
            f'<circle cx="{cx}" cy="{CY}" r="30"/></g>')
def rodas(cor='#EEF2F8'):
    return (f'<svg class="sl-wheels" viewBox="570 18 1050 425" aria-hidden="true">{roda(784, cor)}{roda(1443, cor)}</svg>')
