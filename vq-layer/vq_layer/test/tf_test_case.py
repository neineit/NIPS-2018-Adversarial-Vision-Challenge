import numpy as np
import tensorflow as tf
from typing import List, Union
from unittest import TestCase


class TFTestCase(TestCase):
    msg_output_wrong = 'Output does not match expected value.'

    def setUp(self) -> None:
        tf.set_random_seed(15092017)
        tf.reset_default_graph()
        self.sess = tf.Session()
        self.sess.as_default()

    def init_vars(self) -> None:
        init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.sess.run(init)

    def tearDown(self) -> None:
        self.sess.close()

    def assert_numerically_equal(self, output: Union[List, np.ndarray], desired: Union[List, np.ndarray]) -> None:
        """
        Compares two arrays numerically (small differences are tolerated).
        """
        if not type(output) is np.ndarray:
            output = np.array(output, dtype=np.float32)
        if not type(desired) is np.ndarray:
            desired = np.array(desired, dtype=np.float32)
        self.assertTrue(np.allclose(output, desired), self.msg_output_wrong)
