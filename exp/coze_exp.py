"""
This example describes how to use the workflow interface to chat.
"""

import os
# Our official coze sdk for Python [cozepy](https://github.com/coze-dev/coze-py)
from cozepy import COZE_CN_BASE_URL

# Get an access_token through personal access token or oauth.
coze_api_token = 'pat_lU9WPsqEBNhJYPtl6j9QEnoi3E8D44x6BUkhP4BStHHvSE7o13U85JeyHKPk5KOL'
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = COZE_CN_BASE_URL

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType  # noqa

# Init the Coze client through the access_token.
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.
workflow_id = '7474835190277128231'

# Call the coze.workflows.runs.create method to create a workflow run. The create method
# is a non-streaming chat and will return a WorkflowRunResult class.
workflow = coze.workflows.runs.create(
    workflow_id=workflow_id,
    parameters={
        "input": "https://p26-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/9de4fc56ecec45d5b93ddf121167819d.png~tplv-mdko3gqilj-image.image?rk3s=81d4c505&x-expires=1771483556&x-signature=dy6VVgASagpzhy32C1ECcHnIwiE%3D&x-wf-file_name=model-icon.png"
    }
)

print("workflow.data", workflow.data)