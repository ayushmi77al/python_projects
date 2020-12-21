# importing random module to generate values
import random

choose = {1: '✊', 2: '🖐', 3: '✌'}

# validating that input should be only +ve integer
try:
    chance = int(input('How many chances do you want to play: '))
    if type(chance) != 'int' and chance < 0:
        raise ValueError
except:
    print('Enter only positive integer -ve integer converted to +ve.')
    chance = abs(chance)

# initial score is zero
computer_score = palyer_score = 0

while chance != 0:

    # computer's choice
    computer = random.choice(['✊', '🖐', '✌'])

    # checking if user enter right value
    try:
        player = choose[int(input(
            '\nEnter your choice:\n(a) 1 for Stone(✊)\n(b) 2 for Paper(🖐 )\n(c) 3 for Scissor(✌ )\n'))]
    except:
        print('\nWrong input!!!\nPlease enter 1, 2 or 3')
        continue

    if computer == player:
        pass
    elif computer == '✊' and player == '✌':
        computer_score += 1
    elif computer == '✌' and player == '🖐':
        computer_score += 1
    elif computer == '🖐' and player == '✊':
        computer_score += 1
    else:
        palyer_score += 1

    chance -= 1

    print(f'Computer -> {computer}\tPlayer -> {player} ')
    print(
        f"Your score: {palyer_score} \tComputer's score: {computer_score}\n{chance} chance left:")

# declaring result
if palyer_score != computer_score:
    print('You\'re winner:)') if palyer_score > computer_score else print(
        'Computer is winner:(\n\n')
else:
    print('Match is tie ¯\_(ツ)_/¯\n\n')

print('Thanks for playing:)')
