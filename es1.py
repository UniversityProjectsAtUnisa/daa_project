def lds(arr):
    if len(arr) < 1:
        return []
    DP = [i for i in arr]
    for i in range(1, len(arr)):

        for j in range(i):
            if arr[j] >= arr[i]:
                DP[i] = max(DP[i], DP[j]+arr[i])
    return solution(DP, arr)


def solution(DP, arr):
    left = max(DP)
    i = DP.index(left)

    sol = [arr[i]]
    left -= arr[i]
    while left > 0:
        while DP[i] != left or arr[i] == 0:
            i -= 1
        sol.append(arr[i])
        left -= arr[i]
    return list(reversed(sol))
