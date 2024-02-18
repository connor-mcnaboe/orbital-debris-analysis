import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from orbital_debris_analysis.csv_parser.csv_parser import csv_to_pandas
from orbital_debris_analysis.debris_analysis.debris_analysis import calculate_threat_model, extract_analysis_data
from orbital_debris_analysis.models.mission import Mission
from orbital_debris_analysis.models.threat_report import ThreatReport


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mission Data Input")
        self.geometry("700x900")  # Increased window size for plot

        # Labels and Entries
        tk.Label(self, text="Mission Apogee (km)").grid(row=0, column=0, sticky='w')
        tk.Label(self, text="Mission Perigee (km)").grid(row=1, column=0, sticky='w')
        tk.Label(self, text="Mission Threat Tolerance (+/-km)").grid(row=2, column=0, sticky='w')

        self.apogee_var = tk.IntVar()
        self.perigee_var = tk.IntVar()
        self.threat_tolerance_var = tk.IntVar()

        tk.Entry(self, textvariable=self.apogee_var).grid(row=0, column=1)
        tk.Entry(self, textvariable=self.perigee_var).grid(row=1, column=1)
        tk.Entry(self, textvariable=self.threat_tolerance_var).grid(row=2, column=1)

        # File Upload
        self.file_path = None
        tk.Button(self, text="Upload File", command=self.upload_file).grid(row=3, column=0, columnspan=2)

        # Submit Button
        tk.Button(self, text="Submit", command=self.submit_data).grid(row=4, column=0, columnspan=2)

        # Placeholder for the plot
        self.plot_frame = tk.Frame(self)
        self.plot_frame.grid(row=5, column=0, columnspan=2)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            messagebox.showinfo("File Uploaded", f"File {self.file_path} has been uploaded successfully.")
        else:
            messagebox.showinfo("File Upload", "No file was selected.")

    def submit_data(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a CSV file before submitting.")
            return

        # Assuming the file_path is valid and points to a CSV file
        try:
            extracted_data = csv_to_pandas(self.file_path)
            threat_model = calculate_threat_model(data_frame=extract_analysis_data(data_frame=extracted_data),
                                                  mission=Mission(apogee=self.apogee_var.get(),
                                                                  perigee=self.perigee_var.get(),
                                                                  threat_tolerance_km=self.threat_tolerance_var.get()))
            self.show_plot(threat_report=threat_model)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the CSV file. Error: {str(e)}")

    def show_plot(self, threat_report: ThreatReport):
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create figure for the plot
        fig = Figure(figsize=(7, 8), dpi=100)
        plot = fig.add_subplot(111)

        # Extracting values from the Pydantic model
        categories = ['Total Threat', 'Rocket Body Threat', 'Debris Threat', 'Inactive Satellite Threat',
                      'Active Satellite Threat']
        values = [
            threat_report.total_threat_count,
            threat_report.rocket_body_threat_count,
            threat_report.debris_threat_count,
            threat_report.inactive_sat_threat_count,
            threat_report.active_sat_threat_count
        ]

        plot.bar(categories, values, color='skyblue')

        plot.set_xlabel('Threat Categories')
        plot.set_ylabel('Count')
        plot.set_title('Mission Threat Counts')
        plot.tick_params(axis='x', rotation=45)

        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
