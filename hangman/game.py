from .exceptions import *
from random import choice


class GuessAttempt:
    def __init__(self, letter, hit=False, miss=False):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt("The provided letter cannot be a hit and a miss")
      
    def is_hit(self):
        return self.hit
        
    def is_miss(self):
        return self.miss


class GuessWord:
    def __init__(self, answer):
        if not answer:
            raise InvalidWordException("Please provide a word to guess.")
        self.answer = answer
        self.masked = '*' * len(answer)
        
    def perform_attempt(self, letter):
        if not letter.isalpha():
            raise InvalidGuessAttempt("Invalid guess. Please only guess alphabetic characters")
            
        letter = letter.lower()
        game_word = self.answer.lower()
        masked = ''
            
        if len(letter) > 1:
            raise InvalidGuessedLetterException("You guessed {n_letters} letters. Only 1 letter per guess is accepted.".format(n_letters=len(letter)))
            
        if letter in game_word:
            for i, char in enumerate(game_word):
                if letter == char:
                    masked += letter
                else:
                    masked += self.masked[i]
                        
            self.masked = masked
                
            return GuessAttempt(letter, hit=True)
        return GuessAttempt(letter, miss=True)

class HangmanGame:
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        self.word_list = HangmanGame.WORD_LIST if not word_list else word_list
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word((self.word_list)))
        
    @classmethod
    def select_random_word(cls, words):
        if not words:
            raise InvalidListOfWordsException("A list of words must be provided to play the game.")
        return choice(words)
        
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException("Game Over.")
        
        guessed_letter = letter.lower()
        your_guess = self.word.perform_attempt(guessed_letter)
        
        if your_guess.is_miss():
            self.remaining_misses -= 1
        if letter not in self.previous_guesses:
            self.previous_guesses.append(guessed_letter)
            
        if self.is_won():
            raise GameWonException()
        
        if self.is_lost():
            raise GameLostException()
        
        return your_guess
    
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def is_won(self):
        return self.word.answer == self.word.masked and self.remaining_misses > 1
    
    def is_lost(self):
        return self.remaining_misses < 1 and self.word.answer != self.word.masked   
    
