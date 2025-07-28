import random
import os

def ask_questions():
    # Possible questions in randomized form
    questions = [
        ("What is your name?", "name"),
        ("How old are you?", "age"),
        ("What's your favorite color?", "color"),
        ("What food do you enjoy the most?", "food"),
        ("Which city do you live in?", "city"),
    ]

    random.shuffle(questions)
    answers = {}

    for q, key in questions:
        answers[key] = input(q + " ")

    return answers

def display_summary(data):
    summary = f"""
Hello, {data['name']}!
You are {data['age']} years old, love the color {data['color']}, and enjoy eating {data['food']}.
Life must be awesome in {data['city']}!
"""
    print(summary)
    return summary

def save_to_file(data, summary, rating):
    filename = f"{data['name']}.txt"
    with open(filename, 'w') as file:
        file.write(summary)
        file.write(f"User Rating: {rating} stars\n")
    print(f"Summary saved to {filename}!")

def main():
    while True:
        print("\nLet's get to know you a bit!")
        data = ask_questions()
        summary = display_summary(data)

        save = input("Do you want to save this summary to a file? (yes/no): ").strip().lower()
        if save == 'yes':
            while True:
                try:
                    rating = int(input("Please rate this assistant (1 to 5 stars): "))
                    if 1 <= rating <= 5:
                        break
                    else:
                        print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Enter a valid number.")
            save_to_file(data, summary, rating)

        again = input("\nWould you like to start over and try again? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Thanks for playing! Goodbye ")
            break

if __name__ == "__main__":
    main()
