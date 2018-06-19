#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import Tk, Text, TOP, BOTH, X, Y, N,S,W,E, LEFT, messagebox, BOTTOM, Toplevel, filedialog, StringVar
from tkinter.ttk import Frame, Label, Entry, Combobox, Button
import sqlalchemy_data as db
from sqlalchemy_model import Evidence, Project

project = None


class ProjectSelector(Frame):

    def __init__(self, master):
        self.master = master
        self.master.title("Project-Selector")

        self.project_cmbx = None
        self.frame_header = Frame(self.master)
        self.frame_evidence = Frame(self.master)
        self.frame_footer = Frame(self.master)

        self.init_ui()
        super().__init__()

    def init_ui(self):

        first_column_width = 15

        frame1 = Frame(self.master)
        frame1.pack(fill=X)

        project_lbl = Label(frame1, text="Select Project", width=first_column_width)
        project_lbl.pack(side=LEFT, padx=5, pady=5)

        self.project_cmbx = Combobox(frame1)
        self.project_cmbx['values'] = [x.name for x in db.get_all_projects()]
        self.project_cmbx.bind('<<ComboboxSelected>>', self.project_selected)
        self.project_cmbx.pack(fill=X, padx=5, pady=5)

        self.frame_evidence.pack(fill=X)

        bttn_new_evidence = Button(self.frame_footer, text="New Evidence", command=self.click_new_evidence)
        bttn_new_evidence.pack(side=TOP, padx=5, pady=5)

        self.frame_footer.pack(side=BOTTOM)

    def project_selected(self, e):
        if self.project_cmbx.get():
            global project
            project = db.get_project_by_name(self.project_cmbx.get())
            print(project)

        self.frame_evidence.destroy()
        self.frame_evidence = Frame(self.master)
        self.frame_evidence.pack(fill=X)

        evidences = db.get_evidences_by_project_name(project.id)
        for evidence in evidences:
            evidence_lbl = Label(self.frame_evidence, text=evidence)
            evidence_lbl.pack(side=TOP)

    def click_new_evidence(self):
        if not project:
            messagebox.showerror("Error", "Please select a project")
        else:
            self.ef = EvidenceWindow(Toplevel(self.master))


class EvidenceWindow(Frame):

    def __init__(self, master):
        self.master = master
        self.master.geometry("500x300+300+300")
        self.master.title("Evidence-Selector")
        self.evidence = dict()

        self.init_ui()
        super().__init__()

    def init_ui(self):
        self.frame = Frame(self.master)
        self.frame.pack(fill=X)
        self.frame_footer = Frame(self.master)
        self.frame_footer.pack(side=BOTTOM)


        row=1
        first_column_width = 15
        second_column_width = 60

        lbl_name = Label(self.frame, text="Name")
        lbl_name.grid(row=row, column=0)

        self.entry_name = Entry(self.frame, width=second_column_width)
        self.entry_name.grid(row=row, column=1)

        row+=1
        lbl_description = Label(self.frame, text="Description", width=first_column_width)
        lbl_description.grid(row=row, column=0)

        self.entry_description = Entry(self.frame, width=second_column_width)
        self.entry_description.grid(row=row, column=1)

        row += 1
        lbl_filepath = Label(self.frame, text="Files", width=first_column_width)
        lbl_filepath.grid(row=row, column=0)

        self.filepath_value = StringVar()
        self.entry_filepath = Entry(self.frame, textvariable=self.filepath_value, width=second_column_width)
        self.entry_filepath.grid(row=row, column=1)

        bttn_create_evidence = Button(self.frame, text="Add File", command=self.add_file)
        bttn_create_evidence.grid(row=row, column=2)





        bttn_create_evidence = Button(self.frame_footer, text="Create", command=self.create_incidence)
        bttn_create_evidence.pack(side=BOTTOM, padx=5, pady=5)


    def add_file(self):
        file_path = filedialog.askopenfilename(parent=self.frame, initialdir="/", title="Select file",
                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        if file_path:
            self.evidence['file_path'] = file_path
            self.filepath_value.set(file_path)
        else:
            messagebox.showinfo('Info', 'No folder was selected')

    def create_incidence(self):
        new_evidence = Evidence(name=self.entry_name.get(),
                                description=self.entry_description.get(),
                                file_path=self.filepath_value.get())

        project.evidences.append(new_evidence)
        db.commit_changes()

        print(project.evidences)

def main():
    root = Tk()
    root.geometry("300x300+300+300")
    app = ProjectSelector(root)
    root.mainloop()


if __name__ == '__main__':
    main()
