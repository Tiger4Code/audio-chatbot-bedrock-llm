import os
import sys
from langchain.chains import ConversationChain
from langchain.llms.bedrock import Bedrock
from langchain.memory import ConversationBufferMemory
from utils import bedrock, print_ww
 
def lambda_handler(event, context):
    question = event['text'] 
    bucket = event['bucket']
    module_path = ".."
    sys.path.append(os.path.abspath(module_path))
 
    boto3_bedrock = bedrock.get_bedrock_client(
        region="us-east-1"
    )
             
    model_id = "ai21.j2-ultra-v1" 
    # model_id = "ai21.j2-mid-v1"
    ai21_llm = Bedrock(model_id=model_id, client=boto3_bedrock, model_kwargs={"maxTokens": 1000},) #, temperature=1) #  model_kwargs= parameters)
    print( ai21_llm)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=ai21_llm, verbose=True, memory=memory
    )
    output = ""
    try:
        output = print_ww(conversation.predict(input=question))
    except ValueError as error:
        if  "AccessDeniedException" in str(error):
            print(f"\x1b[41m{error}\
            \nTo troubeshoot this issue please refer to the following resources.\
            \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
            \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")      
            class StopExecution(ValueError):
                def _render_traceback_(self):
                    pass
            raise StopExecution        
        else:
            raise error
    return {
        'statusCode': 200,
        'text': output,
        'bucket': bucket
    }