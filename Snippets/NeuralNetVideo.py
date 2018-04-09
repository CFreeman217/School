import numpy as np

# Plot sigmoid function, computes probabilities
def nonlinearity(x, deriv=False):
    if(deriv==True):
        return (x*(1-x))
    return 1/(1+np.exp(-x))

# Input data: Pairs of x and y values
x = np.array([[0,0,1],
            [0,1,1],
            [1,0,1],
            [1,1,1]])

y = np.array([[0],
            [1],
            [1],
            [0]])

# Seed
np.random.seed(1) # This serves as a way to reproduce these results

# Synapses
syn0 = 2*np.random.random((3,4)) - 1 # 3X4 synapse matrix with a bias of -1
syn1 = 2*np.random.random((4,1)) - 1 # 3X4 synapse matrix with a bias of -1

# Training
for j in range(60000):

    # Layers, we are not directly programming the probabilities
    # Input data
    l0 = x
    # Perform matrix multiplication from the input to generate a hidden layer
    l1 = nonlinearity(np.dot(l0,syn0))
    # Perform matrix multiplication on the hidden layer to generate output
    l2 = nonlinearity(np.dot(l1,syn1))

    # Backpropagation, determine the error
    l2_error = y - l2

    # Log the error every 10,000th iteration
    if(j%10000==0):
        print("Error : " + str(np.mean(np.abs(l2_error))))

    # Calculate Deltas
    l2_delta = l2_error*nonlinearity(l2, deriv=True)
    l1_error = l2_delta.dot(syn1.T)
    l1_delta = l1_error * nonlinearity(l1, deriv=True)

    # Update our synapses
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

print("Output after training :")
print(l2)
