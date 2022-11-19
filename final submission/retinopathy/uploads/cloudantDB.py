from cloudant.client import Cloudant

client = Cloudant.iam('82241234-0f27-4001-9768-39779dda2122-bluemix','yyEb_ODgLWlsuaoiyYQiOMjaaFGI1CKGYYYL8M95OEXY',connect = True)

my_databae = client.create_database('my_database')
print('connected')