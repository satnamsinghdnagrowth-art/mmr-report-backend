import os


def create_required_folders():
    base_path = "database"
    os.makedirs(base_path, exist_ok=True)  # ensure base folder exists

    folders = ["customKPIs", "reportsDataFiles", "uploadedFiles"]
    for folder in folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)
