import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights. # (3073,10)
  - X: A numpy array of shape (N, D) containing a minibatch of data. # (49000,3073)
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in xrange(num_train): # 49000 loops
    scores = X[i].dot(W) # (1,3073).dot(3073,10) = (10,)
    correct_class_score = scores[y[i]]
    for j in xrange(num_classes): # 10 loops
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        dW[:, y[i]] -= X[i, :].T # j==y : accumulate the gradient over incorrect classes to the correct class weight vector
        dW[:, j]    += X[i, :].T # j!=y : incorrect class weight vector gradient

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
    
  # same for gradients
  dW /= num_train

  # Add regularization to the loss.
  loss += 0.5 * reg * np.sum(W * W) # W*W is elementwise computation. WHY 0.5?

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather than first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################
  dW += reg*W # WHY?
  
  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero
  num_train = X.shape[0] # 500
  num_classes = W.shape[1] # 10
  D = X.shape[1]

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  
  scores = X.dot(W) # (500, 3073).(3073, 10) = (500, 10)
  correct_class_score = scores[np.arange(num_train),y] # (500,)
  margins = (scores.T - correct_class_score + 1).T
  margins[np.arange(num_train), y] = 0 # correct class
  margins[margins<0] = 0 # negative number is changed to 0
  loss = np.sum(margins)
  loss /= num_train
  loss += 0.5 * reg * np.sum(W * W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  ############################################################################# 
  binary = margins # binary = mask
  binary[margins>0] = 1
  row_sum = np.sum(binary, axis=1)
  binary[range(num_train), y] = -row_sum
  dW = binary.T.dot(X).T
  dW /= num_train

  dW += reg*W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
