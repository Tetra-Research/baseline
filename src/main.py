from dotenv import load_dotenv
from projects.mvp.test import run as run_mvp
from projects.promptbuf.test import run as run_promptbuf
from projects.promptbuf.full_test import run as run_promptbuf_full

load_dotenv()
if __name__ == "__main__":
    # run_mvp()
    # run_promptbuf()
    run_promptbuf_full()
