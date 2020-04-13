import sagemaker
from sagemaker import get_execution_role
from google.oauth2 import service_account

import numpy
import pandas
import pandas_gbq
import s3fs
import pickle

# session and role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# create an S3 bucket
bucket = sagemaker_session.default_bucket()

# GCP - BigQuery
# load the service account credentials from S3
location_credentials = 's3://{}/credentials/{}'.format(bucket, 'credentials.json')
s3 = s3fs.S3FileSystem(anon=False)
with s3.open(location_credentials, 'rb') as f:
    service_account_info = pandas.read_json(f,typ='series')
f.close()

CREDENTIALS = service_account.Credentials.from_service_account_info(
    service_account_info)
 
# Transformer
location_transformer = 's3://{}/feature_data/{}'.format(bucket,  'transformer.pkl')
s3 = s3fs.S3FileSystem(anon=False)
with s3.open(location_transformer, 'rb') as pickle_file:
    transformer = pickle.load(pickle_file)
    transformer = pickle.loads(transformer)
pickle_file.close()
    
def feature_extraction_individual_address(address):
    # set credentials
    
    # query

    query = f"""
    
        WITH
      -- current balance for an individual instance
      ethereum_balance AS (
      SELECT
        address AS ethereum_address,
        (eth_balance / POWER(10, 18)) AS eth_balance
      FROM
        `bigquery-public-data.crypto_ethereum.balances`
      WHERE
          address = '{address}'
        ),
        
      -- extract top 1000 tokens by transfer count
      top_tokens AS (
      SELECT
        token_address,
        COUNT(1) AS transfer_count
      FROM
        `bigquery-public-data.ethereum_blockchain.token_transfers` AS token_transfers
      GROUP BY
        token_address
      ORDER BY
        transfer_count DESC
      LIMIT
        1000 ),
        
      token_balances AS (
      WITH
        double_entry_book AS (
        SELECT
          token_address,
          to_address AS ethereum_address,
          CAST(value AS float64) AS value,
          block_timestamp,
          transaction_hash
        FROM
          `bigquery-public-data.ethereum_blockchain.token_transfers`
        UNION ALL
        SELECT
          token_address,
          from_address AS ethereum_address,
          -CAST(value AS float64) AS value,
          block_timestamp,
          transaction_hash
        FROM
          `bigquery-public-data.ethereum_blockchain.token_transfers` )
      SELECT
        a.ethereum_address,
        b.token_address,
        SUM(value) AS balance,
        COUNT(DISTINCT transaction_hash) as unique_transfers
      FROM
        ethereum_balance a
      JOIN
        double_entry_book b
      ON
        a.ethereum_address = b.ethereum_address
      JOIN
        top_tokens c
      ON
        c.token_address = b.token_address
      WHERE
        a.ethereum_address != '0x0000000000000000000000000000000000000000'
      GROUP BY
        1,
        2)
    SELECT
      ethereum_address,
      MAX(eth_balance) AS ether_balance,
      COUNT(DISTINCT token_address) AS unique_tokens,
      MAX(unique_transfers) as unique_transfers
    FROM
      ethereum_balance a
    JOIN
      token_balances b
    USING
      (ethereum_address)
    GROUP BY
      1

    """
    
    address_features = pandas_gbq.read_gbq(query, credentials=CREDENTIALS)
    # remove the ethereum address column
    address_features = address_features.iloc[:,1:]
    # use the sklearn pipeline transformer
    address_features = transformer.transform(numpy.array(address_features).reshape(1, -1))
    
    return address_features