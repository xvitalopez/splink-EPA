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
                        {'InstanceId': 'i-0614e367737a78d94'}
                    ]
                }
            ]
        }
        instances = list_instances('eu-north-1')
        self.assertEqual(instances, ['i-0614e367737a78d94'])

if __name__ == '__main__':
    unittest.main()

