from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import IntPrompt,Prompt
console = Console()


class DiceColor(Enum):
    White = 0
    Orange = 1
    Green = 2
    Blue = 3
    Yellow = 4
    Purple = 5


class GameMode(Enum):
    Solo = 7
    Two = 6
    Three = 5
    Four = 4


dices = {DiceColor.White: 0,
         DiceColor.Orange: 0,
         DiceColor.Green: 0,
         DiceColor.Blue: 0,
         DiceColor.Yellow: 0,
         DiceColor.Purple: 0}


def roll(dices: dict):
    if dices == {}:
        return {}
    from random import randint
    for key in dices.keys():
        dices[key] = randint(1, 6)
    return dices


# print(roll(dices))

chosen_dices = []

discard_dices = []


def next_round(dices: dict, chosen_color: DiceColor):
    if dices == {}:
        return {}, {}, {}
    current = dices[chosen_color]
    next_round = {}
    discard = {}
    chosen = {}
    for key, value in dices.items():
        if value < current:
            discard[key] = value
        elif key != chosen_color:
            next_round[key] = value
        else:
            chosen[chosen_color] = current

    return chosen, discard, next_round


def reset_dices(dices: dict):

    dices = {DiceColor.White: 0,
             DiceColor.Orange: 0,
             DiceColor.Green: 0,
             DiceColor.Blue: 0,
             DiceColor.Yellow: 0,
             DiceColor.Purple: 0}
    return dices


def key_to_style(key:DiceColor):
    match key:
        case DiceColor.White:
            style = 'bright_white'
        case DiceColor.Orange:
            style = 'orange1'
        case DiceColor.Green:
            style = 'green4'
        case DiceColor.Blue:
            style = 'dodger_blue3'
        case DiceColor.Purple:
            style = 'purple4'
        case DiceColor.Yellow:
            style = 'yellow3'
    return style

def print_dices(dices: dict, title: str):
    table = Table(title=title)
    table.add_column("Index", justify="center", style="cyan", no_wrap=True)
    table.add_column("Color",justify="left")
    table.add_column("Value", justify="center")
    for key, value in dices.items():
        
        table.add_row(f'{key.value}',Text(f'{key.name}',style=key_to_style(key)),f'{value}')
    console.print(table)


def choose_dice(dices: dict, round: int):
    dices = roll(dices)
    reroll = 0

    print_dices(dices, f'Try {round}')
    
    choices = [str(i.value) for i in dices.keys()] + ['re','skip']
    
    input = Prompt.ask("Choose a dice",choices=choices)
    
    while (input == 're'):
        dices = roll(dices)
        reroll += 1
        print_dices(dices, f'Try {round} Reroll:{reroll}')
        input = Prompt.ask("Choose a dice",choices=choices)
    if input == 'skip':
        chosen, discard, dices = {}, {}, dices
    else:
        #print(type(input_number))
        chosen_color = DiceColor(int(input))
        chosen, discard, dices = next_round(dices, chosen_color)
    return chosen, discard, dices


def solo_choose(dices):
    dices = roll(dices=reset_dices(dices=dices))
    res = sorted(dices.items(), key=lambda d: d[1], reverse=False)
    table = Table(title='Solo')
    table.add_column('Color',justify='left',no_wrap=True)
    table.add_column('Value',justify='center')
    for color, value in res:
        table.add_row(Text(f'{color.name}',style=key_to_style(color)),f'{value}')
        
    console.print(table)



mode = GameMode.Solo

if mode == GameMode.Solo:

    for k in range(1, 7):

        print(f'****** Round {k} ******')
        print('')
        dices = reset_dices(dices)
        for i in range(1, 4):

            chosen, discard, dices = choose_dice(dices, i)
            print_dices(discard, f'Discard {i}')
            print_dices(chosen, f'Chosen {i}')
            chosen_dices.append(chosen)
            discard_dices.append(discard)

        solo_choose(dices=dices)
