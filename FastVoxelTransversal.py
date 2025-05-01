from math import floor, sqrt, inf, ceil


def FastVoxelTraversal(start, end):
    """
    Parameters :
    -------------
    - start : tuple of size n representing the starting point of our segment
    - end : tuple of size n representing the endpoint of our segment
    """
    vector = []
    step_vector = []
    for start_i, end_i in zip(start, end):
        vector.append(end_i - start_i)
        if end_i > start_i:
            step_vector.append(1)
        elif end_i == start_i:
            step_vector.append(0)
        else:
            step_vector.append(-1)
    vector_norm = sqrt(sum(e**2 for e in vector))
    vector = [abs(e/vector_norm) for e in vector]

    current_point = [floor(element) for element in start]
    end_point = [floor(element) for element in end]

    L_points = [tuple(current_point)]
    tDelta = [1/vector[i] if vector[i]!=0 else inf for i in range(len(start))]
    tMax = []
    for i in range(len(start)):
        x = start[i]
        if vector[i] == 0:
            distance = inf
        elif step_vector[i] == 1:
            distance = ceil(x)-x
        else:
            distance = x-floor(x)
        if distance == 0:
            distance = 1
        tMax.append(distance/vector[i])
    while current_point != end_point:
        direction = min(range(len(tMax)), key=tMax.__getitem__)
        tMax[direction] += tDelta[direction]
        current_point[direction] += step_vector[direction]
        L_points.append(tuple(current_point))
    return L_points


print(FastVoxelTraversal((7,1), (8,0)))