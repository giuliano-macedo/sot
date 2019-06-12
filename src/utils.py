def nist_str_to_bytes(s):
	kmg={
		"k":1024**1,
		"m":1024**2,
		"g":1024**3,
		"t":1024**4,
		"p":1024**5
	}
	s=s.lower()
	if s[-1]=="b":
		s=s[:-1]
	state=0
	n=""
	for l in s:
		if l==" ":
			continue
		if state==0:
			if (not l.isdecimal()) and (not l=="."):
				n=float(n)
				state+=1
			else:
				n+=l
		if state==1:
			m=kmg.get(l,None)
			if m==None:
				raise TypeError()
			state+=1
			n*=m
		elif state==2:
			raise TypeError()
	return int(n)