import os
import traceback
import wget
import requests
import time
from threading import Thread
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


tmp_link = "https://media.kantarmedia.pl/multimedia/"

dirname = os.path.dirname(__file__)
folder = os.path.join(dirname, "spoty3")

try:
    os.mkdir("spoty3")
except:
    pass

internet_list = [".jpg"]


def translate_media(audiocode):
    audiocode_media = int(audiocode)
    if audiocode_media >= 70000000 and audiocode_media < 90000000:
        media = "INTERNET"

    return media


def split_list(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(n))


def download(d_list):
    try:
        for row in tqdm(d_list):
            audiocode_spot = str(row[0])
            if translate_media(audiocode_spot) == "INTERNET":
                url = (
                        tmp_link
                        + translate_media(audiocode_spot)
                        + "/MR/"
                        + audiocode_spot[:5]
                        + "/"
                        + audiocode_spot
                        + "__.jpg"
                )
                url1 = (
                        tmp_link
                        + translate_media(audiocode_spot)
                        + "/ALL/"
                        + audiocode_spot[:5]
                        + "/"
                        + audiocode_spot
                )
                response1 = requests.request(
                    "GET", url, verify=False, allow_redirects=False, timeout=30
                )
                tmp = 0
                for internet_spot in internet_list:
                    response2 = requests.request(
                        "GET",
                        (url1 + internet_spot),
                        verify=False,
                        allow_redirects=False,
                        timeout=60
                    )
                    if response2.status_code == 200:
                        try:
                            tmp = 1
                            wget.download(url1 + internet_spot, folder)
                            break
                        except Exception as e:
                            pass
                            # print(f'Could not download {audiocode_spot}')
                    else:
                        pass
                        # print(f'Could not download {audiocode_spot}')
                if response1.status_code == 200 and tmp == 0:
                    try:
                        wget.download(url, folder)
                        tmp = 1
                    except Exception as e:
                        # print(f'Could not download {audiocode_spot}')
                        pass
            else:
                pass
                # print(f'Could not download {audiocode_spot}')
    except Exception as e:
        print(e)


def rename(r_list):
    try:
        for file in r_list:
            if "_" in file:
                name = file.replace("_", "")
                os.rename(os.path.join(folder, file), os.path.join(folder, name))
    except Exception as e:
        pass


def main(list_audiocode):
    try:
        d_lists = list(split_list(list(list_audiocode), 10))

        print("Download stage 1/3:")
        start = time.time()
        threads = []
        for index in range(len(d_lists)):
            x = Thread(target=download, args=(d_lists[index],), )
            threads.append(x)
            x.start()
        for t in threads:
            t.join()
        end = time.time()
        print("")
        print(end - start)

        print("Rename stage 2/3")
        r_lists = list(split_list(os.listdir(folder), 33))
        start = time.time()
        threads = []
        for index in range(len(r_lists)):
            x = Thread(target=rename, args=(r_lists[index],), )
            threads.append(x)
            x.start()
        for t in threads:
            t.join()
        end = time.time()
        print(end - start)

        print(f"All done, downloaded {len(os.listdir(folder))}")
        start = time.time()
        end = time.time()
        print(end - start)

    except Exception as e:
        print(e)
        pass


def chunker(seq, size):
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


if __name__ == '__main__':

    start = time.time()
    try:
        list_audiocode = [[x] for x in range(70000007, 90000000, 3017)]

        print("Codes attempted to download: ", len(list_audiocode))
        all_todo = len(list_audiocode)

        list_audiocode = list(list_audiocode)
        for audio_batch in chunker(list_audiocode, 10000):
            try:
                conn = None
                cur = None
                final_list = []
                print(f"Progress: {len(os.listdir(folder))}/{all_todo}")
                main(audio_batch)
            except Exception as e:
                print(e)
                traceback.print_exc()
                break

    except Exception as e:
        print(e)
        traceback.print_exc()

    finally:
        stop = time.time()
        print("\nTime: " + str(stop - start))