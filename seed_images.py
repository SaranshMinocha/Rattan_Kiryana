import sqlite3

conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# 1. Add column if it does not exist
try:
    cursor.execute("ALTER TABLE Products ADD COLUMN image_url TEXT DEFAULT ''")
    conn.commit()
except Exception:
    pass

# 2. Update real product images directly into your database
brand_images = {
    "Tata": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500&auto=format&fit=crop&q=80",
    "Red Label": "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?w=500&auto=format&fit=crop&q=80",
    "Dettol": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&auto=format&fit=crop&q=80",
    "Dove": "https://images.unsplash.com/photo-1607006314175-103362145b59?w=500&auto=format&fit=crop&q=80",
    "Fortune": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&auto=format&fit=crop&q=80",
    "Maggi": "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=500&auto=format&fit=crop&q=80",
}

for brand, url in brand_images.items():
    cursor.execute("UPDATE Products SET image_url = ? WHERE Brand = ?", (url, brand))

conn.commit()
conn.close()
print("Images seeded successfully!")