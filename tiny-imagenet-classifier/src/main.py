import tensorflow as tf
import trainer.sgd as trainer
import model.tf_cifar10 as model


def main(args=None):
    trainer.train(model)


if __name__ == '__main__':
    tf.app.run()
