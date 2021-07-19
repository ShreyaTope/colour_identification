import cv2
import pandas as pd


# reading csv file
guide= ['color', 'color_name', 'hex', 'R', 'G', 'B']
colour_files = pd.read_csv("colors.csv", names=guide, header=None)


# reading image
img = cv2.imread("clouds.jpg")
img = cv2.resize(img, (800,600))

#declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

#function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R,G,B):
	minval = 1000
	for i in range(len(colour_files)):
		variance = abs(R - int(colour_files.loc[i,'R'])) + abs(G - int(colour_files.loc[i,'G'])) + abs(B - int(colour_files.loc[i,'B']))
		if variance <= minval:
			minval = variance
			colorname = colour_files.loc[i, 'color_name']

	return colorname

#function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b = int(b)
		g = int(g)
		r = int(r)


# creating window to show image
cv2.namedWindow('ImageWindow')
cv2.setMouseCallback('ImageWindow', draw_function)

while True:
	cv2.imshow('ImageWindow', img)
	if clicked:
		#creating a rectangle at top to show color name as text
		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)

		#Creating text string to display( Color name and RGB values )
		text = get_color_name(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

		#displaying the text string
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

		#For very light colours we will display text in black colour
		if r+g+b >= 600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

	#considering esc key as exit condition
	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows() 