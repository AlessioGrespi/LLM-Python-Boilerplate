import uuid
from agents.secretary import main as secretary

session_id = str(uuid.uuid4())  # Replace with a dynamic session ID

output = secretary(session_id)


if output:
    print(output)