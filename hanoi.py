import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class Disco:
    def __init__(self, size, color, x, y):
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.width = 40 + size * 30
        self.height = 25
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)
        self.dragging = False
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
    def update_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x - self.width // 2
        self.rect.y = y

class Torre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.discos = []
        self.base_rect = pygame.Rect(x - 150, y + 200, 300, 20)
        self.pole_rect = pygame.Rect(x - 5, y - 150, 10, 350)
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.base_rect)
        pygame.draw.rect(screen, BROWN, self.pole_rect)
        
    def add_disco(self, disco):
        self.discos.append(disco)
        self.update_discos_positions()
        
    def remove_disco(self):
        if self.discos:
            return self.discos.pop()
        return None
        
    def update_discos_positions(self):
        for i, disco in enumerate(self.discos):
            disco.update_position(self.x, self.y + 175 - i * 30)
            
    def can_add_disco(self, disco):
        if not self.discos:
            return True
        return self.discos[-1].size > disco.size

class HanoiGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Torres de Hanoi")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
        self.torres = [
            Torre(200, 300),
            Torre(400, 300),
            Torre(600, 300)
        ]
        
        self.discos = []
        self.selected_disco = None
        self.selected_torre = None
        self.moves = 0
        self.game_won = False
        self.auto_mode = False
        self.auto_moves = []
        self.auto_index = 0
        self.auto_timer = 0
        self.auto_speed = 500  # milisegundos entre movimientos
        
        self.init_discos()
        
    def init_discos(self):
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        for i in range(6):
            disco = Disco(6 - i, colors[i], 200, 300 + 175 - i * 30)
            self.discos.append(disco)
            self.torres[0].add_disco(disco)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_won and not self.auto_mode:
                self.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and not self.game_won and not self.auto_mode:
                self.handle_mouse_up(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_a and not self.game_won:
                    self.toggle_auto_mode()
                elif event.key == pygame.K_UP and self.auto_mode:
                    self.auto_speed = max(100, self.auto_speed - 100)
                elif event.key == pygame.K_DOWN and self.auto_mode:
                    self.auto_speed = min(2000, self.auto_speed + 100)
                    
    def handle_mouse_down(self, pos):
        mouse_x, mouse_y = pos
        
        for torre in self.torres:
            if torre.discos:
                top_disco = torre.discos[-1]
                if top_disco.rect.collidepoint(pos):
                    self.selected_disco = top_disco
                    self.selected_torre = torre
                    torre.remove_disco()
                    break
                    
    def handle_mouse_up(self, pos):
        if self.selected_disco:
            mouse_x, mouse_y = pos
            
            target_torre = None
            for torre in self.torres:
                if abs(mouse_x - torre.x) < 150:
                    target_torre = torre
                    break
                    
            if target_torre and target_torre.can_add_disco(self.selected_disco):
                target_torre.add_disco(self.selected_disco)
                if target_torre != self.selected_torre:
                    self.moves += 1
                    self.check_win()
            else:
                if self.selected_torre:
                    self.selected_torre.add_disco(self.selected_disco)
                
            self.selected_disco = None
            self.selected_torre = None
            
    def check_win(self):
        if len(self.torres[2].discos) == 6:
            self.game_won = True
            
    def solve_hanoi(self, n, origen, auxiliar, destino):
        if n == 1:
            self.auto_moves.append((origen, destino))
        else:
            self.solve_hanoi(n - 1, origen, destino, auxiliar)
            self.auto_moves.append((origen, destino))
            self.solve_hanoi(n - 1, auxiliar, origen, destino)
    
    def toggle_auto_mode(self):
        if not self.auto_mode:
            self.auto_mode = True
            self.auto_moves = []
            self.auto_index = 0
            self.auto_timer = pygame.time.get_ticks()
            self.solve_hanoi(6, 0, 1, 2)
        else:
            self.auto_mode = False
            self.auto_moves = []
            self.auto_index = 0
    
    def execute_auto_move(self):
        if self.auto_index < len(self.auto_moves):
            origen_idx, destino_idx = self.auto_moves[self.auto_index]
            origen_torre = self.torres[origen_idx]
            destino_torre = self.torres[destino_idx]
            
            if origen_torre.discos:
                disco = origen_torre.remove_disco()
                if disco:
                    destino_torre.add_disco(disco)
                    self.moves += 1
            
            self.auto_index += 1
            
            if self.auto_index >= len(self.auto_moves):
                self.check_win()
                if self.game_won:
                    self.auto_mode = False
    
    def reset_game(self):
        self.torres = [
            Torre(200, 300),
            Torre(400, 300),
            Torre(600, 300)
        ]
        self.discos = []
        self.selected_disco = None
        self.selected_torre = None
        self.moves = 0
        self.game_won = False
        self.auto_mode = False
        self.auto_moves = []
        self.auto_index = 0
        self.init_discos()
        
    def update(self):
        if self.selected_disco:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.selected_disco.update_position(mouse_x, mouse_y)
        
        if self.auto_mode and not self.game_won:
            current_time = pygame.time.get_ticks()
            if current_time - self.auto_timer >= self.auto_speed:
                self.execute_auto_move()
                self.auto_timer = current_time
            
    def draw(self):
        self.screen.fill(WHITE)
        
        for torre in self.torres:
            torre.draw(self.screen)
            
        for disco in self.discos:
            if disco != self.selected_disco:
                disco.draw(self.screen)
                
        if self.selected_disco:
            self.selected_disco.draw(self.screen)
            
        moves_text = self.font.render(f"Movimientos: {self.moves}", True, BLACK)
        self.screen.blit(moves_text, (10, 10))
        
        if self.auto_mode:
            auto_text = self.font.render("MODO AUTOMÁTICO ACTIVO", True, GREEN)
            self.screen.blit(auto_text, (10, 50))
            speed_text = self.font.render(f"Velocidad: {self.auto_speed}ms (↑↓ para cambiar)", True, BLACK)
            self.screen.blit(speed_text, (10, 90))
        else:
            instruction_text = self.font.render("Arrastra los discos. A para auto. R para reiniciar", True, BLACK)
            self.screen.blit(instruction_text, (10, 50))
        
        if self.game_won:
            win_text = self.font.render(f"¡Ganaste! Movimientos: {self.moves}", True, GREEN)
            text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(self.screen, WHITE, text_rect.inflate(20, 10))
            self.screen.blit(win_text, text_rect)
            
            restart_text = self.font.render("Presiona R para reiniciar", True, BLACK)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = HanoiGame()
    game.run()