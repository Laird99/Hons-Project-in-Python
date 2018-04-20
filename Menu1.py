#!/usr/bin/env python
import Tkinter as tk
import tkFont
import random


class Globalmem:
    chips = 0
    bet = 0
    pscore = 0;


class Game(tk.Tk):  # Switching Window- https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # Stores all "Windows" in one array, stacked on top of each other
        # Top one will be the frame visible
        self.frames = {}
        for F in (MenuScreen, CreateProfile, LoadProfile, DeleteProfile, Bet, MainGame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MenuScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MenuScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669613')
        self.controller = controller
        for widget in MenuScreen.winfo_children(self):
            widget.destroy()
        self.draw()

    def draw(self):
        f = tkFont.Font(family="system", size=20)

        top = tk.Frame(self, bg='#669613')
        top.pack(side=tk.TOP, pady=150)
        bottom = tk.Frame(self, bg='#669613')
        bottom.pack(side=tk.BOTTOM)

        CreateBtn = tk.Button(top, text="Create Profile", command=lambda: self.controller.show_frame("CreateProfile"))
        CreateBtn.config(height=5, width=25, font=f)
        CreateBtn.pack(side="left")

        LoadBtn = tk.Button(top, text="Load Profile", command=lambda: self.controller.show_frame("LoadProfile"))
        LoadBtn.config(height=5, width=25, font=f)
        LoadBtn.pack(side="left", padx=200)

        DeleteBtn = tk.Button(top, text="Delete Profile", command=lambda: self.controller.show_frame("DeleteProfile"))
        DeleteBtn.config(height=5, width=25, font=f)
        DeleteBtn.pack(side="left")

        QuitBtn = tk.Button(bottom, text="Quit", command=exit, height=5, width=50, font=f)
        QuitBtn.pack(side="top", pady=50)



class CreateProfile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669613')
        self.controller = controller
        for widget in CreateProfile.winfo_children(self):
            widget.destroy()
        self.draw()

    def draw(self):
        f = tkFont.Font(family="system", size=20)

        top = tk.Frame(self, bg='#669613')
        top.pack(side=tk.TOP, pady=100)
        middle = tk.Frame(self, bg='#669613')
        middle.pack(side=tk.TOP)
        bottom = tk.Frame(self, bg='#669613')
        bottom.pack(side=tk.BOTTOM)

        NameLabel = tk.Label(top, text="Enter Name:", width=10, height=1, font=f)
        NameLabel.pack(side="left", padx=100, ipady=25)

        self.entry = tk.Entry(top, width=60, font=f)
        self.entry.pack(side="left", ipady=25)

        ChipLabel = tk.Label(middle, text="Enter Chip Count:", width=15, height=2, font=f)
        ChipLabel.pack(side="left", padx=50)

        self.chips = tk.Scale(middle, from_=50, to=1500, orient="horizontal")
        self.chips.config(sliderlength=10, tickinterval=50, length=1500, resolution=50)
        self.chips.pack(side="left")

        QuitBtn = tk.Button(bottom, text="Back to Menu", command=lambda: self.controller.show_frame("MenuScreen"))
        QuitBtn.config(height=5, width=20, font=f)
        QuitBtn.pack(side="right", pady=100, padx=50)

        CreateBtn = tk.Button(bottom, text="Create Profile", command=self.saveprofile)
        CreateBtn.config(height=5, width=20, font=f)
        CreateBtn.pack(side="right", pady=100)

    def saveprofile(self):
        # Reading/Writing to file http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
        openfile = open("players.txt", "a", 0)
        openfile.write(str(self.entry.get()) + " \n")
        openfile.write(str(self.chips.get()) + " \n")
        openfile.close()


class LoadProfile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669613')
        self.controller = controller
        for widget in LoadProfile.winfo_children(self):
            widget.destroy()
        self.draw()

    def draw(self):
        f = tkFont.Font(family="system", size=20)

        left = tk.Frame(self, width=50, bg='#669613')
        left.pack(side=tk.LEFT)
        right = tk.Frame(self, width=50, bg='#669613')
        right.pack(side=tk.RIGHT)
        # separating the right panel into text and button frames
        rtop = tk.Frame(right, height=80, bg='#669613')
        rtop.pack(side=tk.TOP)
        rbot = tk.Frame(right, height=30, bg='#669613')
        rbot.pack(side=tk.TOP, pady=100)

        self.NameList = tk.Listbox(left, width=40, height=50, font=f, selectmode="single")
        self.loadprofiles()
        self.NameList.pack(side="right", padx=25, pady=50)

        instructions = tk.Label(rtop, text="INSTRUCTIONS \n ")
        instructions.config(width=50, height=3, font=f, fg="blue", bg='#669613')
        instructions1 = tk.Label(rtop, text="Please Select a Profile from list and start the game")
        instructions1.config(width=50, height=3, font=f, bg='#669613')
        self.instructions2 = tk.Label(rtop, text="Game will not start without a valid profile selected")
        self.instructions2.config(width=50, height=3, font=f, bg='#669613')
        instructions.pack(side="top", pady=50)
        instructions1.pack(side="top")
        self.instructions2.pack(side="top")

        RefreshBtn = tk.Button(rbot, text="Refresh Profiles", height=4, width=20, font=f, command=self.loadprofiles)
        RefreshBtn.pack(side="bottom", pady=25)

        QuitBtn = tk.Button(rbot, text="Back to Menu", command=lambda: self.controller.show_frame("MenuScreen"))
        QuitBtn.config(height=4, width=20, font=f)
        QuitBtn.pack(side="right", padx=120, pady=60)

        self.LoadBtn = tk.Button(rbot, text="Load Profile", height=4, width=20, font=f, command=lambda: self.checkprofile(rbot, f))
        self.LoadBtn.pack(side="left", padx=150, pady=60)

# displaying names on the listbox to user
    def loadprofiles(self):
        i = 1
        self.NameList.delete(0, tk.END)
        openfile = open("players.txt", "r")
        for line in openfile:
            if i % 2 != 0:
                self.NameList.insert("end", line)
            i = i+1
        openfile.close()


# Check to see if profile is selected before launching game
    def checkprofile(self, rbot, f):
        p1 = self.NameList.curselection()

        if p1 == ():
            self.instructions2.config(fg="Red")
        else:
            allnames = self.NameList.get(0, tk.END)
            x = str([allnames[item] for item in p1])
            global profile
            profile = x[2:-4]  # get profile selected

            openfile = open("players.txt", "r")
            content = openfile.readlines()
            openfile.close()  # read file to get chip count

            j = len(content)
            for i in range(0, j):
                k = str(content[i])
                ct = k[0:-1]
                if ct == profile:
                    count = content[i+1]
                    Globalmem.chips = int(count)

            self.LoadBtn.destroy()
            StartBtn = tk.Button(rbot, text="Start", height=4, width=20, font=f, command=lambda: self.controller.show_frame("Bet"))
            StartBtn.pack(side="left", padx=150, pady=60)


class DeleteProfile(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669613')
        self.controller = controller
        for widget in DeleteProfile.winfo_children(self):
            widget.destroy()
        self.draw()

    def draw(self):
        f = tkFont.Font(family="system", size=20)

        left = tk.Frame(self, width=50, bg='#669613')
        left.pack(side=tk.LEFT)
        right = tk.Frame(self, width=50, bg='#669613')
        right.pack(side=tk.RIGHT)
        # separating the right panel into text and button frames
        rtop = tk.Frame(right, height=80, bg='#669613')
        rtop.pack(side=tk.TOP)
        rbot = tk.Frame(right, height=30, bg='#669613')
        rbot.pack(side=tk.TOP,  pady=100)

        self.NameList = tk.Listbox(left, width=40, height=50, font=f)
        self.loadprofiles()
        self.NameList.pack(side="right", padx=25, pady=50)

        instructions = tk.Label(rtop, text="INSTRUCTIONS \n ")
        instructions.config(width=50, height=3, font=f, fg="blue", bg='#669613')
        instructions1 = tk.Label(rtop, text="Please Select a Profile to delete \n All deletions are permanent!")
        instructions1.config(width=50, height=3, font=f, bg='#669613')
        self.instructions2 = tk.Label(rtop, text="ENSURE CORRECT PROFILE IS SELECTED")
        self.instructions2.config(width=50, height=3, font=f, fg="red", bg='#669613')
        instructions.pack(side="top", pady=50)
        instructions1.pack(side="top")
        self.instructions2.pack(side="top")

        RefreshBtn = tk.Button(rbot, text="Refresh Profiles", height=4, width=20, font=f, command=self.loadprofiles)
        RefreshBtn.pack(side="bottom", pady=25)

        QuitBtn = tk.Button(rbot, text="Back to Menu", command=lambda: self.controller.show_frame("MenuScreen"))
        QuitBtn.config(height=4, width=20, font=f)
        QuitBtn.pack(side="right", pady=60, padx=120)

        DeleteBtn = tk.Button(rbot, text="Delete Profile", command=lambda: self.deleteprofile(rtop, f))
        DeleteBtn.config(height=4, width=20, font=f)
        DeleteBtn.pack(side="left", pady=60, padx=150)

# displaying names on the listbox to user

    def loadprofiles(self):
        i = 1
        self.NameList.delete(0, tk.END)
        openfile = open("players.txt", "r")
        for line in openfile:
            if i % 2 != 0:
                self.NameList.insert("end", line)
            i = i+1
        openfile.close()

    def deleteprofile(self, place, f):
        allnames = self.NameList.get(0, tk.END)
        index = self.NameList.curselection()

        if index == ():
            self.instructions2.destroy()
            self.instructions2 = tk.Label(place, text="ENSURE A PROFILE IS SELECTED")
            self.instructions2.config(width=50, height=3, font=f, fg="red", bg='#669613')
            self.instructions2.pack(side="top")
        else:
            # https://stackoverflow.com/questions/34113519/getting-the-text-from-a-listbox-item
            # Get string value from listbox selection instead of tuple value
            x = str([allnames[item] for item in index])

            openfile = open("players.txt", "r")
            content = openfile.readlines()
            openfile.close()

            chip = ""
            j = len(content)
            todelete = x[2:-4]  # removes the [ / ] and ' from each side of x to match text in line for comparison
            for i in range(0, j):
                k = str(content[i])
                ct = k[0:-1]
                if ct == todelete:
                    chip = content[i+1]

            rewrite = open("players.txt", "w")
            for line in content:
                y = line[:-1]
                if y != todelete and line != chip:
                    rewrite.write(line)  # if line is not the profile to delete, rewrite
            rewrite.close()
            self.NameList.delete(0, tk.END)  # remove all entries on list
            self.loadprofiles()  # rewrite updated list


class Bet(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669613')
        self.controller = controller
        for widget in Bet.winfo_children(self):
            widget.destroy()
        self.draw()

    def draw(self):
        f = tkFont.Font(family="system", size=20)

        top = tk.Frame(self, height=80, bg='#669613')
        top.pack(side=tk.TOP)
        bot = tk.Frame(self, height=30, bg='#669613')
        bot.pack(side=tk.TOP, pady=100)

        self.SliderBtn = tk.Button(bot, text="Show Slider", height=4, width=15, font=f, command=lambda: self.getval(top, bot, f))
        self.SliderBtn.pack(side="left", pady=150, padx=50)

        QuitBtn = tk.Button(bot, text="QUIT", command=exit, height=4, width=15, font=f)
        QuitBtn.pack(side="right", padx=100)

    def getval(self, top, bot, f):
        val = int(Globalmem.chips)

        if val > 2000 and val < 5000:
            freq = 250
            res = 100

        elif val > 4999 and val < 10000:
            freq = 1000
            res = 250

        elif val > 9999 and val < 25000:
            freq = 2500
            res = 500

        elif val > 24999 and val < 50000:
            freq = 5000
            res = 1000

        elif val > 49999:
            freq = 10000
            res = 2000

        else:
            freq = 50
            res = 50

        self.SliderBtn.destroy()
        chips = tk.Scale(top, from_=50, to=val, orient="horizontal")
        chips.config(sliderlength=10, tickinterval=freq, length=1500, resolution=res)
        chips.pack(side="top", pady=150)

        SubmitBtn = tk.Button(bot, text="PLACE BET", height=4, width=15, font=f, command=lambda: self.getbet(chips))
        SubmitBtn.pack(side="left")

    def getbet(self, chips):
        Globalmem.bet = chips.get()
        Globalmem.chips = Globalmem.chips - Globalmem.bet
        for widget in Bet.winfo_children(self):
            widget.destroy()
        self.draw()
        self.controller.show_frame("MainGame")


class MainGame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#669613')
        self.controller = controller
        self.drawframe()

    def drawframe(self):
        f = tkFont.Font(family="system", size=20)
        i = tkFont.Font(family="system", size=30)
        buttons = tk.Frame(self, width=35, bg='#669613')
        buttons.pack(side=tk.LEFT)
        dcards = tk.Frame(self, height=35, bg='#669613')
        dcards.pack(side=tk.TOP)
        info = tk.Frame(self, height=15, bg='#669613')
        info.pack(side=tk.TOP)
        pcards = tk.Frame(self, height=40, bg='#669613')
        pcards.pack(side=tk.TOP)
        res = tk.Frame(self, height=40, bg='#669613')
        res.pack(side=tk.BOTTOM)

        self.QuitBtn = tk.Button(buttons, text="QUIT", command=lambda: self.controller.show_frame("MenuScreen"), height=4, width=15, font=f)
        self.QuitBtn.pack(side="bottom")

        self.PlayBtn = tk.Button(buttons, text="DEAL HAND", command=lambda: self.restart())
        self.PlayBtn.config(height=4, width=15, font=f)
        self.PlayBtn.pack(side="bottom", padx=30)

        self.test1 = tk.Label(info, text="BLACKJACK PAYS 3 TO 2", height=4, width=60, font=i, bg='#669613', fg="Yellow")
        self.test1.pack(side="top", pady=25)
# End of main GUI building pt 1 --------------------------------------------------------------------------------------

        global cards
        cards = ['AC', 'AS', 'AD', 'AH', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H',
                 '4C', '4S', '4D', '4H', '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H',
                 '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H', '9C', '9S', '9D', '9H',
                 '10C', '10S', '10D', '10H', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH', 'KC', 'KS', 'KD', 'KH']

        global maxrange
        maxrange = 51
        # declared array and count as globals due to need for other classes to save changes to count
        # and cant assign variables to button callbacks - Begins game
        Globalmem.pscore = dscore = 0

        for i in range(0, 4):
            filepath, suit, pos = self.GetCards()
            # Sort score number for card
            val = self.getvalue(suit)
            # resumes normal process of displaying image
            photo = tk.PhotoImage(file=filepath)
            if i % 2 == 0:
                image = tk.Label(pcards, image=photo, height=200, bg='#669613')
                Globalmem.pscore = Globalmem.pscore + val
            else:
                image = tk.Label(dcards, image=photo, height=200, bg='#669613')
                dscore = dscore + val
            image.image = photo  # keeps reference of image
            image.pack(side="left", pady=20, padx=10)
            # adds image to screen then "removes" card
            maxrange = maxrange - 1

            del cards[pos]
# hands dealt and cards removed from deck --------------------------------------------------------------------------

        if dscore == 22:
            dscore = 12
        if Globalmem.pscore == 22:
            Globalmem.pscore = 12

# error code for scoring issue when being dealt 2 Aces--------------------------------------------------------------
        dout = tk.StringVar()
        pout = tk.StringVar()
        dout.set("Dealers Score: " + str(dscore))
        pout.set("Players Score: " + str(Globalmem.pscore))

        self.DealerS = tk.Label(buttons, textvariable=dout, height=4, width=25, font=f, bg='#669613')
        self.DealerS.pack(side="top")
        self.PlayerS = tk.Label(buttons, textvariable=pout, height=4, width=25, font=f, bg='#669613')
        self.PlayerS.pack(side="top", pady=75)

        extra = tk.Frame(self, bg='#669613')
        extra.pack(side=tk.BOTTOM, pady=20)

        # Stop method on automatically running on launch
        # https://stackoverflow.com/questions/3704568/tkinter-button-command-activates-upon-running-program
        self.HitBtn = tk.Button(extra, command=lambda: self.hit(pcards, buttons, f))
        self.HitBtn.config(text="HIT", height=4, width=15, font=f)
        self.HitBtn.pack(side="left")

        self.StickBtn = tk.Button(extra, command=lambda: self.stick(dscore, dcards, buttons, f, res))
        self.StickBtn.config(text="STICK", height=4, width=15, font=f)
        self.StickBtn.pack(side="left")
# end of GUI building pt 2 ------------------------------------------------------------------------------------------

    def GetCards(self):
        draw = random.randrange(0, maxrange, 1)  # selects random number to draw card from
        image = cards[draw]
        suit = image[1]
        if suit == "0":  # checks to see if number is 10, moves onto next char
            suit = image[2]

        if suit == "C":
            file = "images/deck/c/" + image + ".gif"
        elif suit == "S":
            file = "images/deck/s/" + image + ".gif"
        elif suit == "D":
            file = "images/deck/d/" + image + ".gif"
        else:
            file = "images/deck/h/" + image + ".gif"

        return file, image[0], draw

# ---- Get Card Value------------------------------------------------------------------------------------------------

    def getvalue(self, face):
        if face == "1" or face == "K" or face == "Q" or face == "J":
            face = 10
        elif face == "A":
            face = 11
        else:
            face = int(face)

        return face

# --- User Clicks Hit --------------------------------------------------------------------------------------------

    def hit(self, carea, side, f):
        path, face, pos = self.GetCards()
        val = self.getvalue(face)

        photo = tk.PhotoImage(file=path)
        image = tk.Label(carea, image=photo, height=200, bg='#669613')
        Globalmem.pscore = Globalmem.pscore + val
        image.image = photo  # keeps reference of image
        image.pack(side="left", pady=50, padx=5)

        global maxrange
        maxrange = maxrange - 1

        global cards
        del cards[pos]

        update = tk.StringVar()
        update.set("Players Score: " + str(Globalmem.pscore))
        self.PlayerS.destroy()
        # remove old label
        # https://stackoverflow.com/questions/9879255/is-there-any-way-to-delete-label-or-button-from-tkinter-window-and-then-add-it-b

        self.PlayerS = tk.Label(side, textvariable=update, height=4, width=25, font=f, bg='#669613')
        self.PlayerS.pack(side="bottom", pady=75)

        if Globalmem.pscore > 21:
            self.HitBtn.pack_forget()

# ------User Clicks Stick ----------------------------------------------------------------------------------------

    def stick(self, dscore, carea, buttons, f,  res):
        self.HitBtn.pack_forget()
        self.StickBtn.pack_forget()

        if Globalmem.pscore > 21:
            self.results(dscore, res, f)
        elif dscore > 21:
            self.results(dscore, res, f)
        else:
            while dscore < 17:
                path, face, pos = self.GetCards()
                val = self.getvalue(face)

                photo = tk.PhotoImage(file=path)
                image = tk.Label(carea, image=photo, height=200, bg='#669613')
                dscore = dscore + val
                image.image = photo  # keeps reference of image
                image.pack(side="left", padx=5)

                global maxrange
                maxrange = maxrange - 1

                global cards
                del cards[pos]

            update = tk.StringVar()
            update.set("Dealers Score: " + str(dscore))
            self.DealerS.destroy()
            # remove old label
            UpdDealerS = tk.Label(buttons, textvariable=update, height=4, width=25, font=f, bg='#669613')
            UpdDealerS.pack(side="top")

            self.results(dscore, res, f)

# ------- Get Result ---------------------------------------------------------------------------------------------

    def results(self, dscore, res, f):
        colour = "Blue"
        if Globalmem.pscore > 21:
            mes = "Player Bust! Dealer Wins"
        elif Globalmem.pscore == 21 and dscore != 21:
            mes = "BLACKJACK!, Player Wins"
            Globalmem.chips = Globalmem.chips + int((Globalmem.bet * 2.5))
        elif dscore > 21 and Globalmem.pscore < 22:
            mes = "Dealer Bust! Player Wins"
            Globalmem.chips = Globalmem.chips + int((Globalmem.bet * 2))
        elif Globalmem.pscore > dscore:
            mes = "Player Wins"
            Globalmem.chips = Globalmem.chips + int((Globalmem.bet * 2))
        elif Globalmem.pscore == dscore:
            mes = "Draw, No Winner"
            Globalmem.chips = Globalmem.chips + Globalmem.bet
        else:
            mes = "Dealer Wins"
            colour = "Red"

        Result = tk.Label(res, text=mes, height=4, width=25, font=f, fg=colour, bg='#669613')
        Result.pack(side="top", pady=50)
        openfile = open("players.txt", "r")
        content = openfile.readlines()
        openfile.close()  # read file to get chip count

        j = len(content)
        for i in range(0, j):
            k = str(content[i])
            ct = k[0:-1]
            if ct == profile:
                count = i + 1
                content[count] = str(Globalmem.chips) + "\n"

                rewrite = open("players.txt", "w")
                for line in content:
                    rewrite.write(line)
                rewrite.close()

    def restart(self):
        # http://nullege.com/codes/search/Tkinter.Frame.winfo_children
        # Destroy all items in frame and redraw the frame for next use
        for widget in MainGame.winfo_children(self):
            widget.destroy()
        self.drawframe()
        self.controller.show_frame("Bet")


window = Game()
window.title("Honours Application in Python")
window.attributes('-fullscreen', True)
window.mainloop()

