from py_simple_logging import log, FileLogWidget, ConsoleLogWidget, PyGameLogWidget
import time
import pygame
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
def main():  
  pygame.init()
  pygame.display.set_mode((int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
  pygame.display.set_caption("SWARM")
  screen = pygame.display.get_surface()
  log.add_widget(PyGameLogWidget(pygame=pygame, font=pygame.font.SysFont('Cascadia', 16), font_size=16, canvas=screen))
  log.add_widget(FileLogWidget())
  log.add_widget(ConsoleLogWidget())
  count = 0
  while True:
    pos = log.i("test", "Test {count}", flush=False)
    pos = log.s("test", "Test {count}", pos=pos, flush=False)
    pos = log.w("test", "Test {count}", pos=pos, flush=False)
    pos = log.e("test", "Test {count}", pos=pos, flush=False)
    pos = log.d("test", "Test {count}", pos=pos, flush=False)
    sceneClock = pygame.time.Clock()
    screen_delay = sceneClock.tick()
    screen.fill((0,0,0))
    log.flush()
    pygame.display.flip()
    # time.sleep(0.1)
    
if __name__ == '__main__':
  main()