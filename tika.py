import cv2
import numpy as np
from scipy import ndimage
import cv2
import numpy as np
from scipy import ndimage

class Bbox():
    def __innit__(self,tag,x_coord,y_coord,w_obj,h_obj,cx,loc):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.w_obj = w_obj
        self.h_obj = h_obj
        self.tag = tag
        self.cx = cx
        self.loc = loc
        # noo stands for number of objects

    def getX(self):
        return self.x_coord
    def getY(self):
        return self.y_coord
    def getW(self):
        return self.w_obj
    def getH(self):
        return self.h_obj
    def getTag(self):
        return self.tag
    def getLoc(self):
        return self.loc
    def getCX(self):
        return self.cx

    def setX(self,x):
        self.x_coord = x
    def setY(self,y):
        self.y_coord = y
    def setW(self,w):
        self.w_obj = w
    def setH(self,h):
        self.h_obj = h
    def setTag(self,tag):
        self.tag = tag
    
    
    def setLoc(self,frame_w,tresh):
        """
        bounding_box fonksiyonundan alınan parametrelerden yola çıkarak
        cismin konumunu ekrana göre nerde olduğunu verir bunu belirli bir
        treshhold değerine göre yapar

        cismin merkezinin vulunduğu pikselin x eksenindeki yerini verir

        görüntünün genişliği de parametre olarak verilmeli

        printlerin bir manası yok ros için farklı outpular ayarlanabilir
        """
        
        if self.x_coord != None:
            self.cx = self.x_coord + int(frame_w/2)
            
            if self.cx<int(frame_w/2-tresh):
                print("on the left")
                self.loc = 0
            
            elif self.cx>int(frame_w/2+tresh):
                print("on the middle")
                self.loc = 1
            
            else:
                print("on the rigth")
                self.loc = 2
        else:
            print("no object sent to the function")
            self.cx = None
            self.loc = None
    
    



class Mask:

    def __init__(self, name, image, lower_hsv, upper_hsv):
        print("***test***")
        self.name = name
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        self.image = image
        self.width = image.shape[1]
        self.heigth = image.shape[0]

    def getWidth(self):
        return self.width

    def getImage(self):
        return self.image

    def getLowerHsv(self):
        return self.lower_hsv
    
    def getUpperHsv(self):
        return self.upper_hsv

    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def setWidth(self,width):
        self.width = width

    def setHeigth(self,heigth):
        self.width = heigth

    def setImage(self,image0):
        self.image = image0
        Mask.setWidth(image0.shape[1])
        Mask.setHeigth(image0.shape[0])

    def setLowerHsv(self,lowerhsv):
        self.lower_hsv = lowerhsv

    def setUpperHsv(self, upperhsv):
        self.upper_hsv = upperhsv

    def masking(self,horizon=4, opening=2,medianFltr=2):
        """
        sınır hsv değerleri ile maske çıkarıp 
        bu maskey opening ve median filter ile sadeleştirme fonskiyonu
        input olarak -> görüntü , alt sınır , üst sınır

        *kernel değişkeni ve median filterdaki size değişkeni
        duruma göre değiştirilebilir boyut ne kadar artarsa o kadar yoğun 
        bir filtreleme yapılır
        """

        # creating mask
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lowerHsv, self.upperhsv)
        
        #kameranın konumuna göre yukarı atılcak maskenin boyutunu değiştirbilirsin 
        cv2.rectangle(mask, (0,0), (self.width,int(self.height/horizon)), (0, 0, 0), -1)

        bitw = cv2.bitwise_and(mask, mask, mask=mask)

        # applying opening operation
        kernel = np.ones((opening, 2), np.uint8)
        opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

        # removing parasites
        mask_f = ndimage.median_filter(opening, size=medianFltr)

        return mask_f

    



class Tika(Mask,Bbox):
    print("*****test******")

    def __innit__(self,name, image, lower_hsv, upper_hsv,tag,x_coord,y_coord,w_obj,h_obj,cx,loc):
        super().__innit__(image, lower_hsv, upper_hsv)
        super().__innit__(tag,x_coord,y_coord,w_obj,h_obj,cx,loc)
        


    def setBbox(self,mask,min_area,noo,tag,tresh=30):
        """
        input olarak maskeyi alır ve maskedeki alanların en büyük 4 ünden 
        alanı tresholdun üstünde olanların sol üst köşesinin koordinatları ve 
        bounding box ın uzunluk ve genişliğini verir aksi halde None verir
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        objects = []
        if len(contours) > 0:
            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

            for c in sorted_contours[:noo]:
                obj_area = cv2.contourArea(c)
                
                if obj_area > min_area:
                    x, y, w, h = cv2.boundingRect(c)    
                    object = Bbox(tag,x,y,w,h,-1,-1)
                    object.setLoc(Mask.width,tresh)
                    objects.append(object)

                else:
                    print("no object found bigger than treshold")
        else:
            print("no contour found")

        return objects

    def closest(objects):
        """
        kameraya en yakın bounding boxı verir
        boduning_box fonksiyonun çıktısını ver
        """
        cache = 0
        ind = None
        for index,object in enumerate(objects):
            if cache < object.getY():
                cache = object.getY()
                ind = index
            else:
                continue
        if ind != None:
            return objects[ind]
        else:
            return None

