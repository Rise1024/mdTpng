
# 常见排序算法

本文将介绍常见的排序算法，并附上其伪代码。排序算法通常包括 **冒泡排序**、**选择排序**、**插入排序**、**归并排序**、**快速排序** 等。

## 1. 冒泡排序 (Bubble Sort)

### 简介
冒泡排序是一种简单的交换排序算法。通过不断交换相邻元素，最终将最大（或最小）元素“冒泡”到序列的末尾。

### 伪代码
```java
for i = 0 to n-1 do:
    for j = 0 to n-i-2 do:
        if arr[j] > arr[j+1] then:
            swap(arr[j], arr[j+1])
```

### 图示
```plaintext
[5, 3, 8, 4, 2]
  ↓
[3, 5, 8, 4, 2]
  ↓
[3, 5, 4, 8, 2]
  ↓
[3, 5, 4, 2, 8]
  ↓
[3, 4, 5, 2, 8]
  ↓
[3, 4, 2, 5, 8]
  ↓
[3, 2, 4, 5, 8]
  ↓
[2, 3, 4, 5, 8]  (排序完成)
```

## 2. 选择排序 (Selection Sort)

### 简介
选择排序每次从未排序的部分选择最小的元素，放到已排序部分的末尾。时间复杂度是 O(n²)。

### 伪代码
```java
for i = 0 to n-1 do:
    minIndex = i
    for j = i+1 to n do:
        if arr[j] < arr[minIndex] then:
            minIndex = j
    swap(arr[i], arr[minIndex])
```

### 图示
```plaintext
[5, 3, 8, 4, 2]
  ↓
选择最小： [2, 3, 8, 4, 5]
  ↓
选择最小： [2, 3, 8, 4, 5]
  ↓
选择最小： [2, 3, 4, 8, 5]
  ↓
选择最小： [2, 3, 4, 5, 8]
```

## 3. 插入排序 (Insertion Sort)

### 简介
插入排序将数组分为已排序和未排序两部分，每次将未排序的元素插入到已排序部分中。

### 伪代码
```java
for i = 1 to n-1 do:
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key do:
        arr[j + 1] = arr[j]
        j = j - 1
    arr[j + 1] = key
```

### 图示
```plaintext
[5, 3, 8, 4, 2]
  ↓
插入 3: [3, 5, 8, 4, 2]
  ↓
插入 8: [3, 5, 8, 4, 2]
  ↓
插入 4: [3, 4, 5, 8, 2]
  ↓
插入 2: [2, 3, 4, 5, 8]
```

## 4. 归并排序 (Merge Sort)

### 简介
归并排序是一种分治法排序算法，先将数组分为两半，分别排序后再合并。

### 伪代码
```java
mergeSort(arr):
    if length of arr <= 1 then:
        return arr
    mid = length of arr / 2
    left = mergeSort(arr[0, mid])
    right = mergeSort(arr[mid, end])
    return merge(left, right)

merge(left, right):
    while both arrays are not empty do:
        if left[0] < right[0] then:
            add left[0] to result
        else:
            add right[0] to result
    return result
```

### 图示
```plaintext
[5, 3, 8, 4, 2]
  ↓
分割: [5, 3, 8] 和 [4, 2]
  ↓
分割: [5, 3] 和 [8], [4] 和 [2]
  ↓
合并: [3, 5], [8] 和 [2, 4]
  ↓
合并: [3, 5, 8], [2, 4]
  ↓
最终合并: [2, 3, 4, 5, 8]
```

## 5. 快速排序 (Quick Sort)

### 简介
快速排序通过选择一个“基准”元素，将数组分为两部分，左侧元素比基准小，右侧比基准大，然后递归排序左右两部分。

### 伪代码
```java
quickSort(arr, low, high):
    if low < high then:
        pivotIndex = partition(arr, low, high)
        quickSort(arr, low, pivotIndex - 1)
        quickSort(arr, pivotIndex + 1, high)

partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j = low to high - 1 do:
        if arr[j] <= pivot then:
            i = i + 1
            swap(arr[i], arr[j])
    swap(arr[i + 1], arr[high])
    return i + 1
```

### 图示
```plaintext
[5, 3, 8, 4, 2]
  ↓
基准选择 2: [2, 3, 8, 4, 5]
  ↓
基准选择 3: [2, 3, 8, 4, 5]
  ↓
基准选择 4: [2, 3, 4, 8, 5]
  ↓
基准选择 5: [2, 3, 4, 5, 8] (排序完成)
```

## 总结

- **冒泡排序**：简单，时间复杂度 O(n²)，适合小数据集。
- **选择排序**：简单，时间复杂度 O(n²)，不稳定排序。
- **插入排序**：在部分有序的情况下，时间复杂度接近 O(n)，是稳定排序。
- **归并排序**：时间复杂度 O(n log n)，稳定排序，适合大数据集。
- **快速排序**：时间复杂度 O(n log n)，不稳定排序，实际应用中较为高效。

这些排序算法适用于不同的场景，根据具体数据的特性选择合适的排序算法，可以提高程序效率。
