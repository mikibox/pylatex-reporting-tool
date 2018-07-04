#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import Tk, Text, TOP, BOTH, X, Y, N, S, W, E, LEFT, RIGHT, messagebox, BOTTOM, Toplevel, filedialog, \
    StringVar, Frame
from tkinter.ttk import Label, Entry, Combobox, Button, Labelframe
import sqlalchemy_data as db
from sqlalchemy_model import Proof, Finding, Project
import latex_generator
import os
import sys
import shutil

app = None
project = None




def export_project():
    PROJECT_PATH = "projects"
    global project
    if not os.path.exists(PROJECT_PATH):
        os.mkdir(PROJECT_PATH)
        print("project base path created")

    for finding in project.findings:
        for proof in finding.proofs:
            ext = os.path.splitext(proof.path)[1]
            dst_path = os.path.join(PROJECT_PATH, str(project.id), str(finding.id))
            dst_filename = str(proof.id) + ext
            dst = os.path.join(dst_path, dst_filename)

            if proof.path and not os.path.exists(dst):
                try:
                    os.makedirs(dst_path, exist_ok=True)
                    shutil.copy(proof.path, dst)
                except FileNotFoundError:
                    print("Could not find this path: {}".format(proof.path))

    print("Finished copying files")


class ProjectSelector():

    def __init__(self, master):
        self.master = master
        self.master.title("Project-Selector")

        self.project_cmbx = None
        self.frame_header = Frame(self.master)
        self.frame_finding = Frame(self.master)
        self.frame_footer = Frame(self.master)

        self.init_ui()
        super().__init__()

    def init_ui(self):

        first_column_width = 15

        frame1 = Frame(self.master)
        frame1.pack(fill=X)

        bttn_new_project = Button(frame1, text="New Project", command=self.click_new_project)
        bttn_new_project.pack(side=TOP, padx=10, pady=10)

        project_lbl = Label(frame1, text="Select Project", width=first_column_width)
        project_lbl.pack(side=LEFT, padx=5, pady=5)

        self.project_cmbx = Combobox(frame1)
        self.project_cmbx['values'] = [x.name for x in db.get_all_projects()]
        self.project_cmbx.bind('<<ComboboxSelected>>', self.project_selected)
        self.project_cmbx.pack(fill=X, padx=5, pady=5)

        self.frame_finding.pack(fill=X)

        bttn_new_finding = Button(self.frame_footer, text="New Finding", command=self.click_new_finding)
        bttn_new_finding.pack(side=TOP, padx=5, pady=5)

        bttn_generate_report = Button(self.frame_footer, text="Generate Report", command=self.generate_report)
        bttn_generate_report.pack(side=TOP, padx=5, pady=5)

        self.frame_footer.pack(side=BOTTOM)

    def update_projects(self):
        self.project_cmbx['values'] = [x.name for x in db.get_all_projects()]

    def double_click_finding(self, event, finding):

        # messagebox.showinfo("Info",str(finding_id))
        self.ef = FindingWindow(Toplevel(self.master), finding)

    def update_findings(self):
        self.frame_finding.destroy()
        self.frame_finding = Frame(self.master)
        self.frame_finding.pack(fill=X)

        findings = db.get_findings_by_project_name(project.id)
        for finding in findings:
            label_txt = "{:0>3d} \t {}".format(finding.id, finding.name)
            finding_lbl = Label(self.frame_finding, text=label_txt)
            finding_lbl.pack(side=TOP, anchor=W, padx = 10)
            finding_lbl.bind("<Double-Button-1>",
                             lambda event, finding_var = finding :self.double_click_finding(event, finding_var))

    def project_selected(self, e=None):
        global project
        project = db.get_project_by_name(self.project_cmbx.get())
        self.update_findings()

    def click_new_project(self):
        self.np = ProjectWindow(Toplevel(self.master))

    def click_new_finding(self):
        global project
        if not project:
            messagebox.showerror("Error", "Please select a project")
        else:
            self.ef = FindingWindow(Toplevel(self.master))

    def generate_report(self):
        export_project()
        latex_generator.generate_report(project)
        print("success")


class ProjectWindow():

    def __init__(self, master):
        self.master = master
        # self.master.geometry("500x300+300+300")
        self.master.title("ProjectWindow")
        self.project = dict()

        self.init_ui()
        super().__init__()

    def init_ui(self):
        self.frame = Frame(self.master)
        self.frame.pack(fill=X)
        self.frame_footer = Frame(self.master)
        self.frame_footer.pack(side=BOTTOM)

        row = 1
        first_column_width = 15
        second_column_width = 60

        lbl_name = Label(self.frame, text="Name")
        lbl_name.grid(row=row, column=0)

        self.project_name = Entry(self.frame, width=second_column_width)
        self.project_name.grid(row=row, column=1)

        row += 1
        lbl_description = Label(self.frame, text="Description")
        lbl_description.grid(row=row, column=0)

        self.project_description = Entry(self.frame, width=second_column_width)
        self.project_description.grid(row=row, column=1)

        bttn_create_project = Button(self.frame_footer, text="Create", command=self.create_project)
        bttn_create_project.pack(side=BOTTOM, padx=5, pady=5)

    def create_project(self):
        if self.project_name.get():
            project = Project(name=self.project_name.get(),
                              description=self.project_description.get())
            project = db.create(project)
            db.commit_changes()
            global app
            app.update_projects()
            app.project_cmbx.set(project.name)
            app.project_selected()
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Project Name cannot be null")


