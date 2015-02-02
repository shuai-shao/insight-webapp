def Modellt(fromUser = 'Default', Price = 0):
	print "The price is %i" % Price
	result = '$' + str(Price*1000)
	if fromUser != 'Default':
		return result
	else:
		return 'check your input'