from threading import Thread


class FakePlayer:
    def __init__(self, mes):
        self.mes = mes

    def play(self):
        if self.mes:
            print(self.mes)

    def stop(self):
        return

    def is_playing(self):
        return True


class Player:
    def __init__(self, fn, message, quiet):
        try:
            if quiet:
                raise Exception
            import vlc
            self.mus = vlc.MediaPlayer(fn)
        except Exception:
            self.mus = FakePlayer(message)

    def play(self):
        Thread(target=self.replay).start()

    def replay(self):
        self.mus.stop()
        self.mus.play()

    def is_playing(self):
        return self.mus.is_playing()


class Sound:
    def __init__(self, quiet=False):
        self.back = Player("music/melody.mp3", None, quiet)
        self.nyam = Player("music/nyam.mp3", "Nyam", quiet)
        self.drink = Player("music/drink.mp3", "Hlup", quiet)
        self.waste = Player("music/waste.mp3", "Poof", quiet)
        self.dead = Player("music/dead.mp3", "AAAA", quiet)
        self.boom = Player("music/boom.mp3", "BOOM", quiet)
        self.clock = Player("music/clock.mp3", "Tick", quiet)
