import tensorflow as tf
from resnet_base.model.vq_resnet import VQResNet
from resnet_base.trainer.resnet_trainer import ResNetTrainer
from resnet_base.data.tiny_imagenet_pipeline import TinyImageNetPipeline
from resnet_base.util.logger.factory import LoggerFactory


def main(args):
    tf.reset_default_graph()
    tf.logging.set_verbosity(tf.logging.DEBUG)
    tf.set_random_seed(15092017)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # dynamic GPU memory allocation
    sess = tf.Session(config=config)
    with sess:
        pipeline = TinyImageNetPipeline(batch_size=256)
        imgs, labels = pipeline.get_iterator().get_next()

        logger_factory = LoggerFactory(TinyImageNetPipeline.num_valid_samples // pipeline.batch_size)

        model = VQResNet(logger_factory, imgs, labels)

        trainer = ResNetTrainer(model, pipeline, virtual_batch_size_factor=2)
        trainer.train()


if __name__ == "__main__":
    tf.app.run()
