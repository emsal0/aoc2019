img = input().strip()

layers = []

imglen =  len(img)
offset = imglen // (25 * 6)

while len(img) > 0:
    layers.append(img[:25*6])
    img = img[25*6:]

# part a
golden_row = sorted(layers, key = lambda x: x.count('0'))[0]
    
print(golden_row)
print(golden_row.count('1') * golden_row.count('2'))

# part b

final_img = ''

for i in range(25*6):
    nextpx = '2'
    for j in range(len(layers)):
        condpx = layers[j][i]
        if condpx in ['0', '1']:
            nextpx = condpx
            break
    final_img += nextpx

for i in range(6):
    print(final_img[25*i:25*(i+1)]
            .replace('0', '\033[40m0\033[0m')
            .replace('1', '\033[107m0\033[0m'))
