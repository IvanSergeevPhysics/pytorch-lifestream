import torch
from dltranz.seq_encoder.rnn_encoder import RnnEncoder
from dltranz.trx_encoder import TrxEncoder
from dltranz.metric_learn.ml_models import CPC_Ecoder
from train_cpc import run_experiment
from tests.dltranz_tests.test_trx_encoder import gen_trx_data
from dltranz.data_load import TrxDataset
from dltranz.data_load import create_train_loader, create_validation_loader
from pyhocon import ConfigFactory

def tst_params():
    params = {
        'model_type': 'rnn',
        'rnn': {
            'trainable_starter': 'empty',
            'hidden_size': 16,
            'type': 'gru',
            'bidir': False
        },
        "trx_encoder": {
            "embeddings_noise": .1,
            "norm_embeddings": False,
            'embeddings': {
                'mcc_code': {'in': 21, 'out': 3},
                'trans_type': {'in': 11, 'out': 2},
            },
            'numeric_values': {'amount': 'log'}
        },
        "cpc": {
            "n_forward_steps": 3,
            "n_negatives": 4,
        },
        "train": {
            "weight_decay": 0,
            "lr": 0.004,
            "batch_size": 32,
            "num_workers": 1,
            "trx_dropout": .1,
            "n_epoch": 1,
            "max_seq_len": 30,
        },
        "valid": {
            "batch_size": 32,
            "num_workers": 1,
            "max_seq_len": 30,
            "recall_top_k": 3
        },
        "lr_scheduler": {
            "step_size": 10,
            "step_gamma": 0.8
        }
    }

    params = ConfigFactory.from_dict(params)
    return params

def test_rnn_model():
    config = tst_params()

    trx_e = TrxEncoder(config['trx_encoder'])
    rnn_e = RnnEncoder(trx_e.output_size, config['rnn'])
    cpc_e = CPC_Ecoder(trx_e, rnn_e, 6, config['cpc'])

    train_data = gen_trx_data((torch.rand(1000)*60+1).long())
    train_ds = TrxDataset(train_data)
    test_data = gen_trx_data((torch.rand(100)*60+1).long())
    valid_ds = TrxDataset(test_data)

    train_loader = create_train_loader(train_ds, config['train'])
    valid_loader = create_validation_loader(valid_ds, config['valid'])

    run_experiment(train_loader, valid_loader, cpc_e, {'params': config})
