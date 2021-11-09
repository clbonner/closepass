def checkDistance():
    if (distance > 50 and distance < 150):
        closePass(distance)
    return

def closePass(distance):
    closestDistance = distance

    while (distance > 50 and distance < 150):
        if distance < closestDistance:
            closestDistance = distance

    logClosePass(closestDistance)

# store close pass distance on local datastore
# if storage full then write over log
def logClosePass(distance):
    print("Closest Distance:", distance)
