def _solution(DP, arr):
    """Builds solution based on intermediate dynamic programming list

    Args:
        DP (list of int): Intermediate dynamic programming list
        arr (list of int): list of integers to extract the subsequence from

    Returns:
        list of int: greatest descending subsequence (in wide sense)
    """
    left = max(DP)
    i = DP.index(left)

    last = arr[i]
    sol = [last]
    left -= arr[i]
    while left > 0:
        while DP[i] != left or arr[i] == 0 or arr[i] < last:
            i -= 1
        last = arr[i]
        sol.append(last)
        left -= arr[i]
    return list(reversed(sol))


def gds(arr):
    """Finds greatest descending subsequence (in wide sense) in list of integers

    Args:
        arr (list of int): list of integers to extract the subsequence from

    Returns:
        list of int: greatest descending subsequence (in wide sense)
    """
    if len(arr) < 1:
        return []
    if all(el < 0 for el in arr):
        return []
    DP = arr[:]
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[j] >= arr[i]:
                DP[i] = max(DP[i], DP[j]+arr[i])
    return _solution(DP, arr)
