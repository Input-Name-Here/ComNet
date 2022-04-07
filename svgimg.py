import xml.etree.ElementTree as ET
import webcolors

# This class uses code from another project (VEC2EGP)

class image():

	def __init__(self):
		self.filename = "" # Location of svg file object represents
		self.rects = [] # Array of rectangles, each rect is an array of tuples [(x,y),(width,height),(r,g,b)]
		self.lines = [] # Array of lines, each line is an array [(x1,y1),(x2,y2),(r,g,b)]
		self.width=12
		self.height=12
		self.angle = 0 # Bearing
	
	def print(self):
		for r in self.rects:
			print("RECT:",r)
		for l in self.lines:
			print("LINE:",l)
	def construct(self,fn):
		self.filename = fn
		self.rects = []
		self.lines = []
		Code = ""
		EGP = "egp"
		index = 0
		tree = ET.parse(self.filename)
		root = tree.getroot()
		#for i in root.attrib:
			#print(i)
		for i in root:
			tag = i.tag.replace("{http://www.w3.org/2000/svg}","")
			#print("    +"+tag)
			if tag == "g":
				for element in i:
					tag = element.tag.replace("{http://www.w3.org/2000/svg}","")
					#print("        -"+tag)
					at = element.attrib
					atid = at["id"]
					#print("d")
					if "ignore" in at["id"]:
						print("            = Skipped!")
						continue
					#print("c")
					for attr in at:
						value = at[attr]
						#print("            ="+attr+" : "+value)
					if tag == "rect":
						x=at["x"]
						y=at["y"]
						w=float(at["width"])
						h=float(at["height"])
						x=float(float(x)+float(w)/2)
						y=float(float(y)+float(h)/2)
						pos = (x,y)
						size = (w,h)
						style = at["style"].split(';')
						colour = (255,255,255)
						for s in style:
							if "fill:#" in s:
								s=s.replace("fill:","").upper()
								colour = webcolors.hex_to_rgb(s)
								colour = (colour[0],colour[1],colour[2])
						rect = [pos,size,colour]
						self.rects.append(rect)
					if tag == "text":
						print("TextSkip")
						continue
						x=at["x"]
						y=at["y"]
						text = "test"
						style = at["style"].split(';')
						colour = "255,255,255"
						for s in style:
							if "fill:#" in s:
								s=s.replace("fill:","").upper()
								colour = webcolors.hex_to_rgb(s)
								colour = str(colour[0])+","+str(colour[1])+","+str(colour[2])
						Code+= f"{EGP}:egpColor({index}, vec({colour}))\n"
					index+=1
					if tag == "path":
						#print("Path")
						d=at["d"]
						if "h" in d:
							split1 = d.lower().replace(" ","").split("h")
							M = split1[0].replace("m","").split(",")
							H = float(split1[1])
							Mx = float(M[0])
							My = float(M[1])
							print(f"            @m {Mx},{My},h {H}")
							MxH = Mx+H
							pos1 = (Mx,My)
							pos2 = (MxH,My)
							colour = (255,255,255)
							line = [pos1,pos2,colour]
						elif "v" in d:
							split1 = d.lower().replace(" ","").split("v")
							M = split1[0].replace("m","").split(",")
							V = float(split1[1])
							Mx = float(M[0])
							My = float(M[1])
							print(f"            @m {Mx},{My},v {V}")
							MyV = My+V
							colour = (255,255,255)
							pos1 = (Mx,My)
							pos2 = (Mx,MyV)
							line = [pos1,pos2,colour]
						elif "H" in d:
							split1 = d.lower().replace(" ","").split("h")
							M = split1[0].replace("m","").split(",")
							H = float(split1[1])
							Mx = float(M[0])
							My = float(M[1])
							print(f"            @m {Mx},{My},h {H}")
							MxH = H
							colour = (255,255,255)
							pos1 = (Mx,My)
							pos2 = (MxH,My)
							line = [pos1,pos2,colour]
						elif "V" in d:
							split1 = d.lower().replace(" ","").split("v")
							M = split1[0].replace("m","").split(",")
							V = float(split1[1])
							Mx = float(M[0])
							My = float(M[1])
							print(f"            @m {Mx},{My},v {V}")
							MyV = V
							colour = (255,255,255)
							pos1 = (Mx,My)
							pos2 = (Mx,MyV)
							line = [pos1,pos2,colour]
						elif "M" in d:
							split1 = d.lower().replace("m ","").split(" ")
							M1 = split1[0].split(",")
							M2 = split1[1].split(",")
							M1x = float(M1[0])
							M1y = float(M1[1])
							M2x = float(M2[0])
							M2y = float(M2[1])
							print(f"            @m1 {M1x},{M1y} m2 {M2x},{M2y} ")
							colour = (255,255,255)
							pos1 = (M1x,M1y)
							pos2 = (M2x,M2y)
							line = [pos1,pos2,colour]
						elif "m" in d:
							split1 = d.lower().replace("m ","").split(" ")
							M1 = split1[0].split(",")
							M2 = split1[1].split(",")
							M1x = float( M1[0])
							M1y = float(M1[1])
							M2x = float(M2[0])+float(M1x)
							M2y = float(M2[1])+float(M1y)
							print(f"            @m1 {M1x},{M1y} m2 {M2x},{M2y} ")
							colour = (255,255,255)
							pos1 = (M1x,M1y)
							pos2 = (M2x,M2y)
							line = [pos1,pos2,colour]
						else:
							print("Error!")
							continue
						style = at["style"].split(';')
						colour = "255,255,255"
						width = 1
						for s in style:
							if "stroke-width:" in s:
								s=s.replace("stroke-width:","")
								width = float(s)
						for s in style:
							if "stroke:#" in s:
								s=s.replace("stroke:","").upper()
								colour = webcolors.hex_to_rgb(s)
								colour = str(colour[0])+","+str(colour[1])+","+str(colour[2])
						line[2] = colour
							
						self.lines.append(line)
						#print("            @"+d)
