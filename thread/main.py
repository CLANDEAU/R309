import time
import threading
import concurrent.futures
import requests
import multiprocessing
import sys

img_urls = [
'https://cdn.pixabay.com/photo/2017/03/13/10/31/greylag-goose-2139296_960_720.jpg',
'https://cdn.pixabay.com/photo/2016/04/25/23/53/euro-1353420_960_720.jpg',
'https://cdn.pixabay.com/photo/2017/08/10/22/14/dinosaur-2628309_960_720.jpg'
]

def download_image(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[9]
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)

def thread():
    start = time.perf_counter()
    for i in range(len(img_urls)):
        t=threading.Thread(target=download_image, args=[img_urls[i]])
        t.start()
        t.join()
    end = time.perf_counter()
    temp=round(end - start, 2)
    return f"Tasks ended in {temp} second(s) (thread)", temp

def pool():
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, img_urls)
    end = time.perf_counter()
    temp=round(end - start, 2)
    return f"Tasks ended in {temp} second(s) (pool)",temp

def mutliproc():
    start = time.perf_counter()
    for i in range(len(img_urls)):
        p = multiprocessing.Process(target=download_image(img_urls[i]))
        p.start()
        p.join()
    end = time.perf_counter()
    temp=round(end - start, 2)
    return f"Tasks ended in {temp} second(s) (mutliprocessus)",temp

if __name__=='__main__':
    try:
        nb = sys.argv[1].split("=")[1]
        nb=int(nb)
        list_thread=[]
        list_pool=[]
        list_multiproc=[]
        for i in range(nb):
            print(f"DOWNLOAD {i+1}/{nb}")
            print(thread()[0])
            list_thread.append(thread()[1])
            print(pool()[0])
            list_pool.append(pool()[1])
            print(mutliproc()[0])
            list_multiproc.append(mutliproc()[1])
        print(f"La moyenne de temp pour les Threads est de {round(sum(list_thread)/len(list_thread),2)}")
        print(f"La moyenne de temp pour le Pool est de {round(sum(list_pool) / len(list_pool),2)}")
        print(f"La moyenne de temp pour le Multiprccessus est de {round(sum(list_multiproc) / len(list_multiproc),2)}")
    except:
        print("Veuillez entrez une valeur correcte")