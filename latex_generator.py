from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.package import Package
from pylatex.utils import italic, NoEscape

def add_proof(doc, proof):
    if proof.type.name == 'text':
        doc.append(NoEscape(r'\lstinputlisting{'+proof.path+'}'))
    elif proof.type.name == 'image':
        with doc.create(Figure(position='h!')) as proof_pic:
            proof_pic.add_image(proof.path, width=NoEscape(r'0.8\textwidth'), placement = NoEscape(r'\centering'))
            proof_pic.add_caption('Look it\'s on its back')


def add_finding(doc, finding):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Subsection(finding.name)):
        # doc.append(evidence.created_at)
        doc.append(finding.description)
        doc.append(italic('italic text. '))
        for proof in finding.proofs:
            add_proof(doc,proof)

        # with doc.create(Subsection('A subsection')):
        #     doc.append('Also some crazy characters: $&#{}')


def generate_report(project):
    # Basic document
    geometry_options = {
        "head": "40pt",
        "margin": "1in",
        "bottom": "1in"
    }
    doc = Document(default_filepath="evidences\\{}".format(project.id), geometry_options=geometry_options)
    doc.packages.append(Package('listings'))
    doc.packages.append(Package('color'))
    doc.append(NoEscape(r'''
    
                  \definecolor{codegreen}{rgb}{0,0.6,0}
                  \definecolor{codegray}{rgb}{0.5,0.5,0.5}
                  \definecolor{codepurple}{rgb}{0.58,0,0.82}
                  \definecolor{backcolour}{rgb}{0,0,0}
                  \definecolor{mycolor}{rgb}{1,1,1}
                  \lstdefinestyle{mystyle}{
                      backgroundcolor=\color{backcolour},   
                      commentstyle=\color{codegreen},
                      keywordstyle=\color{magenta},
                      numberstyle=\tiny\color{codegray},
                      stringstyle=\color{codepurple},
                      basicstyle=\footnotesize\color{mycolor},
                      breakatwhitespace=false,         
                      breaklines=true,                 
                      captionpos=b,                    
                      keepspaces=true,                 
                      numbers=left,                    
                      numbersep=5pt,                  
                      showspaces=false,                
                      showstringspaces=false,
                      showtabs=false,                  
                      tabsize=2,
                      inputencoding=latin1
                  }
                  \lstset{style=mystyle}       
                  '''))

    doc.preamble.append(Command('title', project.name))
    doc.preamble.append(Command('author', 'Anonymous author'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    for finding in project.findings:
        add_finding(doc, finding)
        # fill_document(doc)

    doc.generate_tex()
    doc.generate_pdf()

    tex = doc.dumps()  # The document as string in LaTeX syntax


if __name__ == '__main__':
    pass