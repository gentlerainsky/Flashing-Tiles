# Flashing Tiles

This is an attempt to implement "Steady State Visual Potential" experiment using Python. There are 2 associated folders.

1. `pygame/` is implemented using [Pygame](https://github.com/pygame/pygame) as modeled from [gumpy-paradigms](https://github.com/gumpy-bci/gumpy-paradigms) However the update
rate (frame rate) of Pygame is so slow that cause flickering rate too slow as shown in the report as high average error(%).
 
```
On Exit Report
Tile with 6.00 hz:
Average Error: 66.16%
Average Checking Period: 0.10 ms
Tile with 6.57 hz:
Average Error: 80.91%
Average Checking Period: 0.10 ms
Tile with 7.50 hz:
Average Error: 4.39%
Average Checking Period: 0.07 ms
Tile with 8.57 hz:
Average Error: 19.28%
Average Checking Period: 0.07 ms
```

2. `kivy/` is implemented using [Kivy](https://github.com/kivy/kivy). Kivy provides `schedule_interval` that is easier
to implement than Pygame and also provide faster update rate. The error rate is significantly lower.

```
On Exit Report
Tile with 6.00 hz:
Average Error: 0.41%
Average FPS: 76.19 fps
Tile with 6.57 hz:
Average Error: -3.46%
Average FPS: 76.26 fps
Tile with 7.50 hz:
Average Error: 0.59%
Average FPS: 76.28 fps
Tile with 8.57 hz:
Average Error: -3.97%
Average FPS: 76.17 fps
```

Note: *Positive* average error denotes that the rates is *slower* while *negative* average error denote that the rate is *faster* than the specify frequency.
