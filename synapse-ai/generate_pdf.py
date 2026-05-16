from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(filename="Operating_Systems_and_DBMS_Concepts.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center
    heading_style = styles['Heading2']
    body_style = styles['BodyText']
    
    Story = []
    
    # Title
    Story.append(Paragraph("Core Concepts in Operating Systems & DBMS", title_style))
    Story.append(Spacer(1, 20))
    
    # Section 1: Operating Systems
    Story.append(Paragraph("1. Operating Systems: Deadlocks", heading_style))
    Story.append(Spacer(1, 10))
    os_text = """A deadlock in an operating system is a situation where a set of processes are blocked because each process is holding a resource and waiting for another resource acquired by some other process. 
    <br/><br/>
    <b>Conditions for Deadlock:</b><br/>
    1. <b>Mutual Exclusion:</b> At least one resource must be held in a non-shareable mode.<br/>
    2. <b>Hold and Wait:</b> A process is currently holding at least one resource and requesting additional resources.<br/>
    3. <b>No Preemption:</b> Resources cannot be forcibly removed from the processes holding them.<br/>
    4. <b>Circular Wait:</b> A closed chain of processes exists, where each process holds at least one resource needed by the next process in the chain.<br/>
    <br/>
    <b>Example:</b> Two processes, P1 and P2, and two resources, R1 and R2. P1 holds R1 and requests R2. P2 holds R2 and requests R1. Neither can proceed.
    """
    Story.append(Paragraph(os_text, body_style))
    Story.append(Spacer(1, 20))
    
    # Section 2: DBMS
    Story.append(Paragraph("2. Database Management Systems (DBMS)", heading_style))
    Story.append(Spacer(1, 10))
    dbms_text = """A Database Management System (DBMS) is software designed to store, retrieve, define, and manage data in a database.
    <br/><br/>
    <b>Key Concepts:</b><br/>
    - <b>ACID Properties:</b> Atomicity, Consistency, Isolation, and Durability ensure reliable database transactions.<br/>
    - <b>Normalization:</b> The process of organizing data to reduce redundancy and improve data integrity.<br/>
    - <b>Transactions:</b> A logical unit of work that contains one or more SQL statements.<br/>
    <br/>
    Preparing for a DBMS exam involves understanding relational algebra, normalization forms (1NF, 2NF, 3NF, BCNF), transaction management, and concurrency control protocols like Two-Phase Locking (2PL).
    """
    Story.append(Paragraph(dbms_text, body_style))
    
    doc.build(Story)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    create_pdf()
