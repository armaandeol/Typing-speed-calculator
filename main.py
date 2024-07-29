import tkinter as tk
import random
import time
import csv
import matplotlib.pyplot as plt
from text import sentences


class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("2560x1440")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.display_label = tk.Label(root, text="", font=("Arial", 16), wraplength=480)
        self.display_label.pack(pady=20)

        self.input_entry = tk.Entry(root, font=("Arial", 16))
        self.input_entry.pack(pady=20, fill=tk.BOTH, expand=True)
        self.input_entry.focus_set()  # Automatically focus on the input box

        self.current_sentences = []
        self.original_text = ""
        self.start_time = time.time()  # Track the start time
        self.results_window = None  # Initialize results window reference
        self.update_text()

        # Schedule to capture the input after 30 seconds
        self.root.after(30000, self.capture_input)

    def update_text(self):
        # Add 10 random sentences to the display list
        new_sentences = random.sample(sentences, 10)
        self.current_sentences.extend(new_sentences)

        # Keep only the last 10 sentences in the display list
        if len(self.current_sentences) > 10:
            self.current_sentences = self.current_sentences[-10:]

        # Update the display text
        self.original_text = " ".join(self.current_sentences)
        self.display_label.config(text=self.original_text)

    def calculate_wpm(self, text, duration):
        words = len(text.split())
        minutes = duration / 60
        return words / minutes

    def calculate_accuracy(self, user_input, original_text):
        # Clean up text for accuracy calculation
        user_input = user_input.strip()
        original_text = original_text.strip()

        # Determine the length of the relevant original text
        input_words = user_input.split()
        relevant_text = " ".join(original_text.split()[:len(input_words)])

        # Calculate number of correct characters
        correct_chars = sum(1 for u, o in zip(user_input, relevant_text) if u == o)

        # Calculate accuracy percentage
        accuracy = (correct_chars / len(relevant_text)) * 100
        return accuracy

    def capture_input(self):
        user_input = self.input_entry.get()
        end_time = time.time()
        duration = end_time - self.start_time  # Time taken in seconds

        # Calculate WPM
        wpm = self.calculate_wpm(user_input, duration)
        # Calculate Accuracy
        accuracy = self.calculate_accuracy(user_input, self.original_text)

        # Clear the entry
        self.input_entry.delete(0, tk.END)

        # Save WPM data
        self.save_wpm_data(wpm)

        # Show results
        self.show_results(wpm, accuracy)

    def save_wpm_data(self, wpm):
        try:
            with open("wpm_data.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), wpm])
        except Exception as e:
            print(f"Error saving WPM data: {e}")

    def show_results(self, wpm, accuracy):
        # Destroy the previous results window if it exists
        if self.results_window:
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.root)
        self.results_window.title("Results")
        self.results_window.geometry("300x200")

        result_label = tk.Label(self.results_window, text=f"WPM: {wpm:.2f}\nAccuracy: {accuracy:.2f}%",
                                font=("Arial", 16))
        result_label.pack(pady=20)

        # Create buttons for Quit and Restart
        quit_button = tk.Button(self.results_window, text="Quit", command=self.quit_app)
        quit_button.pack(side=tk.LEFT, padx=10, pady=10)

        restart_button = tk.Button(self.results_window, text="Restart", command=self.restart_test)
        restart_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add button to show graph
        show_graph_button = tk.Button(self.results_window, text="Show Graph", command=self.visualize_wpm_data)
        show_graph_button.pack(side=tk.BOTTOM, pady=10)

    def visualize_wpm_data(self):
        try:
            times = []
            wpms = []

            with open("wpm_data.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    times.append(row[0])
                    wpms.append(float(row[1]))

            plt.figure(figsize=(10, 6))
            plt.plot(times, wpms, marker='o', linestyle='-', color='b')
            plt.xlabel('Time')
            plt.ylabel('WPM')
            plt.title('Typing Speed Over Time')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

            # Close the Tkinter application after showing the graph
            self.root.quit()

        except Exception as e:
            print(f"Error visualizing WPM data: {e}")

    def quit_app(self):
        self.root.quit()

    def restart_test(self):
        # Destroy the results window
        if self.results_window:
            self.results_window.destroy()
            self.results_window = None

        self.start_time = time.time()
        self.update_text()
        self.root.after(20000, self.capture_input)


# Main application logic
if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
