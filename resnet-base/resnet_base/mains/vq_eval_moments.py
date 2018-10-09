import tensorflow as tf
from resnet_base.model.vq_resnet import VQResNet
from resnet_base.trainer.resnet_trainer import ResNetTrainer
from resnet_base.data.tiny_imagenet_pipeline import TinyImageNetPipeline
from resnet_base.util.logger.factory import LoggerFactory
from resnet_base.util.logger.tf_logger_init import init as logger_init


tf.flags.DEFINE_integer("physical_batch_size", 32, "Number of samples per batch that is fed through the GPU at once.")
tf.flags.DEFINE_integer("virtual_batch_size_factor", 8, "Number of batches per weight update.")
FLAGS = tf.flags.FLAGS


def main(args):
    tf.reset_default_graph()
    tf.set_random_seed(15092017)
    logger_init()

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # dynamic GPU memory allocation
    sess = tf.Session(config=config)
    with sess:
        # dataset
        pipeline = TinyImageNetPipeline(physical_batch_size=FLAGS.physical_batch_size)
        pipeline.switch_to(tf.estimator.ModeKeys.TRAIN)
        imgs, labels = pipeline.get_iterator().get_next()

        # model
        logger_factory = LoggerFactory()
        model = VQResNet(logger_factory, imgs, labels)

        # evaluation on training set (run one epoch)
        trainer = ResNetTrainer(model, pipeline, FLAGS.virtual_batch_size_factor)
        trainer.train()


if __name__ == "__main__":
    tf.app.run()
