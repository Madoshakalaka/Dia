import cv2
import unittest
import graphviz
import numpy as np


class MyTestCase(unittest.TestCase):
	def test_something(self):
		a = graphviz.Graph(format='png')
		a.node("test")
		x = a.pipe(format='png')
		# print(type(x))


		arr = np.frombuffer(x, np.uint8)
		frame = cv2.imdecode(arr, 0)

		cv2.imshow("lul", frame)

		cv2.waitKey()
		cv2.destroyAllWindows()

if __name__ == '__main__':
	unittest.main()
