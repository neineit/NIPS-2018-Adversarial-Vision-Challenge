import tensorflow as tf
from nips_defense.model.base_model import BaseModel

tf.flags.DEFINE_float("learning_rate", 1e-3, "The learning rate used for training.")
tf.flags.DEFINE_integer("num_epochs", 100, "The number of epochs for which training is performed.")
tf.flags.DEFINE_string("train_log_dir", "../tf_logs/train", "The directory used to save the training summaries.")
tf.flags.DEFINE_string("val_log_dir", "../tf_logs/val", "The directory used to save the validation summaries.")

FLAGS = tf.flags.FLAGS


class BaseTrainer:
    def __init__(self, model: BaseModel):
        self.model = model
        self.sess = tf.get_default_session()
        self.__init_log_writer()

    def __init_log_writer(self) -> None:
        self.train_logger, self.valid_logger = \
            self.model.logger_factory.create_loggers(self.sess, FLAGS.train_log_dir, FLAGS.val_log_dir,
                                                     self.model.global_step)

    def train(self) -> None:
        """
        Performs training for FLAGS.num_epochs epochs and runs one validation epoch after each training epoch.
        """
        init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        self.sess.run(init)

        # restore weights (as specified in the FLAGS)
        self.model.restore(self.sess)

        # get the current epoch so we can re-start training from there
        start_epoch = self.model.current_epoch.eval(self.sess)
        self.val_epoch()  # perform at least one validation epoch before training
        for _ in range(start_epoch, FLAGS.num_epochs + 1):
            self.train_epoch()
            self.val_epoch()  # run validation epoch to monitor training
            self.model.save(self.sess)

    def train_epoch(self) -> None:
        """
        Trains the model for one epoch.
        Should use the batch size defined in FLAGS.train_batch_size.
        """
        raise NotImplementedError

    def val_epoch(self) -> None:
        """
        Performs inference and calculates evaluation metrics for one full epoch of the validation set.
        Should use the batch size defined in FLAGS.val_batch_size.
        """
        raise NotImplementedError
