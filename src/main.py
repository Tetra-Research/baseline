from dotenv import load_dotenv

# from projects.promptbuf.test import run as run_promptbuf_single_eval
from projects.promptbuf.test import run2 as run_promptbuf_with_threshold

load_dotenv()
if __name__ == "__main__":
    run_promptbuf_with_threshold()
