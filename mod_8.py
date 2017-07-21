import numpy as np
import matplotlib.pyplot as plt
import random
import pprint
import copy
import math

plain = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]
forest = [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
hills = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
swamp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0]

figure = plt.figure(figsize=(20, 6))

axes = figure.add_subplot(1, 3, 1)
pixels = np.array([255 - p * 255 for p in plain], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title("Left Camera")
axes.imshow(pixels, cmap='gray')

axes = figure.add_subplot(1, 3, 2)
pixels = np.array([255 - p * 255 for p in forest], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title("Front Camera")
axes.imshow(pixels, cmap='gray')

axes = figure.add_subplot(1, 3, 3)
pixels = np.array([255 - p * 255 for p in hills], dtype='uint8')
pixels = pixels.reshape((4, 4))
axes.set_title("Right Camera")
axes.imshow(pixels, cmap='gray')

# plt.show()
plt.close()

clean_data = {
    "plains": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, "plains"]
    ],
    "forest": [
        [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, "forest"],
        [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, "forest"],
        [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, "forest"],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, "forest"]
    ],
    "hills": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, "hills"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, "hills"]
    ],
    "swamp": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, "swamp"],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, "swamp"]
    ]
}


def view_sensor_image(data):
    figure = plt.figure(figsize=(4, 4))
    axes = figure.add_subplot(1, 1, 1)
    pixels = np.array([255 - p * 255 for p in data[:-1]], dtype='uint8')
    pixels = pixels.reshape((4, 4))
    axes.set_title("Left Camera:" + data[-1])
    axes.imshow(pixels, cmap='gray')
    plt.show()
    plt.close()


def blur(data):
    def apply_noise(value):
        if value < 0.5:
            v = random.gauss(0.10, 0.05)
            if v < 0.0:
                return 0.0
            if v > 0.75:
                return 0.75
            return v
        else:
            v = random.gauss(0.90, 0.10)
            if v < 0.25:
                return 0.25
            if v > 1.00:
                return 1.00
            return v

    noisy_readings = [apply_noise(v) for v in data[0:-1]]
    return noisy_readings + [data[-1]]


def generate_data(data, n, label):
    new_data = []

    for x in range(n):
        random_index = random.randint(0, len(data[label]) - 1)
        correct_type = blur(data[label][random_index])
        correct_type[-1] = 1
        new_data.append([correct_type, data[label][random_index]])

    for x in range(n):
        types = data.keys()
        types.remove(label)
        random_index = random.randint(0, len(types) - 1)
        incorrect_label = types[random_index]
        random_index_terrain = random.randint(0, len(data[incorrect_label]) - 1)
        incorrect_type = blur(data[incorrect_label][random_index_terrain])
        incorrect_type[-1] = 0
        new_data.append([incorrect_type, data[incorrect_label]])

    random.shuffle(new_data)

    return new_data


def learn_model(data, verbose=False):
    '''
    IMPORTANT NOTES:
    * logistic regression model
    * if verbose=True. print out error. should be getting smaller
    * make alpha adaptive (if error increases, alpha = alpha/10)
    * when code is working, only print error every 1000 iterations
    * return list of thetas
    '''
    x_0 = 1
    epsilon = 0.0000001
    alpha = 0.1

    thetas = get_random_thetas(len(data[0][0]) - 1)
    prev_error = 0.0
    current_error = calculate_error(data, thetas)
    num_iterations = 1
    while abs(current_error - prev_error) > epsilon:
        new_thetas = []
        for x in range(len(thetas)):
            new_thetas.append(thetas[x] - (alpha * get_derivative(x, thetas, data)))
        thetas = new_thetas
        prev_error = current_error
        current_error = calculate_error(data, thetas)
        if verbose and (num_iterations % 1000) == 0:
            print(current_error)
        if prev_error < current_error:
            alpha = alpha / 10.0
        num_iterations += 1
    return thetas


def apply_model(model, test_data, labeled=False):
    results = []
    for d in test_data:
        y_hat = get_y_hat(model, d[0])
        if y_hat >= 0.5:
            if not labeled:
                results.append((1, y_hat))
            else:
                results.append((1, d[0][-1]))
        else:
            if not labeled:
                results.append((0, y_hat))
            else:
                results.append((0, d[0][-1]))
    return results


def calculate_confusion_matrix(results):
    # (actual, predicted)
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0
    actual_postive = 0.0
    actual_negative = 0.0

    for r in results:
        if r[0] == 1 and r[1] == 1:
            tp += 1
            actual_postive += 1
        elif r[0] == 0 and r[1] == 0:
            tn += 1
            actual_negative += 1
        elif r[0] == 1 and r[1] == 0:
            fn += 1
            actual_postive += 1
        elif r[0] == 0 and r[1] == 1:
            fp += 1
            actual_negative += 1

    error_rate = (fp + fn) / len(results)
    tpr = tp / actual_postive
    tnr = tn / actual_negative


def get_random_thetas(num):
    thetas = []
    for x in range(num):
        thetas.append(random.uniform(-1.0, 1.0))
    return thetas


def calculate_error(data, thetas):
    err_sum = 0.0
    for datapoint in data:
        x = datapoint[0]
        y = datapoint[1]
        y_hat = get_y_hat(thetas, x)
        y_i = x[-1]
        err_sum += (y_i * math.log(y_hat)) + ((1 - y_i) * math.log(1 - y_hat))
    return (-1.0 / len(data)) * err_sum


def get_derivative(i, thetas, data):
    summ = 0.0
    for a in range(len(data)):
        datapoint = data[a]
        x = datapoint[0]
        y = datapoint[1]
        y_hat = get_y_hat(thetas, x)
        y_i = x[-1]
        summ += (y_hat - y_i) * data[a][0][i]
    return (1.0 / len(data)) * summ


def get_y_hat(thetas, x_col):
    z = -1.0 * get_z(thetas, x_col)
    return 1.0 / (1 + math.exp(z))


def get_z(thetas, x_col):
    dot_product = 0.0
    for x in range(len(thetas)):
        if x == 0:
            dot_product += (1.0 * thetas[0])
        else:
            dot_product += (x_col[x] * thetas[x])
    return dot_product


training_data = generate_data(clean_data, 5, "hills")
# model = learn_model(training_data, True)
model = [0.16312377016373983, -3.259757043839148, -0.6880656920086171, 0.7908715039945684, -2.6849953218780827,
         9.228798683747634, -3.722500524167003, 0.8984327100429845, -2.290627107406444, 5.481769992348481,
         -0.5551872463522771, -8.409021277809163, -0.47114319858870907, -2.545736538430127, 0.14631933185031826,
         0.29118286099789553]
test_data = generate_data(clean_data, 5, "hills")
results = apply_model(model, test_data, labeled=True)
calculate_confusion_matrix(results)
