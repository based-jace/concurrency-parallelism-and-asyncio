import time


print("Starting...")
start = time.time()

for i in range(1000000, 1000016):
    pow(i, i)
    print("okay")

end = time.time()
print(f"Time to complete: {round(end - start, 2)}")
