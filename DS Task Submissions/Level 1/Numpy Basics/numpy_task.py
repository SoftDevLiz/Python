import numpy as np

# [1]

# these commas are splitting the rows into 3 separate groups, which breaks the function
# np.array((1, 0, 0), (0, 1, 0), (0, 0, 1), dtype=float)

# It should look like this:
np.array([(), (), ()], dtype=float)

# [2]

# 1D array
a = np.array([0, 0, 0])

# 2D array
a = np.array([[0, 0, 0]])

# [3]

array = np.linspace(1, 48, 48).reshape(3, 4, 4)
print(array)

# 20.0
print(array[1, 0, 3])
# [ 9. 10. 11. 12.]
print(array[0, 2, :])
# [[33. 34. 35. 36.] [37. 38. 39. 40.] [41. 42. 43. 44.] [45. 46. 47. 48.]]
print(array[2, :, :])
# [[5. 6.] [21. 22.] [37. 38.]]
print(array[:, 1, :2])
# [[36. 35.] [40. 39.] [44. 43.] [48. 47.]]
print(array[2, :, 3:1:-1])
# [[13. 9. 5. 1.] [29. 25. 21. 17.] [45. 41. 37. 33.]]
print(array[:, ::-1, 0].T)
# [[1. 4.] [45. 48.]]
print(array[[0, 2], [0, 3], ::3])

# [[25. 26. 27. 28.] [29. 30. 31. 32.] [33. 34. 35. 36.] [37. 38. 39. 40.]]
array = array.flatten()
print(array)

array = array[24:40].reshape(4, 4)
print(array)
