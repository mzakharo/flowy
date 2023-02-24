from analyze import analyze
import os
from glob import glob
import cv2
import multiprocessing
from pathlib import Path

lookup = {'00239359' :  '002399359',
        '002394300' :   '002399300', 
        '002395359' :   '002399359',
        '4002395705':   '002399705', 
        '4002399725':   '002399725',
        '4002399325':   '002399725',
        '002397420' :   '002399420',
        '002399125' :   '002399725',
        '002399250' :   '002399258',
        '002399310' :   '002399300',
        '002399354' :   '002399359',
        '02399300'  :   '002399300',
        '02399702'  :   '002399702',
        '002399225' :   '002399725',
        '002395122' :   '002399722',
        '002395702' :   '002399702',
        '402399725' :   '002399725',
        '4002399125':   '002399725',
        '1002399125':   '002399725',
        '10023991252':  '002399725',
        '00239935':     '002399351',
        '00239958':     '002399581',
        '00239964':     '002399641',
        '00239965':     '002399651',
        }


def process(img_file):
    #file_name = os.path.basename(img_file)
    stem = Path(img_file).stem
    file_name = lookup.get(stem, stem)
    img = cv2.imread(img_file)
    string, conf = analyze(img)
    if file_name == string:
        print('MATCH',string, conf)
        return False
    else:
        print('MISS', stem, file_name, string, conf)
        return True

if __name__ == '__main__':
    filename_list = glob(os.path.join("./data", "*.jpg"))
    multiprocessing.set_start_method('spawn')
    #with multiprocessing.Pool(processes=6) as p:
    #    p.map(process, filename_list)
    x = [process(f) for f in sorted(filename_list)]
    print('misses', sum(x))
