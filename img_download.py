from bing_image_downloader import downloader
import os
import random

def change_extension_to_jpg(thai_name_folder):
    files = os.listdir(thai_name_folder)
    
    for file in files:
        if not file.endswith('.jpg'):
            base_name = os.path.splitext(file)[0]
            new_name = base_name + '.jpg'
            
            old_path = os.path.join(thai_name_folder, file)
            new_path = os.path.join(thai_name_folder, new_name)
            os.rename(old_path, new_path)

def download(query, limit):
    downloader.download(
        query, 
        limit=limit,  
        output_dir='n-shot/images', 
        adult_filter_off=True, 
        force_replace=False, 
        timeout=60, 
        verbose=False
    )

def split_images(dataset_dir, split):
    thai_names = os.listdir(dataset_dir)

    with open(f'dataset/meta/train.txt', 'w', encoding='utf-8') as train_txt, \
         open(f'dataset/meta/test.txt', 'w', encoding='utf-8') as test_txt:

        for thai_name in thai_names:
            thai_name_folder = os.path.join(dataset_dir, thai_name)

            change_extension_to_jpg(thai_name_folder)

            image_files = [f for f in os.listdir(thai_name_folder) if f.endswith('.jpg')]
            len_data = len(image_files)
            random.shuffle(image_files)

            train_images = image_files[:int(len_data * split)]
            test_images = image_files[int(len_data * split):]

            for img in train_images:
                train_txt.write(f'{thai_name}/{img.split('.jpg')[0]}\n')
            for img in test_images:
                test_txt.write(f'{thai_name}/{img.split('.jpg')[0]}\n')

if __name__ == "__main__":
    N = 10

    thai_name = []
    with open('n-shot/meta/test_classes.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            thai_name.append(line.split('\n')[0].strip())

    for thai in thai_name: 
        download(query=thai, limit=N)
        path = f"n-shot/images/{thai}"
        change_extension_to_jpg(path)