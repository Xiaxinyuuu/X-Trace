from detector import Detector
import argparse
import os


def main(args):
    Det = Detector()

    # 1.检测图片
    if args.img_path:
        Det.img_detect(
            [args.img_path],
            threshold=args.threshold)  # 输入图片路径,方法返回一张图片
    # 2.检测视频
    if args.video_path:
        Det.video_detect(args.img_path,
                         threshold=args.threshold)  # 第一个参数：视频路径，默认保存为./result.avi即当前路径下result.avi文件
    # 3.打开摄像头实时检测
    if args.camera:
        Det.rlt_detect(threshold=args.threshold)  # 没有参数


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='''you can set the video_path or camera_id to start the program, 
        and also can set the display or save_dir to display the results or save the output video.''',
        description="this is the help of this script."
    )

    parser.add_argument("--det_model_dir", type=str, default='model/detection', help="the detection model dir.")
    parser.add_argument("--emb_model_dir", type=str, default='model/embedding', help="the embedding model dir.")
    parser.add_argument("--use_gpu", action="store_true", help="do you want to use gpu.")
    parser.add_argument("--threshold", type=float, default=0.5, help="the threshold of detection model.")
    parser.add_argument("--img_path", type=str, default=None, help="the input img path.")
    parser.add_argument("--video_path", type=str, default=None, help="the input video path or the camera id.")
    parser.add_argument("--camera", type=int, default=0, help="do you want to use the camera.")
    args = parser.parse_args()
    main(args)
