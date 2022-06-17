from hashlib import algorithms_available
from time import sleep
import pygame
from Colors  import Colors
from GenerateDataset import GenerateDataset
pygame.init()

class VisualGraphic:
    
    def __init__(self, algorithm_name, min_dataset_value, max_dataset_value, number_of_elements_in_dataset, width = 1024, height = 720, background_color = Colors.WHITE):
        self.__width = width
        self.__height = height
        self.__background_color = background_color
        self.__algorithm_name = algorithm_name
        self.__min_dataset_value = min_dataset_value
        self.__max_dataset_value = max_dataset_value
        self.__number_of_elements_in_dataset = number_of_elements_in_dataset
        self.__initial_dataset = self.__generate_new_dataset()
        self.__current_dataset = self.__initial_dataset
        self.__gradients = [
            Colors.LIGHT_GREY,
            Colors.GREY,
            Colors.DARK_GREY
        ]


    def run(self):
        run = True
        sorting = False
        ascending = True
        self.__build()
        clock = pygame.time.Clock()
        
        while run:
            clock.tick(60) #fps
            self.__init_screen()

            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    run = False

                if(event.type != pygame.KEYDOWN):
                    continue

                if(event.key == pygame.K_r):
                    self.__current_dataset = self.__initial_dataset
                    sorting = False
                elif(event.key == pygame.K_n):
                    self.__initial_dataset = self.__generate_new_dataset()
                    self.__current_dataset = self.__initial_dataset
                    sorting = False
                elif(event.key == pygame.K_s):
                    self.__save_unsorted_dataset_on_file() 
                elif(event.key == pygame.K_SPACE and not sorting):
                    sorting = True
                elif(event.key == pygame.K_a and not sorting and not ascending):
                    ascending = True
                elif(event.key == pygame.K_d and not sorting and ascending):
                    ascending = False
                elif(event.key == pygame.K_0):
                    self.__algorithm_name = "Bubble sort"
                elif(event.key == pygame.K_1):
                    self.__algorithm_name = "Insertion sort"
                elif(event.key == pygame.K_2):
                    self.__algorithm_name = "Selection sort"

        pygame.quit()


    def __build(self):
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption(f"{self.__algorithm_name} Algorithm Visualization")

        self.__font_smaller = pygame.font.SysFont('comicsans', 25)
        self.__font_bigger = pygame.font.SysFont('comicsans', 30)

        self.__side_padding = self.__width * 8 / 100
        self.__top_padding = self.__height * 30 / 100

        self.__bar_width_size = (self.__width - self.__side_padding) / self.__number_of_elements_in_dataset
        self.__bar_height_size = (self.__height - self.__top_padding) / (self.__max_dataset_value - self.__min_dataset_value)
        self.__bar_start_coordinate_x = self.__side_padding // 2


    def __generate_new_dataset(self):
        dataset_generator = GenerateDataset(self.__number_of_elements_in_dataset, self.__max_dataset_value, self.__min_dataset_value)
        return dataset_generator.generate_random_dataset()


    def __init_screen(self):
        self.__screen.fill((self.__background_color)) #fill all screen with this color

        execution_info = self.__font_smaller.render(f"Algorithm name: {self.__algorithm_name} - Dataset size: {self.__number_of_elements_in_dataset} - Comparisons: {0}", 1, Colors.BLACK)
        self.__screen.blit(execution_info, (self.__width/2 - execution_info.get_width()/2, self.__height*0.02))

        organization_info = self.__font_bigger.render("RESET: R | NEW: N | SORT: SPACE | SAVE DATASET: S | ASCENDING: A | DESCENDING: D", 1, Colors.BLACK)
        self.__screen.blit(organization_info, (self.__width/2 - organization_info.get_width()/2, self.__height*0.08))

        sorting_algorithm_info = self.__font_bigger.render("BUBBLE: 0 | INSERTION: 1 | SELECTION: 2", 1, Colors.BLACK)
        self.__screen.blit(sorting_algorithm_info, (self.__width/2 - sorting_algorithm_info.get_width()/2, self.__height*0.14))

        self.__draw_dataset()
        pygame.display.update()


    def __draw_dataset(self):
        for index, value in enumerate(self.__current_dataset):
            bar_coordinate_x = self.__bar_start_coordinate_x + index * self.__bar_width_size
            bar_coordinate_y = self.__height - (value - self.__min_dataset_value) * self.__bar_height_size
            current_bar_color = self.__gradients[index % 3]

            pygame.draw.rect(self.__screen, current_bar_color, (bar_coordinate_x, bar_coordinate_y, self.__bar_width_size, self.__height))

    def __save_unsorted_dataset_on_file(self):
        with open("random_file.dat", "w") as output_file:
            for value in self.__initial_dataset:
                output_file.write(f"{value}\n")


test = VisualGraphic("Bubble Sort", 1, 200, 100)
test.run()
#print(Colors.WHITE)