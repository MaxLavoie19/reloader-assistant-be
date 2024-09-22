from scipy.stats import norm


class FitnessService:
    @staticmethod
    def get_datapoint_fitness(mean, standard_deviation, datapoint):
        abs_z_score = abs((datapoint - mean) / standard_deviation)
        left_side = norm.cdf(-abs_z_score)
        right_side = norm.cdf(abs_z_score)
        fitness = 1 - (right_side - left_side)
        return fitness
