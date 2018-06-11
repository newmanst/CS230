import keras.backend as K
import keras.callbacks as Kcall
import tensorflow as tf 
class TensorboardKeras(object):
    def __init__(self, model, log_dir):
        self.model = model
        self.log_dir = log_dir
        self.session = K.get_session()
	
	self.lr_ph = tf.placeholder(shape=(), dtype=tf.float32)
	tf.summary.scalar('lr', self.lr_ph)
	
        self.loss_xy = tf.placeholder(shape=(), dtype=tf.float32)
        tf.summary.scalar('loss_xy', self.loss_xy)

   # self.val_loss_ph = tf.placeholder(shape=(), dtype=tf.float32)
   # tf.summary.scalar('val/loss', self.val_loss_ph)

   # self.val_acc_ph = tf.placeholder(shape=(), dtype=tf.float32)
   # tf.summary.scalar('val/acc', self.val_acc_ph)

   # self.train_loss_ph = tf.placeholder(shape=(), dtype=tf.float32)
   # tf.summary.scalar('train/loss', self.train_loss_ph)
#
   # self.train_acc_ph = tf.placeholder(shape=(), dtype=tf.float32)
   # tf.summary.scalar('train/acc', self.train_acc_ph)

        self.merged = tf.summary.merge_all()
        self.writer = tf.summary.FileWriter(self.log_dir)

    def _get_lr(self):
        return K.eval(self.model.optimizer.lr)

    def on_epoch_end(self, epoch, logs):
        summary = self.session.run(self.merged,
				feed_dict={self.lr_ph: self._get_lr(),
					   self.loss_xy: logs["loss_xy"]
					  })
                      #         feed_dict={self.lr_ph: self._get_lr(),
                      #                    self.val_loss_ph: logs["val_loss"],
                      #                    self.train_loss_ph: logs["loss"],
                      #                    self.val_acc_ph: logs["val_acc"],
                      #                    self.train_acc_ph: logs["acc"]
                      #                    })
        self.writer.add_summary(summary, epoch)
        self.writer.flush()

    def on_epoch_end_cb(self):
        return Kcall.LambdaCallback(on_epoch_end=lambda epoch, logs:
                                       self.on_epoch_end(epoch, logs))

