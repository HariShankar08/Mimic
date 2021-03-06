import random
import string
import pickle


class MarkovModel:

    def __init__(self):
        self.model = None

    def learn(self, tokens, n=2):
        model = {}

        for i in range(0, len(tokens) - n):
            gram = tuple(tokens[i:i + n])
            token = tokens[i + n]

            if gram in model:
                model[gram].append(token)
            else:
                model[gram] = [token]

        final_gram = tuple(tokens[len(tokens) - n:])
        if final_gram in model:
            model[final_gram].append("#END#")
        else:
            model[final_gram] = ["#END#"]
        self.model = model
        return model

    def generate(self, n=2, seed=None, max_tokens=100):
        if seed is None:
            seed = random.choice(list(self.model.keys()))

        output = list(seed)
        output[0] = output[0].capitalize()
        current = seed

        for i in range(n, max_tokens):
            # get next possible set of words from the seed word
            if current in self.model:
                possible_transitions = self.model[current]
                choice = random.choice(possible_transitions)
                if choice is "#END#": break

                # check if choice is period and if so append to previous element
                if choice == '.':
                    output[-1] = output[-1] + choice
                else:
                    output.append(choice)
                current = tuple(output[-n:])
            else:
                # should return ending punctuation of some sort
                if current not in string.punctuation:
                    output.append('.')
        return output

    def load_model(self, model_path):
        model_in = open(model_path, "rb")
        self.model = pickle.load(model_in)

    def save_model(self, save_path):
        model_out = open(save_path, "wb")
        pickle.dump(self.model, model_out)
