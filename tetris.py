from tkinter import *
from functools import partial
from random import choice, randint
from copy import deepcopy
from time import sleep

# Dev high score: 134

class TBlock():
    def __init__(self, win, coords, color, move, dorotate, loc):
        self.dorotate = dorotate
        self.abscoords = coords
        self.coords = self.abscoords
        if move:
            self.coords = self.getMove(loc)
            self.center = loc
        self.color = color
        self.imgs = []
        for coords in self.coords:
            img = win.create_rectangle(coords[0] * 10 + 150, coords[1] * 10, 160 + coords[0] * 10, 10 + coords[1] * 10, fill=self.color)
            self.imgs.append(img)
    def getMove(self, tcoords):
        self.moved = []
        for coords in self.coords:
            self.moved.append([coords[0] + tcoords[0], coords[1] + tcoords[1]])
        return self.moved
    def getRotation(self, direction, explode=False):
        if not explode:
            if self.dorotate:
                self.rotated = []
                for coords in self.abscoords:
                    if direction:
                        self.rotated.append([coords[1], -coords[0]])
                    else:
                        self.rotated.append([-coords[1], coords[0]])
                finalrotated = []
                for i in range(len(self.coords)):
                    finalrotated.append([self.center[0] + self.rotated[i][0],
                                         self.center[1] + self.rotated[i][1]])
                self.abscoords = self.rotated
                return finalrotated
            return self.coords
        else:
            finalrotated = []
            newcoordslist = deepcopy(self.coords)
            try:
                while True:
                    random.shuffle(newcoordslist)
                    for coords in newcoordslist:
                        newcoords = [coords[0] + randint(-1, 1), coords[1] + randint(-1, 1)]
                        if len(finalrotated) >= len(self.coords):
                            raise ZeroDivisionError
                        if newcoords not in self.coords and newcoords not in finalrotated:
                            finalrotated.append(newcoords)
            except ZeroDivisionError:
                return finalrotated
    def isValid(self, pcoords, sblock):
        for coords in sblock.coords:
            if coords in pcoords:
                return False
        return True
    def setCoords(self, win, tcoords, move=True):
        assert len(self.coords) == len(tcoords)
        if move:
            self.center[0] += tcoords[0][0] - self.coords[0][0]
            self.center[1] += tcoords[0][1] - self.coords[0][1]
        for i in range(len(self.coords)):
            win.move(self.imgs[i], 10 * (tcoords[i][0] - self.coords[i][0]),
                                   10 * (tcoords[i][1] - self.coords[i][1]))
        self.coords = tcoords

class SBlock():
    def __init__(self):
        self.coords = []
        self.imgs = []
    def addcoords(self, coordlist, imgs, whiteout=False):
        for coords in coordlist:
            self.coords.append(coords)
        for img in imgs:
            if whiteout:
                img.setFill('white')
                img.setOutline('white')
            self.imgs.append(img)
    def killLine(self, win, y, width):
        assert len(self.coords) == len(self.imgs)
        shapes = []
        newcoords = deepcopy(self.coords)
        if False:
            for i in range(25):
                for coords in newcoords:
                    if coords[1] == y and coords[0] not in (0, width + 1):
                        win.itemconfigure(self.imgs[self.coords.index(coords)], fill='black')
                        win.itemconfigure(self.imgs[self.coords.index(coords)], outline='black')
                win.update()
                sleep(0.01)
                for coords in newcoords:
                    if coords[1] == y and coords[0] not in (0, width + 1):
                        win.itemconfigure(self.imgs[self.coords.index(coords)], fill='white')
                        win.itemconfigure(self.imgs[self.coords.index(coords)], outline='white')
                win.update()
                sleep(0.01)
            for coords in newcoords:
                if coords[1] == y and coords[0] not in (0, width + 1):
                    win.delete(self.imgs[self.coords.index(coords)])
        else:
            for coords in newcoords:
                if coords[1] == y and coords[0] not in (0, width + 1):
                    shapes.append(self.imgs[self.coords.index(coords)])
        assert len(self.coords) == len(self.imgs)
        for coords in newcoords:
            if coords[1] == y and coords[0] not in (0, width + 1):
                self.imgs.pop(self.coords.index(coords))
                self.coords.remove(coords)
        for i in range(len(self.coords)):
            if self.coords[i][1] < y and self.coords[i][1] > 0 and self.coords[i][0] not in (0, width + 1):
                self.coords[i] = [self.coords[i][0], self.coords[i][1] + 1]
                win.move(self.imgs[i], 0, 10)
        return shapes

