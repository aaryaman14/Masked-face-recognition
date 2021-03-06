# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Contains the definition of the Inception Resnet V1 architecture.
As described in http://arxiv.org/abs/1602.07261.
  Inception-v4, Inception-ResNet and the Impact of Residual Connections
    on Learning
  Christian Szegedy, Sergey Ioffe, Vincent Vanhoucke, Alex Alemi
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow
if tensorflow.__version__.startswith('1.'):
    import tensorflow as tf
    import tensorflow.contrib.slim as slim
else:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()
    import tf_slim as slim
act_f = tf.nn.relu

def tf_mish(inputs):
    return inputs * tf.math.tanh(tf.math.softplus(inputs))

# Inception-Resnet-A
def block35(net, scale=1.0, activation_fn=act_f, filter=None,scope=None, reuse=None):
    """Builds the 35x35 resnet block."""
    if filter is None:
        filter = 32
    with tf.variable_scope(scope, 'Block35', [net], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            tower_conv = slim.conv2d(net, filter, 1, scope='Conv2d_1x1',activation_fn=activation_fn)
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = slim.conv2d(net, filter, 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
            tower_conv1_1 = slim.conv2d(tower_conv1_0, filter, 3, scope='Conv2d_0b_3x3',activation_fn=activation_fn)
        with tf.variable_scope('Branch_2'):
            tower_conv2_0 = slim.conv2d(net, filter, 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
            tower_conv2_1 = slim.conv2d(tower_conv2_0, filter, 3, scope='Conv2d_0b_3x3',activation_fn=activation_fn)
            tower_conv2_2 = slim.conv2d(tower_conv2_1, filter, 3, scope='Conv2d_0c_3x3',activation_fn=activation_fn)
        mixed = tf.concat([tower_conv, tower_conv1_1, tower_conv2_2], 3)
        up = slim.conv2d(mixed, net.get_shape()[3], 1, normalizer_fn=None,
                         activation_fn=None, scope='Conv2d_1x1')
        net += scale * up
        if activation_fn:
            net = activation_fn(net)
    return net

# Inception-Resnet-B
def block17(net, scale=1.0, activation_fn=act_f, filter=None, scope=None, reuse=None):
    """Builds the 17x17 resnet block."""
    if filter is None:
        filter = 128

    with tf.variable_scope(scope, 'Block17', [net], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            tower_conv = slim.conv2d(net, filter, 1, scope='Conv2d_1x1',activation_fn=activation_fn)
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = slim.conv2d(net, filter, 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
            tower_conv1_1 = slim.conv2d(tower_conv1_0, filter, [1, 7],
                                        scope='Conv2d_0b_1x7',activation_fn=activation_fn)
            tower_conv1_2 = slim.conv2d(tower_conv1_1, filter, [7, 1],
                                        scope='Conv2d_0c_7x1',activation_fn=activation_fn)
        mixed = tf.concat([tower_conv, tower_conv1_2], 3)
        up = slim.conv2d(mixed, net.get_shape()[3], 1, normalizer_fn=None,
                         activation_fn=None, scope='Conv2d_1x1')
        net += scale * up
        if activation_fn:
            net = activation_fn(net)
    return net

def block17_2(net, scale=1.0, activation_fn=act_f, filter=None, scope=None, reuse=None):
    """Builds the 17x17 resnet block."""
    if filter is None:
        filter = 128

    with tf.variable_scope(scope, 'Block17', [net], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            tower_conv = slim.conv2d(net, filter, 1, scope='Conv2d_1x1')
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = slim.conv2d(net, filter, 1, scope='Conv2d_0a_1x1')
            tower_conv1_1 = slim.conv2d(tower_conv1_0, filter, [1, 5],
                                        scope='Conv2d_0b_1x7')
            tower_conv1_2 = slim.conv2d(tower_conv1_1, filter, [5, 1],
                                        scope='Conv2d_0c_7x1')
        mixed = tf.concat([tower_conv, tower_conv1_2], 3)
        up = slim.conv2d(mixed, net.get_shape()[3], 1, normalizer_fn=None,
                         activation_fn=None, scope='Conv2d_1x1')
        net += scale * up
        if activation_fn:
            net = activation_fn(net)
    return net

# Inception-Resnet-C
def block8(net, scale=1.0, activation_fn=act_f, filter=None, scope=None, reuse=None):
    """Builds the 8x8 resnet block."""
    if filter is None:
        filter = 192

    with tf.variable_scope(scope, 'Block8', [net], reuse=reuse):
        with tf.variable_scope('Branch_0'):
            tower_conv = slim.conv2d(net, filter, 1, scope='Conv2d_1x1',activation_fn=activation_fn)
        with tf.variable_scope('Branch_1'):
            tower_conv1_0 = slim.conv2d(net, filter, 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
            tower_conv1_1 = slim.conv2d(tower_conv1_0, filter, [1, 3],
                                        scope='Conv2d_0b_1x3',activation_fn=activation_fn)
            tower_conv1_2 = slim.conv2d(tower_conv1_1, filter, [3, 1],
                                        scope='Conv2d_0c_3x1',activation_fn=activation_fn)
        mixed = tf.concat([tower_conv, tower_conv1_2], 3)
        up = slim.conv2d(mixed, net.get_shape()[3], 1, normalizer_fn=None,
                         activation_fn=None, scope='Conv2d_1x1')
        net += scale * up
        if activation_fn:
            net = activation_fn(net)
    return net
  
def reduction_a(net, k, l, m, n,activation_fn=act_f):
    with tf.variable_scope('Branch_0'):
        tower_conv = slim.conv2d(net, n, 3, stride=2, padding='VALID',
                                 scope='Conv2d_1a_3x3',activation_fn=activation_fn)
    with tf.variable_scope('Branch_1'):
        tower_conv1_0 = slim.conv2d(net, k, 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
        tower_conv1_1 = slim.conv2d(tower_conv1_0, l, 3,
                                    scope='Conv2d_0b_3x3',activation_fn=activation_fn)
        tower_conv1_2 = slim.conv2d(tower_conv1_1, m, 3,
                                    stride=2, padding='VALID',
                                    scope='Conv2d_1a_3x3',activation_fn=activation_fn)
    with tf.variable_scope('Branch_2'):
        tower_pool = slim.max_pool2d(net, 3, stride=2, padding='VALID',
                                     scope='MaxPool_1a_3x3')
    net = tf.concat([tower_conv, tower_conv1_2, tower_pool], 3)
    return net

def reduction_b(net,filter_list=None,activation_fn=act_f):
    if filter_list is None:
        filter_list = [256,384]

    with tf.variable_scope('Branch_0'):
        tower_conv = slim.conv2d(net, filter_list[0], 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
        tower_conv_1 = slim.conv2d(tower_conv, filter_list[1], 3, stride=2,
                                   padding='VALID', scope='Conv2d_1a_3x3',activation_fn=activation_fn)
    with tf.variable_scope('Branch_1'):
        tower_conv1 = slim.conv2d(net, filter_list[0], 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
        tower_conv1_1 = slim.conv2d(tower_conv1, filter_list[0], 3, stride=2,
                                    padding='VALID', scope='Conv2d_1a_3x3',activation_fn=activation_fn)
    with tf.variable_scope('Branch_2'):
        tower_conv2 = slim.conv2d(net, filter_list[0], 1, scope='Conv2d_0a_1x1',activation_fn=activation_fn)
        tower_conv2_1 = slim.conv2d(tower_conv2, filter_list[0], 3,
                                    scope='Conv2d_0b_3x3',activation_fn=activation_fn)
        tower_conv2_2 = slim.conv2d(tower_conv2_1, filter_list[0], 3, stride=2,
                                    padding='VALID', scope='Conv2d_1a_3x3',activation_fn=activation_fn)
    with tf.variable_scope('Branch_3'):
        tower_pool = slim.max_pool2d(net, 3, stride=2, padding='VALID',
                                     scope='MaxPool_1a_3x3')
    net = tf.concat([tower_conv_1, tower_conv1_1,
                        tower_conv2_2, tower_pool], 3)
    return net
  
def inference(images, keep_probability, bottleneck_layer_size=128,
              weight_decay=0.0, reuse=None,filter_list=None,activation=tf.nn.relu):

    # batch_norm_params = {
    #     # Decay for the moving averages.
    #     'decay': 0.995,
    #     # epsilon to prevent 0s in variance.
    #     'epsilon': 0.001,
    #     # force in-place updates of mean and variance estimates
    #     'updates_collections': None,
    #     # Moving averages ends up in the trainable variables collection
    #     'variables_collections': [ tf.GraphKeys.TRAINABLE_VARIABLES ],
    # }
    
    with slim.arg_scope([slim.conv2d, slim.fully_connected],
                        weights_initializer=slim.initializers.xavier_initializer(), 
                        weights_regularizer=slim.l2_regularizer(weight_decay),
                        # normalizer_fn=slim.batch_norm,
                        # normalizer_params=batch_norm_params
                        ):
        return inception_resnet_v1(images,
                                   dropout_keep_prob=keep_probability,
                                   bottleneck_layer_size=bottleneck_layer_size,
                                   reuse=reuse,filter_list=filter_list,
                                   activation=activation)

def inception_resnet_v1(inputs,
                        dropout_keep_prob=0.8,
                        bottleneck_layer_size=128,
                        reuse=None,
                        filter_list=None,
                        activation=tf.nn.relu,
                        scope='InceptionResnetV1'):
    """Creates the Inception Resnet V1 model.
    Args:
      inputs: a 4-D tensor of size [batch_size, height, width, 3].
      num_classes: number of predicted classes.
      is_training: whether is training or not.
      dropout_keep_prob: float, the fraction to keep before final layer.
      reuse: whether or not the network and its variables should be reused. To be
        able to reuse 'scope' must be given.
      scope: Optional variable_scope.
    Returns:
      logits: the logits outputs of the model.
      end_points: the set of end_points from the inception model.
    """
    end_points = {}
    if filter_list is None or len(filter_list) == 0:
        filter_list = [32, 32, 64, 80, 192, 256, 32, 192, 192, 256, 384, 128, 256, 384, 192, 192]
  
    with tf.variable_scope(scope, 'InceptionResnetV1', [inputs], reuse=reuse):
        with slim.arg_scope([slim.conv2d, slim.max_pool2d, slim.avg_pool2d],
                            stride=1, padding='SAME'):

            # 149 x 149 x 32
            net = slim.conv2d(inputs, filter_list[0], 3, stride=2, padding='VALID',activation_fn=activation,
                              scope='Conv2d_1a_3x3')
            end_points['Conv2d_1a_3x3'] = net
            print('Conv2d_1a_3x3 shape:', net.shape)
            # 147 x 147 x 32
            net = slim.conv2d(net, filter_list[1], 3, padding='VALID',activation_fn=activation,
                              scope='Conv2d_2a_3x3')
            end_points['Conv2d_2a_3x3'] = net
            print('Conv2d_2a_3x3 shape:', net.shape)
            # 147 x 147 x 64
            net = slim.conv2d(net, filter_list[2], 3, scope='Conv2d_2b_3x3',activation_fn=activation,)
            end_points['Conv2d_2b_3x3'] = net
            print('Conv2d_2b_3x3 shape:', net.shape)
            # 73 x 73 x 64
            net = slim.max_pool2d(net, 3, stride=2, padding='VALID',
                                  scope='MaxPool_3a_3x3')
            end_points['MaxPool_3a_3x3'] = net
            print('MaxPool_3a_3x3 shape:', net.shape)
            # 73 x 73 x 80
            net = slim.conv2d(net, filter_list[3], 1, padding='VALID',activation_fn=activation,
                              scope='Conv2d_3b_1x1')
            end_points['Conv2d_3b_1x1'] = net
            print('Conv2d_3b_1x1 shape:', net.shape)
            # 71 x 71 x 192
            net = slim.conv2d(net, filter_list[4], 3, padding='VALID',activation_fn=activation,
                              scope='Conv2d_4a_3x3')
            end_points['Conv2d_4a_3x3'] = net
            print('Conv2d_4a_3x3 shape:', net.shape)
            # 35 x 35 x 256
            net = slim.conv2d(net, filter_list[5], 3, stride=2, padding='VALID',activation_fn=activation,
                              scope='Conv2d_4b_3x3')
            end_points['Conv2d_4b_3x3'] = net
            print('Conv2d_4b_3x3 shape:', net.shape)

            # 5 x Inception-resnet-A
            net = slim.repeat(net, 5, block35, scale=0.17,activation_fn=activation,filter=filter_list[6])
            end_points['Mixed_5a'] = net
            print('Mixed_5a shape:', net.shape)

            # Reduction-A
            k,l,m,n = filter_list[7:11]
            with tf.variable_scope('Mixed_6a'):
                net = reduction_a(net, k,l,m,n,activation_fn=activation)
            end_points['Mixed_6a'] = net
            print('Mixed_6a shape:', net.shape)

            # 10 x Inception-Resnet-B
            net = slim.repeat(net, 10, block17, scale=0.10,activation_fn=activation,filter=filter_list[11])
            end_points['Mixed_6b'] = net
            print('Mixed_6b shape:', net.shape)

            # Reduction-B
            with tf.variable_scope('Mixed_7a'):
                net = reduction_b(net,filter_list=filter_list[12:14],activation_fn=activation)
            end_points['Mixed_7a'] = net
            print('Mixed_7a shape:', net.shape)

            # 5 x Inception-Resnet-C
            net = slim.repeat(net, 5, block8, scale=0.20,activation_fn=activation,filter=filter_list[14])
            end_points['Mixed_8a'] = net
            print('Mixed_8a shape:', net.shape)

            net = block8(net, filter=filter_list[15], activation_fn=None)
            end_points['Mixed_8b'] = net
            print('Mixed_8b shape:', net.shape)

            with tf.variable_scope('Logits'):
                end_points['PrePool'] = net
                #pylint: disable=no-member
                net = slim.avg_pool2d(net, net.get_shape()[1:3], padding='VALID',
                                      scope='AvgPool_1a_8x8')
                net = slim.flatten(net)
                #print("flatten shape:",net.shape)

                # net = slim.dropout(net, dropout_keep_prob, is_training=is_training,
                #                    scope='Dropout')
                net = tf.nn.dropout(net, keep_prob=dropout_keep_prob)

                end_points['PreLogitsFlatten'] = net
                print("pre-logit flatten shape:", net.shape)

            net = slim.fully_connected(net, bottleneck_layer_size, activation_fn=None,
                    scope='Bottleneck', reuse=False)
  
    return net, end_points

def inference_reduction(images, keep_probability, phase_train=True, bottleneck_layer_size=128,
              weight_decay=0.0, reuse=None, filter_list=None, activation=tf.nn.relu):
    batch_norm_params = {
        # Decay for the moving averages.
        'decay': 0.995,
        # epsilon to prevent 0s in variance.
        'epsilon': 0.001,
        # force in-place updates of mean and variance estimates
        'updates_collections': None,
        # Moving averages ends up in the trainable variables collection
        'variables_collections': [ tf.GraphKeys.TRAINABLE_VARIABLES ],
    }

    with slim.arg_scope([slim.conv2d, slim.fully_connected],
                        weights_initializer=slim.initializers.xavier_initializer(),
                        weights_regularizer=slim.l2_regularizer(weight_decay),
                        normalizer_fn=slim.batch_norm,
                        normalizer_params=batch_norm_params
                        ):
        return inception_resnet_v1_reduction(images,is_training=phase_train,
                                   dropout_keep_prob=keep_probability,
                                   bottleneck_layer_size=bottleneck_layer_size,
                                   reuse=reuse, filter_list=filter_list,
                                   activation=activation)


def inception_resnet_v1_reduction(inputs,is_training=True,
                        dropout_keep_prob=0.8,
                        bottleneck_layer_size=128,
                        reuse=None,
                        filter_list=None,
                        activation=tf.nn.relu,
                        scope='InceptionResnetV1'):
    """Creates the Inception Resnet V1 model.
    Args:
      inputs: a 4-D tensor of size [batch_size, height, width, 3].
      num_classes: number of predicted classes.
      is_training: whether is training or not.
      dropout_keep_prob: float, the fraction to keep before final layer.
      reuse: whether or not the network and its variables should be reused. To be
        able to reuse 'scope' must be given.
      scope: Optional variable_scope.
    Returns:
      logits: the logits outputs of the model.
      end_points: the set of end_points from the inception model.
    """
    end_points = {}
    if filter_list is None or len(filter_list) == 0:
        # filter_list = [32, 32, 64, 80, 192, 256, 32, 192, 192, 256, 384, 128, 256, 384, 192, 192]
        filter_list = [32, 32, 64, 80, 96, 128, 16, 96, 96, 128, 192, 64, 128, 192, 96, 96]

    with tf.variable_scope(scope, 'InceptionResnetV1', [inputs], reuse=reuse):
        with slim.arg_scope([slim.batch_norm, slim.dropout],
                            is_training=is_training):
            with slim.arg_scope([slim.conv2d, slim.max_pool2d, slim.avg_pool2d],
                                stride=1, padding='SAME'):
                # 149 x 149 x 32
                net = slim.conv2d(inputs, filter_list[0], 3, stride=2, padding='VALID', activation_fn=activation,
                                  scope='Conv2d_1a_3x3')
                end_points['Conv2d_1a_3x3'] = net
                print('Conv2d_1a_3x3 shape:', net.shape)
                # 147 x 147 x 32
                net = slim.conv2d(net, filter_list[1], 3, padding='VALID', activation_fn=activation,
                                  scope='Conv2d_2a_3x3')
                end_points['Conv2d_2a_3x3'] = net
                print('Conv2d_2a_3x3 shape:', net.shape)
                # 147 x 147 x 64
                net = slim.conv2d(net, filter_list[2], 3, scope='Conv2d_2b_3x3', activation_fn=activation, )
                end_points['Conv2d_2b_3x3'] = net
                print('Conv2d_2b_3x3 shape:', net.shape)
                # 73 x 73 x 64
                net = slim.max_pool2d(net, 3, stride=2, padding='VALID',
                                      scope='MaxPool_3a_3x3')
                end_points['MaxPool_3a_3x3'] = net
                print('MaxPool_3a_3x3 shape:', net.shape)
                # 73 x 73 x 80
                net = slim.conv2d(net, filter_list[3], 1, padding='VALID', activation_fn=activation,
                                  scope='Conv2d_3b_1x1')
                end_points['Conv2d_3b_1x1'] = net
                print('Conv2d_3b_1x1 shape:', net.shape)
                # 71 x 71 x 192
                net = slim.conv2d(net, filter_list[4], 3, padding='SAME', activation_fn=activation,
                                  scope='Conv2d_4a_3x3')
                end_points['Conv2d_4a_3x3'] = net
                print('Conv2d_4a_3x3 shape:', net.shape)
                # 35 x 35 x 256
                # net = slim.conv2d(net, filter_list[5], 3, stride=2, padding='VALID', activation_fn=activation,
                #                   scope='Conv2d_4b_3x3')
                # end_points['Conv2d_4b_3x3'] = net
                # print('Conv2d_4b_3x3 shape:', net.shape)

                # 5 x Inception-resnet-A
                net = slim.repeat(net, 5, block35, scale=0.17, activation_fn=activation, filter=filter_list[6])
                end_points['Mixed_5a'] = net
                print('Mixed_5a shape:', net.shape)

                # Reduction-A
                k, l, m, n = filter_list[7:11]
                with tf.variable_scope('Mixed_6a'):
                    net = reduction_a(net, k, l, m, n, activation_fn=activation)
                end_points['Mixed_6a'] = net
                print('Mixed_6a shape:', net.shape)

                # 10 x Inception-Resnet-B
                net = slim.repeat(net, 10, block17, scale=0.10, activation_fn=activation, filter=filter_list[11])
                end_points['Mixed_6b'] = net
                print('Mixed_6b shape:', net.shape)

                # Reduction-B
                with tf.variable_scope('Mixed_7a'):
                    net = reduction_b(net, filter_list=filter_list[12:14], activation_fn=activation)
                end_points['Mixed_7a'] = net
                print('Mixed_7a shape:', net.shape)

                # 5 x Inception-Resnet-C
                net = slim.repeat(net, 5, block8, scale=0.20, activation_fn=activation, filter=filter_list[14])
                end_points['Mixed_8a'] = net
                print('Mixed_8a shape:', net.shape)

                net = block8(net, filter=filter_list[15], activation_fn=None)
                end_points['Mixed_8b'] = net
                print('Mixed_8b shape:', net.shape)

                with tf.variable_scope('Logits'):
                    end_points['PrePool'] = net
                    # pylint: disable=no-member
                    net = slim.avg_pool2d(net, net.get_shape()[1:3], padding='VALID',
                                          scope='AvgPool_1a_8x8')
                    net = slim.flatten(net)
                    # print("flatten shape:",net.shape)

                    # net = slim.dropout(net, dropout_keep_prob, is_training=is_training,
                    #                    scope='Dropout')
                    net = tf.nn.dropout(net, keep_prob=dropout_keep_prob)

                    end_points['PreLogitsFlatten'] = net
                    print("pre-logit flatten shape:", net.shape)

                net = slim.fully_connected(net, bottleneck_layer_size, activation_fn=None,
                                           scope='Bottleneck', reuse=False)

    return net, end_points


