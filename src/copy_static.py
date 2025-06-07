import os
import shutil

def copy_directory_recursive(src, dst):
    # Delete the destination directory if it exists
    if os.path.exists(dst):
        print(f"Deleting existing contents of: {dst}")
        shutil.rmtree(dst)
    
    # Recreate the destination directory
    os.mkdir(dst)

    def copy_contents(current_src, current_dst):
        for item in os.listdir(current_src):
            src_path = os.path.join(current_src, item)
            dst_path = os.path.join(current_dst, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copied file: {src_path} -> {dst_path}")
            elif os.path.isdir(src_path):
                os.mkdir(dst_path)
                print(f"Created directory: {dst_path}")
                copy_contents(src_path, dst_path)

    copy_contents(src, dst)

def main():
    source_dir = 'static'
    destination_dir = 'public'
    copy_directory_recursive(source_dir, destination_dir)

if __name__ == '__main__':
    main()
