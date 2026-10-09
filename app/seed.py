from sqlalchemy.orm import Session
from .models import User, Exam, Question
from .security import hash_password
EXAMS = [
("Python Fundamentals","Programming","Core Python syntax, data structures and problem solving.",15,[
("Which keyword defines a function in Python?","func","def","function","lambda","B"),
("What is the result of len([2, 4, 6])?","2","3","4","6","B"),
("Which type is immutable?","list","dict","set","tuple","D"),
("Which symbol starts a single-line comment?","//","#","<!--",";","B"),
("What does 10 // 3 return?","3.33","3","1","0","B")]),
("Data Structures","Computer Science","Assess arrays, stacks, queues and complexity basics.",15,[
("Which structure follows LIFO?","Queue","Stack","Tree","Graph","B"),
("Binary search requires data to be…","Random","Sorted","Unique only","Reversed","B"),
("Which is a FIFO structure?","Stack","Heap","Queue","Tree","C"),
("Average lookup in a hash table is typically…","O(1)","O(n²)","O(log n)","O(n log n)","A"),
("A tree with n nodes has how many edges?","n","n+1","n-1","2n","C")]),
("Database Fundamentals","Databases","SQL, keys and relational database concepts.",15,[
("Which SQL command retrieves rows?","GET","SELECT","FETCHALL","OPEN","B"),
("A primary key must be…","Nullable","Unique and non-null","Text only","Repeated","B"),
("Which clause filters grouped results?","WHERE","ORDER BY","HAVING","LIMIT","C"),
("Which operation combines rows from tables?","JOIN","MERGEFILE","BIND","STACK","A"),
("Which command removes table rows but keeps the table?","DROP","ALTER","TRUNCATE","CREATE","C")]),
("Web Development Basics","Web Technology","HTTP, frontend and API fundamentals.",15,[
("Which protocol is used for web APIs?","HTTP","FTP only","SMTP","SSH only","A"),
("Which status code means success?","404","500","200","301","C"),
("Which language structures a web page?","SQL","HTML","Bash","R","B"),
("CSS is mainly used for…","Styling","Database queries","Server routing","Encryption","A"),
("JSON represents data as…","Only images","Key-value structures","Compiled binaries","SQL tables only","B")]),
("Operating Systems","Systems","Processes, memory and operating system concepts.",15,[
("Which is responsible for process scheduling?","Compiler","OS scheduler","Browser","DNS","B"),
("A deadlock requires how many Coffman conditions?","2","3","4","5","C"),
("Virtual memory commonly uses…","Disk space","GPU cache only","Printer memory","DNS records","A"),
("Which is a process state?","Ready","Markup","Encoded","Indexed","A"),
("A context switch changes the…","CPU execution context","File extension","IP address","Screen size","A")]),
("Computer Networks","Networking","Networking layers, addressing and common protocols.",15,[
("DNS translates domain names to…","MAC addresses only","IP addresses","Passwords","HTML","B"),
("HTTPS adds which protection to HTTP?","TLS encryption","Compression only","Caching only","Routing tables","A"),
("Which device forwards packets between networks?","Router","Keyboard","Repeater only","Monitor","A"),
("TCP is…","Connection-oriented","Always broadcast","A file format","A database","A"),
("IPv4 addresses are how many bits?","16","32","64","128","B")]),
("Software Engineering","Engineering","Testing, design principles and delivery practices.",15,[
("Unit testing focuses on…","Small units of code","Entire country network","Only UI colors","Production servers only","A"),
("What does CI stand for?","Continuous Integration","Code Inspection only","Central Internet","Compiled Interface","A"),
("Which is a version-control system?","Git","Figma","Nginx","SQLite only","A"),
("A requirement describes…","Expected system behavior","Only code formatting","CPU temperature","A random test result","A"),
("Which design principle reduces coupling?","Single responsibility","Global state everywhere","Duplicate logic","Hard-coded secrets","A")]),
("Cybersecurity Essentials","Security","Authentication, access control and common security concepts.",15,[
("Authentication verifies…","Identity","File size","Network speed","Page layout","A"),
("Which is a strong password practice?","Reuse everywhere","Use unique long passwords","Share with team","Store in plain text","B"),
("SQL injection targets…","Database queries","CSS layout","Image resolution","RAM timing","A"),
("MFA means…","Multi-Factor Authentication","Main File Access","Managed Fast API","Multiple File Archive","A"),
("HTTPS certificates help verify…","Server identity","User typing speed","Database schema","Wi-Fi strength","A")]),
("Cloud Computing","Cloud","Scalability, service models and cloud architecture.",15,[
("Horizontal scaling adds more…","Instances","RAM to one instance only","Columns","CSS rules","A"),
("SaaS stands for…","Software as a Service","Storage as a Server","Security at a Site","System and Software","A"),
("A load balancer distributes…","Incoming traffic","Passwords","Source code","Database schemas","A"),
("Which is object storage?","Blob storage","CPU register","Stack memory","DNS cache","A"),
("Autoscaling responds to…","Configured demand/metrics","Font choice","Manual typing only","File names","A")]),
("System Design Basics","Architecture","APIs, caching, queues and scalable system design.",15,[
("A cache primarily reduces…","Repeated data access latency","User accounts","Network addresses","Data correctness","A"),
("A message queue helps…","Decouple services","Render CSS","Replace every database","Encrypt passwords automatically","A"),
("REST resources are commonly identified by…","URIs","CSS classes","CPU cores","File permissions","A"),
("Which status often indicates resource creation?","201","401","503","204","A"),
("A database index usually improves…","Read lookup speed","Every write at no cost","Data privacy automatically","Network bandwidth","A")]),
]
def seed(db: Session):
    if not db.query(User).filter_by(email="student@examflow.demo").first():
        db.add_all([User(name="Demo Student",email="student@examflow.demo",password_hash=hash_password("Student@123"),role="student"),
                    User(name="Platform Admin",email="admin@examflow.demo",password_hash=hash_password("Admin@123"),role="admin")])
    if db.query(Exam).count()==0:
        for title,subject,desc,duration,qs in EXAMS:
            exam=Exam(title=title,subject=subject,description=desc,duration_minutes=duration,is_published=True)
            db.add(exam); db.flush()
            for prompt,a,b,c,d,correct in qs:
                db.add(Question(exam_id=exam.id,prompt=prompt,option_a=a,option_b=b,option_c=c,option_d=d,correct_option=correct,points=1))
    db.commit()