def mk_block(difficulty, frame, loc):
    color = choice(('red', 'orange', 'yellow', 'green', 'blue', 'purple', 'gray', 'brown', 'pink', 'aquamarine', 'navy', 'coral', 'green yellow', 'magenta', 'violet', 'tomato'))
    if difficulty > 150 and difficulty <= 160:
        color = 'white'
    if difficulty == 0:
        pattern = choice(([[0, 0], [-1, 0], [-2, 0], [1, 0]],
                          [[0, 0], [1, 0], [0, 1], [1, 1]],
                          [[0, 0], [-1, 0], [1, 0], [0, -1]],
                          [[0, 0], [-1, 0], [1, 0], [1, -1]],
                          [[0, 0], [-1, 0], [1, 0], [-1, -1]]))
    else:
        pattern = choice(([[0, 0], [-1, 0], [-2, 0], [1, 0]],
                          [[0, 0], [1, 0], [0, 1], [1, 1]],
                          [[0, 0], [-1, 0], [1, 0], [0, -1]],
                          [[0, 0], [-1, 0], [1, 0], [1, -1]],
                          [[0, 0], [-1, 0], [1, 0], [-1, -1]],
                          [[0, 0], [0, -1], [-1, -1], [1, 0]],
                          [[0, 0], [0, -1], [1, -1], [-1, 0]]))
    if difficulty >= 10 and not randint(0, 19):
        pattern = choice(([[0, 0], [-1, 0], [-2, 0], [1, 0], [2, 0]],
                          [[0, 0], [-1, 0], [0, 1], [0, -1], [1, -1]],
                          [[0, 0], [1, 0], [0, 1], [0, -1], [-1, -1]],
                          [[0, 0], [1, 0], [-1, 0], [-2, 0], [-2, -1]],
                          [[0, 0], [1, 0], [-1, 0], [-2, 0], [-2, 1]],
                          [[0, 0], [-1, 0], [1, 0], [0, -1], [1, -1]],
                          [[0, 0], [2, 0], [1, 0], [0, -1], [1, -1]],
                          [[0, 0], [0, 1], [0, -1], [-1, -1], [1, -1]],
                          [[-1, 0], [1, 0], [-1, 1], [1, 1], [0, 1]],
                          [[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1]],
                          [[0, 0], [1, 0], [0, 1], [-1, 1], [1, -1]],
                          [[0, 0], [-1, 0], [1, 0], [0, 1], [0, -1]],
                          [[0, 0], [-1, 0], [0, -1], [0, 1], [0, 2]],
                          [[0, 0], [1, 0], [0, -1], [0, 1], [0, 2]],
                          [[0, 0], [0, -1], [0, 1], [1, -1], [-1, 1]],
                          [[0, 0], [0, -1], [0, 1], [-1, -1], [1, 1]]))
    elif difficulty >= 25 and not randint(0, 24):
        pattern = choice(([[-1, 0], [1, 0]],
                          [[0, 0], [1, 0]],
                          [[0, 0], [1, -1]],
                          [[0, 0], [-2, 0], [2, 0]],
                          [[-1, -1], [1, -1], [1, 1]],
                          [[0, 0], [-1, 1], [1, 1]],
                          [[0, 0], [-1, 1], [1, 0]],
                          [[0, 0], [-1, -1], [1, 0]],
                          [[0, 0], [-1, 0], [1, 0]],
                          [[0, 0], [0, -1], [1, 0]],
                          [[0, 0], [1, -1], [-1, -1]],
                          [[0, 1], [0, -1], [-1, -1]],
                          [[0, 1], [0, -1], [1, -1]],
                          [[0, 0], [-1, 0], [2, 0]],
                          [[0, 0], [-1, 1], [2, 0]],
                          [[0, 0], [-1, -1], [2, 0]]))
    elif difficulty >= 40 and not randint(0, 34):
        pattern = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]
    dorotate = True
    if pattern == [[0, 0], [1, 0], [0, 1], [1, 1]]:
        dorotate = False
    return TBlock(frame, pattern, color, True, dorotate, loc)

def moveLeft(globaldict):
    if globaldict['state'] == 1:
        frame, tblock, sblock = globaldict['frame'], globaldict['tblock'], globaldict['sblock']
        tcoords = tblock.getMove([-1, 0])
        if tblock.isValid(tcoords, sblock):
            tblock.setCoords(frame, tcoords, True)
        globaldict['frame'], globaldict['tblock'], globaldict['sblock'] = frame, tblock, sblock
    keyPressed(globaldict)
