class AStar:
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    MAZE_DIRECTIONS = [(-2, 0), (2, 0), (0, -2), (0, 2)]


class Clusterization:
    MIN_CLUSTERS: int = 2
    MAX_CLUSTERS: int = 6
    EPS: int = 32


class Genetic:
    POPULATION_SIZE: int = 100
    GENERATIONS: int = 500
    ELITE_SIZE: int = 10
    MUTATION_RATE: float = 0.02
    MARGIN: int = 40
    DEFAULT_WIDTH: int = 500
    DEFAULT_HEIGHT: int = 350


class AntColony:
    EVAPORATION: float = 0.5
    Q: int = 100
    DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    NUM_ANTS: int = 50
    EPS: int = 100


class Tree:
    ...


class NeuralNetwork:
    HEIGHT:int = 28
    WIDTH:int = 28


class Config:
    a_star = AStar()
    clusterization = Clusterization()
    genetic = Genetic()
    ant_colony = AntColony()
    tree = Tree()
    neural_network = NeuralNetwork()


config = Config()
