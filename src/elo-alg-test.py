import random

def make_random_array(x):

    ints = list(range(x))
    random.shuffle(ints)

    return [[num, 0] for num in ints]


def count_inversions(arr):
    def merge_and_count(arr, temp_arr, left, right):
        if left == right:
            return 0
        
        mid = (left + right) // 2
        inv_count = 0
        inv_count += merge_and_count(arr, temp_arr, left, mid)
        inv_count += merge_and_count(arr, temp_arr, mid + 1, right)
        inv_count += merge_and_merge_count(arr, temp_arr, left, mid, right)
        
        return inv_count

    def merge_and_merge_count(arr, temp_arr, left, mid, right):
        i = left  # Starting index for left subarray
        j = mid + 1  # Starting index for right subarray
        k = left  # Starting index to be sorted
        inv_count = 0

        # Merge the two subarrays
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp_arr[k] = arr[i]
                i += 1
            else:
                temp_arr[k] = arr[j]
                inv_count += (mid-i + 1)  # Count inversions
                j += 1
            k += 1

        # Copy the remaining elements of the left subarray
        while i <= mid:
            temp_arr[k] = arr[i]
            i += 1
            k += 1

        # Copy the remaining elements of the right subarray
        while j <= right:
            temp_arr[k] = arr[j]
            j += 1
            k += 1

        # Copy the sorted subarray into original array
        for i in range(left, right + 1):
            arr[i] = temp_arr[i]

        return inv_count

    n = len(arr)
    temp_arr = [0] * n
    return merge_and_count(arr, temp_arr, 0, n - 1)






#1: constant win/loss for eq ranks (elo basically)
def const_sort(arr, iterations):

    for j in range(iterations):
        for i in range(0, len(arr), 2):
            c = arr[i][0] > arr[i+1][0]
            inc = 10
            arr[i][1] += inc if c else -inc
            arr[i+1][1] += inc if not c else -inc
        
        arr.sort(key=lambda x: x[1])
    
    return arr


#2: time-decreasing win/loss (elo w/ time decrease)
def td_sort(arr, iterations):

    for j in range(iterations):
        current_change = 10*0.83**j
        for i in range(0, len(arr), 2):
            c = arr[i][0] > arr[i+1][0]
            arr[i][1] += current_change if c else -current_change
            arr[i+1][1] += current_change if not c else -current_change
        
        arr.sort(key=lambda x: x[1])
    
    return arr


#3: rating-proportional win/loss
def rp_sort(arr, iterations):

    for j in range(iterations):
        for i in range(0, len(arr), 2):
            c = arr[i][0] > arr[i+1][0]
            d = arr[i][1] 

            if d == 0:
                dw=10
                dl=10
            if d>0:
                dw = 10
                dl = -10*(0.99**d)
            else:
                dl = -10
                dw = 10*(0.99**abs(d))

            arr[i][1] += dw if c else dl
            arr[i+1][1] += dw if not c else dl
        
        arr.sort(key=lambda x: x[1])
    
    return arr


averages = [0,0,0,0]

for i in range(100):
    averages[0] += count_inversions(make_random_array(2048))
    averages[1] += count_inversions(const_sort(make_random_array(2048), 11))
    averages[2] += count_inversions(td_sort(make_random_array(2048), 11))
    averages[3] += count_inversions(rp_sort(make_random_array(2048), 11))

averages = [x/100 for x in averages]

unsorted_rating =  make_random_array(2048)
const_rating = const_sort(make_random_array(2048), 11)
td_rating = td_sort(make_random_array(2048), 11)
rp_rating = rp_sort(make_random_array(2048), 11)

print(rp_rating)
print(f"Number of inversions: {count_inversions(unsorted_rating)}")
print(f"Number of inversions: {count_inversions(const_rating)}")
print(f"Number of inversions: {count_inversions(td_rating)}")
print(f"Number of inversions: {count_inversions(rp_rating)}")

print(averages)