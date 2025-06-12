import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_column_from_csv(file_path: str, x_col: str, y_col: str):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Error reading the file: {e}")
        return

    # Show column names
    print("📄 Available columns:")
    print(df.columns.tolist())

    # Check if columns exist
    if x_col not in df.columns or y_col not in df.columns:
        print(f"❌ One or both columns not found in the CSV!")
        return

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(df[x_col], df[y_col], marker='o', linestyle='-', color='blue')
    plt.title(f"{y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 🧪 Example usage:
if __name__ == "__main__":
    path = "./raw_data/Bitcoin.csv"
    x_column = "Price"
    y_column = "Low"

    plot_column_from_csv(path, x_column, y_column)