class FindingWindow():

    def __init__(self, master, finding=None):
        self.master = master
        self.finding = finding
        self.master.geometry("400x300+300+300")
        self.master.title("Finding-Selector")
        self.proof_selectors = dict()
        self.proof_count = 0

        self.init_ui()

        if self.finding:
            self.fill_finding()

        self.proof_selectors[self.proof_count]=ProofSelector(self.frame_proofs)

        super().__init__()

    def init_ui(self):
        self.frame = Frame(self.master)
        self.frame.pack(fill=X, padx=20, pady=20)
        self.frame_proofs = Labelframe(self.master, text='Proofs')
        self.frame_proofs.pack(side=TOP, fill=BOTH, expand=True, padx=20)
        self.frame_proofs_footer = Frame(self.frame_proofs)
        self.frame_proofs_footer.pack(side=BOTTOM, anchor=E)
        self.frame_footer = Frame(self.master)
        self.frame_footer.pack(side=BOTTOM)

        self.entry_name_text =  StringVar()
        self.entry_description_text = StringVar()

        row = 1
        first_column_width = 15
        second_column_width = 40

        lbl_name = Label(self.frame, text="Name", width=first_column_width)
        lbl_name.grid(row=row, column=0, padx=10)

        self.entry_name = Entry(self.frame, text=self.entry_name_text, width=second_column_width)
        self.entry_name.grid(row=row, column=1)

        row += 1
        lbl_description = Label(self.frame, text="Description", width=first_column_width)
        lbl_description.grid(row=row, column=0, padx=10)

        self.entry_description = Entry(self.frame, text=self.entry_description_text, width=second_column_width)
        self.entry_description.grid(row=row, column=1)


        bttn_add_more_proof = Button(self.frame_proofs_footer, text="AddProof", command=self.add_more_proof)
        bttn_add_more_proof.pack(padx=5, pady=5)

        if self.finding:
            bttn_create_finding_text = "Update"
        else:
            bttn_create_finding_text = "Create"

        bttn_create_finding = Button(self.frame_footer, text=bttn_create_finding_text, command=self.commit_incidence)
        bttn_create_finding.pack(side=BOTTOM, padx=5, pady=5)

    def fill_finding(self):
        print(self.finding)
        self.entry_name_text.set(self.finding.name)
        self.entry_description_text.set(self.finding.description)
        for proof in self.finding.proofs:
            print(proof)
            self.add_more_proof(proof)

    def add_more_proof(self, proof=None):
        self.proof_count+=1
        self.proof_selectors[self.proof_count]=ProofSelector(self.frame_proofs, proof)


    def commit_incidence(self):
        active_proofs = list()
        for proof_key in self.proof_selectors.keys():
            if self.proof_selectors[proof_key].active and self.proof_selectors[proof_key].proof:
                active_proofs.append(self.proof_selectors[proof_key].proof)
        print("this is the active proofs")
        print(active_proofs)
        if not self.finding:
            new_finding = Finding(name=self.entry_name.get(),
                                  description=self.entry_description.get(),
                                  proofs=active_proofs)

            project.findings.append(new_finding)
        else:
            self.finding.name = self.entry_name.get()
            self.finding.description = self.entry_description.get()
            self.finding.proofs.extend(active_proofs)
            print("finding already existing, updated?")


        db.commit_changes()

        global app
        app.update_findings()
        self.master.destroy()


class ProofSelector:

    def __init__(self, frame, proof=None):
        self.frame = frame
        self.proof = proof
        self.active = True
        self.modified = False

        self.init_ui()

        if self.proof:
            self.fill_proof()

    def init_ui(self):

        self.frame_single_proof = Frame(self.frame, bg='white')
        self.frame_single_proof.pack(side=TOP, fill=X)

        self.filepath_value = StringVar()
        self.entry_filepath = Entry(self.frame_single_proof, textvariable=self.filepath_value)
        self.entry_filepath.pack(side=LEFT, expand=True, fill=X)

        if self.proof:
            self.entry_filepath.configure(state='readonly')

        bttn_select_file = Button(self.frame_single_proof, text="Add File", command=self.select_file)
        bttn_select_file.pack(side=LEFT)

        bttn_delette_file = Button(self.frame_single_proof, text="Delete File", command=self.delete_file)
        bttn_delette_file.pack(side=LEFT)

    def fill_proof(self):
        self.filepath_value.set(self.proof.path)

    def select_file(self):
        file_path = filedialog.askopenfilename(parent=self.frame, initialdir="/", title="Select file")
        # filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        if file_path:
            file_ext = os.path.splitext(file_path)[1]

            if file_ext in (".txt", ".sh", ".py"):
                proof_type = db.get_proof_type_by_name('text')
            elif file_ext in (".png", ".jpeg", ".gif"):
                proof_type = db.get_proof_type_by_name('image')
            else:
                messagebox.showerror("Extension Error",
                                     "the file extension {} is not suported, sorry :(".format(file_ext))
                return

            if self.proof:
                self.proof.path = file_path
                self.proof.type = proof_type
                self.modified = True

            else:
                new_proof = Proof(path=file_path,
                                  type=proof_type)

                self.proof = new_proof

            self.filepath_value.set(self.proof.path)

        else:
            messagebox.showinfo('Info', 'No folder was selected')

    def delete_file(self):
        if self.proof or self.modified:
            db.delete(self.proof)

        self.active = False
        self.frame_single_proof.destroy()

def main():
    global app
    root = Tk()
    root.geometry("300x300+300+300")
    app = ProjectSelector(root)
    root.mainloop()


if __name__ == '__main__':
    main()
