# 该脚本文件需要修改第10行（classes）即可
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
from os import getcwd

sets = ["train", 'test', 'val']
# 这里改成自己的类别
classes = ['fall']

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x = round(x, 6)
    w = round(w, 6)
    y = round(y, 6)
    h = round(h, 6)
    return x, y, w, h

# 后面只需要修改各个文件夹的位置
def convert_annotation(image_id):
    try:
        in_file = open(r"C:\Users\22950\Desktop\fall\Annotations\{0}.xml".format(image_id), encoding="utf-8")
        out_file = open(r"C:\Users\22950\Desktop\fall\labels\{0}.txt".format(image_id), 'w', encoding="utf-8")
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            b1, b2, b3, b4 = b
            # 标签越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + ' ' + " ".join([str(a) for a in bb]) + '\n')
    except Exception as e:
        print(e, image_id)


# 这一步生成的txt文件写在data.yaml文件里
wd = getcwd()
for image_set in sets:
    if not os.path.exists(r"C:\Users\22950\Desktop\fall\labels"):
        os.makedirs(r"C:\Users\22950\Desktop\fall\labels")
    image_ids = open(r"C:\Users\22950\Desktop\fall\ImageSets\{0}.txt".format(image_set)).read().strip().split()
    list_file = open(r"C:\Users\22950\Desktop\fall\fall_{0}.txt".format(image_set), "w")
    for image_id in tqdm(image_ids):
        list_file.write(r"C:\Users\22950\Desktop\fall\images\{0}.jpg".format(image_id) + '\n')
        convert_annotation(image_id)
    list_file.close()
