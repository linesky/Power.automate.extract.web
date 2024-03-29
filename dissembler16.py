import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os

st1=".text\r\nstart:\r\nnop\r\ndb "

class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("dissembler 16 bits")

        # Janela amarela
        self.root.configure(bg='blue')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="from a file", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="string", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="new file", command=self.copy_file)
        self.copy_button.pack(pady=5)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END,"0x90,0x0")

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):
        filename = tk.filedialog.askopenfilename(title="Select file")
        self.text_area.delete(1.0, tk.END)
        self.execute_command("cp  $1 /tmp/my.o".replace("$1",filename),False)
        self.execute_command("chmod 777 /tmp/my.o",False)
        self.execute_command("objdump -M intel -D -b binary -mi386  -Maddr16,data16 /tmp/my.o",True)

    def run_kernel(self):
        #self.text_area.delete(1.0, tk.END)
        st=self.text_area.get(1.0,"end-1c")
        tt="\n------------------"
        
        posss=st.find(tt)
        if posss>-1:
            #posss+=len(tt)
            st=st[0:posss]
            
        print(st)
        st2=st1+st+"\n"
        f1=open("/tmp/my.asm","w")
        f1.write(st2)
        f1.close
        self.text_area.insert(tk.END,tt)
        self.execute_command("rm /tmp/my.o",False)
        self.execute_command("chmod 777 /tmp/my.o",False)
        self.execute_command("as86 -1 /tmp/my.asm -o /tmp/my.o",True)
        self.execute_command("objdump -M intel -D -b binary -mi386  -Maddr16,data16 /tmp/my.o",True)


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END,"0x90,0x0")

if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
