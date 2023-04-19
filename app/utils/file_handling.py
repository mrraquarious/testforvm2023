import os
import threading

def schedule_file_deletion(filename, delay):
    timer = threading.Timer(delay, delete_file, args=[filename])
    timer.start()

def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f"File {filename} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file {filename}: {str(e)}")
