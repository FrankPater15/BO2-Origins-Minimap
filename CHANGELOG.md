# Cambios

La numeración sigue las versiones internas de desarrollo: `0.18.0` es la versión 18.

## 0.25.0 (2026-11-24)

Primera versión estable.

- El generador en peligro se dibuja por encima de los zombis
- Nombres del mapa grande más legibles y con el fondo ajustado
- Piso alto de la cripta sin puntas
- El centro del laboratorio también se ilumina

### Sin comprobar

- Cooperativo

### Limitaciones

- El piso alto de la cripta es aproximado

## 0.24.0-beta (2026-11-24)

Probada con un recorrido automático por 22 puntos del mapa.

- Iglesia completa y separada por pisos
- Piso alto de la cripta con bordes más suaves
- Nombres por encima de las líneas en el mapa grande
- Leyenda más corta y con los dibujos de bastón y portal
- `pruebas/recorrido.gsc`: recorrido automático para probar el minimapa

### Visto en el juego

- Cuevas, cripta, iglesia, laboratorio, G1, búnker y Crazy Place
- Ataque a generadores: aviso, icono en el borde y cambio de objetivo
- Panzer Soldat en el minimapa y en el mapa grande

### Sin comprobar

- Cooperativo

### Fallos conocidos

- Los zombis tapan el icono del generador que atacan
- El piso alto de la cripta es aproximado

## 0.23.0-beta (2026-11-24)

Probada en el juego con un video de 6 minutos.

- **0.23** Cripta en dos pisos, laboratorio y G1 separados, iglesia por pisos, cuevas limpias; nombres con línea a su lugar en el mapa grande
- **0.22** Una botella propia por ventaja
- **0.21** Estado de los generadores, aviso de ataque y pisadas según la dirección del robot; botella y caja nuevas
- **0.20** Iconos ilustrados; zombi como punto rojo y Panzer como rombo naranja

### Visto en el juego

- Mapa grande con leyenda
- Giro: en un video de la 0.19 el error bajó de 2,14° a 0,22°
- Captura de un generador (porcentaje y verde)
- Dirección de los pies de robot
- Cripta, laboratorio, G1 y búnker

### Sin comprobar

- Ataque a un generador y Panzer
- Crazy Place y cooperativo
- Iglesia por pisos

### Fallos conocidos

- En el mapa grande, las líneas pasan por encima de los nombres (corregido, saldrá en la siguiente)
- El piso alto de la cripta es aproximado y la planta alta de la iglesia está incompleta

## 0.19.0-beta (2026-11-24)

Corregido a partir de un video de la 0.18. Pendiente de probar en el juego.

- El giro de las imágenes se retrasa un cuadro para que coincida con los iconos (la corrección de la 0.15 iba en sentido contrario)
- `mm_giro 3`: retraso de dos cuadros
- La cripta se detecta también en su piso alto

Visto en el video de la 0.18: estructuras iluminadas, relieve, iconos de ventajas, generador capturado y pies de robot.

### Pendiente

- Dibujar el anillo alto de la cripta
- Probar el mapa grande y la leyenda

## 0.18.0-beta (2026-11-24)

Primera versión publicada. Desde la 0.15 no se ha probado en el juego.

- **0.18** Leyenda de iconos en el mapa grande; anillos visibles en G1–G6
- **0.17** Relieve: alturas, desniveles, rampas y sombras
- **0.16** Iconos del juego para las ventajas, derechos y sobre el resaltado; dibujo propio para la Wunderfizz
- **0.15** Estructuras detectadas por los techos reales (15 zonas); corrección del giro con `mm_giro`

### Por comprobar

- Que el mapa y las cuevas no se muevan al girar la cámara
- Mapa grande, leyenda, relieve e iconos de las ventajas
- Pies de robots, Panzer, generadores capturados y Crazy Place
- Pedestales de los bastones en la cripta
- Numeración de G3, G4 y G5
- Cooperativo

### Fallos conocidos

- Algunos nombres tapan caminos en el mapa grande
- El laboratorio y G1 se iluminan juntos; la iglesia une dos pisos
- La cueva de rayo tiene un corte recto y la de hielo un pedazo doblado
- Stamin-Up y la Wunderfizz de G5 se tocan en el mapa grande

## Anteriores, sin publicar

- **0.14** Bastones y portales; zoom en cuevas; la cripta en el mapa grande
- **0.13** Mapa grande con la tecla M; cuevas con su color
- **0.12** Iconos nuevos, nombres de los lugares, N, E, S y O. *Iconos, nombres y letras vistos en el juego*
- **0.11** Mapa trazado con la geometría del nivel
- **0.10** Mapa con más resolución y limpieza de líneas
- **0.9** Cuevas separadas
- **0.8** Movimiento suavizado
- **0.7** Zoom ajustable y generadores capturados
- **0.6** Pisadas de los robots gigantes
- **0.5** Generadores G1–G6
- **0.4** Iconos, panel de zombis y vida, resaltado de cuevas
- **0.3** Superficie y túneles
- **0.2** Flecha, marco, norte y Crazy Place
- **0.1** Primer minimapa que sigue, gira y se recorta
