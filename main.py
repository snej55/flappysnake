import pygame, moderngl, array, time, random, math

from src.util import *
from src.snake import Snake

pygame.init()

WIDTH, HEIGHT = 640, 640
SCALE = 1

class App:
    def __init__(self):
        # sanity test
        print(f"Running from {get_script_path()}")

        # make sure pygame and gl play nice on mac
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        # update this stuff on resizing
        self.display = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF)
        self.screen = pygame.Surface((WIDTH // SCALE, HEIGHT // SCALE))
        
        # moderngl (type annotations for lsp)
        self.ctx: moderngl.Context = None
        self.prog: moderngl.Program = None
        self.vbo = None
        self.vao = None
        self.setup_gl()
        self.setup_framebuffer()
        
        self.clock = pygame.time.Clock()

        self.dt = 1
        self.last_time = time.time() - 1/60
        
        self.assets = {}

        self.snake = Snake([500, 50])
    
    def create_prog(self, vert_path, frag_path):
        vert_src = ""
        frag_src = ""
        with open(get_script_path() + vert_path, "r") as f:
            vert_src = f.read()
        with open(get_script_path() + frag_path, "r") as f:
            frag_src = f.read()
        
        return self.ctx.program(
            vertex_shader=vert_src,
            fragment_shader=frag_src
        )
    
    def setup_gl(self):
        self.ctx = moderngl.create_context()
        self.prog = self.create_prog("data/shaders/screenShader.vert", "data/shaders/screenShader.frag")
        self.prog["screenTex"].value = 0

        vertices = array.array("f", [-1.0, 1.0, 0.0, 0.0, -1.0, -1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, -1.0, 1.0, 1.0])
        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, "2f 2f", "aPos", "aTexCoord")])
    
    def setup_framebuffer(self):
        self.screenTex = self.ctx.texture(self.screen.get_size(), 4)
        self.screenTex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.screenTex.swizzle = "BGRA"
        self.screenTex.repeat_x = False
        self.screenTex.repeat_y = False
        self.fbo = self.ctx.framebuffer(color_attachments=[self.screenTex])

    def setup_snake_gl(self):
        self.snake_prog = self.create_prog("data/shaders/snake.vert", "data/shaders/snake.frag")
        self.snake_prog["snakeTex"].value = 1
    
    def close(self):
        self.screenTex.release()
        pygame.quit()
        sys.exit()
    
    def update(self):
        self.snake.update()
        self.snake.draw(self.screen, [0, 0])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    self.ctx.viewport = (0, 0, width, height)
                    self.display = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF)
                    self.screen = pygame.Surface((width // SCALE, height // SCALE))
                    self.screenTex.release()
                    self.setup_framebuffer()
            
            self.dt = (time.time() - self.last_time) * 60
            self.dt = min(self.dt, 3) # if you're under 20 fps you're screwed anyway tbh
            self.last_time = time.time()
            
            self.screen.fill((100, 0, 0))
            self.update()
            self.screenTex.write(self.screen.get_view('1'))
            self.screenTex.use(0)

            self.ctx.clear(0, 0, 0)
            self.vao.render(moderngl.TRIANGLE_STRIP)

            pygame.display.flip()
            pygame.display.set_caption("Flappy Snake")
            self.clock.tick(60)

if __name__ == "__main__":
    App().run()