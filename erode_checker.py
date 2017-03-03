def is_erode(rect1, rect2):
    [x1, y1, w1, h1] = rect1
    [x2, y2, w2, h2] = rect2
    if x1+w1>x2>x1 and y1+h1>y2>y1:
        return True
    elif x2+w2>x1>x2 and y2+h2>y1>y2:
        return True
    elif x1==x2 and y1==y2:
        return True
    else:
        return False

def are_u_erode(cur_rect,segment):
    for seg_rect in segment:
        if is_erode(seg_rect, cur_rect):
            return True

def find_max_area(segment, seg_idx):
    max = -1
    for idx, rect in enumerate(segment):
        area = rect[2] * rect[3] # [2] == w [3] == h
        if max < area:
            max = area
            max_idx = idx
    return seg_idx[max_idx]

def find_independant_idx(contours):
    import cv2
    segments = []
    segs_idx = []
    seg_idx = []

    for idx, c in enumerate(contours):
        cur_rect = cv2.boundingRect(c)
        if len(segments) is not 0:
            for segment in segments:
                if are_u_erode(cur_rect, segment):
                    segment.append(cur_rect)
                    seg_idx.append(idx)
                else:
                    new_segment = [cur_rect]
                    new_idx = [idx]
                    segments.append(new_segment)
                    segs_idx.append(new_idx)
        else:
            new_segment = [cur_rect]
            new_idx = [idx]
            segments.append(new_segment)
            segs_idx.append(new_idx)

    max_area_idxs = []
    for idx, segment in enumerate(segments):
        max_area_idx = find_max_area(segment, segs_idx[idx])
        max_area_idxs.append(max_area_idx)

    return max_area_idxs

