
import curses
import time
import keyboard
import random

screen = curses.initscr()

my_window = curses.initscr()
my_window.keypad(True)

curses.noecho()
curses.cbreak()
curses.curs_set(0)



def draw(syms, playerData, globalData):
    try:
        apples = globalData['apples']

        window_height, window_width = my_window.getmaxyx()
        my_window.clear()

        if playerData['head']['y'] < window_height and playerData['head']['x'] < window_width and playerData['head']['y'] >= 0 and playerData['head']['x'] >= 0:
            my_window.addstr(playerData['head']['y'], playerData['head']['x'], syms[playerData['head']['sym']])

        for tail in playerData['tail']:
            my_window.addstr(tail['y'], tail['x'], syms[tail['sym']])

        for apple in apples:
            if apple['y'] < window_height and apple['x'] < window_width and apple['y'] >= 0 and apple['x'] >= 0:
                my_window.addstr(apple['y'], apple['x'], syms[apple['sym']])

        
        my_window.addstr(0, 0, 'X: ' + str(playerData['head']['x']) + ', Y:' + str(playerData['head']['y']))

        my_window.addstr(window_height - 1, 0, 'Q - вийти.')
        my_window.addstr(window_height - 2, 0, 'W, A, S, D - керування.')
    except:
        pass

def move():
    global playerData

    window_height, window_width = my_window.getmaxyx()

    tail_ind = len(playerData['tail']) - 1
    while (tail_ind > -1):
        playerData['tail'][tail_ind]['x'] = playerData['tail'][tail_ind - 1]['x']
        playerData['tail'][tail_ind]['y'] = playerData['tail'][tail_ind - 1]['y']
    
        tail_ind -= 1
    
    playerData['tail'][0]['x'] = playerData['head']['x']
    playerData['tail'][0]['y'] = playerData['head']['y']

    if playerData['move']['direction'] == 'RIGHT' and playerData['move']['direction'] != 'LEFT':
        playerData['head']['x'] += 1

        if playerData['head']['x'] > window_width - 1:
            playerData['head']['x'] = 0

    elif playerData['move']['direction'] == 'LEFT':
        playerData['head']['x'] -= 1

        if playerData['head']['x'] < 0:
            playerData['head']['x'] = window_width - 1

    elif playerData['move']['direction'] == 'UP':
        playerData['head']['y'] -= 1

        if playerData['head']['y'] < 0:
            playerData['head']['y'] = window_height - 1

    elif playerData['move']['direction'] == 'DOWN':
        playerData['head']['y'] += 1

        if playerData['head']['y'] > window_height - 1:
            playerData['head']['y'] = 0

def collision():
    global playerData
    global apples
    window_height, window_width = my_window.getmaxyx()

    tail_ind = 0
    for tail in playerData['tail']:
        for apple in apples:
            if apple['x'] == playerData['head']['x']:
                if apple['y'] == playerData['head']['y']:
                    apple['x'] = random.randint(0, window_width - 1)
                    apple['y'] = random.randint(0, window_height - 1)
                    playerData['tail'].append({ 'x': 0, 'y': 0, 'sym': 3 })

        if playerData['head']['x'] == tail['x']:
            if playerData['head']['y'] == tail['y']:
                exit()

        tail_ind += 1

def start():
    syms = ['!', '🟢', '🍎', '🟩']
    syms = [' ', 'Q', '+', 'B']

    window_height, window_width = my_window.getmaxyx()
    
    global playerData
    global apples

    playerData = {
        'head': { 'x': 0, 'y': 0, 'sym': 1 },
        'tail': [{ 'x': -0, 'y': 0, 'sym': 3 }],
        'move': { 'direction': 'RIGHT' }
    }
    apples = [ { 'x': 5, 'y': 5, 'sym': 2} ]

    for apple in range(10): 
        apples.append({ 'x': random.randint(0, window_width - 1), 'y': random.randint(0, window_height - 1), 'sym': 2 })


    while True:
        move()
        collision()
        draw(syms, playerData, { 'apples': apples }) 
        
        my_window.refresh()
        

        try:
            if keyboard.is_pressed('q'):
                break

            elif keyboard.is_pressed('s') and playerData['move']['direction'] != 'UP':
                playerData['move']['direction'] = 'DOWN'
            
            elif keyboard.is_pressed('d') and playerData['move']['direction'] != 'LEFT':
                playerData['move']['direction'] = 'RIGHT'

            elif keyboard.is_pressed('w') and playerData['move']['direction'] != 'DOWN':
                playerData['move']['direction'] = 'UP'
        
            elif keyboard.is_pressed('a') and playerData['move']['direction'] != 'RIGHT':
                playerData['move']['direction'] = 'LEFT'
        except:
            break
        time.sleep(0.1)
    
    
    #curses.napms(2000)


    screen.clear()
    screen.refresh()

    curses.endwin()

start()
