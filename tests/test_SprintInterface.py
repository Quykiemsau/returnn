
from nose.tools import assert_equal, assert_is_instance, assert_in, assert_not_in, assert_true, assert_false
import SprintInterface as SprintAPI
import os
import sys
from tempfile import mkdtemp
from Engine import Engine
from Config import Config
from Log import log
import shutil
import numpy


sys.stderr = sys.stdout
log.initialize()


def create_first_epoch(config_filename):
  config = Config()
  config.load_file(config_filename)
  engine = Engine([])
  engine.init_train_from_config(config=config, train_data=None)
  engine.epoch = 1
  engine.save_model(engine.get_epoch_model_filename(), epoch=engine.epoch)




def test_forward():
  tmpdir = mkdtemp("crnn-test-sprint")
  olddir = os.getcwd()
  os.chdir(tmpdir)

  open("config", "w").write(
    """
    num_inputs 2
    num_outputs 3
    hidden_size 1
    hidden_type forward
    activation relu
    bidirectional false
    model model
    """)

  create_first_epoch("config")

  inputDim = 2
  outputDim = 3
  SprintAPI.init(inputDim=inputDim, outputDim=outputDim,
                 config="action:forward,configfile:config,epoch:1",
                 targetMode="forward-only")

  features = numpy.array([[0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5]])
  seq_len = features.shape[0]
  posteriors = SprintAPI.forward("segment1", features.T).T
  assert_equal(posteriors.shape, (seq_len, outputDim))

  SprintAPI.exit()

  os.chdir(olddir)
  shutil.rmtree(tmpdir)
