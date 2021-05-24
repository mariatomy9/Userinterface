from flask import Flask, render_template
import time
from plyer import notification
import threading
app = Flask(__name__ , static_folder='assets' ,template_folder='Templates')

def msg(title,message):
   notification.notify(
         title=title,
         message=message,
         timeout=1,
   )
time.sleep(4)

def azure():


   #----------------------------------VIDEO INDEXER---------------------------------

   import requests
   import os
   import io
   import json

   video_url ="https://storage123indexer.blob.core.windows.net/container2/New%20Directory/Conversation%20between%20Two%20Friends%20in%20English_Conversation%20about%20Sport_Daily%20Usage%20EnglishConversation.mp4"
   file_name = 'videoplayback-test2.mp4' # Example: myfile.wav

   # Important stuff
   video_indexer_account_id = 'e9d3648f-54b1-4936-92b7-5b3eb8b47c23' # Get this from https://www.videoindexer.ai/settings/account
   video_indexer_api_key = 'a924aa2e5bff4d22b5896993dbe4e6cf' # Get this from subscription at https://api-portal.videoindexer.ai/products/authorization
   video_indexer_api_region = 'eastus' # Get this from https://www.videoindexer.ai/settings/account


   auth_uri = 'https://api.videoindexer.ai/auth/{}/Accounts/{}/AccessToken'.format(video_indexer_api_region,video_indexer_account_id)
   auth_params = {'allowEdit':'true'}
   auth_header = {'Ocp-Apim-Subscription-Key': video_indexer_api_key}
   auth_token = requests.get(auth_uri,headers=auth_header,params=auth_params).text.replace('"','')

   msg('Video Indexer API','Authorization Complete')
   print('Video Indexer API: Authorization Complete.')
   print('Video Indexer API: Uploading file: ',file_name)

   # Upload Video to Video Indexer API
   upload_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos'.format(video_indexer_api_region,video_indexer_account_id)
   upload_header = {'Content-Type': 'multipart/form-data'}
   upload_params = {
      'name':file_name,
      'accessToken':auth_token,
      'streamingPreset':'Default',
      'fileName':file_name,
      'videoUrl':video_url
      }
   #files= {'file': (file_name, audio_file)}
   r = requests.post(upload_uri,params=upload_params)
   response_body = r.json()

   msg('Video Indexer API','Upload Completed')
   print('Video Indexer API: Upload Completed.')
   print('Video Indexer API: File Id: {} .'.format(response_body.get('id')))

   #---------------------------------------
   import time
   video_id=response_body.get('id')

   upload_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos/{}/Index'.format(video_indexer_api_region,video_indexer_account_id,video_id)
   upload_params = {
      'accessToken': auth_token,
      'language': 'English'
   }
   print('Getting video info for: {}'.format(video_id))

   g = requests.get(upload_uri,params=upload_params)
   response =g.json()
   while (response["state"] == 'Processing'):
      g = requests.get(upload_uri,params=upload_params)
      response =g.json()
      msg('video indexer',f"Current status : {response['videos'][0]['processingProgress']}")
      print('Video still processing, current status: {}'.format(
            response['videos'][0]['processingProgress'],
      time.sleep(10)
            ))
   msg('Video Indexer','Video Indexed')
   print('Video Indexed')

   #-----EMOTION CALCULATION---------

   msg('Video Indexer','Calculating')
   for x in response['videos'][0]['insights']['transcript']:
      print(x['text'])
   for j in x['instances']:
      print(f"start time is {j['start']} and end time is {j['end']}")
   print('\n\n')

   for i in response['summarizedInsights']['sentiments']:
      print(i['sentimentKey'])
   for j in i['appearances']:
      print(f"start time is {j['startTime']} and end time is {j['endTime']}")
   print('\n\n')

   for x in response['videos'][0]['insights']['transcript']:
      for y in x['instances']:
         a=y['start']
         b=y['end']
         #print((a,b))
         for i in response['summarizedInsights']['sentiments']:
            for j in i['appearances']:
               c=j['startTime']
               d=j['endTime']
               #print((c,d))
               #for time in (a, b):
               if c <= a < d or c< b <=d :
                  print(i['sentimentKey'])
                  print((a,b))

   msg('Video Indexer','Calculating')
   l1=[]
   for x in response['videos'][0]['insights']['transcript']:
      if (x['speakerId']==int(1) or x['speakerId']==int(3)):
         for y in x['instances']:
            a=y['start']
            b=y['end']
            #print((a,b))
            for i in response['summarizedInsights']['sentiments']:
               for j in i['appearances']:
                  c=j['startTime']
                  d=j['endTime']
                  #print((c,d))
                  if c <= a < d or c< b <=d :
                     #print(i['sentimentKey'])
                     l1.append(str(i['sentimentKey']))
                     #print((a,b))

   print(l1)

   msg('Video Indexer','Completed')
   l2=[]
   for x in response['videos'][0]['insights']['transcript']:
      if (x['speakerId']==int(2) or x['speakerId']==int(4)):
         for y in x['instances']:
            a=y['start']
            b=y['end']
            #print((a,b))
            for i in response['summarizedInsights']['sentiments']:
               for j in i['appearances']:
                  c=j['startTime']
                  d=j['endTime']
                  #print((c,d))
                  if c <= a < d or c< b <=d :
                     #print(i['sentimentKey'])
                     l2.append(str(i['sentimentKey']))
                     #print((a,b))

   print(l2)

   #------------TOPIC EXTRACTION----------------
   l3=[]
   for i in response['summarizedInsights']['topics']:
      l3.append(i['name'])
   print(l3)

   thisdict = {
  "Positive": 9,
  "Neutral": 5,
  "Negative": 1
   }
   person1=[thisdict[k] for k in l1]
   person2=[thisdict[k] for k in l2]
   def Average(lst):
      return sum(lst) / len(lst)

   print(Average(person1))
   print(Average(person2))


   #----------------------FORM RECOGNISER-----------------------------

   # import os
   # #! pip install azure-ai-formrecognizer --pre
   # #print(os.getcwd())
   # class RecognizeCustomForms(object):

   #    def recognize_custom_forms(self):

   #       # path_to_sample_forms ="test.jpeg"
   #       # [START recognize_custom_forms]
   #       from azure.core.credentials import AzureKeyCredential
   #       from azure.ai.formrecognizer import FormRecognizerClient

   #       endpoint = "https://feedbackform.cognitiveservices.azure.com/"
   #       key = "5d3f9679d8e84d33b89e326f60865132"
   #       model_id = "b00bf70d-d55f-4f02-a6eb-3ec8604f8462"

   #       form_recognizer_client = FormRecognizerClient(
   #             endpoint=endpoint, credential=AzureKeyCredential(key)
   #       )

   #       # Make sure your form's type is included in the list of form types the custom model can recognize
   #       # with open(path_to_sample_forms, "rb") as f:

   #       #     poller = form_recognizer_client.begin_recognize_custom_forms(
   #       #         model_id=model_id, form=f, include_field_elements=True
   #       #     )
   #       form_url = "https://storage123indexer.blob.core.windows.net/container2/New%20Directory/formdocument.jpeg"
   #       poller = form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=model_id, form_url=form_url)

   #       forms = poller.result()

   #       for idx, form in enumerate(forms):
   #             print("--------Recognizing Form #{}--------".format(idx+1))
   #             print("Form has type {}".format(form.form_type))
   #             print("Form has form type confidence {}".format(form.form_type_confidence))
   #             print("Form was analyzed with model with ID {}".format(form.model_id))
   #             for name, field in form.fields.items():
   #                # each field is of type FormField
   #                # label_data is populated if you are using a model trained without labels,
   #                # since the service needs to make predictions for labels if not explicitly given to it.
   #                if field.label_data:
   #                   print("...Field '{}' has label '{}' with a confidence score of {}".format(
   #                         name,
   #                         field.label_data.text,
   #                         field.confidence
   #                   ))

   #                print("...Label '{}' has value '{}' with a confidence score of {}".format(
   #                   field.label_data.text if field.label_data else name, field.value, field.confidence
   #                ))

   #             # iterate over tables, lines, and selection marks on each page
   #             for page in form.pages:
   #                for i, table in enumerate(page.tables):
   #                   print("\nTable {} on page {}".format(i+1, table.page_number))
   #                   for cell in table.cells:
   #                         print("...Cell[{}][{}] has text '{}' with confidence {}".format(
   #                            cell.row_index, cell.column_index, cell.text, cell.confidence
   #                         ))
   #                print("\nLines found on page {}".format(page.page_number))
   #                for line in page.lines:
   #                   print("...Line '{}' is made up of the following words: ".format(line.text))
   #                   for word in line.words:
   #                         print("......Word '{}' has a confidence of {}".format(
   #                            word.text,
   #                            word.confidence
   #                         ))
   #                if page.selection_marks:
   #                   print("\nSelection marks found on page {}".format(page.page_number))
   #                   for selection_mark in page.selection_marks:
   #                         print("......Selection mark is '{}' and has a confidence of {}".format(
   #                            selection_mark.state,
   #                            selection_mark.confidence
   #                         ))

   #             print("-----------------------------------")
   #       # [END recognize_custom_forms]



   # sample = RecognizeCustomForms()
   # sample.recognize_custom_forms()

   #----------------------DATABASE------------------------------------
   import uuid
   entry1 = {
      'id': 'Andersen_' + str(uuid.uuid4()),
               "Customer ID": "CD700",
               "Service Agent ID": "AG10003",
               "VIP": "N",
               "Location": "Shrajah",
               "Department": "Health",
               "Language": "Tagalog",
               "Gender": "M",
               "Age": "30",
               "Complaint": "N",
               "Key Phrase": "",
               "Cu_Sentiments": "",
               "AG_Sentiments": ""
         }

   entry2 ={
    'id': 'Andersen2_' + str(uuid.uuid4()),
            "Customer ID": "CD701",
            "Service Agent ID": "AG10002",
            "VIP": "Y",
            "Location": "Dubai",
            "Department": "Health",
            "Language": "English",
            "Gender": "M",
            "Age": "25",
            "Complaint": "N",
            "Key Phrase": "affordable,heartfelt,happiness",
            "Cu_Sentiments": "8",
            "AG_Sentiments": "9"
        }

   
   from azure.cosmos import exceptions, CosmosClient, PartitionKey

   # Initialize the Cosmos client
   endpoint = "https://cosmostrials.documents.azure.com:443/"
   key = 'sC22JndQuhxLXjSzTwtsnDTjPNR8tqI6aEpXnc68nVn1TjGN9IJa9zfTjuxf6ATx0GOWnKwWUSon7M8JFp92Hw=='

   # <create_cosmos_client>
   client = CosmosClient(endpoint, key)
   # </create_cosmos_client>

   # Create a database
   # <create_database_if_not_exists>
   database_name = 'Details'
   database = client.create_database_if_not_exists(id=database_name)
   # </create_database_if_not_exists>

   # Create a container
   # Using a good partition key improves the performance of database operations.
   # <create_container_if_not_exists>
   container_name = 'Details6'
   container = database.create_container_if_not_exists(
      id=container_name, 
      partition_key=PartitionKey(path="/Location"),
      offer_throughput=400
   )
   # </create_container_if_not_exists>


   # Add items to the container
   family_items_to_create = [entry1,entry2]
   # family_items_to_create = b
   # <create_item>
   for family_item in family_items_to_create:
      container.create_item(body=family_item)
   # </create_item>

   # Read items (key value lookups by partition key and id, aka point reads)
   # <read_item>

   msg("Database created","Data entered")
   for family in family_items_to_create:
      item_response = container.read_item(item=family['id'], partition_key=family['Location'])
      request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
      print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
   # </read_item>

   # Query these items using the SQL query syntax. 
   # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
   # <query_items>
   query = "SELECT * FROM c WHERE c.Location IN ('Shrajah', 'Dubai')"

   items = list(container.query_items(
      query=query,
      enable_cross_partition_query=True
   ))

   request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

   print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
   # </query_items>



@app.route('/')
def home():
   #threading.Thread(target=azure).start()
   return render_template('index.html')
if __name__ == '__main__':
   app.run()