def moveRight(globaldict):
    if globaldict['state'] == 1:
        frame, tblock, sblock = globaldict['frame'], globaldict['tblock'], globaldict['sblock']
        tcoords = tblock.getMove([1, 0])
        if tblock.isValid(tcoords, sblock):
            tblock.setCoords(frame, tcoords, True)
        globaldict['frame'], globaldict['tblock'], globaldict['sblock'] = frame, tblock, sblock
    keyPressed(globaldict)
def rotateRight(globaldict):
    if globaldict['state'] == 1:
        frame, tblock, sblock = globaldict['frame'], globaldict['tblock'], globaldict['sblock']
        tcoords = tblock.getRotation(False)
        if tblock.isValid(tcoords, sblock):
            tblock.setCoords(frame, tcoords, False)
        globaldict['frame'], globaldict['tblock'], globaldict['sblock'] = frame, tblock, sblock
    keyPressed(globaldict)
def moveDown(globaldict, move):
    if globaldict['state'] == 1:
        frame, tblock, sblock, ntblocks = globaldict['frame'], globaldict['tblock'], globaldict['sblock'], globaldict['ntblocks']
        tcoords = tblock.getMove([0, 1])
        if tblock.isValid(tcoords, sblock):
            tblock.setCoords(frame, tcoords, True)
        elif move:
            sblock.addcoords(tblock.coords, tblock.imgs)
            for y in range(1, globaldict['height'] + 1):
                checked = 0
                for i in range(1, globaldict['width'] + 1):
                    for coords in sblock.coords:
                        if coords == [i, y]:
                            checked += 1
                if checked == globaldict['width']:
                    shapes = sblock.killLine(frame, y, globaldict['width'])
                    for shape in shapes:
                        globaldict['shapes'].append(shape)
                        globaldict['shapes_v'].append([randint(-300, 300)/100,
                                                       randint(-600, 0)/100])
                        globaldict['shapes_r'].append(randint(-3000, 3000)/100)
                    globaldict['score'] += 1
                    if globaldict['difficulty'] < 60:
                        globaldict['difficulty'] += 1
                    frame.itemconfigure(globaldict['text_id'], text=str(globaldict['score']))
            for ntblock in ntblocks[1:]:
                ntblock.setCoords(frame, ntblock.getMove([0, -5]))
            ntblocks[0].setCoords(frame, ntblocks[0].getMove([-8, 0]))
            tblock = ntblocks[0]
            ntblocks.pop(0)
            ntblocks.append(mk_block(globaldict['difficulty'], frame, [13, 22]))
            if not tblock.isValid(tblock.coords, sblock):
                for img in tblock.imgs:
                    frame.delete(img)
                for y in range(globaldict['height'], 0, -1):
                    for x in range(globaldict['width'], 0, -1):
                        for coords in sblock.coords:
                            if coords == [x, y]:
                                frame.itemconfigure(sblock.imgs[sblock.coords.index(coords)], fill='black')
                                frame.itemconfigure(sblock.imgs[sblock.coords.index(coords)], outline='black')
                                frame.update()
                        sleep(0.01)
                print(('Score:', globaldict['score']))
                frame.create_text(75, 60, text='Game over. Press any\nkey to continue.')
                globaldict['state'] = 0
                return
            globaldict['id_num'] = frame.after(1000 - (globaldict['difficulty']*10), moveDown, globaldict, True)
        globaldict['frame'], globaldict['tblock'], globaldict['sblock'] = frame, tblock, sblock
        if tblock.isValid(tcoords, sblock):
            frame.after_cancel(globaldict['id_num'])
            globaldict['id_num'] = frame.after(1000 - (globaldict['difficulty']*10), moveDown, globaldict, True)
        globaldict['frame'], globaldict['tblock'], globaldict['sblock'], globaldict['ntblocks'] = frame, tblock, sblock, ntblocks
    keyPressed(globaldict)

def dropDown(globaldict):
    if globaldict['state'] == 1:
        frame, tblock, sblock = globaldict['frame'], globaldict['tblock'], globaldict['sblock']
        do_reset = False
        while True:
            tcoords = tblock.getMove([0, 1])
            if tblock.isValid(tcoords, sblock):
                tblock.setCoords(frame, tcoords, True)
                do_reset = True
            else:
                break
        if do_reset:
            frame.after_cancel(globaldict['id_num'])
            globaldict['id_num'] = frame.after(1000 - (globaldict['difficulty']*10), moveDown, globaldict, True)
    keyPressed(globaldict)

