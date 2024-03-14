from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.memory import FileChatMessageHistory, ConversationSummaryMemory

# load env vars
load_dotenv()

# create instance of chat model
chat = ChatOpenAI()  

# ConversationBufferMemory - useful with conversational models; allows previous messages to be sent along with current message to model.
# FileChatMessageHistory - allows you to save messages to a file as json for later use
# ConversationSummaryMemory - uses it's own LLM to summarize the chat to avoid huge chats stacking up (but doesn't play well with FileChatMessageHistory)
# Adds some performance overhead bc every sent message results in a second step of summarizing the chat.
memory = ConversationSummaryMemory(
    # chat_memory=FileChatMessageHistory("messages.json"),
    memory_key="messages", 
    return_messages=True,
    llm=chat,
    )

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory
)

while True:
    # built in fn - will pause execution and wait for user input + user hits Enter
    content = input(">> ")

    result = chain({"content": content})
    print(result["text"])