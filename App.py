import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import socket
import datetime

from requests import get
from bs4 import BeautifulSoup

import sqlite3

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Vulnerability Scanner")
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New",command=clear_text)
        filemenu.add_command(label="Save",command=file_save)
        filemenu.add_command(label="Exit",command=close_window)
        menubar.add_cascade(label="File",menu=filemenu)
        menubar.add_command(label="About",command=about_file)
        tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        for F in (StartPage, VulnPage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
        
global ports
ports = []

def close_window():
    #StartPage.ext
    app.destroy()    #closes the GUI application
    exit()
    

def clear_text():   # function is to clear all the text fields ||just like a new file
    texttarget.delete(0)
    textstart.delete(0)
    textend.delete(0)
    output.delete(0.0)

def file_save():    #saves the data into a text file
    #opens the directory for you to save at a particular location
    #StartPage.ext()
    f = filedialog.asksaveasfilename(initialdir = "/", title="Save File",filetypes = (("txt files","*.txt"),("all files","*.*")))
    file = open(f,'w')
    text2save = str(output.get(0.0,100.0))
    file.write(text2save)
    file.close()

def about_file(): 
    messagebox.showinfo(title="About",message="It's a Vulnerablility scanner\nVulnerability scanning is an inspection of the potential points of exploit on a computer or network to identify security holes. A vulnerability scan detects and classifies system weaknesses in computers, networks and communications equipment and predicts the effectiveness of countermeasures.")
    
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global texttarget,textstart,textend,output
        
        label1 = tk.Label(self, text = "Target", font ="none 12")
        label1.pack(pady=5,padx=10)

        texttarget = tk.Entry(self, width = 30, bg = "white")
        texttarget.pack()

        label2 = tk.Label(self, text = "Port start", font ="none 12")
        label2.pack(pady=5,padx=10)
        
        textstart = tk.Entry(self,width = 10, bg = "white")
        textstart.pack()

        label3 = tk.Label(self, text = "Port end", font ="none 12")
        label3.pack(pady=5,padx=10)
        
        textend = tk.Entry(self,width = 10, bg = "white")
        textend.pack()


        def pscan(port):
            try:
                target = texttarget.get()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #AF_INET refers to address family IPv4, SOCK_STRAM means connected oriented TCP
                s.connect((target,port))
                return True
            except:
                return False

        def scan():
            if texttarget.get() is "":
                messagebox.showerror("Error","No target is given!") #gives a error message if nothing is entered
            now = datetime.datetime.now()   #creating time date object
            output.insert(0.0,now.strftime("%Y-%m-%d %H:%M\n"))   #to display the time and date 
            output.insert(1.0,"The scanned target for ports is: "+str(texttarget.get())+"\n")    #displays the target address
            for x in range(int(textstart.get()),int(textend.get())):    #gets the start and end ports from the GUI
                if pscan(x):
                    ports.append(x)
                    show = 'Port '+str(x)+' is open\n'  
                    output.insert(0.0,show) #prints the opened ports
            messagebox.showinfo(title="Message",message="Scan Complete!")   #once the scan is complete it shows a message box


        button1 = ttk.Button(self,width = 10, text="Scan",command=scan)
        button1.pack(pady=5,padx=10)

        button2 = ttk.Button(self,width =20, text="Vulnerability Scan",
                            command = lambda: controller.show_frame(VulnPage))
        button2.pack(pady=5,padx=10)

        output = tk.Text(self, width = 50, height=25, bg="white")
        output.pack()

           
class VulnPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button3 = ttk.Button(self,width =10, text="Back",
                            command = lambda: controller.show_frame(StartPage))
        button3.pack(pady=5,padx=10)

        scroll = tk.Scrollbar()
        vuloutput = tk.Text(self, width = 200, height=150, bg="white")
        vuloutput.pack(pady=10,padx=10)
        scroll.pack(side = "right", fill = "y")
        scroll.config(command = vuloutput.yview)
        vuloutput.config(yscrollcommand = scroll.set)
        def VulnScan():
            connection = sqlite3.connect("vulnerability.db")
            cursor = connection.cursor()
            if 80 in ports:
                sql_command = """SELECT * FROM cve WHERE des LIKE '%http%';"""
                cursor.execute(sql_command)
                row = cursor.fetchall()
                for r in range(5):
                    vuloutput.insert(0.0,"\n------------------------------\n")
                    vuloutput.insert(0.0,"\nCVSS Severity:\t"+str(row[r][3]))
                    vuloutput.insert(0.0,"\nPublished Date:\t"+str(row[r][2]))
                    vuloutput.insert(0.0,"\nDescription:\t"+str(row[r][1]))
                    vuloutput.insert(0.0,"Vuln ID:\t" + str(row[r][0]))
                    vuloutput.insert(0.0,"PORT--80\n")

            sql_command = """SELECT * FROM cve WHERE des LIKE '%netBIOS%';"""
            cursor.execute(sql_command)
            row = cursor.fetchall()
            for r in range(5):
                vuloutput.insert(0.0,"\n------------------------------\n")
                vuloutput.insert(0.0,"\nCVSS Severity:\t"+str(row[r][3]))
                vuloutput.insert(0.0,"\nPublished Date:\t"+str(row[r][2]))
                vuloutput.insert(0.0,"\nDescription:\t"+str(row[r][1]))
                vuloutput.insert(0.0,"Vuln ID:\t" + str(row[r][0]))
                vuloutput.insert(0.0,"PORT--139\n")

            sql_command = """SELECT * FROM cve WHERE des LIKE '%smb%';"""
            cursor.execute(sql_command)
            row = cursor.fetchall()
            for r in range(5):
                vuloutput.insert(0.0,"\n------------------------------\n")
                vuloutput.insert(0.0,"\nCVSS Severity:\t"+str(row[r][3]))
                vuloutput.insert(0.0,"\nPublished Date:\t"+str(row[r][2]))
                vuloutput.insert(0.0,"\nDescription:\t"+str(row[r][1]))
                vuloutput.insert(0.0,"Vuln ID:\t" + str(row[r][0]))
                vuloutput.insert(0.0,"PORT--445\n")

                           
        VulnScan()

app = Application()
app.geometry("1280x720")
app.mainloop()
