import os,cv2
img_format = {'png' ,'jpg','bmp'}

def image_check(root_dir):
    qty = 0
    error_count = 0
    if not os.path.exists(root_dir):
        print("Error:root dir doesn't exist:",root_dir)
    else:
        for dir_path,sub_dir,filename_list in os.walk(root_dir):
            if len(filename_list) > 0:
                for filename in filename_list:
                    if qty > 0 and qty % 5000 == 0:
                        print("have processed {} images".format(qty))

                    if filename.split(".")[-1] in img_format:
                        img_path = os.path.join(dir_path,filename)
                        # print("img_path:",img_path)

                        img = cv2.imread(img_path)
                        qty += 1
                        if img is None:
                            print("Read failed:",img_path)
                            error_count += 1

        #----
        print("image quantity: {}, error count: {}".format(qty,error_count))



if __name__ == "__main__":
    root_dir = r"F:\dataset\FLW_detect_aligned"
    image_check(root_dir)#this function is used to exam if each image can be readable.




