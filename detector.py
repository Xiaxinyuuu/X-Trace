from deepsort import DeepSort
from model.embedding import Embedding
from sqlite import *
import numpy as np
import cv2, time

global pts, ROIs


class Detector(object):
    def __init__(self,video_path = None,img_arr = None,track = None, ROI=None):
        global pts, ROIs

        self.deepsort = DeepSort('../model/detection', '../model/embedding', True)
        self.video_path = video_path
        self.img_arr = img_arr
        self.track = track
        self.object_dic = {}
        self.frame_num = 0
        self.capture = cv2.VideoCapture(video_path)
        self.emb = Embedding('../model/embedding', use_gpu=True)
        self.cap = cv2.VideoCapture(video_path)
        ROIs = ROI
        pts = []
       

    def get_img(self,videos):
        imgs = []

        for video in videos:
            cap = cv2.VideoCapture(video)
            _, img = cap.read()
            imgs.append(img)

        return imgs


    def img_detect(self,threshold):
        results = []
        imgs = np.array([]).astype(np.float)
        for i, img in enumerate(self.img_arr):
            confid = 0
            temp_dic = {}
            bboxes = []
            img = cv2.imread(img)
            result = self.deepsort.detector.predict(img)
            for j in range(len(result)):
                if result[j]['score'] < threshold:
                    continue
                bboxes.append(result[j]['bbox'])
                confid += result[j]['score']
            temp_dic['person_num'] = len(bboxes)
            if len(bboxes) == 0:
                temp_dic['confid'] = 0
            else:
                temp_dic['confid'] = confid * 1.0 / len(bboxes)
            results.append(temp_dic)
            for k, bbox in enumerate(bboxes):
                cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                              (0, 69, 255), 2)
                cv2.putText(img, 'id' + "-" + str(k + 1), (int(bbox[0]), int(bbox[1] - 10)), 0, 0.75, (0, 69, 255), 2)
            imgs = np.append(imgs, img)
            cv2.imwrite('./temp_imgs/' + f'{i + 1}.jpg', img)
        return results


    def video_detect(self, threshold, ID=None, video_cnt=None):
        global pts

        current_time = time.strftime('%Y-%m-%d %H.%M.%S', time.localtime(time.time()))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter("./temp_vdo/" + current_time + ".mp4", fourcc, 30, (768, 576), True)
        if ROIs and video_cnt == 1:
            _, temp = self.capture.read()

            def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    xy = "%d,%d" % (x, y)
                    cv2.circle(temp, (x, y), 1, (0, 0, 255), thickness=-1)
                    cv2.putText(temp, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                                1.0, (0, 0, 0), thickness=1)
                    cv2.imshow("image", temp)
                    pts.append([x, y])
                    # if len(pts1) == 4:
                    # print(pts1)

            cv2.namedWindow("image")
            cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
            while (1):
                cv2.imshow('image', temp)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('q'):
                    break
            cv2.destroyAllWindows()

        while True:
            success, frame = self.capture.read()
            self.frame_num += 1
            # if not select and frame_cnt < frame_id:
            #     continue
            if not success:
                break
            outputs, confid = self.deepsort.update(frame, threshold)

            target = []
            person = 0
            id_bbox = {}
            for output in outputs:

                # if not "%d" % output[-1] in self.object_dic:
                #     # 创建当前id的字典：key(ID):val{轨迹，丢帧计数器}   当丢帧数超过10帧就删除该对象
                #     self.object_dic["%d" % output[-1]] = {"trace": [], 'traced_frames': 10}
                #     self.object_dic["%d" % output[-1]]["trace"].append(center)
                #     self.object_dic["%d" % output[-1]]["traced_frames"] += 1

                    # 如果有，直接写入
                # else:
                #     self.object_dic["%d" % output[-1]]["trace"].append(center)
                #     self.object_dic["%d" % output[-1]]["traced_frames"] += 1

                if ID == None:
                    person = person + 1
                    cv2.rectangle(frame, (int(output[0]), int(output[1])), (int(output[2]), int(output[3])), (0, 69, 255),
                                  2)
    
                    cv2.putText(frame, 'id' + "-" + str(int(output[-1])), (int(output[0]), int(output[1] - 10)), 0, 0.75,
                                (0, 69, 255), 2)


                if ID == output[-1]:
                    person = person + 1
                    cv2.rectangle(frame, (int(output[0]), int(output[1])), (int(output[2]), int(output[3])),
                                  (0, 69, 255),
                                  2)

                    cv2.putText(frame, 'id' + "-" + str(int(output[-1])), (int(output[0]), int(output[1] - 10)), 0,
                                0.75,
                                (0, 69, 255), 2)

                center = [int((output[0] + output[2]) / 2), int((output[1] + output[3]) / 2),
                          int(output[2] - output[0]),
                          int(output[3] - output[1])]

                id_bbox[str(int(output[4]))] = [output[0], output[1], output[2], output[3]]

                if not "%d" % output[-1] in self.object_dic:
                    # 创建当前id的字典：key(ID):val{轨迹，丢帧计数器}   当丢帧数超过30帧就删除该对象
                    self.object_dic["%d" % output[-1]] = {"trace": [], 'traced_frames': 30}
                    self.object_dic["%d" % output[-1]]["trace"].append(center)
                    self.object_dic["%d" % output[-1]]["traced_frames"] += 1

                    # 如果有，直接写入
                else:
                    self.object_dic["%d" % output[-1]]["trace"].append(center)
                    self.object_dic["%d" % output[-1]]["traced_frames"] += 1

                if ROIs:

                    pts1 = np.array(pts, np.int32).reshape((-1, 1, 2))

                    cv2.polylines(frame, [pts1], True, (0, 255, 0), thickness=2)
                    # 判断目标是否在roi区域内
                    # 这部分使用了PNPloy算
                    testp = [int(output[2]), int(output[3])]

                    n = len(pts)
                    j = n - 1
                    res = False
                    for i in range(n):
                        if (pts[i][1] > testp[1]) != (pts[j][1] > testp[1]) and \
                                testp[0] < (pts[j][0] - pts[i][0]) * (testp[1] - pts[i][1]) / (
                                pts[j][1] - pts[i][1]) + pts[i][0]:
                            res = not res
                        j = i

                    if res == True:
                        target.append(testp)
                        cv2.putText(frame, str('enter'), (int(output[2] - 65), int(output[3] - 5)),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (60, 20, 220), 2)
                

            # 绘制轨迹
            if self.track:
                track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                                (0, 255, 255), (255, 0, 255), (255, 127, 255),
                                (127, 0, 255), (127, 0, 127), (193, 182, 255), (139, 0, 139)]
                for s in self.object_dic:
                    i = int(s)
                    # 限制轨迹最大长度
                    if len(self.object_dic["%d" % i]["trace"]) > 10:
                        for k in range(len(self.object_dic["%d" % i]["trace"]) - 10):
                            del self.object_dic["%d" % i]["trace"][k]
                    # # # 绘制轨迹
                    if len(self.object_dic["%d" % i]["trace"]) > 2:
                        for j in range(1, len(self.object_dic["%d" % i]["trace"]) - 1):
                            pot1_x = self.object_dic["%d" % i]["trace"][j][0]
                            pot1_y = self.object_dic["%d" % i]["trace"][j][1]
                            pot2_x = self.object_dic["%d" % i]["trace"][j + 1][0]
                            pot2_y = self.object_dic["%d" % i]["trace"][j + 1][1]
                            # if pot2_x == pot1_x and pot1_y == pot2_y:
                            #     del self.object_dic["%d" % i]

                            clr = i % 10  # 轨迹颜色随机
                            cv2.line(frame, (pot1_x, pot1_y), (pot2_x, pot2_y), track_colors[clr], 5)

                # 对已经消失的目标予以排除
                for s in self.object_dic:
                    if self.object_dic["%d" % int(s)]["traced_frames"] > 0:
                        self.object_dic["%d" % int(s)]["traced_frames"] -= 1
                for n in list(self.object_dic):
                    if self.object_dic["%d" % int(n)]["traced_frames"] == 0:
                        del self.object_dic["%d" % int(n)]



            id_bbox["所有行人"] = [0, 0, 0, 0]

            # get方法参数按顺序对应下表（从0开始编号，比如这里为了获取视频的总帧数，在下表是排第八个的 CV_CAP_PROP_FRAME_COUNT
            minutes = int(self.frame_num / self.cap.get(5)) // 60
            seconds = int((self.frame_num / self.cap.get(5))) % 60
            video_lenth = str(minutes) + 'min ' + str(seconds) + 's'

            frame = cv2.resize(frame, (768, 576))
            video.write(frame)
            if ROIs:
                yield frame, person, len(target), confid, id_bbox, self.frame_num
            else:
                yield frame, person, confid, id_bbox, self.frame_num
        self.data_base = Database("../videos.db")
        self.data_base.insert_data("temp_vdo/" + current_time + ".mp4", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), video_lenth, threshold)
        self.data_base.close_db()

    def rlt_detect(self, threshold):
        capture = cv2.VideoCapture(0)
        retval = cv2.VideoCapture.isOpened(capture)
        self.object_dic = {}
        if retval:
            while True:
                success, frame = capture.read()
                if not success:
                    break
                outputs, confid = self.deepsort.update(frame, threshold)
                person = 0
                id_bbox = {}
                for output in outputs:
                    person = person + 1
                    cv2.rectangle(frame, (int(output[0]), int(output[1])), (int(output[2]), int(output[3])),
                                  (0, 69, 255),
                                  2)

                    cv2.putText(frame, 'id' + "-" + str(int(output[-1])), (int(output[0]), int(output[1] - 10)), 0,
                                0.75,
                                (0, 69, 255), 2)
                    center = [int((output[0] + output[2]) / 2), int((output[1] + output[3]) / 2),
                              int(output[2] - output[0]),
                              int(output[3] - output[1])]

                    id_bbox[str(int(output[4]))] = [output[0], output[1], output[2], output[3]]

                    if not "%d" % output[-1] in self.object_dic:
                        # 创建当前id的字典：key(ID):val{轨迹，丢帧计数器}   当丢帧数超过10帧就删除该对象
                        self.object_dic["%d" % output[-1]] = {"trace": [], 'traced_frames': 10}
                        self.object_dic["%d" % output[-1]]["trace"].append(center)
                        self.object_dic["%d" % output[-1]]["traced_frames"] += 1

                        # 如果有，直接写入
                    else:
                        self.object_dic["%d" % output[-1]]["trace"].append(center)
                        self.object_dic["%d" % output[-1]]["traced_frames"] += 1
                if self.track:
                    track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                                    (127, 0, 255), (127, 0, 127), (193, 182, 255), (139, 0, 139)]
                    for s in self.object_dic:
                        i = int(s)
                        # 限制轨迹最大长度
                        if len(self.object_dic["%d" % i]["trace"]) > 10:
                            for k in range(len(self.object_dic["%d" % i]["trace"]) - 10):
                                del self.object_dic["%d" % i]["trace"][k]
                        # # # 绘制轨迹
                        if len(self.object_dic["%d" % i]["trace"]) > 2:
                            for j in range(1, len(self.object_dic["%d" % i]["trace"]) - 1):
                                pot1_x = self.object_dic["%d" % i]["trace"][j][0]
                                pot1_y = self.object_dic["%d" % i]["trace"][j][1]
                                pot2_x = self.object_dic["%d" % i]["trace"][j + 1][0]
                                pot2_y = self.object_dic["%d" % i]["trace"][j + 1][1]
                                # if pot2_x == pot1_x and pot1_y == pot2_y:
                                #     del self.object_dic["%d" % i]

                                clr = i % 10  # 轨迹颜色随机
                                cv2.line(frame, (pot1_x, pot1_y), (pot2_x, pot2_y), track_colors[clr], 5)

                    # 对已经消失的目标予以排除
                    for s in self.object_dic:
                        if self.object_dic["%d" % int(s)]["traced_frames"] > 0:
                            self.object_dic["%d" % int(s)]["traced_frames"] -= 1
                    for n in list(self.object_dic):
                        if self.object_dic["%d" % int(n)]["traced_frames"] == 0:
                            del self.object_dic["%d" % int(n)]

                res_img = cv2.resize(frame, (1035, 679))
                yield frame, person, confid

    def ReID(self, videos=None, img=None, hit_num=None):
        imgs_gallery = []
        index_score = {}
        messages = []
        scores = []
        ID = 0

        for k,video in enumerate(videos):
            capture = cv2.VideoCapture(video)
            frame_num = 0
            frame_rate = capture.get(5)
            while True:
                success, frame = capture.read()
                frame_num += 1
                persons = []
                if not success:
                    break
                result = self.deepsort.detector.predict(frame)
                for j in range(len(result)):
                    if result[j]['score'] < 0.8:
                        continue
                    persons.append(result[j]['bbox'])

                for _ in persons:
                    crop = frame[int(_[1]):int(_[1] + _[3]), int(_[0]):int(_[0] + _[2])]
                    # cv2.imwrite('./output/'+'ID'+'.jpg', crop)

                    result1 = self.emb.predict([crop])[0]
                    result2 = self.emb.predict([cv2.imread(img)])[0]
                    score = np.sum((np.array(result1) - np.array(result2)) * (np.array(result1) - np.array(result2)))
                    imgs_gallery.append(crop)
                    index_score[score] = ID
                    scores.append(score)
                    s = frame_num / frame_rate
                    messages.append([k,s])
                    ID += 1
                    yield 0, 0, ID

        scores = sorted(scores)
        # print(index_score)
        results = []
        for i,score in enumerate(scores):
            # cv2.imwrite('./output/'+str(i)+'.jpg',imgs_gallery[index_score[score]])
            results.append(imgs_gallery[index_score[score]])
            if i == hit_num:
                break

        # return messages,scores
        sort_mes = []
        for i, score in enumerate(scores):
            sort_mes.append(messages[index_score[score]])
            if i == hit_num:
                break
        yield results, sort_mes, ID