import tkinter as tk
from tkinter import messagebox
import pandas as pd
import charset_normalizer


def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        result = charset_normalizer.detect(raw_data)
        return result['encoding']
    except Exception as e:
        messagebox.showerror("Error", f"Failed to detect encoding for {file_path}: {e}")
        return None


def load_data():
    try:
        
        dataset_paths = [
            "C:\\Users\\KRISHNAN\\Downloads\\tcc_ceds_music.csv",
            "C:\\Users\\KRISHNAN\\Downloads\\Hindi_songs.csv",
            "C:\\Users\\KRISHNAN\\Downloads\\Malayalam_songs.csv",
            "C:\\Users\\KRISHNAN\\Downloads\\Tamil_songs.csv"
        ]

        # Load each dataset and combine them
        combined_data = pd.DataFrame()
        for file_path in dataset_paths:
            encoding = detect_encoding(file_path)
            data = pd.read_csv(file_path, encoding=encoding)

            # Combine the datasets
            combined_data = pd.concat([combined_data, data], ignore_index=True)

        return combined_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return None

# Function to filter and recommend music
def recommend_music(release_date, artist, genre, data):
    # Start with the dataset
    filtered_data = data.copy()

    # Filter by release_date if the 'release_date' column exists
    if release_date:
        try:
            filtered_data = filtered_data[filtered_data['release_date'] == int(release_date)]
        except (KeyError, ValueError):
            pass  # Ignore invalid or missing 'release_date' column/inputs

    # Filter by artist if the 'artist_name' column exists
    if artist and 'artist_name' in filtered_data.columns:
        filtered_data['artist_name'] = filtered_data['artist_name'].astype(str)
        filtered_data = filtered_data[filtered_data['artist_name'].str.contains(artist, case=False, na=False)]

    # Filter by genre if the 'genre' column exists
    if genre and 'genre' in filtered_data.columns:
        filtered_data['genre'] = filtered_data['genre'].astype(str)
        filtered_data = filtered_data[filtered_data['genre'].str.contains(genre, case=False, na=False)]

    # Return top 100 recommendations or a message if no results found
    if filtered_data.empty:
        return "No recommendations found for the given inputs."

    # Return the filtered data with specified columns (only if they exist)
    available_columns = [col for col in ['track_name', 'artist_name', 'genre', 'release_date'] if col in filtered_data.columns]
    return filtered_data[available_columns].head(100)

# Handle the input from Tkinter and display recommendations
def get_recommendations():
    release_date = entry_release_date.get().strip()
    artist = entry_artist.get().strip()
    genre = entry_genre.get().strip()

    if not (release_date or artist or genre):
        messagebox.showwarning("Input Error", "Please enter at least one filter (Release Date, Artist, or Genre).")
        return

    recommendations = recommend_music(release_date, artist, genre, data)

    # Display the recommendations
    text_output.delete(1.0, tk.END)
    if isinstance(recommendations, pd.DataFrame):
        recommendations_str = recommendations.to_string(index=False)
    else:
        recommendations_str = recommendations
    
    text_output.insert(tk.END, recommendations_str)

# Create Tkinter window
root = tk.Tk()
root.title("🎵 Music Recommendation System 🎵")
root.geometry("800x600")  # Initial window size
root.minsize(800, 600)    # Minimum window size

# Add a gradient-like background using Canvas
canvas = tk.Canvas(root, bg="#f0f0f0", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Gradient background
canvas.create_rectangle(0, 0, 2000, 2000, fill="#6a11cb", outline="")  # Dark purple
canvas.create_rectangle(0, 0, 2000, 1000, fill="#2575fc", outline="")  # Light blue

# Add a stylish heading
heading_label = tk.Label(root, text="🎵 Music Recommendation System 🎵", font=("Poppins", 24, "bold"), bg="#2575fc", fg="white")
heading_label.place(relx=0.5, rely=0.1, anchor="center")


data = load_data()


label_release_date = tk.Label(root, text="Enter Release Date:", font=("Arial", 14), bg="#f0f0f0", fg="#333333")
label_release_date.place(relx=0.35, rely=0.3, anchor="e")
entry_release_date = tk.Entry(root, font=("Arial", 14))
entry_release_date.place(relx=0.36, rely=0.3, anchor="w", relwidth=0.3)  

label_artist = tk.Label(root, text="Enter Artist:", font=("Arial", 14), bg="#f0f0f0", fg="#333333")
label_artist.place(relx=0.35, rely=0.4, anchor="e")  
entry_artist = tk.Entry(root, font=("Arial", 14))
entry_artist.place(relx=0.36, rely=0.4, anchor="w", relwidth=0.3)  

label_genre = tk.Label(root, text="Enter Genre:", font=("Arial", 14), bg="#f0f0f0", fg="#333333")
label_genre.place(relx=0.35, rely=0.5, anchor="e")  
entry_genre = tk.Entry(root, font=("Arial", 14))
entry_genre.place(relx=0.36, rely=0.5, anchor="w", relwidth=0.3)  

button_recommend = tk.Button(root, text="Get Recommendations", command=get_recommendations, font=("Arial", 16, "bold"), bg="#ff9900", fg="white", relief="flat")
button_recommend.place(relx=0.5, rely=0.65, anchor="center", relwidth=0.4, relheight=0.08)


text_output = tk.Text(root, font=("Arial", 14), bg="#ffffff", fg="#333333", relief="groove", wrap="word")
text_output.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.8, relheight=0.2)


root.mainloop()
