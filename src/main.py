from dotenv import load_dotenv
from projects.promptbuf.test import run as run_promptbuf_full

load_dotenv()
if __name__ == "__main__":
    run_promptbuf_full()
