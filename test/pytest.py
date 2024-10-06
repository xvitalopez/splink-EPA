import unittest
from unittest.mock import patch
from script import list_instances

class TestScript(unittest.TestCase):

    @patch('script.boto3.client')
    def test_list_instances(self, mock_boto_client):
        mock_ec2 = mock_boto_client.return_value
        mock_ec2.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {'InstanceId': 'i-1234567890abcdef0'}
                    ]
                }
            ]
        }
        instances = list_instances('us-east-1')
        self.assertEqual(instances, ['i-1234567890abcdef0'])

if __name__ == '__main__':
    unittest.main()