def keyPressed(globaldict):
    if globaldict['state'] == 0:
        globaldict['state'] = -2
        globaldict['root'].destroy()
    if globaldict['state'] == -1:
        globaldict['state'] = 1
        globaldict['frame'].delete(globaldict['text_id_2'])
        globaldict['id_num'] = globaldict['frame'].after(1000, moveDown, globaldict, True)

def doFrame(globaldict):
    assert len(globaldict['shapes']) == len(globaldict['shapes_v']) == len(globaldict['shapes_r'])
    for i in range(len(globaldict['shapes']) -1, -1, -1):
        globaldict['frame'].move(globaldict['shapes'][i], globaldict['shapes_v'][i][0], globaldict['shapes_v'][i][1])
        if globaldict['shapes_v'][i][0]:
            globaldict['shapes_v'][i][0] -= 0.01
            if abs(globaldict['shapes_v'][i][0]) <= 0.01:
                globaldict['shapes_v'][i][0] = 0
        globaldict['shapes_v'][i][1] += 0.1
        if tuple(globaldict['frame'].coords(globaldict['shapes'][i]))[1] >= 415:
            globaldict['shapes'].pop(i)
            globaldict['shapes_v'].pop(i)
            globaldict['shapes_r'].pop(i)
    globaldict['after'] = True

def checkFrame(globaldict):
    if globaldict['after']:
        globaldict['after'] = False
        frame.after(3, doFrame, globaldict)
        frame.update()
    frame.after(1, checkFrame, globaldict)

def makePause(globaldict):
    if globaldict['state'] == 1:
        globaldict['state'] = -3
        globaldict['rect_id'] = globaldict['frame'].create_rectangle(100, 0, 400, 400, fill='white', outline='white')
        globaldict['rect_text'] = globaldict['frame'].create_text(200, 135, text='Paused')
    elif globaldict['state'] == -3:
        globaldict['state'] = 1
        globaldict['frame'].delete(globaldict['rect_id'])
        globaldict['frame'].delete(globaldict['rect_text'])
        globaldict['frame'].after_cancel(globaldict['id_num'])
        globaldict['id_num'] = globaldict['frame'].after(1000, moveDown, globaldict, True)
    keyPressed(globaldict)

while True:
    try:
        root = Tk()
        root.title('Tetris')
        frame = Canvas(root, width=400, height=400)
        tblock = mk_block(0, frame, [5, 2])
        ntblocks = []
        for i in range(5):
            ntblocks.append(mk_block(0, frame, [13, 2 + i*5]))
        width, height = 8, 25
        coordslist = []
        for i in range(height + 2):
            coordslist.append([0, i])
            coordslist.append([width + 1, i])
        for i in range(1, width + 2):
            coordslist.append([i, 0])
            coordslist.append([i, height + 1])
        tsblock = TBlock(frame, coordslist, 'black', False, False, [0, 0])
        sblock = SBlock()
        sblock.addcoords(tsblock.coords, tsblock.imgs)
        globaldict = {'frame':frame,'tblock':tblock,'ntblocks':ntblocks,'sblock':sblock,'width':width,'height':height,'difficulty':0,'score':0,'state':-1,'root':root,'shapes':[],'shapes_v':[],'shapes_r':[],'after':True}
        frame.bind_all('<Left>', lambda event, arg=globaldict: moveLeft(arg))
        frame.bind_all('<Right>', lambda event, arg=globaldict: moveRight(arg))
        frame.bind_all('<Up>', lambda event, arg=globaldict: rotateRight(arg))
        frame.bind_all('<Down>', lambda event, arg=globaldict: moveDown(arg, False))
        frame.bind_all('<space>', lambda event, arg=globaldict: dropDown(arg))
        frame.bind_all('p', lambda event, arg=globaldict: makePause(arg))
        for key in ('1','2','3','Key','Cancel','BackSpace','Tab','Return','Shift_L','Control_L','Alt_L','Pause','Caps_Lock','Escape','Prior','Next','End','Home','Print','Insert','Delete','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','Num_Lock','Scroll_Lock'):
            frame.bind_all('<'+key+'>', lambda event, arg=globaldict: keyPressed(arg))
        globaldict['text_id'] = frame.create_text(50, 30, text=str(globaldict['score']))
        globaldict['text_id_2'] = frame.create_text(75, 60, text='Press any key\n  to continue.')
        frame.after(3, doFrame, globaldict)
        frame.after(1, checkFrame, globaldict)
        frame.pack()
        root.mainloop()
        if globaldict['state'] != -2:
            break
    except SystemExit:
        break
