#! /usr/bin/python

import string

precedence = {'~':7, '^':6, '|':5, '@':4, '#':3, '(':2, ')':1}

def parsing(infix):
	x = infix.replace('<->','#');
	x = x.replace('->','@');
	x = x.replace('=>','$');
	return x
		
def in2post(infix):
	var_list = []
	sym_list = []
	s = ''
	for i in infix:
		if i in ['~','^','|','@','#']:
			while len(sym_list) and precedence[i] <= precedence[sym_list[-1]]:
				var_list.append(sym_list.pop())
			sym_list.append(i)
    		elif i.isalpha():
			var_list.append(i)
		elif i == '(':
			sym_list.append(i)
		elif i == ')':
			while sym_list[-1] != '(':
				var_list.append(sym_list.pop())
			sym_list.pop()
	while len(sym_list):
			var_list.append(sym_list.pop())
	for i in var_list:
		s = s+i
	s = s.replace('~~','')

	return list(s)

def makeTree(x):
	stack = []
	for i in x:
		if i.isalpha():
			stack.append(i)
		else:
			if i == '~':
				tup = ('~',stack.pop())
				stack.append(tup)
			else:
				right = stack.pop()
				left = stack.pop()
				l = [left,i,right]
				stack.append(l)
	return stack[0]

def removeBiDirectional(tree):
	if isinstance(tree, (list)):
		left = removeBiDirectional(tree[0])
		right = removeBiDirectional(tree[2])
	 	
		if tree[1] == '#':
	 		return [[left,'@',right],'^',[right,'@',left]]
	 	return [left,tree[1],right]
	elif isinstance(tree, (tuple)) and isinstance(tree[1], (list)):
		left = removeBiDirectional(tree[1][0])
		right = removeBiDirectional(tree[1][2])
		
		if tree[1][1] == '#':
			return ('~',[[left,'@',right],'^',[right,'@',left]])
		return ('~',[left,tree[1][1],right])
	else:
		return tree
		
def removeConditional(tree):
	if isinstance(tree, (list)):
		left = removeConditional(tree[0])
		right = removeConditional(tree[2])
	 	
		if tree[1] == '@':
			if isinstance(left, (tuple)):
				return [left[1],'|',right]
			else:
				return [('~',left),'|',right]					
	 	return [left,tree[1],right]
	elif isinstance(tree, (tuple)) and isinstance(tree[1], (list)):
		left = removeConditional(tree[1][0])
		right = removeConditional(tree[1][2])
		
		if tree[1][1] == '@':
			if isinstance(right ,(tuple)):
				return [left,'^',right[1]]
			else:
				return [left,'^',('~',right)]
		return ('~',[left,tree[1][1],right])
	else:
		return tree
def changeOp(x):
	if x == '^':
		return '|'
	elif x == '|':
		return '^'

def deMorgan(tree):
	if isinstance(tree, (tuple)):
		if isinstance(tree[1] ,(list)):
			tree[1][1] = changeOp(tree[1][1])
			left = tree[1][0]
			right = tree[1][2]
			
			if isinstance(tree[1][0], (tuple)):
				left = deMorgan(tree[1][0][1])
			else:
				left = deMorgan(('~',tree[1][0]))
	
			if isinstance(tree[1][2], (tuple)):
				right = deMorgan(tree[1][2][1])
			else:
				right = deMorgan(('~',tree[1][2]))
	
			return [left,tree[1][1],right]
		else:
			return tree
	elif isinstance(tree ,(list)):
		left = deMorgan(tree[0])
		right = deMorgan(tree[2])
		return [left,tree[1],right]
	else:
		return tree

def distributiveLaw(tree):
	if isinstance(tree, (list)):
		left = tree[0]
		right = tree[2]
		if isinstance(tree[0], (list)):
			tree[0] = distributiveLaw(tree[0])
		if isinstance(tree[2], (list)):
			tree[2] = distributiveLaw(tree[2])
		if tree[1] == '|':
			tree = changeNode(tree)
		return tree
	return tree
	
def changeNode(tree):
	if isinstance(tree[0], (list)) and tree[0][1] is '^':
		tree = [[tree[0][0],'|',tree[2]],'^',[tree[0][2],'|',tree[2]]]
		tree = distributiveLaw(tree)
	elif isinstance(tree[2], (list)) and tree[2][1] is '^':
		tree = [[tree[0],'|',tree[2][0]],'^',[tree[0],'|',tree[2][2]]]
		tree = distributiveLaw(tree)
	return tree

def inorderTraversal(tree):
	global eachClause
	global listClause
	if not isinstance(tree, (list)):
		eachClause.append(tree)
		return
	if isinstance(tree, (list)):
		inorderTraversal(tree[0])
	if tree[1] == '^':
		if eachClause not in listClause:
			listClause.append(eachClause)
		eachClause = []
	if isinstance(tree, (list)):
		inorderTraversal(tree[2])

def getRidTauto(x):
	removed = []
	ret = []
	for i in x:
		for j in i:
			for k in i:
				if isinstance(k, (tuple)) and not isinstance(j, (tuple)) and j == k[1]:
					removed.append(i)
	for i in x:
		if i not in removed:
			ret.append(i)
	return ret

def resolution():
	global listClause
	while True:
		ret = findnewclause()
		if ret == 'emptyclause':
			return True
		if ret == 'nonew':
			return False

def findnewclause():
	global listClause
	for clause1 in listClause:
		for clause2 in listClause:
			if clause1 != clause2:
				for literal1 in clause1:
					for literal2 in clause2:
						if isinstance(literal1, (tuple)) and not isinstance(literal2, (tuple)) and literal1[1] == literal2:
							l = []
							for i in clause1:
								if i != literal1:
									l.append(i)
							for i in clause2:
								if i != literal2:
									l.append(i)
							if len(l):
								if l not in listClause and getRidTauto([l]):
									listClause.append(l)
									return 'gotnew'
							else:
							 	return 'emptyclause'
	return 'nonew'

def main():
	global eachClause
	global listClause
        print 'Enter the number of cases'
	cases = int(raw_input())
	while cases:
		cases = cases -1
		listClause = []
                print 'Enter the theorem'
		inp = raw_input()
		inp = parsing(inp)
		inp = inp.split('$')
		if len(inp) == 1:
			print 'conclusion missing'
			continue
		elif len(inp[0]) == 0:
			print '1'
			continue
		elif len(inp[1]) == 0:
			print 'conclusion missing'
			continue
		inp[0] = inp[0].split(',')
		inp[1] = '~('+inp[1]+')'
		inp[0].append(inp[1])
		for premise in inp[0]:
			eachClause = []
			tree = makeTree(in2post(premise))
			tree = removeBiDirectional(tree)
			tree = removeConditional(tree)
			tree = deMorgan(tree)
			tree = distributiveLaw(tree)
			inorderTraversal(tree)
			if len(eachClause):
				listClause.append(eachClause)
		listClause = getRidTauto(listClause)
		ret = resolution()
		if ret:
			print '1'
		else:
			print '0'

if __name__ == '__main__':
	main()
