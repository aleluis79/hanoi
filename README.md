# Torres de Hanoi - Juego en Pygame

Implementación interactiva del clásico puzzle de las Torres de Hanoi usando Python y Pygame.

## Descripción

El juego consiste en mover todos los discos de la torre izquierda a la torre derecha, siguiendo estas reglas:
- Solo se puede mover un disco a la vez
- Un disco más grande nunca puede estar encima de uno más pequeño
- Se pueden usar las tres torres como posiciones intermedias

## Características

- **Modo Manual**: Arrastra y suelta discos con el mouse
- **Modo Automático**: La PC resuelve el puzzle usando el algoritmo óptimo
- **Animación Fluida**: Movimientos suaves y visuales atractivos
- **Contador de Movimientos**: Seguimiento del progreso
- **Control de Velocidad**: Ajusta la velocidad de la animación automática
- **Detección de Victoria**: Notificación cuando completas el puzzle

## Requisitos

- Python 3.6+
- Pygame

## Instalación

1. Clona o descarga el repositorio
2. Instala Pygame:
```bash
pip install pygame
```

## Ejecución

```bash
python hanoi.py
```

## Controles

### Modo Manual
- **Mouse**: Arrastra y suelta discos para moverlos entre torres
- **R**: Reiniciar el juego
- **A**: Activar modo automático

### Modo Automático
- **A**: Activar/desactivar modo automático
- **↑**: Aumentar velocidad de animación
- **↓**: Disminuir velocidad de animación
- **R**: Reiniciar el juego

## Estructura del Código

### Clases Principales

- **`Disco`**: Representa cada disco individual con propiedades de tamaño, color y posición
- **`Torre`**: Maneja una torre individual, incluyendo validación de movimientos
- **`HanoiGame`**: Clase principal que gestiona el estado del juego, eventos y renderizado

### Algoritmo de Solución

El modo automático implementa el algoritmo recursivo clásico para las Torres de Hanoi:

```python
def solve_hanoi(self, n, origen, auxiliar, destino):
    if n == 1:
        self.auto_moves.append((origen, destino))
    else:
        self.solve_hanoi(n - 1, origen, destino, auxiliar)
        self.auto_moves.append((origen, destino))
        self.solve_hanoi(n - 1, auxiliar, origen, destino)
```

Este algoritmo garantiza la solución óptima en 2^n - 1 movimientos.

## Configuración

### Personalización del Juego

Puedes modificar estos parámetros en el código:

- **Número de discos**: Cambia el valor en `init_discos()`
- **Colores de los discos**: Modifica la lista `colors`
- **Velocidad de animación**: Ajusta `self.auto_speed`
- **Dimensiones de la ventana**: Modifica `WIDTH` y `HEIGHT`

### Constantes de Color

```python
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
```

## Información Matemática

Las Torres de Hanoi es un problema matemático clásico con propiedades interesantes:

- **Número mínimo de movimientos**: 2^n - 1 (donde n es el número de discos)
- **Complejidad temporal**: O(2^n)
- **Relación con números binarios**: Cada movimiento corresponde a un bit en la representación binaria

Para 6 discos (configuración actual):
- Movimientos mínimos: 63
- Tiempo estimado en modo automático (500ms por movimiento): ~31.5 segundos

## Contribuciones

¡Las contribuciones son bienvenidas! Algunas ideas para mejorar el proyecto:

- [ ] Diferentes niveles de dificultad
- [ ] Sistema de puntuación
- [ ] Efectos de sonido
- [ ] Modo multijugador
- [ ] Interfaz gráfica mejorada
- [ ] Guardar/cargar partidas

## Licencia

Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo, modificarlo y distribuirlo.

## Créditos

Creado como proyecto educativo para demostrar conceptos de programación, algoritmos recursivos y desarrollo de juegos con Pygame.