#!/usr/bin/env python3

import math
import sys

from typing import List
from typing import Tuple


base_chance: int = 70


def input_option(msg: str) -> str:
    while True:
        try:
            option: str = input(msg).upper()
            break
        except (KeyboardInterrupt, EOFError):
            print(end='\n')
    return option


def calc_bet_size(bankroll: int, win_chance: int) -> int:
    return math.ceil(bankroll * (win_chance / 50.0 - 1.0))


def calc_all_outcomes(
        outcomes: List[int], bankroll: int, win_chance: int, turn: int) -> List[int]:
    if turn == 0:
        outcomes.append(bankroll)
    else:
        bet_size: int = calc_bet_size(bankroll, win_chance)
        calc_all_outcomes(outcomes, bankroll + bet_size, win_chance + 1, turn - 1)
        calc_all_outcomes(outcomes, bankroll - bet_size, base_chance, turn - 1)
    return outcomes


def calc_stats(
        bankroll: int, win_chance: int, turns: int) -> Tuple[List[int], List[int]]:
    outcomes: List[int] = []
    outcomes = calc_all_outcomes(outcomes, bankroll, win_chance, turns)
    win_outcomes: List[int] = [outcome for outcome in outcomes if outcome > bankroll]
    loss_outcomes: List[int] = [outcome for outcome in outcomes if outcome < bankroll]
    return win_outcomes, loss_outcomes


def calc_value_pct(bankroll: int, outcome: int) -> Tuple[int, float]:
    value: int = outcome - bankroll
    pct: float = value / bankroll * 100.0
    return value, pct


def print_profit_stats(bankroll: int, win_outcomes: List[int]) -> None:
    max_profit, max_profit_pct = calc_value_pct(bankroll, max(win_outcomes))
    print(f'Max profit forecast: {max(win_outcomes):,}', end=' ')
    print(f'({max_profit:+,}, {max_profit_pct:+.2f}%)')

    avg_profit_bankroll: int = math.ceil(sum(win_outcomes) / len(win_outcomes))
    avg_profit, avg_profit_pct = calc_value_pct(bankroll, avg_profit_bankroll)
    print(f'Avg profit forecast: {avg_profit_bankroll:,}', end=' ')
    print(f'({avg_profit:+,}, {avg_profit_pct:+.2f}%)')

    min_profit, min_profit_pct = calc_value_pct(bankroll, min(win_outcomes))
    print(f'Min profit forecast: {min(win_outcomes):,}', end=' ')
    print(f'({min_profit:+,}, {min_profit_pct:+.2f}%)')


def print_loss_stats(bankroll: int, loss_outcomes: List[int]) -> None:
    min_loss, min_loss_pct = calc_value_pct(bankroll, max(loss_outcomes))
    print(f'Min loss forecast: {max(loss_outcomes):,}', end=' ')
    print(f'({min_loss:+,}, {min_loss_pct:+.2f}%)')

    avg_loss_bankroll: int = math.ceil(sum(loss_outcomes) / len(loss_outcomes))
    avg_loss, avg_loss_pct = calc_value_pct(bankroll, avg_loss_bankroll)
    print(f'Avg loss forecast: {avg_loss_bankroll:,}', end=' ')
    print(f'({avg_loss:+,}, {avg_loss_pct:+.2f}%)')

    max_loss, max_loss_pct = calc_value_pct(bankroll, min(loss_outcomes))
    print(f'Max loss forecast: {min(loss_outcomes):,}', end=' ')
    print(f'({max_loss:+,}, {max_loss_pct:+.2f}%)')


def main() -> None:
    bankroll: int = int(input('Bankroll: '))
    win_chance: int = int(input('Chance of winning: '))
    init_bankroll: int = bankroll
    init_win_chance: int = win_chance
    turns: int = 4

    win_outcomes, loss_outcomes = calc_stats(bankroll, win_chance, turns)
    print(f'{"-" * base_chance}')
    print_profit_stats(bankroll, win_outcomes)
    print_loss_stats(bankroll, loss_outcomes)

    for _ in range(turns):
        optimal_bet: int = calc_bet_size(bankroll, win_chance)
        print(f'{"-" * base_chance}')
        print(f'Optimal bet: ({optimal_bet:,}) {optimal_bet}')

        option: str = input_option('[W]in, [L]oss or [Q]uit: ')
        if option == 'Q':
            break
        bankroll += optimal_bet if option == 'W' else -optimal_bet
        win_chance = win_chance + 1 if option == 'W' else base_chance

    bankroll_value, bankroll_pct = calc_value_pct(init_bankroll, bankroll)
    print(f'{"-" * base_chance}')
    print(f'Current bankroll: {bankroll:,}', end=' ')
    print(f'({bankroll_value:+,}, {bankroll_pct:+.2f}%)')
    print(f'Current win chance: {win_chance} ({win_chance - init_win_chance:+})')


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit()
