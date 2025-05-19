from robocorp.tasks import task
from RPA.Archive import Archive
import os

archive = Archive()

file_path = os.path.join(os.getcwd()+"/"+"Image")
dest_file = os.path.join(os.getcwd()+"/"+"output")

@task
def archive_task():
   archive.archive_folder_with_tar(file_path, archive_name="Image.tar" ,recursive=True)
   files = archive.list_archive("Image.tar")
   for file in files:
      print(file["name"])

   archive.add_to_archive(os.getcwd()+"/"+"robot.yaml", "Image.tar")
   get_info = archive.get_archive_info("Image.tar")
   print(get_info)
   archive.extract_archive("Image.tar",dest_file )

