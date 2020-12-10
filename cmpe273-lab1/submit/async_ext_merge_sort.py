#CMPE 273 lab 1
#Use any kind of External Sorting algorithm to
# sort all numbers from input/unsorted_*.txt files
# and save the sorted result into output/sorted.txt
# file amd async_sorted.txt file.
import sys
import asyncio

def read_file(filename):
	fp=open(filename,'r')
	contents=fp.readlines()
	fp.close()
	return contents

# organize data as elements in a list
def parse_data(data):
	dstore =[]
	for x in range(len(data)):
		if (data[x][-1] == '\n'):
			split = data[x][:-1]
		else:
			split = data[x]
		split = int(split)
		dstore.append(split)
	return dstore

def findMin(numArr, n):
    min = sys.maxsize
    pos = 0
    for x in range (0,n):
        if numArr[x]!= None:
            if numArr[x] < min:
                min = numArr[x]
                pos = x
    return pos

def lineToInt(line):
    if line[-1]== '\n':
        number = int(line[:-1])
    else:
        number = int(line)
    return number

def merge(arr,l, m , r):
    n1 = m - l + 1
    n2 = r - m
    # create temp arrays, initialized as 0
    L = [0]*n1
    R = [0]*n2
    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]
    for j in range(0, n2):
        R[j] = arr[m + 1 + j]
    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] =L[i]
            i += 1
        else:
            arr[k] = R[j]
            j+= 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
# l is for left index and r is right index of the
# sub-array of arr to be sorted
def mergeSort(arr, l, r):
    if l < r:
    # Same as (l+r)/2, but avoids overflow for
    # large l and h.
        m = (l + r-1) // 2
    # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
        merge(arr, l, m, r)


# list is use to put 10 element to compare
async def putNumber(myQueue):
    fileClosed = 0
    while True:
#        print ("putNumber is working!")
        index = findMin(numArray,10)
        await myQueue.put(numArray[index])
        await asyncio.sleep(0)
        numToFill = fps[index].readline()

        if numToFill == '':
            numArray[index] = None
            fps[index].close()
            fileClosed = fileClosed +1
        else:
            numArray[index] = lineToInt(numToFill)
        if fileClosed == 10:
            break

async def writeFile(myQueue):
    numWrote =0
    while True:
        await asyncio.sleep(0)
        item = await myQueue.get()
        outFilePointer.write(str(item) + '\n')
        numWrote= numWrote+1
        if (numWrote >= 1000):
            break
    outFilePointer.close()

# start the main program
# Specifiy the path of folder , files
folder ='/Users/yao/Documents/Study/SJSU_course/273_enterprise_tech_platform/cmpe273-spring20-labs-master/lab1/'
inPath= 'input/unsorted_'
prePath= 'output/presorted_'
outPath = 'output/async_sorted'
fileExt = '.txt'

# sort each individual file
for x in range(1, 11):
    inputFile = folder + inPath + str(x) + fileExt
    preFile = folder + prePath + str(x) + fileExt
    context = read_file(inputFile)
    numArray = parse_data(context)
    mergeSort(numArray, 0, 99)
    with open (preFile,'w+') as f:
        for line in numArray:
            f.write(str(line) + "\n")

### Big Sort
filenames = []
# read in presorted files
for x in range (0,10):
    filenames.append(folder + prePath + str(x+1) + fileExt)

fps = []
for filename in filenames:
    fps.append(open(filename, 'r'))

numArray = []
for fp in fps:
    line = fp.readline()
    number = lineToInt(line)
    numArray.append(number)

outputFile = folder + outPath + fileExt
outFilePointer = open(outputFile, 'w+')

loop = asyncio.get_event_loop()
myQueue = asyncio.Queue(maxsize =20)

try:
    loop.run_until_complete(asyncio.gather(putNumber(myQueue), writeFile(myQueue)))
except KeyboardInterrupt:
    pass
finally:
    loop.close()
