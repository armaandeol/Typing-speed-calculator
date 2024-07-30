import tkinter as tk
import random
import time
import csv
import matplotlib.pyplot as plt
from text import sentences
import math

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("2560x1440")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        top = []
        try:
            with open("wpm_data.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    top.append(float(row[1]))
        except FileNotFoundError:
            pass

        self.score = math.floor(max(top)) if top else 0
        self.high_score = tk.Label(root, text=f"High Score: {self.score}", font=("Arial", 30))
        self.high_score.pack(pady=10)

        self.display_label = tk.Label(root, text="", font=("Arial", 16), wraplength=480)
        self.display_label.pack(pady=20)

        self.input_entry = tk.Entry(root, font=("Arial", 16))
        self.input_entry.pack(pady=20, fill=tk.BOTH, expand=True)
        self.input_entry.focus_set()
        self.input_entry.bind("<KeyRelease>", self.check_input)

        self.timer_label = tk.Label(root, text="Time: 30s", font=("Arial", 16))
        self.timer_label.pack(pady=10)

        self.current_sentences = []
        self.original_text = ""
        self.start_time = None
        self.results_window = None

        self.update_text()
        self.start_test()

    def update_text(self):
        self.current_sentences = random.sample(sentences, 7)
        self.original_text = " ".join(self.current_sentences)
        self.display_label.config(text=self.original_text)

    def start_test(self):
        self.start_time = time.time()
        self.update_timer()
        self.root.after(30000, self.capture_input)

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, 30 - int(elapsed_time))
        self.timer_label.config(text=f"Time: {remaining_time}s")

        if remaining_time > 0:
            self.root.after(1000, self.update_timer)

    def calculate_wpm(self, text, duration):
        words = len(text.split())
        minutes = duration / 60
        return words / minutes

    def check_input(self, event):
        user_input = self.input_entry.get()
        correct_input = self.original_text[:len(user_input)]

        # Change background color based on correctness
        if user_input == correct_input:
            self.input_entry.config(bg="green")
        else:
            self.input_entry.config(bg="red")

    def capture_input(self):
        user_input = self.input_entry.get()
        end_time = time.time()
        duration = end_time - self.start_time

        # Calculate WPM
        wpm = self.calculate_wpm(user_input, duration)

        # Clear the entry
        self.input_entry.delete(0, tk.END)

        # Save WPM data
        self.save_wpm_data(wpm)

        # Show results
        self.show_results(wpm)

    def save_wpm_data(self, wpm):
        try:
            with open("wpm_data.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), wpm])
        except Exception as e:
            print(f"Error saving WPM data: {e}")

    def show_results(self, wpm):
        if self.results_window:
            self.results_window.destroy()

        self.results_window = tk.Toplevel(self.root)
        self.results_window.title("Results")
        self.results_window.geometry("300x200")

        result_label = tk.Label(self.results_window, text=f"WPM: {wpm:.2f}",
                                font=("Arial", 16))
        result_label.pack(pady=20)

        quit_button = tk.Button(self.results_window, text="Quit", command=self.quit_app)
        quit_button.pack(side=tk.LEFT, padx=10, pady=10)

        restart_button = tk.Button(self.results_window, text="Restart", command=self.restart_test)
        restart_button.pack(side=tk.RIGHT, padx=10, pady=10)

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

            self.root.quit()

        except Exception as e:
            print(f"Error visualizing WPM data: {e}")

    def quit_app(self):
        self.root.quit()

    def restart_test(self):
        if self.results_window:
            self.results_window.destroy()
            self.results_window = None

        self.input_entry.delete(0, tk.END)
        self.update_text()
        self.start_test()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
