"Command line demo  of the MEDIQUEST ASSISTANT "

"Run with: python main.py "

import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from MEDIQUEST_ASSISTANT import ask , build_MEDIQUEST_ASSISTANT

def main():
    print("Building the MEDIQUEST assistant...")
    agent = build_MEDIQUEST_ASSISTANT()
    print("Assistant ready!\n")

    demo_questions = [
        "What is dengue?",
        "What is Heat atttack how to avoid it?",
        "What is hip fillers?",
    ]   

    for question in demo_questions:
            print("=" * 60)
            print("QUESTION:", question)
            print("-" * 60)

             
            answer = ask(agent, question)
            print("ANSWER:", answer)
            print("=" * 60)
            print()



if __name__ == "__main__":
      main()





