from math import floor, sqrt, inf, ceil


def get_start_voxel(start, step_vector):
    """
    If the starting point is on the edge of a voxel, we 'choose' the closest voxel towards the end point
    """
    start_voxel = []
    for i in range(len(start)):
        x = start[i]
        if step_vector[i] < 0 and floor(x) == x:
            start_voxel.append(floor(x)-1)
        else:
            start_voxel.append(floor(x))
    return start_voxel

def get_end_voxel(end, step_vector):
    """
    If the end point is on the edge of a voxel, we 'choose' the closest voxel towards the start point
    """
    end_voxel = []
    for i in range(len(end)):
        x = end[i]
        if step_vector[i] > 0 and floor(x) == x:
            end_voxel.append(floor(x)-1)
        else:
            end_voxel.append(floor(x))
    return end_voxel


def FastVoxelTraversal(start, end):
    """
    Parameters :
    -------------
    - start : tuple of size n representing the starting point of our segment
    - end : tuple of size n representing the endpoint of our segment
    """
    if tuple(start) == tuple(end):
        return [floor(x) for x in start]
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

    current_point = [floor(element) for element in start] #get_start_voxel(start, step_vector)
    end_point = get_end_voxel(end, step_vector)

    L_points = [tuple(current_point)]
    tDelta = [1/abs(vector[i]) if vector[i]!=0 else inf for i in range(len(start))]
    tMax = []
    for i in range(len(start)):
        x = start[i]
        if vector[i] == 0:
            distance = inf
            tMax.append(distance)
        elif step_vector[i] == 1:
            distance = floor(x)+1-x
            tMax.append(distance/abs(vector[i]))
        else:
            distance = x-floor(x)
            tMax.append(distance/abs(vector[i]))
    while current_point != end_point:
        direction = min(range(len(tMax)), key=tMax.__getitem__)
        tMax[direction] += tDelta[direction]
        current_point[direction] += step_vector[direction]
        L_points.append(tuple(current_point))
    return L_points


if __name__ == "__main__":
    print(FastVoxelTraversal((5,3), (3, 5)))