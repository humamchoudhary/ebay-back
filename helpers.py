from pymongo import cursor


def cur_to_list(cur, first=False):
    if type(cur) == cursor:
        if not first:
            return [dict(item, _id=str(item["_id"])) for item in cur]
        else:
            return [dict(item, _id=str(item["_id"])) for item in cur][0]
    else:
        cur["_id"] = str(cur["_id"])
        return cur
