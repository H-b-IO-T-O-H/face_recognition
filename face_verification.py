import dlib
import cv2
from skimage import io
import pickle
import os
from scipy.spatial import distance
import time


def take_pic_from_video():
	video_capture = cv2.VideoCapture("/dev/video0")
	while True:
		ret, frame = video_capture.read()
		img = frame[:, :, ::-1]
		win1 = dlib.image_window()
		win1.clear_overlay()
		win1.set_image(img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			exit()
		dets = detector(img, 1)
		if dets:
			time.sleep(1)
			return img, dets, win1


def face_recognition_from_video(img, dets, win1):
	for k, d in enumerate(dets):
		print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
			k, d.left(), d.top(), d.right(), d.bottom()))
		shape = sp(img, d)
		win1.clear_overlay()
		win1.add_overlay(d)
		win1.add_overlay(shape)
	time.sleep(2)
	return facerec.compute_face_descriptor(img, shape)


def import_deep_models():
	sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
	facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
	detector = dlib.get_frontal_face_detector()
	return sp, facerec, detector


def import_pictures_from_base():
	img = io.imread('../images_base/test.jpg')
	win2 = dlib.image_window()
	win2.clear_overlay()
	win2.set_image(img)
	dets_webcam = detector(img, 1)
	for k, d in enumerate(dets_webcam):
		print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
			k, d.left(), d.top(), d.right(), d.bottom()))
		shape = sp(img, d)
		win2.clear_overlay()
		win2.add_overlay(d)
		win2.add_overlay(shape)
	time.sleep(2)
	return facerec.compute_face_descriptor(img, shape)


def getsubs(dir, face_descriptor1):
	flag = 0
	face_descriptor_new = None
	for dirname, dirnames, files in os.walk(dir):
		if flag:
			s = dirname + '/distance_base.txt'
			print(s)
			with open(s, 'rb') as f:
				face_descriptor_new = pickle.load(f)
			a = distance.euclidean(face_descriptor1, face_descriptor_new)
			if a < 0.55:
				return 1
		else:
			flag = 1
	return 0


def write_distance_to_base():
	print("ADD USER NAME:")
	s1 = input()
	s2 = os.getcwd() + "/images_base/" + s1
	print(s2)
	os.mkdir(s2)
	img, dets, win2 = take_pic_from_video()
	cv2.imwrite(s2 + '/face.jpeg', img)
	face_descriptor2 = face_recognition_from_video(img, dets, win2)
	with open(s2 + '/distance_base.txt', 'wb') as f:
		pickle.dump(face_descriptor2, f)


def take_distance_from_base():
	f = open('../distance_base.txt', 'a')

	print(f)

s_passwd = '12345'
s_login = 'admin'
sp, facerec, detector = import_deep_models()
print("Shall i add some new users?")
if input() == 'yes':
	print("Enter login:")
	s1 = input()
	print("Enter password:")
	s2 = input()
	if s1 == s_login and s2 == s_passwd:
			write_distance_to_base()
	else:
		print("\033[01m\033[031minvalid login or password!")
print("Start recognition ?")
if input() == 'yes':
	while True:
		img, dets, win1 = take_pic_from_video()
		print("\033[037m")
		time.sleep(1)
		face_descriptor1 = face_recognition_from_video(img, dets, win1)
		if getsubs(os.getcwd() + "/images_base/", face_descriptor1):
			print("\033[01m\033[032mAccess is allowed")
		else:
			print("\033[01m\033[031mUser not found")

# face_descriptor2 = import_pictures_from_base()
# поправка: a необходимо сравнивать с 0.5
# write_distance_to_base()
# take_distance_from_base()
# print(a)
