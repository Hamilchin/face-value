import random
import math

def merge_sort(arr):
    comparisons = [0]  # Counter for the number of comparisons

    def merge(left, right):
        sorted_list = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1  # Count each comparison
            if left[i] <= right[j]:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list

    def merge_sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left_half = merge_sort_recursive(arr[:mid])
        right_half = merge_sort_recursive(arr[mid:])
        return merge(left_half, right_half)

    sorted_arr = merge_sort_recursive(arr)

    return sorted_arr, comparisons[0]



n = 1024

average_comparisons = 0
rounds = 10000

for i in range(rounds):

    if (i % 100 == 0):
        print(i)

    test = [x for x in range(n)]
    random.shuffle(test)
    average_comparisons += merge_sort(test)[1]

average_comparisons /= rounds


calculated_comparisons = 0
for p in range (1, int(math.log(n, 2))):
    calculated_comparisons += (n*2**(p-1)) / (2**(p-1) + 1)

print(average_comparisons, calculated_comparisons)
