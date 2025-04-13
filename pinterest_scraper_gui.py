# Updated image paths to absolute dynamic paths for .exe compatibility

import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import webbrowser
import sys

# Handle base path for .exe compatibility
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Scraping logic
def scrape_pinterest_kw_suggestions(keyword):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    suggestions = []
    try:
        driver.get(f"https://www.pinterest.com/search/pins/?q={keyword}")
        time.sleep(3)
        buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-test-id="one-bar-pill"]')
        for btn in buttons:
            suggestions.append(btn.text.strip())
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        driver.quit()
    return suggestions

# Create circle image
def circle_image(filename, size=(80, 80)):
    path = os.path.join(base_path, filename)
    img = Image.open(path).resize(size).convert("RGBA")
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

# Open website
def open_website(event):
    webbrowser.open_new("https://muhammadahsaniqbal.com/")

# Download .txt
def download_file():
    if not long_tail_keywords:
        messagebox.showerror("Download Error", "No long-tail keywords to download.")
        return
    dest_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if dest_path:
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.writelines([kw + "\n" for kw in long_tail_keywords])
        messagebox.showinfo("Downloaded", f"Long-tail keywords saved to:\n{dest_path}")

# GUI
root = tk.Tk()
root.title("Pinterest Keyword Suggestion Scraper")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="white")

# Load images
pinterest_logo = circle_image("pinterest_logo.png")
avatar_image = circle_image("ahsan_avatar.png")

# Header
header_frame = tk.Frame(root, bg="white")
header_frame.pack(pady=10)

logo_label = tk.Label(header_frame, image=pinterest_logo, bg="white")
logo_label.pack(side=tk.LEFT, padx=5)

x_label = tk.Label(header_frame, text="X", font=("Arial", 24, "bold"), fg="#8F49EB", bg="white")
x_label.pack(side=tk.LEFT, padx=5)

avatar_label = tk.Label(header_frame, image=avatar_image, bg="white", cursor="hand2")
avatar_label.pack(side=tk.LEFT, padx=5)
avatar_label.bind("<Button-1>", open_website)

# Title
title_label = tk.Label(root, text="PINTEREST KEYWORD SUGGESTION SCRAPER", font=("Barlow Semi Condensed", 16, "bold"), fg="#8F49EB", bg="white")
title_label.pack(pady=(0, 15))

# Entry field
entry = tk.Entry(root, font=("Arial", 14), width=30, bd=1, relief="solid")
entry.pack(pady=5)
entry.configure(highlightbackground="#ccc", highlightcolor="#ccc", highlightthickness=1)

# Table frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("Seed Keyword", "Suggestion", "Long-tail KW")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, stretch=True, width=200)
tree.pack()

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
style.configure("Treeview", font=("Arial", 10), rowheight=25)

long_tail_keywords = []

# Scrape button
def on_scrape():
    tree.delete(*tree.get_children())
    long_tail_keywords.clear()
    keyword = entry.get().strip()
    if not keyword:
        messagebox.showwarning("Input Required", "Please enter a seed keyword.")
        return
    suggestions = scrape_pinterest_kw_suggestions(keyword)
    for sug in suggestions:
        long_tail = f"{sug} {keyword}".strip()
        tree.insert("", tk.END, values=(keyword, sug, long_tail))
        long_tail_keywords.append(long_tail)
    download_btn.pack(pady=5)

scrape_btn = tk.Button(root, text="Scrape Suggestions", bg="#8F49EB", fg="white", font=("Arial", 12), command=on_scrape)
scrape_btn.pack(pady=10)

# Download button (initially hidden)
download_btn = tk.Button(root, text="Download Long-tail KWs", bg="red", fg="white", font=("Arial", 11), command=download_file)
download_btn.pack_forget()

# Footer
footer = tk.Label(root, text="Made with Love ❤️ by Ahsan Iqbal", font=("Arial", 9), fg="#666", bg="white", cursor="hand2")
footer.pack(side=tk.BOTTOM, pady=10)
footer.bind("<Button-1>", open_website)

root.mainloop()