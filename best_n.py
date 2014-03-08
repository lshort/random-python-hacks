def best_n(input, n):
    """Select the smallest N of the input array"""
    if n >= len(input):
        return input
    output = input[0:n+1]
    for i in range(0,n):
        counter = i
        while  counter > 0 and output[counter-1] > input[i]:
            output[counter] = output[counter-1]
            counter -= 1
        output[counter] = input[i]
    for i in range(n,len(input)):
        counter = n
        while  counter > 0 and output[counter-1] > input[i]:
            output[counter] = output[counter-1]
            counter -= 1
        output[counter] = input[i]
    return output[0:n]

def __best_test__(input,count):
    print("best " + str(count) + " of "+ str(input))
    print("  -->" + str(best_n(input,count)))

if __name__ == "__main__":
    __best_test__([9,8,7,6,5,4,3,2,1],4)
    __best_test__([9,8,7,6,5,4,3,2,1],14)
    __best_test__([9,8,7,6,5,3,1],3)
    __best_test__([9,5,3,1,8,7,6],3)
    __best_test__([9,3,2,1,8,7,6,5,4],4)
    __best_test__([9,3,2,1,8,7,6,5,4],3)
    __best_test__([9,3,2,1,8,7,6,5,4],2)
    __best_test__([9,3,2,1,8,7,6,5,4],1)
    __best_test__([9,3,2,1,8,7,6,5,4],9)
    __best_test__([9,3,2,1,8,7,6,5,4],7)
    __best_test__([],2)
    __best_test__([2,1],2)
    __best_test__([2,1,3],2)
    __best_test__([1],2)
