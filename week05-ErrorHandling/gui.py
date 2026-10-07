import pygame

class LoginInterface:
    SCREEN_WIDTH  = 500
    SCREEN_HEIGHT = 500
    BOX_WIDTH     = 400
    BOX_HEIGHT    =  40
    BUTTON_WIDTH  = 200
    BUTTON_HEIGHT =  60

    def __init__(self, backend_link):
        # This function is not overly important to your task.
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Account Login")
        pygame.init()

        self.font  = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.unlocked = False

        self.selected = None

        self.username_box = pygame.Rect((self.SCREEN_WIDTH-self.BOX_WIDTH)//2, self.SCREEN_HEIGHT//3 - self.BOX_HEIGHT//2, self.BOX_WIDTH, self.BOX_HEIGHT)
        self.password_box = pygame.Rect((self.SCREEN_WIDTH-self.BOX_WIDTH)//2, self.SCREEN_HEIGHT//2 - self.BOX_HEIGHT//2, self.BOX_WIDTH, self.BOX_HEIGHT)
        self.submit_button = pygame.Rect((self.SCREEN_WIDTH-self.BUTTON_WIDTH)//2, 3*self.SCREEN_HEIGHT//4 - self.BUTTON_HEIGHT//2, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.username = ''
        self.password = ''
        self.error_text = ''

        self.backend_link = backend_link

    def main_loop(self):
        # This function is not overly important to your task.
        while True:
            self._process_input()
            self._draw()
            self.clock.tick(60)

    def _process_input(self):
        # This function is not overly important to your task.
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
            # Typing input, box must be selected to type
            elif event.type == pygame.KEYDOWN:
                if self.selected == 'username':
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif len(self.username) < 20: #Character limit for formatting
                        self.username += event.unicode
                elif self.selected == 'password':
                    if event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    elif len(self.password) < 20: #Character limit for formatting
                        self.password += event.unicode

            # Click input
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.username_box.collidepoint(pos):
                    self.selected = 'username'
                elif self.password_box.collidepoint(pos):
                    self.selected = 'password'
                elif self.submit_button.collidepoint(pos):
                    self._submit_credentials()

    def _draw(self):
        # This function is not overly important to your task.
        self.screen.fill((230,230,220))

        if self.unlocked:
            entry_message = self.font.render('ACCESS GRANTED', True, (0,255,0))
            entry_message_box = entry_message.get_rect()
            self.screen.blit(entry_message, ((self.SCREEN_WIDTH-entry_message_box.width)//2,
                                             (self.SCREEN_HEIGHT-entry_message_box.height)//2))
        else:
            # Highlight selected input box
            if self.selected == 'username':
                pygame.draw.rect(self.screen, (255,255,255), self.username_box)
            pygame.draw.rect(self.screen, (100,100,100), self.username_box, width = 2)
            if self.selected == 'password':
                pygame.draw.rect(self.screen, (255,255,255), self.password_box)
            pygame.draw.rect(self.screen, (100,100,100), self.password_box, width = 2)

            # Submit button
            pygame.draw.rect(self.screen, (0,100,200), self.submit_button)
            pygame.draw.rect(self.screen, (100,100,100), self.submit_button, width = 2)

            
            # Text
            username_text = (self.font.render('username', True, (150,150,150)) if len(self.username) < 1 
                            else self.font.render(self.username, True, (0,0,0)))

            password_text = (self.font.render('password', True, (150,150,150)) if len(self.password) < 1 
                            else self.font.render('*'*len(self.password), True, (0,0,0)))
            
            submit_text = self.font.render('Submit', True, (255,255,255))
            submit_text_box = submit_text.get_rect()

            error_text = self.font_small.render(self.error_text, True, (255,0,0))
            error_text_box = error_text.get_rect()

            self.screen.blit(username_text, (self.username_box.left + 10, self.username_box.top + 10))
            self.screen.blit(password_text, (self.password_box.left + 10, self.password_box.top + 10))
            self.screen.blit(submit_text,   (self.submit_button.left + (self.BUTTON_WIDTH  - submit_text_box.width)  //2,
                                             self.submit_button.top + (self.BUTTON_HEIGHT - submit_text_box.height) //2 ))
            self.screen.blit(error_text,    ((self.SCREEN_WIDTH - error_text_box.width)//2,
                                             7*self.SCREEN_HEIGHT//8))
        pygame.display.update() # Border
    
    def _submit_credentials(self):
        # Function is run when submit button is pressed.
        try:
            self.backend_link(self.username, self.password)
            self.unlocked = True
        except Exception as e:
            self.error_text = str(e)
            