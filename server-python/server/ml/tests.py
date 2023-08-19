from django.test import TestCase
from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
from ml.registry import MLRegistry

class MLRegistryTests(TestCase):
    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "btcsticker"
        algorithm_object = BTCPredictionUsingLSTM()
        algorithm_name = "LSTM using ROC, MA, SD"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Binh Mai"
        algorithm_description = "test deploy LSTM on Django Project"
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
                            algorithm_status, algorithm_version, algorithm_owner,
                            algorithm_description)
        self.assertEqual(len(registry.endpoints), 1)
