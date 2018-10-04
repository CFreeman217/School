import os
import numpy as np

def prob5_43():
    p_inv = np.array([[-4, 9, -3],
                      [0, -4, 7],
                      [-1, -4, -9]])
    p_arr = np.linalg.inv(p_inv)
    a_mat = np.array([[-1, -7, 6],
                      [-8, 4, 8],
                      [4, 7, -8]])
    b_mat = np.transpose([[-5, -7, 5]])
    c_mat = np.array([-9, -9, 8])
    piap = np.linalg.multi_dot([p_inv,a_mat,p_arr])
    pinvb = np.matmul(np.diag(b_mat), p_inv)
    cp = np.linalg.multi_dot([p_arr,np.diag(c_mat)])

    # pinvb = np.dot(b_mat,p_inv)
    # cp = np.dot(p_arr, c_mat)
    print("P Matrix")                  
    print(p_arr)
    print("Pinv * A * P")
    print(piap)
    print("Pinv * B")
    print(pinvb)
    print("C * P")
    print(cp)


# prob5_43()
# # arr_A = np.array([[-1, -7, 6],
# #                    [-8, 4, 8],
# #                    [4, 7, -8]])
# # arr_B = np.transpose([[-1, 2, -2]])

arr_A = np.array([[-5, -5, 4],
                   [2, 0, -2],
                   [0, -2, -1]])
# arr_B = np.transpose([[-1, 2, -2]])
# arr_C = np.array([1, -3, 4])

A_prime, P_vec = np.linalg.eig(arr_A)

A_diag = np.diag(A_prime)
print("eigenvectors")
print(-P_vec)
print("A Prime")
print(A_prime)

# B_prime = np.linalg.inv(P_vec)*arr_B
# C_prime = arr_C*P_vec
# print("B Prime")
# print(B_prime)
# print("C Prime")
# print(C_prime)
# print("New A")
# new_a = np.linalg.pinv(P_vec)*A_diag*P_vec
# print(new_a)
# # print(np.linalg.pinv(P_vec)*arr_A*P_vec)