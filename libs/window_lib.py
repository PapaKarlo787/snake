from tkinter import Label, Tk, Canvas
from tkinter import messagebox as mb, filedialog as fd, PhotoImage as PhIm
from snake_lib import Object as Obj
import copy


class Window:
    def ask(message, title):
        win = Tk()
        win.withdraw()
        result = mb.askyesno(title=title, message=message)
        win.destroy()
        return result

    def __init__(self, snake):
        size = 32
        self.c = lambda x: size//2+size*x
        self.snake = snake
        self.size = size
        self.w = snake.w
        self.h = snake.h
        self.drawable = [Obj.WALL, Obj.APPLE, Obj.POISON, Obj.VOID]
        self.lastmap = copy.deepcopy(self.snake.map)
        message = "{}\nLoad empty level?".format(snake.error)
        if snake.error and self.wrong_input(message):
            return
        self.win = Tk()
        self.win.geometry('{}x{}'.format(self.w*size, (self.h+1)*size))
        self.win.resizable(False, False)
        self.win.title("Snake")
        self.win.bind('<Key>', self.keypress)
        self.canv = Canvas(self.win, width=self.w*size, height=self.h*size,
                           bg='green yellow')
        self.canv.pack()
        self.prepare_pics()
        self.setup()
        self.create_infolabels()
        self.refresh()
        self.win.after(1500, self.timer)
        self.win.mainloop()

    def create_infolabels(self):
        self.infolabels = {}
        x = 0
        size = self.size
        for elem in [Obj.HEART, Obj.POISON, Obj.SCORE, Obj.CLOCK]:
            Label(self.win, image=self.pictures[elem]).\
                place(x=x, y=self.h*size, height=size, width=size)
            self.infolabels[elem] = Label(self.win, text="0")
            self.infolabels[elem].place(x=x+size, y=self.h*size,
                                        height=size, width=size)
            x += size * 2

    def prepare_pics(self):
        names = ['HEAD_LEFT', 'HEAD_RIGHT', 'HEAD_UP', 'HEAD_DOWN', 'HEART',
                 'HORISONTAL', 'VERTICAL', 'UP-LEFT', 'UP-RIGHT', 'DOWN-LEFT',
                 'DOWN-RIGHT', 'BLOOD', 'TAIL_LEFT', 'TAIL_RIGHT', 'TAIL_UP',
                 'VOID', 'TAIL_DOWN', 'APPLE', 'POISON', 'PORTAL', 'WALL',
                 'SCORE', 'CLOCK']
        self.pictures = {}
        for name in names:
            self.pictures[name] = PhIm(file="pics/{}.PNG".format(name))

    def setup(self):
        for i in range(self.h):
            for l in range(self.w):
                image = self.pictures[self.snake.map[i][l]]
                self.canv.create_image(self.c(l), self.c(i), image=image)

    def timer(self):
        self.update()
        if self.snake.killed:
            self.win.destroy()
        elif self.snake.timeout:
            mes = "Your score at this level is {}".format(self.snake.score)
            mb.showinfo("End of level", message=mes)
            self.win.destroy()
            self.snake.killed = True
        else:
            self.win.after(self.snake.delay, self.timer)

    def update(self):
        self.snake.move()
        self.refresh()
        sn = self.snake
        timer = int(self.snake.timer)
        if not self.snake.lev:
            timer = 0
        values = (self.snake.lives, self.snake.poisons, self.snake.score,
                  timer)
        labels = dict(zip(self.infolabels.keys(), values))
        for item in self.infolabels:
            self.infolabels[item]['text'] = str(labels[item])
        self.lastmap = copy.deepcopy(self.snake.map)

    def keypress(self, event):
        actions = {111: self.snake.up, 113: self.snake.left,
                   116: self.snake.down, 114: self.snake.right,
                   65: self.snake.shoot, 86: self.snake.faster,
                   82: self.snake.slower, 36: self.snake.start_pause}
        if event.keycode in actions:
            actions[event.keycode]()
        elif event.char.encode() == b'\x0f':
            self.choose_file()

    def choose_file(self):
        if self.snake.lev:
            return
        fn = fd.askopenfilename()
        if fn:
            self.snake.killed = True
            self.snake.fn = fn

    def wrong_input(self, message):
        if not message:
            return False
        win = Tk()
        win.withdraw()
        result = not mb.askyesno(title="Error", message=message)
        win.destroy()
        return result

    def refresh(self):
        self.canv.delete("all")
        for i in range(self.h):
            for l in range(self.w):
                if self.snake.map[i][l] in self.drawable:
                    image = self.pictures[self.snake.map[i][l]]
                    self.canv.create_image(self.c(l), self.c(i), image=image)
        for i in range(self.snake.hp+1):
            image = self.pictures[self.snake.mem[i][1]]
            n, m = self.snake.mem[i][0]
            self.canv.create_image(self.c(n), self.c(m), image=image)
