import cv2
import mediapipe as mp
import time




class FaceMesh():

    def __init__(self, static = False, maxFaces = 2, refmarks = True, Detcon = 0.5):
    
        self.static = static
        self.maxFaces = maxFaces
        self.refmarks = refmarks
        self.Detcon = Detcon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.static, self.maxFaces, self.refmarks, self.Detcon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)


    def find_mesh(self, img, draw=True):
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        if self.results.multi_face_landmarks:
            if draw:
                for faceLms in self.results.multi_face_landmarks:
                    self.mpDraw.draw_landmarks(img, faceLms,self.mpFaceMesh.FACEMESH_TESSELATION,
                                          self.drawSpec, self.drawSpec)
        return img

    def get_pos(self, img):

        lmList = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                for id, lm in enumerate(faceLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
        return lmList
        



if __name__ == "__main__":
    
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceMesh()
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        img = detector.find_mesh(img)

        lis = detector.get_pos(img)

        #cv2.circle(img, (lis[10][1], lis[10][2]), 5, (255, 255, 255), cv2.FILLED)
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, 'FPS: ' + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)
