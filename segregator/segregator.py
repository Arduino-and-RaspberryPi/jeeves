from core.strategies import strategies
from grammifier.grammifier import Grammifier
from strategist.strategist import Strategist
from time import strftime
from utils.say import say

import nltk

times = {
    "morning": xrange(0, 12),
    "afternoon": xrange(12, 16),
    "evening": xrange(16, 20),
    "night": xrange(20, 24)
}

class Segregator:
    def __init__(self, sentence):
        self.words = nltk.word_tokenize(sentence)

    def check_if_greeting(self):
        greetings = ['morning', 'afternoon', 'evening', 'night']

        for greeting in greetings:
            if greeting in self.words:
                self.react(greeting)
                return True

        return False

    def react(self, greeting):
        time_of_day = int(strftime("%H"))

        if time_of_day not in times[greeting]:
            say("Actually, its...")

        for key in times.keys():
            if time_of_day in times[key]:
                say("Good %s" % key)
                break

    def segregate_and_react(self):
        if not self.check_if_greeting():
            grammifier = Grammifier(self.words)

            print("Referrer is %s" % grammifier.get_referrer())
            mental_state = grammifier.get_stemmed_mental_state()
            action_type = grammifier.get_action_type()

            strategist = Strategist(strategies)
            strategist.get_strategy_for(mental_state, action_type)
