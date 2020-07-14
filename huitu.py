import matplotlib.pyplot as plt
import numpy as np
with plt.style.context(['science','ieee','no-latex','vibrant']):
    plt.plot([-0.4,-0.43,-0.78,-0.94])
    plt.title('space 1')

    # plt.figure()
    # plt.plot([-0.04])
    plt.figure()
    plt.plot(np.abs([-0.07, -0.4, -0.29, -0.42]))
    plt.title('space 2')
    plt.figure()
    plt.plot(np.abs([0.23, 0.53, 0.76, 0.85]))
    plt.title('space 3')
    plt.figure()
    plt.plot(np.abs([-0.45, -0.47, -0.5, -0.6]))
    plt.title('space 5')
    plt.figure()
    plt.plot(np.abs([-0.42, -0.23, -0.08, -0.64]))
    plt.title('space 7')

    plt.show()